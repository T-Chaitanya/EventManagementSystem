from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from events.models import Event
from django.utils.timezone import now, timedelta

class EventTests(APITestCase):

    def setUp(self):
        self.url = reverse("event-list-create")
        self.event_data = {
            "event_name": "Test Event",
            "location": "Hyderabad",
            "start_time": (now() + timedelta(days=1)).isoformat(),
            "end_time": (now() + timedelta(days=2)).isoformat(),
            "max_capacity": 5,
        }

    def test_create_event(self):
        response = self.client.post(self.url, self.event_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 1)

    def test_list_events(self):
        Event.objects.create(**self.event_data)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
