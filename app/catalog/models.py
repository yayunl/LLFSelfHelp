from django.db import models
# from django.conf import settings
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.utils.html import format_html

import django_filters, datetime, pinyin
# from users.models import User

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

GENDER = (('Male', 'Male'),
          ('Female', 'Female'))


class Group(models.Model):
    """
    A group class. Each member belongs to a group.
    """
    id = models.IntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=20, null=True)
    description = models.CharField(max_length=100, null=True, blank=True)
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

    def _get_unique_id(self):
        groups = Group.objects.all()
        return len(groups)+1

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        if not self.id:
            self.id = self._get_unique_id()
        super().save(*args, **kwargs)


class Category(models.Model):
    # id = models.IntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=40, unique=True, primary_key=True)
    description = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = 'Category'
        ordering = ['name']

    # methods
    def __str__(self):
        return f"<Category: {self.name}>"

    def get_absolute_url(self):
        """
        Used in urls and details template.
        :return:
        """
        return reverse('category_detail', args=[self.name])

    def save(self, *args, **kwargs):
        # print("here")
        super().save(*args, **kwargs)


class Service(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    note = models.CharField(max_length=100, null=True, blank=True)
    service_date = models.DateField(null=True, blank=True)
    # unique identifier
    slug = models.SlugField(max_length=100, blank=True, default=None)

    # Many-to-many relationship
    categories = models.ManyToManyField(Category)
    servants = models.ManyToManyField('users.User')

    @property
    def servant_names(self):
        return ', '.join([s.name for s in self.servants.all()])

    @property
    def category_names(self):
        return self.categories.all()[0].name

    def __str__(self):
        return f"<Service: {self.id}-{self.date_to_str()}>"

    def date_to_str(self):
        return datetime.datetime.strftime(self.service_date, '%Y-%m-%d')

    def get_absolute_url(self):
        """
        Used in urls and detail template.
        :return:
        """
        return reverse('service_update', args=[self.slug])

    def _get_unique_slug(self):
        slug = slugify(f"service{self.id}-on-{self.date_to_str()}")
        unique_slug = slug
        num = 1
        while Service.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def _get_unique_id(self):
        services = Service.objects.all()
        return len(services) + 1

    def save(self, *args, **kwargs):
        # todo: duplicate service exists
        # service = Service.objects.filter(service_date=kwargs.get('servicedate'),
        #                                  category=kwargs.get('category')).first()
        # if not service:
        if not self.id:
            self.id = self._get_unique_id()
        if not self.slug:
            self.slug = self._get_unique_slug()

        super().save(*args, **kwargs)

