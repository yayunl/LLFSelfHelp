from django.contrib.auth import get_user

GENDER = (('Male', 'Male'),
          ('Female', 'Female'))

SERMON_CATEGORY = ('sunday service', 'sunday services',
                'Sunday Service', 'Sunday Services',
                'Sunday service', 'Sunday services',
                '主日安排', '周日安排', 'Sunday sermons')

SERMON_GROUP = ('Sermon group', 'Sermon Group')


class ProfileGetObjectMixin:

    def get_object(self, queryset=None):
        current_user = get_user(self.request)
        return current_user.profile


class UserGetObjectMixin:

    def get_object(self, queryset=None):
        current_user = get_user(self.request)
        return current_user