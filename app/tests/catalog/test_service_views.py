import pytest
from pytest_factoryboy import LazyFixture
from django.urls import reverse
from tests.utils import export_to_html, str2bytes


# Test service views
@pytest.mark.django_db
def test_get_services_view(auto_login_user, user_factory, category_factory, service_factory):
    # create initial test data
    servants = user_factory.create_batch(2)
    cat = category_factory.create()
    service = service_factory.create(categories=[cat], servants=servants)
    # logon
    client, user = auto_login_user() # create a regular user
    # get the page
    url = reverse('service_list')
    resp = client.get(url)
    assert resp.status_code == 200
    export_to_html(resp, 'get_services_view.html')
    # asserts
    for ser in servants:
        assert str2bytes(ser.name) in resp.content
    assert str2bytes(cat.name) in resp.content


@pytest.mark.django_db
def test_create_service_view(auto_login_user, auto_login_staff,
                             user_factory, category_factory, service_factory):
    # Create test data
    servants = user_factory.create_batch(2)
    cat = category_factory.create()
    service = service_factory.create(categories=[cat], servants=servants)
    reg_client, reg_user = auto_login_user() # create a regular user
    # Get the service create route
    url = reverse('service_create')
    resp = reg_client.post(url,
                           data=dict(note='test note',
                                     service_date=service.date_to_str,
                                     categories=cat,
                                     servants=servants
                                     ),
                           follow=True)
    assert resp.status_code == 200
    export_to_html(resp, 'create_services_view_by_reg_user.html')
    # asserts
    # for ser in servants:
    #     assert str2bytes(ser.name) in resp.content
    # assert str2bytes(cat.name) in resp.content


@pytest.mark.django_db
@pytest.mark.parametrize("service__servants", [LazyFixture("default_user")])
@pytest.mark.parametrize("service__categories", [(LazyFixture("default_category"))])
def test_detail_service_view(auto_login_user, service):
    service_slug = service.slug
    servants = service.servant_names
    client, user = auto_login_user() # create auto logon user

    url = reverse('service_detail', kwargs={'slug': service_slug})
    resp = client.get(url)
    assert resp.status_code == 200
    export_to_html(resp, 'detail_service_view.html')

    # asserts
    assert str2bytes(service.category_names) in resp.content
    assert str2bytes(service.note) in resp.content
    for ser in servants:
        assert str2bytes(ser) in resp.content


# @pytest.mark.django_db
# @pytest.mark.parametrize("service__servants", [LazyFixture("default_user")])
# @pytest.mark.parametrize("service__categories", [(LazyFixture("default_category"))])
# def test_update_service_view_get_method(auto_login_staff, service, another_user, another_category):
#     service_slug = service.slug
#     servants = service.servant_names
#     client, user = auto_login_staff() # create auto logon user
#
#     url = reverse('service_update', kwargs={'slug': service_slug})
#
#     resp = client.post(url,
#                        data=dict(note='New note',
#                                  service_date=service.date_to_str,
#                                  categories=another_category,
#                                  servants=another_user
#                                  ),
#                        follow=True)
#     export_to_html(resp, 'update_service_view.html')
#     assert resp.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize("service__servants", [LazyFixture("default_user")])
@pytest.mark.parametrize("service__categories", [(LazyFixture("default_category"))])
def test_delete_service_view(auto_login_user, auto_login_staff, service):
    service_slug = service.slug
    # get delete route
    url = reverse('service_delete', kwargs={'slug': service_slug})

    # create regular user
    reg_client, reg_user = auto_login_user()
    # actual test
    resp = reg_client.get(url)
    export_to_html(resp, 'delete_service_view_by_reg_user.html')
    assert resp.status_code == 403
    assert str2bytes("Permission Denied") in resp.content

    # Create staff user
    staff_client, staff = auto_login_staff()
    resp = staff_client.get(url)
    export_to_html(resp, 'delete_service_view_by_staff_user.html')
    assert resp.status_code == 200
    assert str2bytes(f"Are you sure you want to delete Service: {service.slug}") in resp.content

