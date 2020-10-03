# app/catalog/resources.py

from import_export import resources
from import_export.fields import Field
from .models import Service, Group, Category
from users.utils import SERMON_GROUP, SERMON_CATEGORY


class ServiceResource(resources.ModelResource):
    servant_name = Field(attribute='servant_names', column_name="Servants")

    class Meta:
        model = Service
        exclude = ('slug', 'id', 'servants', 'services_of_week')
        export_order = ('categories', 'service_date', 'servant_name', 'description', 'note')

    def get_queryset(self):
        return self._meta.model.objects.filter().exclude(categories__name__in=SERMON_GROUP).order_by('service_date')

    def dehydrate_servant_name(self, service):
        servants = service.servants.all()
        servant_names = [servant.name for servant in servants]
        return ','.join(servant_names)

    def dehydrate_categories(self, record):
        cat_name = record.category_names
        return cat_name


class GroupResource(resources.ModelResource):
    members = Field(attribute='members', column_name="Members")

    class Meta:
        model = Group
        exclude = ('slug', 'id')
        export_order = ('name', 'description', 'members')

    def get_queryset(self):
        return self._meta.model.objects.order_by('id')

    def dehydrate_members(self, record):
        members = [u.name for u in record.user_set.all()]
        return ','.join(members)


class CategoryResource(resources.ModelResource):
    servants = Field(attribute='servants', column_name='Servants')

    class Meta:
        model = Category
        exclude = ('slug', 'id')
        export_order = ('name', 'description', 'servants')

    def get_queryset(self):
        return self._meta.model.objects.order_by('id')

    def dehydrate_servants(self, record):
        services = Service.objects.filter(categories__name=record.name).all()
        servants = set([servant.name for service in services for servant in service.servants.all()])
        return ','.join(servants) if servants else None


class ServiceResourceAdmin(resources.ModelResource):

    class Meta:
        model = Service

    def get_queryset(self):
        return self._meta.model.objects.filter().exclude(categories__name__in=SERMON_GROUP)\
            .order_by('service_date')


class GroupResourceAdmin(resources.ModelResource):

    class Meta:
        model = Group

    def get_queryset(self):
        return self._meta.model.objects.order_by('-id')


class CategoryResourceAdmin(resources.ModelResource):

    class Meta:
        model = Category

    def get_queryset(self):
        return self._meta.model.objects.order_by('-id')
