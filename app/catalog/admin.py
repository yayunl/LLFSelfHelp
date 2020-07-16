from django.contrib import admin
from import_export import resources
# Register your models here.
from .models import Group, Service, Category


class ServiceAdmin(admin.ModelAdmin):
    # prepopulated_fields = {'slug': ('name', 'service_date'), }
    # list_display = ['service_date', 'name']
    exclude = ('slug', 'id')


class GroupAdmin(admin.ModelAdmin):
    exclude = ('id', 'slug')


# register the classes
admin.site.register(Group, GroupAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Category)