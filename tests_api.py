import pytest
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db


class TestApiEndpoints:
    def test_api_profiles_list(self, client):
        response = client.get('/api/profiles/')
        assert response.status_code == status.HTTP_200_OK

    def test_api_posts_list(self, client):
        response = client.get('/api/posts/')
        assert response.status_code == status.HTTP_200_OK

    def test_api_products_list(self, client):
        response = client.get('/api/products/')
        assert response.status_code == status.HTTP_200_OK

    def test_api_reviews_list(self, client):
        response = client.get('/api/reviews/')
        assert response.status_code == status.HTTP_200_OK

    def test_api_root_authenticated(self, authenticated_client):
        response = authenticated_client.get('/api/')
        assert response.status_code == status.HTTP_200_OK

    def test_api_post_create(self, authenticated_client, user):
        data = {'title': 'API Post', 'content': 'From API'}
        response = authenticated_client.post('/api/posts/', data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'API Post'

    def test_api_post_upvote(self, authenticated_client, user):
        from social.models import Post
        post = Post.objects.create(author=user.profile, title='Test', content='X')
        response = authenticated_client.post(f'/api/posts/{post.id}/upvote/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['upvotes'] == 1

    def test_api_post_favorite(self, authenticated_client, user):
        from social.models import Post
        post = Post.objects.create(author=user.profile, title='Test', content='X')
        response = authenticated_client.post(f'/api/posts/{post.id}/favorite/')
        assert response.status_code == status.HTTP_200_OK
        assert 'is_favorited' in response.data

    def test_api_notifications(self, authenticated_client):
        response = authenticated_client.get('/api/notifications/')
        assert response.status_code == status.HTTP_200_OK

    def test_api_conversations(self, authenticated_client):
        response = authenticated_client.get('/api/conversations/')
        assert response.status_code == status.HTTP_200_OK

    def test_api_mark_notifications_read(self, authenticated_client):
        response = authenticated_client.post('/api/notifications/mark_all_read/')
        assert response.status_code == status.HTTP_200_OK

    def test_api_profile_detail(self, client, user):
        response = client.get(f'/api/profiles/{user.profile.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['business_name'] == 'Test Business'
