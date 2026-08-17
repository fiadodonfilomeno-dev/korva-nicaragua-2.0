from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event
from users.models import Profile


def events_list(request):
    """Lista de eventos"""
    events = Event.objects.filter(is_active=True).select_related('organizer')
    category = request.GET.get('category')
    if category:
        events = events.filter(category=category)
    context = {'events': events, 'category': category, 'categories': Event.CATEGORY_CHOICES}
    return render(request, 'events/events_list.html', context)


@login_required(login_url='login')
def create_event(request):
    """Crear evento"""
    if request.method == 'POST':
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        category = request.POST.get('category', 'feria')
        date = request.POST.get('date', '')
        time = request.POST.get('time', '')
        location = request.POST.get('location', '')
        city = request.POST.get('city', 'managua')
        max_attendees = request.POST.get('max_attendees', '')
        image = request.FILES.get('image')
        if title and description and date:
            event = Event.objects.create(
                title=title, description=description, category=category,
                organizer=request.user.profile, date=date, time=time or None,
                location=location, city=city, image=image,
                max_attendees=int(max_attendees) if max_attendees else None
            )
            messages.success(request, 'Evento creado.')
            return redirect('event_detail', event_id=event.pk)
    context = {'cities': Profile.CITY_CHOICES, 'categories': Event.CATEGORY_CHOICES}
    return render(request, 'events/create_event.html', context)


def event_detail(request, event_id):
    """Detalle de evento"""
    event = get_object_or_404(Event, pk=event_id)
    is_attending = False
    if request.user.is_authenticated:
        is_attending = event.attendees.filter(pk=request.user.profile.pk).exists()
    context = {'event': event, 'is_attending': is_attending}
    return render(request, 'events/event_detail.html', context)


@login_required(login_url='login')
def toggle_attend(request, event_id):
    """Confirmar/rechazar asistencia"""
    event = get_object_or_404(Event, pk=event_id)
    profile = request.user.profile
    if event.attendees.filter(pk=profile.pk).exists():
        event.attendees.remove(profile)
        messages.success(request, 'Asistencia cancelada.')
    else:
        if event.is_full:
            messages.error(request, 'Evento lleno.')
        else:
            event.attendees.add(profile)
            messages.success(request, 'Asistencia confirmada.')
    return redirect('event_detail', event_id=event.pk)
