import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from suppliers.models import Contact, Product, Supplier

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def active_user(db):
    return User.objects.create_user(username="testuser", email="test@example.com", password="password", is_active=True)


@pytest.fixture
def inactive_user(db):
    return User.objects.create_user(
        username="inactiveuser", email="inactive@example.com", password="password", is_active=False
    )


@pytest.fixture
def contact(db):
    return Contact.objects.create(
        email="new_contact@example.com", country="Russia", city="Moscow", street="Lenina", house_number="1"
    )


@pytest.fixture
def product(db):
    return Product.objects.create(name="Test Product", model="Model X", release_date="2023-01-01")


@pytest.fixture
def supplier(db, contact, product):
    supplier = Supplier.objects.create(name="Test Supplier", contacts=contact, debt=100.00)
    supplier.products.add(product)
    return supplier
