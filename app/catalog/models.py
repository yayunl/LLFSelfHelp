from django.db import models
# from django.conf import settings
from django.urls import reverse
from django.template.defaultfilters import slugify
from django_tables2 import tables, TemplateColumn
from datetime import datetime as dt
import django_filters, datetime, pinyin



SERVICE_GROUP = (("Chairman-of-week", "Chairman-of-week"),
                  ("Clean-up", "Clean-up"),
                  ("Food-pickup", "Food-pickup"),
                  ("Fruit-dessert", "Fruit-dessert"),
                  ("Dish-wash", "Dish-wash"),
                  ("Child-care", "Child-care"),
                  ("Newcomer-welcome", "Newcomer-welcome"),
                  ("Birthday-celebrate", "Birthday-celebrate"),
                  ("Worship-leader", "Worship-leader"),
                  ("Worship", "Worship"),
                  ("Content", "Content"),
                  ("Prayer-meeting", "Prayer-meeting"),
                  ("Sharing", "Sharing"),
                  ("BS-designer", "BS-designer"),
                  ("BS-advisor", "BS-advisor"),
                  ("Reminder", "Reminder"),
                  ("Bible-study-servants", "Bible-study-servants"))


def service_dates():
    """
    Get the service dates in string of this week and the next week.
    :return: tuple. (this_week_service_date_str in YYYY-MM-DD format,
                     following_week_service_date_str in YYYY-MM-DD format,
                     this_week_sunday_date_str in YYYY-MM-DD format)
    """
    today_full_date = dt.today()

    today_wk_int = int(dt.strftime(today_full_date, '%w'))

    delta_days_to_fri = 5 - today_wk_int

    if delta_days_to_fri == -2:
        # The date of next week
        service_date = today_full_date + datetime.timedelta(5)

    elif delta_days_to_fri == -1:
        # The date of this week
        service_date = today_full_date - datetime.timedelta(1)
    else:
        service_date = today_full_date + datetime.timedelta(delta_days_to_fri)

    # The service date a week after
    following_service_date = service_date + datetime.timedelta(7)

    # This week's Sunday date
    this_week_sunday_date = service_date + datetime.timedelta(2)

    this_week_service_date_str = service_date.strftime('%Y-%m-%d')
    following_week_service_date_str = following_service_date.strftime('%Y-%m-%d')
    this_week_sunday_date_str = this_week_sunday_date.strftime('%Y-%m-%d')

    return this_week_service_date_str, following_week_service_date_str, this_week_sunday_date_str


class Group(models.Model):
    """
    A group class. Each member belongs to a group.
    """
    id = models.IntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=20, null=True)
    description = models.CharField(max_length=100, null=True)
    slug = models.SlugField(max_length=31, null=True)

    def __str__(self):
        return f"<Group: {self.name}>"

    def get_absolute_url(self):
        """
        Used in urls and detail template.
        :return:
        """
        return reverse('group_detail', args=[self.slug])

    def _get_unique_slug(self):
        slug = pinyin.get(self.name,format='strip',delimiter='')
        # slug = slugify(f"{self.name}")
        unique_slug = slug
        num = 1
        while Group.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


class Member(models.Model):
    # fields
    id = models.IntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=50, null=True, blank=True, unique=True)

    # meta data
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

    # One-to-one relationship
    group = models.ForeignKey(Group,
                              on_delete=True,
                              related_name='members',
                              null=True)
    group_leader = models.BooleanField(default=False)
    # Active member?
    active = models.BooleanField(default=True)

    # credentials
    username = models.CharField(max_length=50, null=True, blank=True, default=None)
    password_hash = models.CharField(max_length=128, null=True, blank=True, default=None)
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

    def _get_unique_id(self):
        members = Member.objects.all()
        return len(members)+1

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        if not self.id:
            self.id = self._get_unique_id()

        super().save(*args, **kwargs)


class SocialMediaAccount(models.Model):
    media_name = models.CharField(max_length=20, null=True, blank=True)
    account_id = models.CharField(max_length=20, null=True, blank=True)
    member = models.ForeignKey(Member, on_delete=True, related_name='social_media_accounts')


class Service(models.Model):
    # id = models.IntegerField(unique=True, primary_key=True)
    service_category = models.CharField(max_length=20, null=True, blank=True)
    service_date = models.DateField(null=True)
    servants = models.ManyToManyField(Member,
                                      related_name='services',
                                      null=True,
                                      blank=True)
    service_note = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(max_length=63, primary_key=True)

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
        service_date = datetime.datetime.strftime(self.service_date, '%Y-%m-%d')
        slug = slugify(f"{self.service_category}-{service_date}")
        unique_slug = slug
        num = 1
        while Service.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        # Create/update an object
        super().save(*args, **kwargs)

    @property
    def servant_names(self):
        return ','.join([f'{servant.name}' for servant in self.servants.all()])


class ServiceFilter(django_filters.FilterSet):
    class Meta:
        model = Service
        fields = ['service_date']
        # widgets = {
        #     'service_date': DatePickerInput(),  # default date-format %m/%d/%Y will be used
        # }


class ServiceTable(tables.Table):

    change = TemplateColumn(template_name='catalog/service_table_update_column.html')

    class Meta:
        model = Service
        fields = ('service_date', 'service_category', 'servants', 'service_note', 'change')
        row_attrs = {
            'data-id': lambda record: '1'
            if dt.strftime(record.service_date, '%Y-%m-%d') == service_dates()[0] or
               dt.strftime(record.service_date, '%Y-%m-%d') == service_dates()[-1]
            else '0',
            'category': lambda record: record.service_category
        }