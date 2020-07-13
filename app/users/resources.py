from import_export import resources
from import_export.fields import Field
from .models import User


class UserResource(resources.ModelResource):

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
        model = User
        exclude = ('username', 'password_hash', 'slug')
        export_order = ('id', 'name', 'english_name', 'gender', 'job', 'email', 'phone_number', 'hometown',\
                        'birthday', 'habits', 'first_time')

        # widgets = {
        #     'first_time': {'format': '%m/%d/%Y'},
        # }

