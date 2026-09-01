import pytest
from django.contrib.auth.models import User
from users.models import Profile
from social.models import Post
from marketplace.models import Product


@pytest.fixture
def user(db):
    user = User.objects.create_user(username='testuser', password='testpass123')
    Profile.objects.create(user=user, business_name=user.username, ruc='J0310000123456', city='managua', sector='otros')
    return user


@pytest.fixture
def user2(db):
    u = User.objects.create_user(username='testuser2', password='testpass123')
    Profile.objects.create(user=u, business_name=u.username, ruc='J0310000123457', city='leon', sector='servicios')
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
