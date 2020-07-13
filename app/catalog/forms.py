from django.forms import ModelForm
from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from bootstrap_modal_forms.forms import BSModalModelForm

from .models import Service, Group, ServiceNote, SERVICE_GROUP


class GroupForm(BSModalModelForm):
    class Meta:
        model = Group
        fields = ['name']


class ServiceForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
        self.fields['name'] = forms.ChoiceField(choices=SERVICE_GROUP)

    class Meta:
        model = Service
        exclude = ('slug', )
        # fields = ('service_date', 'service_category', 'edit')
        attrs = {'class': 'table table-sm'}
        # widgets = {
        #     'service_date': DatePickerInput(),  # default date-format %m/%d/%Y will be used
        #     # 'service_category': widgets.Select(attrs={'class': 'select'}),
        # }


class ServiceUpdateForm(ModelForm):
    notes = forms.ModelChoiceField(ServiceNote.objects.all())

    def __init__(self, *args, **kwargs):
        super(ServiceUpdateForm, self).__init__(*args, **kwargs)
        # self.fields['name'].widget.attrs['readonly'] = True

    class Meta:
        model = Service
        fields = ('servants', 'notes', )
        attrs = {'class': 'table table-sm'}
        # widgets = {
        #     'service_date': DatePickerInput(),
        # }

        def save(self, commit=True):
            instance = super().save(commit)
            # set ServiceNote reverse foreign key from the Service model
            instance.servicenote_set.add(self.cleaned_data['notes'])
            return instance



