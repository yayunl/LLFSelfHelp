from bootstrap_modal_forms.forms import BSModalModelForm
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django import forms
from django.forms import ModelForm
from django.template.defaultfilters import slugify
from bootstrap_datepicker_plus import DatePickerInput
# Project imports
from catalog.utils import ActivationMailFormMixin
from .models import User, Profile
from .utils import GENDER


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


class RegistrationForm(
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
        if send_mail:
            self.send_mail(user=user, **kwargs)
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
