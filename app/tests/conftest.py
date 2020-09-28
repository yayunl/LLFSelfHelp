import pytest
from pytest_factoryboy import register
from .factories import UserFactory, GroupFactory, CategoryFactory, \
    ServiceFactory, ServicesOfWeekFactory, ProfileFactory

register(UserFactory, "default_user")
register(UserFactory, "another_user")
register(UserFactory, "staff_user", is_staff=True)
register(GroupFactory)
register(CategoryFactory, "default_category")
register(CategoryFactory, "another_category")
register(ServiceFactory)
register(ServicesOfWeekFactory)
register(ProfileFactory)


@pytest.fixture
def test_password():
    return 'fakepassword'


# @pytest.fixture
# def chrome_options(chrome_options):
#     chrome_options.binary_location = 'chromedriver.exe' # Add the driver path to system env
#     chrome_options.add_argument('--kiosk')
#     return chrome_options


@pytest.fixture
def auto_login_user(db, client, user_factory, test_password):
   def make_auto_login(user=None):
       if user is None:
           user = user_factory(username='regular_user')
       client.login(username=user.username, password=test_password)
       return client, user
   return make_auto_login


@pytest.fixture
def auto_login_staff(db, client, user_factory, test_password):
   def make_auto_login(user=None):
       if user is None:
           user = user_factory.create(username='staff_user', is_staff=True)
       client.login(username=user.username, password=test_password)
       return client, user
   return make_auto_login


@pytest.fixture
def auto_login_superuser(db, client, user_factory, test_password):
   def make_auto_login(user=None):
       if user is None:
           user = user_factory.create(username='super_user', is_staff=True, is_superuser=True)
       client.login(username=user.username, password=test_password)
       return client, user
   return make_auto_login

# Do not use fixture data to initialize test data.
# Recommend to use factory boy to create test data.

# @pytest.fixture(scope="function")
# def django_db_setup(django_db_setup, django_db_blocker):
#     with django_db_blocker.unblock():
#         call_command('loaddata', 'initial_fixture.json')

