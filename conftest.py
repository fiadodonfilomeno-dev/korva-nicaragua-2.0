import pytest
from django.contrib.auth.models import User
from users.models import Profile
from social.models import Post
from marketplace.models import Product


@pytest.fixture
def user(db):
    user = User.objects.create_user(username='testuser', password='testpass123')
    profile = user.profile
    profile.business_name = user.username
    profile.ruc = 'J0310000123456'
    profile.city = 'managua'
    profile.sector = 'otros'
    profile.save()
    return user


@pytest.fixture
def user2(db):
    u = User.objects.create_user(username='testuser2', password='testpass123')
    profile = u.profile
    profile.business_name = u.username
    profile.ruc = 'J0310000123457'
    profile.city = 'leon'
    profile.sector = 'servicios'
    profile.save()
    return u


@pytest.fixture
def profile(user):
    return Profile.objects.get(user=user)


@pytest.fixture
def profile2(user2):
    return Profile.objects.get(user=user2)


@pytest.fixture
def post(profile):
    return Post.objects.create(
        title='Test Post',
        content='Test content for the post',
        author=profile
    )


@pytest.fixture
def product(profile):
    return Product.objects.create(
        name='Test Product',
        description='Test description',
        price=100.00,
        category='ventas',
        contact_whatsapp='+50587654321',
        user=profile
    )


@pytest.fixture
def client_logged_in(client, user):
    client.login(username='testuser', password='testpass123')
    return client
