from django.contrib import admin
from import_export import resources
# Register your models here.
from .models import Group, Service, ServiceDate, ServiceNote


class ServiceAdmin(admin.ModelAdmin):
    # prepopulated_fields = {'slug': ('name', 'service_date'), }
    # list_display = ['service_date', 'name']
    exclude = ('slug',)


class GroupAdmin(admin.ModelAdmin):
    exclude = ('id', 'slug')


class ServiceDateAdmin(admin.ModelAdmin):
    exclude = ('id', )


class ServiceNoteAdmin(admin.ModelAdmin):
    exclude = ('id', 'slug',)


# register the classes
admin.site.register(Group, GroupAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceNote, ServiceNoteAdmin)
admin.site.register(ServiceDate, ServiceDateAdmin)