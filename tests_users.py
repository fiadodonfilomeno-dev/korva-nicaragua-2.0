import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from users.models import Profile

pytestmark = pytest.mark.django_db


class TestUserRegistration:
    def test_register_page_status(self, client):
        response = client.get(reverse('register'))
        assert response.status_code == 200

    def test_register_new_user(self, client):
        data = {
            'username': 'nuevo',
            'email': 'nuevo@korva.ni',
            'password': 'Compleja123!',
            'password_confirm': 'Compleja123!',
            'business_name': 'Nueva Empresa',
            'city': 'managua',
            'sector': 'tecnologia',
            'ruc': 'J0310000211113',
        }
        response = client.post(reverse('register'), data)
        assert User.objects.filter(username='nuevo').exists()


class TestUserLogin:
    def test_login_page_status(self, client):
        response = client.get(reverse('login'))
        assert response.status_code == 200

    def test_login_valid_user(self, client, user):
        response = client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123',
        })
        assert response.url == reverse('home')

    def test_login_invalid_password(self, client, user):
        response = client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrong',
        })
        assert response.status_code == 200


class TestProfile:
    def test_profile_exists(self, user):
        assert hasattr(user, 'profile')
        assert user.profile.business_name == 'Test Business'

    def test_profile_page(self, client, user):
        client.force_login(user)
        response = client.get(reverse('profile', args=[user.username]))
        assert response.status_code == 200

    def test_profile_str(self, user):
        assert str(user.profile) == f"{user.profile.business_name} ({user.username})"

    def test_profile_created_at(self, user):
        assert user.profile.created_at is not None


class TestLogout:
    def test_logout_get_redirects(self, client, user):
        client.force_login(user)
        response = client.get(reverse('logout'))
        assert response.status_code == 302

    def test_logout_post_redirects(self, client, user):
        client.force_login(user)
        response = client.post(reverse('logout'))
        assert response.status_code == 302
