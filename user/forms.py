from django.forms import ModelForm
from django import forms
from .models import Member, Service


class MemberForm(ModelForm):
    class Meta:
        model = Member
        fields = ['name','english_name', 'gender','email', 'group']
            # ,'phone_number','job',
            #       'birthday','hometown','active','group_leader','christian',
            #       'group','first_time','habits']
        # widgets = {'slug': forms.HiddenInput()}


class ServiceForm(ModelForm):
    class Meta:
        model = Service
        exclude = ('slug',)
