import pytest
from pytest_factoryboy import register
from .factories import UserFactory, GroupFactory, CategoryFactory, \
    ServiceFactory, ServicesOfWeekFactory, ProfileFactory

register(UserFactory)
register(GroupFactory)
register(CategoryFactory)
register(ServiceFactory)
register(ServicesOfWeekFactory)
register(ProfileFactory)


@pytest.fixture
def test_password():
    return 'fakepassword'


@pytest.fixture
def auto_login_user(db, client, user_factory, test_password):
   def make_auto_login(user=None):
       if user is None:
           user = user_factory()
       client.login(username=user.username, password=test_password)
       return client, user
   return make_auto_login

# Do not use fixture data to initialize test data.
# Recommend to use factory boy to create test data.

# @pytest.fixture(scope="function")
# def django_db_setup(django_db_setup, django_db_blocker):
#     with django_db_blocker.unblock():
#         call_command('loaddata', 'initial_fixture.json')

