from .models import Notification
from django.contrib.auth.models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json


def create_notification(recipient, notification_type, title, message, sender=None, related_object_id=None, related_object_type=''):
    if recipient == sender:
        return None
    notification = Notification.objects.create(
        recipient=recipient,
        sender=sender,
        notification_type=notification_type,
        title=title,
        message=message,
        related_object_id=related_object_id,
        related_object_type=related_object_type,
    )
    try:
        channel_layer = get_channel_layer()
        unread_count = Notification.objects.filter(recipient=recipient, is_read=False).count()
        async_to_sync(channel_layer.group_send)(
            f"user_{recipient.id}",
            {
                'type': 'notification_message',
                'notification': {
                    'id': notification.id,
                    'type': notification.notification_type,
                    'title': notification.title,
                    'message': notification.message,
                    'sender': sender.username if sender else None,
                    'is_read': notification.is_read,
                    'created_at': notification.created_at.isoformat(),
                    'icon': notification.icon,
                }
            }
        )
        async_to_sync(channel_layer.group_send)(
            f"user_{recipient.id}",
            {
                'type': 'unread_count_update',
                'count': unread_count,
            }
        )
    except Exception:
        pass
    return notification
