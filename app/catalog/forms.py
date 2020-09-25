from django.forms import ModelForm, formset_factory
from django.forms.models import inlineformset_factory

from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit

from django.core.exceptions import ValidationError
from .utils import Formset, str2date
from .models import Service, Group, Category, ServicesOfWeek
from users.models import User


class GroupForm(ModelForm):

    class Meta:
        model = Group
        fields = ['name', 'description']

        labels= {
            'name': 'Group name',
            'description': 'Group description',
        }

    # def clean_name(self):
    #     """
    #     Clean_fieldname method to sanitize the input name.
    #     :return:
    #     """
    #     return self.cleaned_data['name'].lower()

    def save(self, commit=True):
        instance = super().save(commit)
        if commit:
            instance.save()
        return instance


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

        labels= {
            'name': 'Category name',
            'description': 'Category description',
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.name = self.cleaned_data['name']
        instance.description = self.cleaned_data['description']
        if commit:
            instance.save()
        return instance


class ServiceForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
        # self.fields['service_date'].required=False

    def save(self, commit=True):
        service_date = self.instance.service_date
        services_of_week = ServicesOfWeek(services_date=str2date(service_date))
        services_of_week.save()

        instance = super().save(commit=False)
        # set ServiceNote reverse foreign key from the Service model
        # for servant in self.cleaned_data['servants']:
        #     instance.user_set.add(servant)
        instance.services_of_week = services_of_week
        instance.save()

        # instance.service_date = self.cleaned_data['service_date']
        instance.categories.add(self.cleaned_data['categories'][0])
        instance.servants.set(list())
        for ser in self.cleaned_data['servants']:
            instance.servants.add(ser)

        if commit:
            instance.save()
        return instance

    class Meta:
        model = Service
        fields = ('service_date', 'categories', 'servants', 'note')
        widgets = {
            'note': forms.Textarea(attrs={'cols': 10, 'rows': 5}),  # default date-format %m/%d/%Y will be used
            'service_date': DatePickerInput(),
            # 'service_category': widgets.Select(attrs={'class': 'select'}),
        }


class ServiceUpdateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        # service = kwargs.get('instance')
        # initial = kwargs.get('initial', {})
        # initial['servants'] = service.servants
        # kwargs['initial'] = initial
        # Initialize the instance
        super(ServiceUpdateForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit)
        # set ServiceNote reverse foreign key from the Service model
        # for servant in self.cleaned_data['servants']:
        #     instance.user_set.add(servant)

        return instance

    class Meta:
        model = Service
        fields = ('servants', 'service_date', 'categories', 'note')
        attrs = {'class': 'table table-sm'}
        widgets = {
            'service_date': DatePickerInput(),
        }


# Bulk form
class ServicesOfWeekForm(ModelForm):

    class Meta:
        model = ServicesOfWeek
        exclude = ('id',)
        widgets = {
            'services_date': DatePickerInput(),
        }

    def __init__(self, *args, **kwargs):
        super(ServicesOfWeekForm, self).__init__(*args, **kwargs)
        # self.fields['services_date'].required=True
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2 create-label'
        self.helper.field_class = 'col-md-10'
        self.helper.layout = Layout(
            Div(
                Field('services_date'),
                Fieldset('Add services',
                         Formset('services')),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'Save')),
            )
        )


ServiceFormSet = inlineformset_factory(ServicesOfWeek, Service, form=ServiceForm,
                                       fields=['categories', 'servants', 'note'], #'service_date',
                                       extra=1, can_delete=True)

