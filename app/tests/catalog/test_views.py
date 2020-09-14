# tests/catalog/test_views.py

import pytest
from pytest_factoryboy import LazyFixture
from django.urls import reverse
from tests.utils import export_to_html, str2bytes


# Test group views
@pytest.mark.django_db
def test_list_group_view(auto_login_user, group_factory):
    client, user = auto_login_user() # create auto logon user
    # create 3 test groups
    groups = group_factory.create_batch(3)
    url = reverse('group_list')
    resp = client.get(url)
    assert resp.status_code == 200
    export_to_html(resp, 'get_groups_view.html')
    # Assert group names are on the response content
    for gp in groups:
        assert str2bytes(gp.name) in resp.content


@pytest.mark.django_db
def test_create_group_view(auto_login_user):
    client, user = auto_login_user() # create auto logon user
    url = reverse('group_create')
    resp = client.post(url,
                       data=dict(name='New Group',
                                 description='new group'),
                       follow=True
                       )
    assert resp.status_code == 200
    export_to_html(resp, 'create_group_view.html')
    assert b"Group: New Group was created." in resp.content
    assert b"New Group" in resp.content


@pytest.mark.django_db
def test_update_group_view(auto_login_user, group_factory):
    client, user = auto_login_user() # create auto logon user
    # Create a test group
    test_group = group_factory.create()
    test_group_slug = test_group.slug
    # Assert the test group is added
    url = reverse('group_list')
    resp = client.get(url)
    assert str2bytes(test_group.name) in resp.content

    # Update the test group
    url = reverse('group_update', kwargs={'slug' : test_group_slug})
    resp = client.post(url,
                       data=dict(name='Update Group', # New name
                                 description='update group'),
                       follow=True
                       )
    # Assert the update
    assert resp.status_code == 200
    export_to_html(resp, 'update_group_view.html')
    assert str2bytes("Group: Update Group was updated.") in resp.content
    assert str2bytes("Update Group") in resp.content


@pytest.mark.django_db
def test_detail_group_view(auto_login_user, group_factory):
    client, user = auto_login_user() # create auto logon user
    test_group = group_factory.create()
    test_group_slug = test_group.slug
    # Assert the test group is added
    url = reverse('group_list')
    resp = client.get(url)
    assert str2bytes(test_group.name) in resp.content

    # View details of the test group
    url = reverse('group_detail', kwargs={'slug' : test_group_slug})
    resp = client.get(url, follow=True)

    # Assert the details
    assert resp.status_code == 200
    export_to_html(resp, 'detail_group_view.html')
    assert str2bytes(test_group.name) in resp.content
    assert str2bytes(test_group.description) in resp.content

    
# Test category views
@pytest.mark.django_db
def test_list_category_view(auto_login_user, category_factory):
    client, user = auto_login_user() # create auto logon user
    # Create three service categories
    cats = category_factory.create_batch(3)

    url = reverse('category_list')
    resp = client.get(url)
    assert resp.status_code == 200
    export_to_html(resp, 'get_categories_view.html')

    for cat in cats:
        assert str2bytes(cat.name) in resp.content


@pytest.mark.django_db
def test_create_category_view(auto_login_user):
    client, user = auto_login_user() # create auto logon user
    url = reverse('category_create')
    resp = client.post(url,
                       data=dict(name='New Category',
                                 description='new category'),
                       follow=True
                       )
    assert resp.status_code == 200
    export_to_html(resp, 'create_category_view.html')
    assert b"Category: New Category was created." in resp.content
    assert b"New Category" in resp.content


@pytest.mark.django_db
def test_update_category_view(auto_login_user, category_factory):
    client, user = auto_login_user() # create auto logon user
    # Create a test category
    test_category = category_factory.create()
    test_category_slug = test_category.slug

    # Assert the test group is added
    url = reverse('category_list')
    resp = client.get(url)
    assert str2bytes(test_category.name) in resp.content

    # Update the test group
    url = reverse('group_update', kwargs={'slug': test_category_slug})
    resp = client.post(url,
                       data=dict(name='Update Category',
                                 description='update category'),
                       follow=True
                       )
    # Assert the update
    assert resp.status_code == 200
    export_to_html(resp, 'update_category_view.html')
    assert str2bytes(f"Category: Update Category was updated.") in resp.content
    assert str2bytes("Update Category") in resp.content


@pytest.mark.django_db
def test_detail_category_view(auto_login_user, category_factory):
    client, user = auto_login_user() # create auto logon user

    # Create a test category
    test_cat = category_factory.create()
    test_cat_slug = test_cat.slug

    # Assert the test category is added
    url = reverse('category_list')
    resp = client.get(url)
    assert str2bytes(test_cat.name) in resp.content

    # View details of the test category
    url = reverse('category_detail', kwargs={'slug' : test_cat_slug})
    resp = client.get(url, follow=True)

    # Assert the details
    assert resp.status_code == 200
    export_to_html(resp, 'detail_category_view.html')
    assert str2bytes(test_cat.name) in resp.content
    assert str2bytes(test_cat.description) in resp.content
