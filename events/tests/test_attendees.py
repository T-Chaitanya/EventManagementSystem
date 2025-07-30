import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from events.models import Event, Attendee
from django.utils.timezone import now, timedelta

@pytest.mark.django_db
def test_attendee_list():
    client = APIClient()
    event = Event.objects.create(
        event_name="View Attendees",
        event_location="Kolkata",
        start_time=now() + timedelta(days=3),
        end_time=now() + timedelta(days=4),
        max_capacity=5
    )
    Attendee.objects.create(event=event, attendee_name="A1", email="a1@example.com")
    Attendee.objects.create(event=event, attendee_name="A2", email="a2@example.com")
    url = reverse('event-attendees', args=[event.id])
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data['results']) == 2
