import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile, EmailVerificationToken


class TestProfileModel:
    def test_profile_created_on_user_create(self, user):
        profile = Profile.objects.get(user=user)
        assert profile.business_name == user.username
        assert profile.popularity_score == 0

    def test_profile_str(self, profile):
        assert f"({profile.user.username})" in str(profile)
        assert profile.business_name in str(profile)

    def test_tier_bronze(self, profile):
        profile.popularity_score = 0
        assert profile.tier == 'bronce'

    def test_tier_plata(self, profile):
        profile.popularity_score = 1000
        assert profile.tier == 'plata'

    def test_tier_oro(self, profile):
        profile.popularity_score = 2500
        assert profile.tier == 'oro'

    def test_tier_vip(self, profile):
        profile.popularity_score = 5000
        assert profile.tier == 'vip'


class TestEmailVerificationToken:
    def test_token_created(self, user):
        token = EmailVerificationToken.objects.create(user=user)
        assert token.is_valid()

    def test_token_str(self, user):
        token = EmailVerificationToken.objects.create(user=user)
        assert str(token) == f"Token para {user.email}"


class TestAuthViews:
    def test_register_view(self, client):
        response = client.get(reverse('register'))
        assert response.status_code == 200

    def test_login_view(self, client):
        response = client.get(reverse('login'))
        assert response.status_code == 200

    def test_register_user(self, client, db):
        data = {
            'username': 'newuser',
            'email': 'new@test.com',
            'password': 'TestPass123!',
            'password_confirm': 'TestPass123!',
            'business_name': 'New User Business',
            'ruc': 'J0310000123499',
            'city': 'managua',
            'sector': 'otros',
        }
        response = client.post(reverse('register'), data)
        assert User.objects.filter(username='newuser').exists()

    def test_login_user(self, client, user):
        response = client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123',
        })
        assert response.status_code == 302

    def test_profile_view(self, client, user):
        client.login(username='testuser', password='testpass123')
        response = client.get(reverse('profile', args=['testuser']))
        assert response.status_code == 200

    def test_edit_profile_view(self, client_logged_in):
        response = client_logged_in.get(reverse('edit_profile'))
        assert response.status_code == 200

    def test_logout(self, client_logged_in):
        response = client_logged_in.get(reverse('logout'))
        assert response.status_code == 302
