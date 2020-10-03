from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from .models import User
from .resources import UserResourceAdmin


class UserAdmin(ImportExportModelAdmin):
    # exclude = ('id', 'service_dates')
    resource_class = UserResourceAdmin
    to_encoding = "utf-8-sig"
    from_encoding = "utf-8-sig"


# register the classes
admin.site.register(User, UserAdmin)

