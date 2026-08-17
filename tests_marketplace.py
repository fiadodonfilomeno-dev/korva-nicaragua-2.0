import pytest
from django.urls import reverse
from marketplace.models import Product
from decimal import Decimal

pytestmark = pytest.mark.django_db


class TestMarketplace:
    def test_marketplace_status(self, client):
        response = client.get(reverse('marketplace'))
        assert response.status_code == 200

    def test_create_product_page(self, authenticated_client):
        response = authenticated_client.get(reverse('create_product'))
        assert response.status_code == 200

    def test_product_detail(self, authenticated_client, user):
        product = Product.objects.create(
            user=user.profile,
            name='Producto Detalle',
            description='Desc',
            price=Decimal('50.00'),
            currency='NIO',
            category='ventas',
            contact_whatsapp='+50588888888',
        )
        response = authenticated_client.get(reverse('product_detail', args=[product.id]))
        assert response.status_code == 200

    def test_my_products(self, authenticated_client, user):
        Product.objects.create(
            user=user.profile,
            name='Mi Producto',
            description='Desc',
            price=Decimal('30.00'),
            currency='NIO',
            category='ventas',
            contact_whatsapp='+50588888888',
        )
        response = authenticated_client.get(reverse('my_products'))
        assert response.status_code == 200

    def test_toggle_favorite(self, authenticated_client, user):
        product = Product.objects.create(
            user=user.profile,
            name='Fav Product',
            description='Desc',
            price=Decimal('10.00'),
            currency='NIO',
            category='ventas',
            contact_whatsapp='+50588888888',
        )
        response = authenticated_client.post(reverse('toggle_favorite_product', args=[product.id]))
        assert response.status_code in (200, 302)


class TestProductModel:
    def test_product_str(self, user):
        product = Product.objects.create(
            user=user.profile,
            name='Test',
            description='X',
            price=Decimal('10.00'),
            currency='USD',
            category='ventas',
            contact_whatsapp='+50588888888',
        )
        assert str(product) == f'Test - {user.profile.business_name}'

    def test_default_active(self, user):
        product = Product.objects.create(
            user=user.profile,
            name='Test', description='X',
            price=Decimal('10.00'), currency='USD',
            category='ventas',
            contact_whatsapp='+50588888888',
        )
        assert product.is_active is True

    def test_default_views_count(self, user):
        product = Product.objects.create(
            user=user.profile,
            name='Test', description='X',
            price=Decimal('10.00'), currency='USD',
            category='ventas',
            contact_whatsapp='+50588888888',
        )
        assert product.views_count == 0
