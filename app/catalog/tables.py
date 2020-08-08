import django_tables2 as tables2
from django_tables2 import tables, TemplateColumn
import django_filters
from django.utils.html import format_html
from django.urls import reverse
from bootstrap_datepicker_plus import DatePickerInput
# import from apps
from .models import Service
from .utils import service_dates, str2date


class ServiceTable(tables.Table):

    action = TemplateColumn(template_name='helpers/_table_update_column.html', orderable=False)
    note = tables2.Column(orderable=False)
    categories = tables2.Column(orderable=False, verbose_name='Category')
    service_date = tables2.Column(verbose_name='Date')

    class Meta:
        model = Service
        fields = ('service_date',  'categories', 'servants',  'note', 'action')
        order_by = '-service_date' # Order by the column of service date in desc
        row_attrs = {
            'data-id': 0,
            # 'data-id': lambda record: '1'  if record.objects.filter(service_dates__service_date)
            # if dt.strftime(record.service_date, '%Y-%m-%d') == service_dates()[0] or
            #    dt.strftime(record.service_date, '%Y-%m-%d') == service_dates()[-1]
            # else '0',
            # 'category': lambda record: record.category
        }

    def render_servants(self, value, record):
        servant_names = list()
        for servant in record.servants.all():
            servant_detail_link = reverse('user_detail', args=[servant.slug])
            servant_names.append(f'<a href="{servant_detail_link}">{servant.name}</a>')
        servant_names_html = ', '.join(servant_names)
        return format_html(servant_names_html)

    def render_categories(self, value, record):
        categories = record.categories.all().first()
        return categories.name if categories else None

    def get_top_pinned_data(self):
        """
        Returns the matched services on the top of the table.
        :return:
        """
        return Service.objects.filter(service_date=str2date(service_dates()[0]))


class ServiceFilter(django_filters.FilterSet):
    class Meta:
        model = Service
        fields = ['service_date', 'note']
        widgets = {
            'service_date': DatePickerInput(),  # default date-format %m/%d/%Y will be used
        }
