from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserChangeForm as BaseUserChangeForm,
    UserCreationForm as BaseUserCreationForm)

from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django import forms
from .models import Member, Service
from .utils import ActivationMailFormMixin

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


class UserCreationForm(
        ActivationMailFormMixin,
        BaseUserCreationForm):

    username = forms.CharField(
        max_length=255,
        help_text=(
            "The name displayed on your "
            "public profile."))

    mail_validation_error = (
        'User created. Could not send activation '
        'email. Please try again later. (Sorry!)')

    class Meta(BaseUserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email')

    def clean_username(self):
        username = self.cleaned_data['username']
        disallowed = (
            'activate',
            'create',
            'disable',
            'login',
            'logout',
            'password',
            'profile',
        )
        if username in disallowed:
            raise ValidationError(
                "A user with that username"
                " already exists.")
        return username

    def save(self, **kwargs):
        user = super().save(commit=False)
        if not user.pk:
            user.is_active = False
            send_mail = True
        else:
            send_mail = False
        user.save()
        self.save_m2m()
        Member.objects.update_or_create(
            username=user,
            defaults={
                'username': self.cleaned_data['username'],
                'slug': slugify(f"{self.cleaned_data['username']}-{self.cleaned_data['email'].split('@')[0]}"),
            })
        if send_mail:
            self.send_mail(user=user, **kwargs)
        return user