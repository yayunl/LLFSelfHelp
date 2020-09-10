import datetime

from django.test import TestCase

from users.forms import UserForm, RegisterationForm


class UserFormTest(TestCase):

    def test_user_form_name_field_label(self):
        form = UserForm()
        self.assertEqual(form.fields['name'].label, 'Name')

    def test_user_form_name_field_help_text(self):
        form = UserForm()
        self.assertEqual(form.fields['name'].help_text, 'Required field')


class RegisterationFormTest(TestCase):

    def test_registeration_form_username_field_label(self):
        form = RegisterationForm()
        self.assertTrue(form.fields['username'].label == None or
                        form.fields['username'].label == 'Username')

    def test_registeration_form_username_field_help_text(self):
        form = RegisterationForm()
        self.assertTrue(form.fields['username'].help_text =='The name displayed on your public profile.')

    def test_registeration_form_email_field_label(self):
        form = RegisterationForm()
        self.assertTrue(form.fields['email'].label==None)

    def test_registeration_form_email_field_max_length(self):
        form = RegisterationForm()
        self.assertEqual(form.fields['email'].max_length, 255)