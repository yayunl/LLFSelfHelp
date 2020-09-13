# app/tests/users/test_models.py

import pytest

from users.models import User

@pytest.mark.django_db
def test_user_model():
    user = User(username='fakeuser', password='fakepass', email='fakeemail@test.com', name='fakeuser')
    user.save()

    assert user.username == 'fakeuser'
    assert user.password == 'fakepass'
    assert user.email == 'fakeemail@test.com'