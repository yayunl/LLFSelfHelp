from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from django.forms import ModelForm
from django import forms
from django.template.defaultfilters import slugify
from bootstrap_datepicker_plus import DatePickerInput
from django.conf import settings
import os
# Project imports
from catalog.utils import ActivationMailFormMixin
from .models import User, Profile


class UserForm(ModelForm):
    class Meta:
        model = User
        exclude = ('id', 'username', 'password', 'slug', 'last_login', 'is_superuser',
                   'groups', 'user_permissions', 'is_staff')
        # labels = {
        #     'name': 'Chinese Name',
        # }

        help_texts ={
            'name': 'Required field',
            'email': 'Required field'
        }

        widgets = {
            'first_time_visit': DatePickerInput(),
            'date_joined': DatePickerInput(),
            'birthday': DatePickerInput(),
            # 'service_category': widgets.Select(attrs={'class': 'select'}),
        }


class LoginForm(AuthenticationForm):
    # username = forms.CharField(widget=forms.Textarea, label='')

    def __init__(self, request, *args, **kwargs):
        # simply do not pass 'request' to the parent
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'

    class Meta:
        model = User
        fields = ('username', 'password')
        labels = {
            'username': '',
            'password': ''
        }


class RegistrationForm(
        ActivationMailFormMixin,
        BaseUserCreationForm):

    name = forms.CharField(
        max_length=255,
        help_text=(
            "Your real name.")
    )
    username = forms.CharField(
        max_length=255,
        # help_text=(
        #     "The name displayed on your "
        #     "public profile.")
    )

    email = forms.EmailField(
        max_length=255,
        # help_text=(
        #     "The email displayed on your "
        #     "public profile.")
    )

    mail_validation_error = (
        'User created. Could not send activation '
        'email. Please try again later. (Sorry!)')

    class Meta(BaseUserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'name')

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
        admin = User.objects.filter(email=settings.ADMIN_EMAIL).first()

        # valid_member = Member.objects.filter(email=user.email).count()

        # if not valid_member:
        #     # raise ValidationError("You are not a LLF member. Please contact the LLF admin to add you to the group first.")
        #
        if not user.pk:
            user.is_active = False
            send_mail = True
        else:
            send_mail = False
        user.save()
        self.save_m2m()
        Profile.objects.update_or_create(
            user=user,
            defaults={
                'slug': slugify(user.get_name()),
            }
        )
        # Member.objects.update_or_create(
        #     username=user,
        #     defaults={
        #         'username': self.cleaned_data['username'],
        #         'slug': slugify(f"{self.cleaned_data['username']}-{self.cleaned_data['email'].split('@')[0]}"),
        #     })

        # Send email to admin for approval
        if send_mail and admin:
            self.send_mail(recipient=admin, **kwargs)
        return user


class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'english_name', 'phone_number',
                  'job', 'hometown', 'habits', 'birthday', 'gender', 'facebook',
                  'wechat', 'twitter', 'group')


class ResendActivationEmailForm(
        ActivationMailFormMixin, forms.Form):

    email = forms.EmailField()

    mail_validation_error = (
        'Could not re-send activation email. '
        'Please try again later. (Sorry!)')

    def save(self, **kwargs):
        User = get_user_model()
        admin = User.objects.filter(email=settings.ADMIN_EMAIL).first()

        try:
            user = User.objects.get(
                email=self.cleaned_data['email'])
        except:
            # logger.warning(
            #     'Resend Activation: No user with '
            #     'email: {} .'.format(
            #         self.cleaned_data['email']))
            return None

        # Notify the admin
        if admin:
            self.send_mail(recipient=admin, **kwargs)

        return user
