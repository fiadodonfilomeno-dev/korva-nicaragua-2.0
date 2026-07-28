from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Report, Block
from notifications.utils import create_notification


def get_blocked_user_ids(user):
    """Retorna IDs de usuarios bloqueados por o que bloquearon a user"""
    blocked_by_me = Block.objects.filter(blocker=user).values_list('blocked_id', flat=True)
    blocked_me = Block.objects.filter(blocked=user).values_list('blocker_id', flat=True)
    return set(blocked_by_me) | set(blocked_me)


@login_required(login_url='login')
def report_user(request, username):
    reported = get_object_or_404(User, username=username)
    if reported == request.user:
        messages.error(request, 'No puedes reportarte a ti mismo.')
        return redirect('profile', username=username)
    if request.method == 'POST':
        reason = request.POST.get('reason', 'other')
        description = request.POST.get('description', '')
        Report.objects.create(
            reporter=request.user,
            reported=reported,
            reason=reason,
            description=description,
        )
        messages.success(request, 'Reporte enviado. Lo revisaremos pronto.')
        return redirect('profile', username=username)
    return render(request, 'users/report_user.html', {'reported': reported})


@login_required(login_url='login')
def block_user(request, username):
    to_block = get_object_or_404(User, username=username)
    if to_block == request.user:
        messages.error(request, 'No puedes bloquearte a ti mismo.')
        return redirect('profile', username=username)
    if request.method == 'POST':
        Block.objects.get_or_create(blocker=request.user, blocked=to_block)
        messages.success(request, f'Has bloqueado a {username}.')
        return redirect('profile', username=username)
    return render(request, 'users/confirm_block.html', {'to_block': to_block, 'action': 'bloquear'})


@login_required(login_url='login')
def unblock_user(request, username):
    to_unblock = get_object_or_404(User, username=username)
    if request.method == 'POST':
        Block.objects.filter(blocker=request.user, blocked=to_unblock).delete()
        messages.success(request, f'Has desbloqueado a {username}.')
        return redirect('profile', username=username)
    return render(request, 'users/confirm_block.html', {'to_block': to_unblock, 'action': 'desbloquear'})


@login_required(login_url='login')
def blocked_users_list(request):
    blocks = Block.objects.filter(blocker=request.user).select_related('blocked')
    return render(request, 'users/blocked_users.html', {'blocks': blocks})
