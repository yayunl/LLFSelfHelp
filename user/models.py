from django.db import models
from django.urls import reverse

# Create your models here.


class Group(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True, unique=True)

    slug = models.SlugField(max_length=31)

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

    name = models.CharField(max_length=50, null=True, blank=True, unique=True)
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
    group = models.ForeignKey(Group, on_delete=True, related_name='members')
    group_leader = models.BooleanField(default=False)
    # Active member?
    active = models.BooleanField(default=True)

    # username
    username = models.CharField(max_length=50, null=True, blank=True)
    password = models.CharField(max_length=50, null=True, blank=True)

    slug = models.SlugField(max_length=31)

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
        return f"{self.name}"


class SocialMediaAccount(models.Model):
    media_name = models.CharField(max_length=20, null=True, blank=True)
    account_id = models.CharField(max_length=20, null=True, blank=True)
    member = models.ForeignKey(Member, on_delete=True, related_name='social_media_accounts')


class Service(models.Model):
    category = models.CharField(max_length=20, null=True, blank=True, unique=True)
    service_date = models.DateField(null=True)
    coordinator = models.ManyToManyField(Member)
    servants = models.ManyToManyField(Member,
                                      related_name='services')

    slug = models.SlugField(max_length=63)

    def __str__(self):
        return f"{self.category}"

    class Meta:
        verbose_name = 'Service Team'
        ordering = ['category']
        get_latest_by = 'service_date'

