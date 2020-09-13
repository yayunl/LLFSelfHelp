import pytest


@pytest.mark.django_db
def test_user_user_factory(user_factory):
   user = user_factory()
   assert user.username == 'fakeuser0'
   assert user.email == 'fakeuser0@test.com'
   assert user.check_password('fakepassword')
   # assert user.groups.count() == 1