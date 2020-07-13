from import_export import resources
from import_export.fields import Field
from .models import Service


class ServiceResource(resources.ModelResource):
    servant_name = Field(attribute='servant_names', column_name="Servants")
    service_category = Field(attribute='name', column_name='Category')
    service_date = Field(attribute='service_date', column_name='Date')
    service_note = Field(attribute='description', column_name='Note')

    class Meta:
        model = Service
        exclude = ('slug', 'id', 'servants')

    def dehydrate_servant_name(self, service):
        servants = service.servants.all()
        servant_names = [servant.name for servant in servants]
        return ','.join(servant_names)
