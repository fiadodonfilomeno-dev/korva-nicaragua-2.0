import pytest
from django.urls import reverse
from social.models import Post

pytestmark = pytest.mark.django_db


class TestSocialFeed:
    def test_home_status(self, client):
        response = client.get(reverse('home'))
        assert response.status_code == 200

    def test_create_post(self, authenticated_client, user):
        data = {
            'title': 'Test Post',
            'content': 'Contenido de prueba',
            'tags': 'test,prueba',
        }
        response = authenticated_client.post(reverse('create_post'), data)
        assert Post.objects.filter(author=user.profile, title='Test Post').exists()

    def test_post_detail(self, authenticated_client, user):
        post = Post.objects.create(
            author=user.profile,
            title='Detalle Post',
            content='Contenido de prueba',
        )
        response = authenticated_client.get(reverse('post_detail', args=[post.id]))
        assert response.status_code == 200

    def test_upvote_post(self, authenticated_client, user):
        post = Post.objects.create(
            author=user.profile,
            title='Upvote Test',
            content='Contenido de prueba',
        )
        response = authenticated_client.post(reverse('upvote_post', args=[post.id]))
        assert response.status_code in (200, 302)

    def test_toggle_favorite(self, authenticated_client, user):
        post = Post.objects.create(
            author=user.profile,
            title='Favorite Test',
            content='Contenido de prueba',
        )
        response = authenticated_client.post(reverse('toggle_favorite_post', args=[post.id]))
        assert response.status_code in (200, 302)


class TestPostModel:
    def test_post_ordering(self, user):
        post1 = Post.objects.create(author=user.profile, title='Primero', content='A')
        post2 = Post.objects.create(author=user.profile, title='Segundo', content='B')
        posts = Post.objects.all()
        assert posts[0] == post2
        assert posts[1] == post1

    def test_post_str(self, user):
        post = Post.objects.create(author=user.profile, title='Test', content='X')
        assert str(post) == f'Test by {user.profile.business_name}'

    def test_default_moderation(self, user):
        post = Post.objects.create(author=user.profile, title='Test', content='X')
        assert post.moderation_status == 'approved'
