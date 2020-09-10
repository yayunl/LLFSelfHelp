from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import User


# tutorial : https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing

class UserListViewTest(TestCase):

    def setUp(self):
        # Create 13 users for pagination tests
        number_of_users = 13

        for user_id in range(number_of_users):
            usr = User.objects.create(
                name=f'User_{user_id}',
                username=f'user_{user_id}',
                # password='password',
                email=f'user_{user_id}@test.com'
            )
            usr.set_password('password')
            usr.save()

    # def test_redirect_if_not_logged_in(self):
    #     response = self.client.get(reverse('user_list'))
    #     self.assertRedirects(response, '/auth/login/?next=/user/list/')

    def test_logged_in_view_url_exists_at_desired_location(self):
        login = self.client.login(username='user_0', password='password')
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, 200)
        # Check the correct template is used
        self.assertTemplateUsed(response, 'users/user_list.html')

    def test_pagination_is_ten(self):
        login = self.client.login(username='user_0', password='password')
        response = self.client.get(reverse('user_list'))
        table = response.context.get('table')
        page = getattr(table, 'page')
        self.assertTrue(len(page.object_list.data)==10)

    def test_lists_all_users(self):
        login = self.client.login(username='user_0', password='password')
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('user_list')+ '?page=2')
        self.assertEqual(response.status_code, 200)
        table = response.context.get('table')
        self.assertTrue(len(table.page.object_list.data) == 3)


class UserCreateTest(TestCase):

    def test_create_account_view(self):
        self.client.post()