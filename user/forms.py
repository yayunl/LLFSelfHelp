from django.forms import ModelForm
from .models import Member


class MemberForm(ModelForm):
    class Meta:
        model = Member
        fields = ['name','english_name', 'gender','email','phone_number','job',
                  'birthday','hometown','active','group_leader','christian',
                  'group','first_time','habits','slug']