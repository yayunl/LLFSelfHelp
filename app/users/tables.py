import django_tables2 as tables2
from django_tables2 import tables, TemplateColumn
import django_filters
from django.utils.html import format_html
from django.urls import reverse
from .models import User


class UserTable(tables.Table):
    action = TemplateColumn(template_name='helpers/_table_update_column.html', orderable=False)
    email = tables2.Column(orderable=False)
    name = tables2.Column(orderable=False)

    class Meta:
        model = User
        fields = ('name',  'gender', 'group',  'email', 'action')
        row_attrs = {
            'data-id': 0,
        }

    def render_name(self, value, record):
        user_detail_link = reverse('user_detail', args=[record.slug])
        user_html_str = f'<a href="{user_detail_link}">{record.name}</a>'
        return format_html(user_html_str)

    def render_group(self, value, record):
        return record.group.name


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ['name', 'group', 'gender']

