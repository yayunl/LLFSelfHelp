from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserChangeForm as BaseUserChangeForm,
    UserCreationForm as BaseUserCreationForm)

from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.forms.widgets import SelectDateWidget
from django import forms
from bootstrap_datepicker_plus import DatePickerInput

from .models import Member, Service
from .utils import ActivationMailFormMixin
from django.forms import widgets


class MemberForm(ModelForm):
    class Meta:
        model = Member
        fields = ['name','english_name', 'gender','email', 'group']
            # ,'phone_number','job',
            #       'birthday','hometown','active','group_leader','christian',
            #       'group','first_time','habits']
        # widgets = {'slug': forms.HiddenInput()}


class ServiceForm(ModelForm):
    try:
        service_category = forms.ChoiceField(choices=set([(s.service_category, s.id) for s in Service.objects.all()]))
    except:
        service_category = forms.ChoiceField(choices=set())

    class Meta:
        model = Service
        exclude = ('slug', 'coordinator')
        # fields = ('service_date', 'service_category', 'edit')
        attrs = {'class': 'table table-sm'}
        widgets = {
            'service_date': DatePickerInput(),  # default date-format %m/%d/%Y will be used
            'service_category': widgets.Select(attrs={'class': 'select'}),
        }


class ServiceUpdateForm(ModelForm):
    # service_category = forms.ChoiceField(choices=set([(s.service_category, s.service_category) for s in Service.objects.all()]))

    class Meta:
        model = Service
        exclude = ('slug', 'coordinator')
        # fields = ('service_date', 'service_category', 'edit')
        attrs = {'class': 'table table-sm'}
        widgets = {
            'service_date': DatePickerInput(),  # default date-format %m/%d/%Y will be used
            'service_category': widgets.Select(attrs={'class': 'select'}),
        }


class ResendActivationEmailForm(
        ActivationMailFormMixin, forms.Form):

    email = forms.EmailField()

    mail_validation_error = (
        'Could not re-send activation email. '
        'Please try again later. (Sorry!)')

    def save(self, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(
                email=self.cleaned_data['email'])
        except:
            # logger.warning(
            #     'Resend Activation: No user with '
            #     'email: {} .'.format(
            #         self.cleaned_data['email']))
            return None
        self.send_mail(user=user, **kwargs)
        return user


class UserCreationForm(
        ActivationMailFormMixin,
        BaseUserCreationForm):

    username = forms.CharField(
        max_length=255,
        help_text=(
            "The name displayed on your "
            "public profile."))

    email = forms.EmailField(
        max_length=255,
        help_text=(
            "The email displayed on your "
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
        # Member.objects.update_or_create(
        #     username=user,
        #     defaults={
        #         'username': self.cleaned_data['username'],
        #         'slug': slugify(f"{self.cleaned_data['username']}-{self.cleaned_data['email'].split('@')[0]}"),
        #     })
        if send_mail:
            self.send_mail(user=user, **kwargs)
        return user