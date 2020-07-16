from django.forms import ModelForm
from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from bootstrap_modal_forms.forms import BSModalModelForm
from datetime import datetime as dt
from .models import Service, Group, SERVICE_GROUP
from users.models import User

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
    servants = forms.ModelChoiceField(User.objects.filter())
    # note = forms.CharField(initial='Make a note')

    def __init__(self, *args, **kwargs):
        service = kwargs.get('instance')
        # self.servicedate = kwargs.pop('servicedate')
        # category = kwargs.pop('category')
        # note = Service.objects.filter(service_date=kwargs.get('instance'),
        #                                   service_date=dt.strptime(self.servicedate, '%Y-%m-%d').date()).first().note
        # Change the initial note conent
        initial = kwargs.get('initial', {})
        initial['servants'] = service.servants
        kwargs['initial'] = initial
        # Initialize the instance
        super(ServiceUpdateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Service
        fields = ('servants', 'description', 'service_date', 'note')
        attrs = {'class': 'table table-sm'}
        widgets = {
            'service_date': DatePickerInput(),
        }

    # def save(self, commit=True):
    #     # service = Service.objects.filter(service)
    #     instance = super().save(commit)
    #     # set ServiceNote reverse foreign key from the Service model
    #     instance.servicenote_set.add(self.cleaned_data['note'])
    #     return instance



