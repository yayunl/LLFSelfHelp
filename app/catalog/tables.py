import django_tables2 as tables2
from django_tables2 import tables, TemplateColumn
import django_filters
from datetime import datetime as dt
from django.utils.html import format_html
from django.urls import reverse
from .utils import service_dates
from .models import Service
# from users.models import User


class ServiceTable(tables.Table):

    action = TemplateColumn(template_name='catalog/_service_table_update_column.html', orderable=False)
    # notes = tables2.Column(orderable=False, verbose_name='Note')
    category = tables2.Column(orderable=False)

    class Meta:
        model = Service
        fields = ('service_date', 'description', 'category', 'servants',  'action')
        row_attrs = {
            'data-id': 0,
            # 'data-id': lambda record: '1'  if record.objects.filter(service_dates__service_date)
            # if dt.strftime(record.service_date, '%Y-%m-%d') == service_dates()[0] or
            #    dt.strftime(record.service_date, '%Y-%m-%d') == service_dates()[-1]
            # else '0',
            'category': lambda record: record.name
        }

    def render_servants(self, value, record):
        servant_names = list()
        for servant in record.servants.all():
            servant_detail_link = reverse('user_detail', args=[servant.slug])
            servant_names.append(f'<a href="{servant_detail_link}">{servant.name}</a>')
        servant_names_html = ', '.join(servant_names)
        return format_html(servant_names_html)

    # def render_notes(self, value, record):
    #     sdate_str = service_dates()[0]
    #     sdate = dt.strptime(sdate_str, '%Y-%m-%d').date()
    #     try:
    #         snote = ServiceNote.objects.filter(service=record, service_date=sdate).first()
    #         note= snote.note
    #         return note
    #     except:
    #         return ""

    # def render_action(self, value, record):
    #     return ""


# class ServiceFilter(django_filters.FilterSet):
#     class Meta:
#         model = Service
#         fields = ['service_dates']
        # widgets = {
        #     'service_date': DatePickerInput(),  # default date-format %m/%d/%Y will be used
        # }
