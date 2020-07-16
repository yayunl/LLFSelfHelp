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


class Service(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    note = models.CharField(max_length=100, null=True, blank=True)
    service_date = models.DateField(null=True, blank=True)
    # unique identifier
    slug = models.SlugField(max_length=100, blank=True, default=None)

    # One-to-one relationships
    category = models.OneToOneField(Category, on_delete=models.CASCADE)
    # @property
    # def categories(self):
    #     return self.category_set.all()

    @property
    def servants(self):
        return self.user_set.all()

    def __str__(self):
        return f"<Service: {self.category}-{self.date_to_str()}>"

    def date_to_str(self):
        return datetime.datetime.strftime(self.service_date, '%Y-%m-%d')

    def _get_unique_slug(self):
        slug = slugify(f"{self.category}-on-{self.date_to_str()}")
        unique_slug = slug
        num = 1
        while Service.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def _get_unique_id(self):
        members = Service.objects.all()
        return len(members) + 1

    def save(self, *args, **kwargs):
        service = Service.objects.filter(service_date=kwargs.get('servicedate'),
                                         category=kwargs.get('category')).first()
        if not service:
            if not self.slug:
                self.slug = self._get_unique_slug()
            if not self.id:
                self.id = self._get_unique_id()

            super().save(*args, **kwargs)




    # def _get_unique_slug(self):
    #     service_date = datetime.datetime.strftime(self.service_date, '%Y-%m-%d')
    #     slug = slugify(f"{self.name}-{service_date}")
    #     unique_slug = slug
    #     num = 1
    #     while Service.objects.filter(slug=unique_slug).exists():
    #         unique_slug = '{}-{}'.format(slug, num)
    #         num += 1
    #     return unique_slug

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = self._get_unique_slug()
    #     # Create/update an object
    #     super().save(*args, **kwargs)


# class ServiceNote(models.Model):
#     # id = models.IntegerField(unique=True, primary_key=True)
#     note = models.CharField(max_length=100, null=True, blank=True)
#     slug = models.SlugField(max_length=31, null=True)
#     # One-to-many relationships
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     service_date = models.ForeignKey(Service, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f"ServiceNote: {self.note}>"
#
#     def _get_slug(self):
#         return self.category.name+'@'+self.service_date.date_to_str()



