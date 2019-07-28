from django.db import models
# from django.conf import settings
from django.urls import reverse
from django.template.defaultfilters import slugify
from django_tables2 import tables, TemplateColumn
from .utils import service_dates
from datetime import datetime as dt
import datetime
import django_filters
# Create your models here.


class Group(models.Model):
    name = models.CharField(max_length=20, default='New member', null=True)

    slug = models.SlugField(max_length=31, default='new-members', null=True)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        """
        Used in urls and detail template.
        :return:
        """
        return reverse('group_detail', args=[self.slug])


class Member(models.Model):
    # fields
    id = models.IntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=50, null=True, blank=True, unique=True)
    # name = models.OneToOneField(settings.AUTH_USER_MODEL)
    english_name = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    christian = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True)
    job = models.CharField(max_length=50, null=True, blank=True)
    hometown = models.CharField(max_length=50, null=True, blank=True)
    first_time = models.DateField(null=True)
    habits = models.TextField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)

    # A member belongs to only one group.
    group = models.ForeignKey(Group, on_delete=True, related_name='members', null=True)
    group_leader = models.BooleanField(default=False)
    # Active member?
    active = models.BooleanField(default=True)

    # username
    username = models.CharField(max_length=50, null=True, blank=True, default=None)
    slug = models.SlugField(max_length=31, blank=True, default=None)

    # Metadata
    class Meta:
        ordering = ['-name']

    # methods
    def get_absolute_url(self):
        """
        Used in urls and details template.
        :return:
        """
        return reverse('member_detail', args=[self.slug])

    def __str__(self):
        try:
            return f"{self.name} ({self.group.name})"
        except:
            return f"{self.name} (New comers)"

    def _get_unique_slug(self):
        email = self.email.split('@')[0]
        slug = slugify(f"{self.english_name}-{email}")
        unique_slug = slug
        num = 1
        while Member.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


class SocialMediaAccount(models.Model):
    media_name = models.CharField(max_length=20, null=True, blank=True)
    account_id = models.CharField(max_length=20, null=True, blank=True)
    member = models.ForeignKey(Member, on_delete=True, related_name='social_media_accounts')


class Service(models.Model):
    service_category = models.CharField(max_length=20, null=True, blank=True)
    service_date = models.DateField(null=True)
    service_content = models.CharField(max_length=50, null=True, blank=True,
                                       help_text='Required if the service has specific title.')
    coordinator = models.ManyToManyField(Member,
                                         null=True,
                                         blank=True)
    servants = models.ManyToManyField(Member,
                                      related_name='services',
                                      null=True,
                                      blank=True)
    slug = models.SlugField(max_length=63)

    def __str__(self):
        return f"{self.service_category} of {self.service_date}"

    class Meta:
        verbose_name = 'Service'
        ordering = ['service_date', 'service_category']

    # methods
    def get_absolute_url(self):
        """
        Used in urls and details template.
        :return:
        """
        return reverse('service_detail', args=[self.slug])

    def _get_unique_slug(self):
        slug = slugify(f"{self.service_category}-{self.service_date}")
        unique_slug = slug
        num = 1
        while Service.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

    @property
    def servant_names(self):
        return ','.join([f'{servant.name}({servant.group.name})' for servant in self.servants.all()])


class ServiceFilter(django_filters.FilterSet):
    class Meta:
        model = Service
        fields = ['service_date', 'service_category']


class ServiceTable(tables.Table):

    change = TemplateColumn(template_name='catalog/service_table_update_column.html')

    class Meta:
        model = Service
        fields = ('service_date', 'service_category', 'service_content', 'servant_names', 'change')
        row_attrs = {
            'data-id': lambda record: '1'

            if dt.strftime(record.service_date, '%Y-%m-%d') == service_dates()[0] or
               dt.strftime(record.service_date, '%Y-%m-%d') == service_dates()[-1]
            else '0'
        }