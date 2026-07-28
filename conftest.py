import pytest
from django.test import Client
from django.contrib.auth.models import User
from users.models import Profile


pytestmark = pytest.mark.django_db


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def user():
    user = User.objects.create_user(
        username='testuser',
        email='test@korva.ni',
        password='testpass123',
    )
    Profile.objects.create(
        user=user,
        business_name='Test Business',
        city='managua',
        sector='tecnologia',
        ruc='J0310000211111',
    )
    return user


@pytest.fixture
def authenticated_client(client, user):
    client.force_login(user)
    return client


@pytest.fixture
def another_user():
    user = User.objects.create_user(
        username='otheruser',
        email='other@korva.ni',
        password='testpass456',
    )
    Profile.objects.create(
        user=user,
        business_name='Other Business',
        city='leon',
        sector='alimentos',
        ruc='J0310000211112',
    )
    return user
