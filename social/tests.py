import pytest
from django.urls import reverse
from .models import Post
from users.models import Profile


class TestPostModel:
    def test_post_creation(self, post):
        assert post.title == 'Test Post'
        assert post.upvotes == 0
        assert post.downvotes == 0

    def test_post_str(self, post):
        assert str(post) == f"{post.title} by {post.author.business_name}"

    def test_post_upvote(self, post, profile):
        post.upvote(profile)
        assert post.upvotes == 1
        assert profile.popularity_score == 10

    def test_post_downvote(self, post, profile):
        post.downvote(profile)
        assert post.downvotes == 1
        assert profile.popularity_score == 0

    def test_post_upvote_downvote_combined(self, post, profile):
        post.upvote(profile)
        post.downvote(profile)
        assert post.upvotes == 1
        assert post.downvotes == 1
        assert profile.popularity_score == 5

    def test_post_ordering(self, profile):
        post1 = Post.objects.create(title='First', content='A', author=profile)
        post2 = Post.objects.create(title='Second', content='B', author=profile)
        posts = Post.objects.all()
        assert posts[0] == post2
        assert posts[1] == post1


class TestSocialViews:
    def test_home_view(self, client):
        response = client.get(reverse('home'))
        assert response.status_code == 200

    def test_home_view_with_posts(self, client_logged_in, post):
        response = client_logged_in.get(reverse('home'))
        assert response.status_code == 200
        assert 'Test Post'.encode() in response.content

    def test_create_post_view_requires_login(self, client):
        response = client.get(reverse('create_post'))
        assert response.status_code == 302

    def test_create_post_view_authenticated(self, client_logged_in):
        response = client_logged_in.get(reverse('create_post'))
        assert response.status_code == 200

    def test_create_post(self, client_logged_in):
        response = client_logged_in.post(reverse('create_post'), {
            'title': 'New Post',
            'content': 'New content',
        })
        assert Post.objects.filter(title='New Post').exists()

    def test_post_detail(self, client, post):
        response = client.get(reverse('post_detail', args=[post.id]))
        assert response.status_code == 200
        assert b'Test Post' in response.content

    def test_upvote_post(self, client_logged_in, post):
        response = client_logged_in.post(reverse('upvote_post', args=[post.id]))
        assert response.status_code == 302
        post.refresh_from_db()
        assert post.upvotes == 1

    def test_downvote_post(self, client_logged_in, post):
        response = client_logged_in.post(reverse('downvote_post', args=[post.id]))
        assert response.status_code == 302
        post.refresh_from_db()
        assert post.downvotes == 1

    def test_search_posts(self, client, post):
        response = client.get(reverse('home') + '?q=Test')
        assert response.status_code == 200
