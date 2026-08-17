import pytest
from django.urls import reverse
from messaging.models import Message, Conversation

pytestmark = pytest.mark.django_db


class TestMessaging:
    def test_messages_page(self, authenticated_client):
        response = authenticated_client.get(reverse('messages'))
        assert response.status_code == 200

    def test_start_conversation(self, authenticated_client, user, another_user):
        response = authenticated_client.get(
            reverse('start_conversation', args=[another_user.username])
        )
        assert response.status_code == 302

    def test_send_message(self, user, another_user):
        conv = Conversation.objects.create(
            user1=user.profile, user2=another_user.profile
        )
        msg = Message.objects.create(
            sender=user.profile,
            recipient=another_user.profile,
            content='Hola!',
        )
        assert msg.content == 'Hola!'
        assert msg.sender == user.profile

    def test_conversation_detail(self, authenticated_client, user, another_user):
        conv, _ = Conversation.objects.get_or_create(
            user1=user.profile, user2=another_user.profile
        )
        Message.objects.create(
            sender=user.profile,
            recipient=another_user.profile,
            content='Mensaje de prueba',
        )
        response = authenticated_client.get(
            reverse('conversation_detail', args=[conv.id])
        )
        assert response.status_code == 200


class TestMessageModel:
    def test_message_str(self, user, another_user):
        msg = Message.objects.create(
            sender=user.profile, recipient=another_user.profile,
            content='Test msg',
        )
        assert str(msg) == f'De {user.profile.business_name} a {another_user.profile.business_name}'

    def test_read_status(self, user, another_user):
        msg = Message.objects.create(
            sender=user.profile, recipient=another_user.profile,
            content='Test',
        )
        assert msg.is_read_by(another_user.profile) is False
        msg.mark_as_read(another_user.profile)
        assert msg.is_read_by(another_user.profile) is True
