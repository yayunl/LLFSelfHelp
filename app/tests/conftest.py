import os, pytest
from django.urls import reverse
from django.core.management import call_command
from users.models import User


# @pytest.fixture(scope="function")
# def test_with_logon_client(client):
#     user = User.objects.create(name='fakeuser',
#                                username='fakeuser',
#                                email='fakeuser@test.com',
#                                password='fakepassword')
#     client.login(username=user.username, password=user.password)
#     response = client.get('/', follow=True)
#     assert response.status_code == 200
#     return client # testing starts here


@pytest.fixture(scope="function")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'initial_fixture.json')


@pytest.fixture
def test_password():
    return 'fakepassword'


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = 'fakeuser'
        if 'email' not in kwargs:
            kwargs['email'] = 'fakeuser@test.com'
        if 'name' not in kwargs:
            kwargs['name'] = 'fakeuser'
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def auto_login_user(db, client, create_user, test_password):
   def make_auto_login(user=None):
       if user is None:
           user = create_user()
       client.login(username=user.username, password=test_password)
       return client, user
   return make_auto_login
