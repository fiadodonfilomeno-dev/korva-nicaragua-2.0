import pytest
from django.urls import reverse
from events.models import Event
from datetime import date, time

pytestmark = pytest.mark.django_db


class TestEvents:
    def test_events_list(self, client):
        response = client.get(reverse('events_list'))
        assert response.status_code == 200

    def test_create_event(self, authenticated_client, user):
        data = {
            'title': 'Evento Test',
            'description': 'Descripcion del evento',
            'category': 'taller',
            'date': date.today().isoformat(),
            'time': '14:00',
            'location': 'Managua',
            'city': 'MGA',
        }
        response = authenticated_client.post(reverse('create_event'), data)
        assert Event.objects.filter(organizer=user.profile, title='Evento Test').exists()

    def test_event_detail(self, authenticated_client, user):
        event = Event.objects.create(
            organizer=user.profile,
            title='Evento Detalle',
            description='Desc',
            category='taller',
            date=date.today(),
            time=time(14, 0),
            location='Managua',
            city='MGA',
        )
        response = authenticated_client.get(reverse('event_detail', args=[event.id]))
        assert response.status_code == 200


class TestEventModel:
    def test_event_str(self, user):
        today = date.today()
        event = Event.objects.create(
            organizer=user.profile,
            title='Mi Evento',
            description='X',
            category='taller',
            date=today,
            time=time(14, 0),
            location='Managua',
            city='MGA',
        )
        assert str(event) == f'Mi Evento - {today}'
