from django.contrib import admin

# Register your models here.
from .models import User


class UserAdmin(admin.ModelAdmin):
    exclude = ('id', 'service_dates')


# register the classes
admin.site.register(User, UserAdmin)

