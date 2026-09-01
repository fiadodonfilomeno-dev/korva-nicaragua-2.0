import pytest
from django.urls import reverse
from .models import AIConversation, AIMessage


class TestAIModels:
    def test_create_conversation(self, profile):
        conv = AIConversation.objects.create(user=profile)
        assert profile.business_name in str(conv)
        assert "Conversación" in str(conv)

    def test_create_message(self, profile):
        conv = AIConversation.objects.create(user=profile)
        msg = AIMessage.objects.create(
            conversation=conv,
            role='user',
            content='Hola, necesito ayuda'
        )
        assert msg.role == 'user'
        assert "Mensaje" in str(msg) and profile.business_name in str(msg)

    def test_ai_message_ordering(self, profile):
        conv = AIConversation.objects.create(user=profile)
        msg1 = AIMessage.objects.create(conversation=conv, role='user', content='Primero')
        msg2 = AIMessage.objects.create(conversation=conv, role='assistant', content='Segundo')
        messages = AIMessage.objects.filter(conversation=conv)
        assert messages[0] == msg1
        assert messages[1] == msg2


class TestRankingsView:
    def test_rankings_view(self, client):
        response = client.get(reverse('rankings'))
        assert response.status_code == 200

    def test_rankings_with_category(self, client):
        response = client.get(reverse('rankings') + '?category=general')
        assert response.status_code == 200

    def test_rankings_novatos(self, client):
        response = client.get(reverse('rankings') + '?category=novatos')
        assert response.status_code == 200

    def test_rankings_establecidas(self, client):
        response = client.get(reverse('rankings') + '?category=establecidas')
        assert response.status_code == 200


class TestAIViews:
    def test_ai_view_requires_login(self, client):
        response = client.get(reverse('korva_ai'))
        assert response.status_code == 302

    def test_ai_view_authenticated(self, client_logged_in, profile):
        response = client_logged_in.get(reverse('korva_ai'))
        assert response.status_code in (200, 302)

    def test_ai_tutorial(self, client_logged_in):
        response = client_logged_in.get(reverse('ai_tutorial'))
        assert response.status_code == 200
