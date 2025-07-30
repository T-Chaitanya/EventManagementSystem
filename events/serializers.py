from rest_framework import serializers
from .models import Event, Attendee

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"

    def validate(self, data):
        if data['end_time'] <= data['start_time']:
            raise serializers.ValidationError("End time must be after start time.")
        return data

class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = ['attendee_name', 'email']

class AttendeeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = ['id', 'attendee_name', 'email', 'registered_at']
