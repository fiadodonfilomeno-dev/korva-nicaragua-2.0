import pytest
from django.urls import reverse
from .models import Message, Conversation


class TestConversationModel:
    def test_create_conversation(self, profile, profile2):
        conv = Conversation.objects.create(user1=profile, user2=profile2)
        assert profile.business_name in str(conv) and profile2.business_name in str(conv)


class TestMessageModel:
    def test_create_message(self, profile, profile2):
        msg = Message.objects.create(sender=profile, recipient=profile2, content='Hola!')
        assert msg.content == 'Hola!'
        assert msg.is_read_by(profile2) is False

    def test_mark_as_read(self, profile, profile2):
        msg = Message.objects.create(sender=profile, recipient=profile2, content='Hola!')
        msg.mark_as_read(profile2)
        assert msg.is_read_by(profile2) is True

    def test_read_status_property(self, profile, profile2):
        msg = Message.objects.create(sender=profile, recipient=profile2, content='Hola!')
        assert msg.read_status is False
        msg.mark_as_read(profile2)
        assert msg.read_status is True

    def test_message_str(self, profile, profile2):
        msg = Message.objects.create(sender=profile, recipient=profile2, content='Hola!')
        assert str(msg) == f"De {profile.business_name} a {profile2.business_name}"


class TestMessagingViews:
    def test_messages_view_requires_login(self, client):
        response = client.get(reverse('messages'))
        assert response.status_code == 302

    def test_messages_view_authenticated(self, client_logged_in):
        response = client_logged_in.get(reverse('messages'))
        assert response.status_code == 200

    def test_start_conversation(self, client_logged_in, user2):
        response = client_logged_in.get(reverse('start_conversation', args=['testuser2']))
        assert response.status_code in (200, 302)

    def test_send_message(self, client_logged_in, profile2):
        response = client_logged_in.post(reverse('send_message'), {
            'recipient_id': profile2.id,
            'content': 'Test message content',
        })
        assert Message.objects.filter(content='Test message content').exists()
