from django.contrib import admin
from import_export import resources
# Register your models here.
from .models import Member, Group, Service, ServiceDate
from import_export.admin import ImportExportModelAdmin


# class MemberResource(resources.ModelResource):
#
#     class Meta:
#         model = Member
#         skip_unchanged = True
#         report_skipped = False
#         exclude = ('id', 'username', 'password_hash', 'slug')
#
#
# class MemberAdminImport(ImportExportModelAdmin):
#     resource_class = MemberResource
#     #: import data encoding
#     from_encoding = "utf8"

class MemberAdmin(admin.ModelAdmin):
    exclude = ('id', 'username', 'password_hash', 'slug', 'service_dates')


class ServiceAdmin(admin.ModelAdmin):
    # prepopulated_fields = {'slug': ('name', 'service_date'), }
    # list_display = ['service_date', 'name']
    exclude = ('slug',)


class GroupAdmin(admin.ModelAdmin):
    exclude = ('id', 'slug')


class ServiceDateAdmin(admin.ModelAdmin):
    exclude = ('id', )


# register the classes
# admin.site.register(Member, MemberAdminImport)
admin.site.register(Member, MemberAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceDate, ServiceDateAdmin)