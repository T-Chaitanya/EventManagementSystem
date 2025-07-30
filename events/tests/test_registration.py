import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from events.models import Event
from django.utils.timezone import now, timedelta

@pytest.mark.django_db
def test_successful_registration():
    client = APIClient()
    event = Event.objects.create(
        event_name="Registerable",
        event_location="Delhi",
        start_time=now() + timedelta(days=1),
        end_time=now() + timedelta(days=2),
        max_capacity=1
    )
    url = reverse('event-register', args=[event.id])
    payload = {"attendee_name": "John Doe", "email": "john@example.com"}
    response = client.post(url, payload, format='json')
    assert response.status_code == 201
    assert response.data['email'] == "john@example.com"

@pytest.mark.django_db
def test_duplicate_registration_fails():
    client = APIClient()
    event = Event.objects.create(
        event_name="Limited Event",
        event_location="Pune",
        start_time=now() + timedelta(days=1),
        end_time=now() + timedelta(days=2),
        max_capacity=2
    )
    url = reverse('event-register', args=[event.id])
    payload = {"attendee_name": "John", "email": "john@example.com"}
    client.post(url, payload, format='json')
    response = client.post(url, payload, format='json')
    assert response.status_code == 400
    assert "already registered" in response.data['error']