from django.contrib import admin
from import_export import resources
# Register your models here.
from .models import Member,Group, Service
from import_export.admin import ImportExportModelAdmin


class MemberResource(resources.ModelResource):

    class Meta:
        model = Member
        skip_unchanged = True
        report_skipped = False
        exclude = ('chinese_name','bapatized','Month','Day','lunar_birthday','social_media_type','social_media_account')


class MemberAdminImport(ImportExportModelAdmin):
    resource_class = MemberResource
    #: import data encoding
    from_encoding = "utf8"


class ServiceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('service_category','service_date'), }
    list_display = ['service_date', 'service_category']


# register the classes
admin.site.register(Member, MemberAdminImport)
admin.site.register(Group)
admin.site.register(Service, ServiceAdmin)