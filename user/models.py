from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
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
    service_category = models.CharField(max_length=20, null=True, blank=True)
    service_date = models.DateField(null=True)

    coordinator = models.ManyToManyField(Member, null=True)
    servants = models.ManyToManyField(Member,
                                      related_name='services',
                                      null=True)

    slug = models.SlugField(max_length=63)

    def __str__(self):
        return f"{self.service_date}"

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.s = slugify(self.service_category)

        super(Service, self).save(*args, **kwargs)

    # methods
    def get_absolute_url(self):
        """
        Used in urls and details template.
        :return:
        """
        return reverse('service_detail', args=[self.slug])

    class Meta:
        verbose_name = 'Service'
        ordering = ['service_date', 'service_category']



