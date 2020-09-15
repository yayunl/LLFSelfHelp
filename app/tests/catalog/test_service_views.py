import pytest
from pytest_factoryboy import LazyFixture
from django.urls import reverse
from tests.utils import export_to_html, str2bytes


# Test service views
@pytest.mark.django_db
@pytest.mark.parametrize("service__servants", [LazyFixture("default_user")])
@pytest.mark.parametrize("service__categories", [LazyFixture("default_category")])
def test_create_service_view(auto_login_user, service):
    client, user = auto_login_user() # create auto logon user

    url = reverse('service_list')
    resp = client.get(url)
    assert resp.status_code == 200
    export_to_html(resp, 'get_services_view.html')
    # assert