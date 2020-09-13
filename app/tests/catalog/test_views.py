# tests/catalog/test_views.py

import pytest
from django.urls import reverse
from tests.utils import export_to_html


# Test group views
@pytest.mark.django_db
def test_list_group_view(auto_login_user, django_db_setup):
    client, user = auto_login_user() # create auto logon user
    url = reverse('group_list')
    resp = client.get(url)
    assert resp.status_code == 200
    export_to_html(resp, 'get_groups_view.html')
    assert b"Group 1" in resp.content
    assert b"Group 2" in resp.content
    assert b"Group 3" in resp.content
    # Sermon group is not shown on the page if the tester is not admin
    assert b"Sermon" not in resp.content


# Test category views
@pytest.mark.django_db
def test_list_category_view(auto_login_user, django_db_setup):
    client, user = auto_login_user() # create auto logon user
    url = reverse('category_list')
    resp = client.get(url)
    assert resp.status_code == 200
    export_to_html(resp, 'get_categories_view.html')
    assert b"Category 1" in resp.content
    assert b"Category 2" in resp.content
    assert b"Category 3" in resp.content
    assert b"Sermon" in resp.content
