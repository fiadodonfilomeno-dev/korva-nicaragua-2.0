import pytest
from django.urls import reverse
from .models import Notification, NotificationPreference


class TestNotificationModel:
    def test_create_notification(self, user, user2):
        notif = Notification.objects.create(
            recipient=user,
            sender=user2,
            notification_type='message',
            title='Nuevo mensaje',
            message='Tienes un nuevo mensaje'
        )
        assert notif.is_read is False
        assert notif.icon == 'fas fa-envelope'

    def test_notification_str(self, user, user2):
        notif = Notification.objects.create(
            recipient=user, sender=user2,
            notification_type='like',
            title='Like', message='Te dieron like'
        )
        assert str(notif) == f"like para {user.username}"

    def test_notification_ordering(self, user, user2):
        n1 = Notification.objects.create(
            recipient=user, sender=user2,
            notification_type='message', title='First', message='First msg'
        )
        n2 = Notification.objects.create(
            recipient=user, sender=user2,
            notification_type='like', title='Second', message='Second msg'
        )
        notifications = Notification.objects.all()
        assert notifications[0] == n2
        assert notifications[1] == n1

    def test_notification_icon_types(self, user, user2):
        types = {
            'message': 'fas fa-envelope', 'like': 'fas fa-thumbs-up',
            'comment': 'fas fa-comment', 'follow': 'fas fa-user-plus',
            'product_inquiry': 'fas fa-shopping-bag', 'mention': 'fas fa-at',
            'system': 'fas fa-bell',
        }
        for ntype, icon in types.items():
            notif = Notification.objects.create(
                recipient=user, sender=user2,
                notification_type=ntype, title='Test', message='Test'
            )
            assert notif.icon == icon


class TestNotificationPreferenceModel:
    def test_create_preferences(self, user):
        prefs = NotificationPreference.objects.create(user=user)
        assert prefs.email_messages is True
        assert prefs.push_messages is True

    def test_preferences_str(self, user):
        prefs = NotificationPreference.objects.create(user=user)
        assert str(prefs) == f"Preferencias de {user.username}"
