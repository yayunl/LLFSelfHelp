from import_export import resources
from import_export.fields import Field
from .models import Member, Service


class MemberResource(resources.ModelResource):

    name = Field(attribute='name', column_name='Chinese Name')
    gender = Field(attribute='gender', column_name='Gender')
    christian = Field(attribute='christian', column_name='Christian')
    phone_number = Field(attribute='phone_number', column_name='Phone Number')
    email = Field(attribute='email', column_name='Email')
    job = Field(attribute='job', column_name='Job')
    hometown = Field(attribute='hometown', column_name='Hometown')
    first_time = Field(attribute='first_time', column_name='First Visit Time')
    habits = Field(attribute='habits', column_name='Habits')
    birthday = Field(attribute='birthday', column_name='Birthday')
    english_name = Field(attribute='english_name', column_name='English Name')

    class Meta:
        model = Member
        # exclude = ('christian', 'group', 'group_leader', 'active', 'username', 'slug')
        export_order = ('id', 'name', 'english_name', 'gender', 'job', 'email', 'phone_number', 'hometown',\
                        'birthday', 'habits', 'first_time')

        # widgets = {
        #     'first_time': {'format': '%m/%d/%Y'},
        # }


class ServiceResource(resources.ModelResource):
    servant_name = Field(column_name="Servants")
    service_category = Field(attribute='service_category', column_name='Category')
    service_date = Field(attribute='service_date', column_name='Date')
    # service_content = Field(attribute='service_content', column_name='Note')

    class Meta:
        model = Service
        exclude = ('id', 'coordinator', 'slug', 'servants')

    def dehydrate_servant_name(self, service):
        servants = service.servants.all()
        servant_names = [servant.name for servant in servants]
        return ','.join(servant_names)
