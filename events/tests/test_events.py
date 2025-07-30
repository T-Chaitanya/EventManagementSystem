import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from events.models import Event
from django.utils.timezone import now, timedelta

@pytest.mark.django_db
def test_create_event():
    client = APIClient()
    url = reverse('event-list-create')
    payload = {
        "event_name": "Test Event",
        "event_location": "Mumbai",
        "start_time": (now() + timedelta(days=1)).isoformat(),
        "end_time": (now() + timedelta(days=2)).isoformat(),
        "max_capacity": 100
    }
    response = client.post(url, payload, format='json')
    assert response.status_code == 201
    assert response.data['event_name'] == "Test Event"

@pytest.mark.django_db
def test_list_events():
    client = APIClient()
    url = reverse('event-list-create')
    Event.objects.create(
        event_name="Event X",
        event_location="Chennai",
        start_time=now() + timedelta(days=2),
        end_time=now() + timedelta(days=3),
        max_capacity=50
    )
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data['results']) >= 1
