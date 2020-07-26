from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.db.models import Q


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, username, password, name, email, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, name=name, **extra_fields)
        user.set_password(password)
        user.save()
        from users.models import Profile
        Profile.objects.update_or_create(
            user=user,
            defaults={
                'slug': slugify(user.get_name()),
            }
        )
        return user

    def create_superuser(self, username='admin', password='password',
                         name='admin', email='admin@gmail.com', **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, password, name, email, **extra_fields)

    def search(self, query=None):
        """
        Define a search function for the query to call and returns proper results.
        :param query:
        :return: QuerySet
        """
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(username__icontains=query) |
                         Q(name__icontains=query) |
                         Q(english_name__icontains=query) |
                         Q(hometown__icontains=query) |
                         Q(email__icontains=query))
            qs = qs.filter(or_lookup).distinct()
        return qs