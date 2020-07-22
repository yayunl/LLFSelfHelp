from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.urls import reverse
from django.template.defaultfilters import slugify
from .managers import CustomUserManager
from .utils import GENDER


class User(AbstractBaseUser, PermissionsMixin):
    id = models.IntegerField(unique=True, primary_key=True)
    # required fields
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128, null=False, blank=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)
    # optional fields
    english_name = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    job = models.CharField(max_length=50, null=True, blank=True)
    hometown = models.CharField(max_length=50, null=True, blank=True)
    first_time_visit = models.DateField(null=True)
    habits = models.TextField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    gender = models.CharField(max_length=20, choices=GENDER, default='Male')
    # Social media accounts
    facebook = models.CharField(max_length=20, null=True, blank=True, default=None)
    wechat = models.CharField(max_length=20, null=True, blank=True, default=None)
    twitter = models.CharField(max_length=20, null=True, blank=True, default=None)

    # Boolean attributes
    is_christian = models.BooleanField(default=True)
    is_group_leader = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # One-to-many relationships defined on the `many` side
    group = models.ForeignKey('catalog.Group',
                              on_delete=models.CASCADE,
                              blank=True,
                              null=True)    # one-to-many

    # unique identifier
    slug = models.SlugField(max_length=31, blank=True, default=None)

    objects = CustomUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    # Methods
    def __str__(self):
        return f"<User: {self.name}>"

    def get_name(self):
        return self.name

    def get_absolute_url(self):
        """
        Used in urls and detail template.
        :return:
        """
        return reverse('user_detail', args=[self.slug])

    def get_absolute_delete_url(self):
        """
        Used in urls and delete template.
        :return:
        """
        return reverse('user_delete', args=[self.slug])

    def get_absolute_update_url(self):
        """
        Used in urls and update template.
        :return:
        """
        return reverse('user_update', args=[self.slug])

    def _get_unique_slug(self):
        email = self.email.split('@')[0]
        slug = slugify(f"{email}")
        unique_slug = slug
        num = 1
        while User.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def _get_unique_id(self):
        members = User.objects.all()
        return len(members) + 1

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        if not self.id:
            self.id = self._get_unique_id()

        super().save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    slug = models.SlugField(max_length=30, unique=True)

    def __str__(self):
        return f"<Profile: %s>"%self.user.get_name()

    def get_absolute_url(self):
        return reverse('profile_detail', args=[self.slug])

    def get_absolute_update_url(self):
        return reverse('profile_update', args=[self.slug])
