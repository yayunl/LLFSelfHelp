from django.test import TestCase
from users.models import User


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        test_user = User.objects.create(name='tester',
                                        email='tester@test.com',
                                        username='tester',
                                        )
        test_user.set_password("password")

    # def setUp(self):
    #     print("setUp: Run once for every test method to setup clean data.")
    #     pass

    def test_name_label(self):
        tester = User.objects.get(id=1)
        field_label = tester._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_username_max_length(self):
        tester = User.objects.get(id=1)
        max_length = tester._meta.get_field('username').max_length
        self.assertEqual(max_length, 50)

    def test_email_label(self):
        tester = User.objects.get(id=1)
        field_label = tester._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'email')

    def test_get_unique_slug(self):
        tester = User.objects.get(id=1)
        self.assertEqual(tester.slug, 'tester')

    def test_get_absolute_url(self):
        tester = User.objects.get(id=1)
        self.assertEqual(tester.get_absolute_url(), '/user/tester/detail')

    def test_get_absolute_delete_url(self):
        tester = User.objects.get(id=1)
        self.assertEqual(tester.get_absolute_delete_url(), '/user/tester/delete')

    def test_get_absolute_update_url(self):
        tester = User.objects.get(id=1)
        self.assertEqual(tester.get_absolute_update_url(), '/user/tester/update')