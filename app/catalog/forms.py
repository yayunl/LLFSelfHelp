from django.forms import ModelForm
from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from bootstrap_modal_forms.forms import BSModalModelForm

from .models import Service, Group, Category
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
        instance = super().save(commit=False)
        instance.name = self.cleaned_data['name']
        instance.description = self.cleaned_data['description']
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
        self.fields['service_date'].required=True

    def save(self, commit=True):
        instance = super().save(commit)
        # set ServiceNote reverse foreign key from the Service model
        # for servant in self.cleaned_data['servants']:
        #     instance.user_set.add(servant)
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





