from import_export import resources
import datetime
from .models import User
from .utils import SERMON_GROUP


class UserResource(resources.ModelResource):

    class Meta:
        model = User
        exclude = ('id', 'username', 'password', 'last_login', 'user_permissions', 'is_group_leader', 'slug', 'groups',
                   'is_superuser', 'is_staff', 'is_active')
        export_order = ('name', 'english_name', 'gender', 'is_christian', 'group', 'job', 'email', 'phone_number', 'hometown',
                        'birthday', 'habits', 'first_time_visit', 'date_joined', 'facebook', 'wechat', 'twitter',)

    def get_queryset(self):
        # Oly query the valid members
        return self._meta.model.objects.exclude(group__name__in=SERMON_GROUP).order_by('id')

    def dehydrate_is_christian(self, record):
        return "是" if record.is_christian else "否"

    def dehydrate_gender(self, record):
        return "男" if record.gender.lower() == 'male' else "女"

    def dehydrate_group(self, record):
        return record.group_name

    def dehydrate_birthday(self, record):
        # Birthday in m/d format
        birthday = record.birthday
        return datetime.datetime.strftime(birthday, '%m/%d') if birthday else None


class UserResourceAdmin(resources.ModelResource):

    class Meta:
        model = User

        export_order = ('id', 'name', 'username', 'password', 'english_name', 'gender', 'is_christian', 'group',
                        'job', 'email', 'phone_number', 'hometown',
                        'birthday', 'habits', 'first_time_visit', 'date_joined', 'facebook', 'wechat', 'twitter',
                        'last_login', 'is_group_leader', 'slug', 'groups', 'is_superuser', 'is_staff', 'is_active',
                        'user_permissions'
                        )

    def get_queryset(self):
        return self._meta.model.objects.order_by('-id')