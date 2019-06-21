from django.forms import ModelForm
from django import forms
from .models import Member


class MemberForm(ModelForm):
    class Meta:
        model = Member
        fields = ['name','english_name', 'gender','email','phone_number','job',
                  'birthday','hometown','active','group_leader','christian',
                  'group','first_time','habits','slug']
        widgets = {'slug': forms.HiddenInput()}

        def clean_slug(self):
            """
            Clean the slug field
            :return:
            """
            eng_name = self.cleaned_data['english_name']
            email = self.cleaned_data['email'].split('@')[0]
            return '_'.join([eng_name, email]).lower()

        def save(self, request, commit=True):
            post = super().save(commit=False)
            # if not post.pk:
            #     post.author = get_user(request)
            if commit:
                post.save()
                self.save_m2m()
            return post