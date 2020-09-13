# tests/users/test_views.py

import pytest

from django.urls import reverse


@pytest.mark.django_db
def test_user_detail(client, create_user):
   user = create_user(username='someone')
   url = reverse('user-detail-view', kwargs={'pk': user.pk})
   response = client.get(url)
   assert response.status_code == 200
   assert 'someone' in response.content


@pytest.mark.django_db
def test_superuser_detail(client, create_user):
   admin_user = create_user(
       username='custom-admin-name',
       is_staff=True, is_superuser=True
   )
   url = reverse(
       'superuser-detail-view', kwargs={'pk': admin_user.pk}
   )
   response = client.get(url)
   assert response.status_code == 200
   assert 'custom-admin-name' in response.content
