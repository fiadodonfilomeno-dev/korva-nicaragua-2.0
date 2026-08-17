from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Notification


@login_required(login_url='login')
def notifications_list(request):
    notifications = Notification.objects.filter(recipient=request.user).select_related('sender')
    unread_count = notifications.filter(is_read=False).count()
    return render(request, 'notifications/notifications.html', {
        'notifications': notifications,
        'unread_count': unread_count,
    })


@login_required(login_url='login')
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'ok'})
    return redirect('notifications_list')


@login_required(login_url='login')
def mark_all_read(request):
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'ok'})
    return redirect('notifications_list')


@login_required(login_url='login')
def unread_count_api(request):
    count = Notification.objects.filter(recipient=request.user, is_read=False).count()
    return JsonResponse({'count': count})
