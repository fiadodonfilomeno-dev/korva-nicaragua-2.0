import pytest
from django.urls import reverse
from .models import Product


class TestProductModel:
    def test_product_creation(self, product):
        assert product.name == 'Test Product'
        assert product.price == 100.00
        assert product.views_count == 0

    def test_product_str(self, product):
        assert product.name in str(product) and product.user.business_name in str(product)

    def test_views_count_default(self, product):
        assert product.views_count == 0


class TestMarketplaceViews:
    def test_marketplace_view(self, client, db):
        response = client.get(reverse('marketplace'))
        assert response.status_code == 200

    def test_marketplace_with_products(self, client, db, product):
        response = client.get(reverse('marketplace'))
        assert response.status_code == 200

    def test_marketplace_search(self, client, db, product):
        response = client.get(reverse('marketplace') + '?q=Test')
        assert response.status_code == 200

    def test_marketplace_filter_category(self, client, db, product):
        response = client.get(reverse('marketplace') + '?category=ventas')
        assert response.status_code == 200

    def test_create_product_requires_login(self, client):
        response = client.get(reverse('create_product'))
        assert response.status_code == 302

    def test_create_product_authenticated(self, client_logged_in):
        response = client_logged_in.get(reverse('create_product'))
        assert response.status_code == 200

    def test_product_detail(self, client, db, product):
        response = client.get(reverse('product_detail', args=[product.id]))
        assert response.status_code == 200

    def test_product_detail_increments_views(self, client, db, product):
        client.get(reverse('product_detail', args=[product.id]))
        product.refresh_from_db()
        assert product.views_count == 1
