import pytest
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db


def test_get_suppliers_list(api_client, active_user, supplier):
    api_client.force_authenticate(user=active_user)
    url = reverse("supplier-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) >= 1


def test_create_supplier(api_client, active_user, contact):
    api_client.force_authenticate(user=active_user)
    url = reverse("supplier-list")

    data = {
        "name": "New Supplier",
        "contacts": {
            "email": contact.email,
            "country": contact.country,
            "city": contact.city,
            "street": contact.street,
            "house_number": contact.house_number,
        },
        "debt": 200.00,
    }

    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == "New Supplier"


def test_update_debt_is_not_allowed(api_client, active_user, supplier):
    api_client.force_authenticate(user=active_user)
    url = reverse("supplier-detail", kwargs={"pk": supplier.id})
    data = {"debt": 500.00}
    response = api_client.patch(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert float(response.data["debt"]) == 100.00


def test_filter_by_country(api_client, active_user, supplier):
    api_client.force_authenticate(user=active_user)
    url = reverse("supplier-list")
    response = api_client.get(url + "?contacts__country=Russia")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["name"] == supplier.name


def test_inactive_user_cannot_access_api(api_client, inactive_user):
    api_client.force_authenticate(user=inactive_user)
    url = reverse("supplier-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
