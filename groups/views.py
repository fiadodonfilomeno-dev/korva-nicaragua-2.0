from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Group, GroupPost
from users.models import Profile


def groups_list(request):
    """Lista de grupos"""
    groups = Group.objects.all()
    sector = request.GET.get('sector')
    if sector:
        groups = groups.filter(sector=sector)
    context = {'groups': groups, 'sector': sector, 'sectors': Profile.SECTOR_CHOICES}
    return render(request, 'groups/groups_list.html', context)


@login_required(login_url='login')
def create_group(request):
    """Crear grupo"""
    if request.method == 'POST':
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')
        sector = request.POST.get('sector', 'otros')
        image = request.FILES.get('image')
        if name and description:
            group = Group.objects.create(
                name=name, description=description, sector=sector,
                admin=request.user.profile, image=image
            )
            group.members.add(request.user.profile)
            messages.success(request, 'Grupo creado.')
            return redirect('group_detail', group_id=group.pk)
    context = {'sectors': Profile.SECTOR_CHOICES}
    return render(request, 'groups/create_group.html', context)


def group_detail(request, group_id):
    """Detalle de grupo"""
    group = get_object_or_404(Group, pk=group_id)
    is_member = False
    if request.user.is_authenticated:
        is_member = group.members.filter(pk=request.user.profile.pk).exists()
    posts = group.posts.select_related('author').all()

    if request.method == 'POST' and is_member:
        content = request.POST.get('content', '')
        image = request.FILES.get('image')
        if content or image:
            GroupPost.objects.create(group=group, author=request.user.profile, content=content, image=image)
            messages.success(request, 'Publicado.')
            return redirect('group_detail', group_id=group.pk)

    context = {'group': group, 'is_member': is_member, 'posts': posts}
    return render(request, 'groups/group_detail.html', context)


@login_required(login_url='login')
def toggle_group_member(request, group_id):
    """Unirse/salir de grupo"""
    group = get_object_or_404(Group, pk=group_id)
    profile = request.user.profile
    if group.members.filter(pk=profile.pk).exists():
        group.members.remove(profile)
        messages.success(request, 'Saliste del grupo.')
    else:
        group.members.add(profile)
        messages.success(request, 'Te uniste al grupo.')
    return redirect('group_detail', group_id=group.pk)
