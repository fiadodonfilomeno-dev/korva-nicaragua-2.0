from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


@login_required
def ws_config(request):
    protocol = 'wss' if request.is_secure() else 'ws'
    host = request.get_host()
    return JsonResponse({
        'ws_url': f'{protocol}://{host}/ws/chat/',
        'poll_url': '/api/messages/unread/',
        'notification_ws_url': f'{protocol}://{host}/ws/notifications/',
        'notification_poll_url': '/api/notifications/unread/',
    })


@login_required
def notifications_unread(request):
    try:
        from notifications.models import Notification
        count = Notification.objects.filter(recipient=request.user, is_read=False).count()
        return JsonResponse({'count': count})
    except Exception:
        return JsonResponse({'count': 0})


@login_required
def messages_unread(request):
    try:
        from messaging.models import Message
        profile = request.user.profile
        count = Message.objects.filter(
            recipient=profile,
        ).exclude(read_by=profile).count()
        return JsonResponse({'count': count})
    except Exception:
        return JsonResponse({'count': 0})
