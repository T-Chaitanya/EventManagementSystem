import pytz
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.timezone import now
from .models import Event, Attendee
from .serializers import EventSerializer, AttendeeSerializer, AttendeeListSerializer

class EventListCreateView(APIView):
    @extend_schema(request=EventSerializer, responses=EventSerializer)
    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses=EventSerializer(many=True),
        parameters=[
            OpenApiParameter(name='type', type=str, required=False, location=OpenApiParameter.QUERY,
                             description="Filter events by time: 'past', 'upcoming' or omit for upcoming"),
            OpenApiParameter(name='page', type=int, required=False, location=OpenApiParameter.QUERY,
                             description="Page number for pagination"),
            OpenApiParameter(name='size', type=int, required=False, location=OpenApiParameter.QUERY,
                             description="Page size for pagination"),
            OpenApiParameter(name='tz', type=str, required=False,
                             description="Timezone to convert event slots into (e.g. Asia/Kolkata, UTC, America/New_York)"),
        ]
    )
    def get(self, request):
        all_events = Event.objects.all().order_by('start_time')
        past = [e for e in all_events if e.start_time < now()]
        upcoming = [e for e in all_events if e.start_time >= now()]

        filter_param = request.GET.get('type', 'upcoming')  # 'past', 'upcoming', or None
        if filter_param == 'past':
            result = past
        elif filter_param == 'upcoming':
            result = upcoming
        else:
            result = all_events

        total = len(result)

        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 10))
        start = (page - 1) * size
        end = start + size
        tzname = request.GET.get('tz', 'Asia/Kolkata')
        user_tz = pytz.timezone(tzname)

        data = []
        for event in result[start:end]:
            obj = EventSerializer(event).data
            obj['start_time'] = event.start_time.astimezone(user_tz).isoformat()
            obj['end_time'] = event.end_time.astimezone(user_tz).isoformat()
            data.append(obj)
        return Response({
        "count": total,
        "page": page,
        "size": size,
        "results": data
    })

class EventRegisterView(APIView):
    @extend_schema(request=AttendeeSerializer, responses=AttendeeListSerializer)
    def post(self, request, event_id):
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return Response({"error": "Event not found."}, status=404)

        if event.attendees.count() >= event.max_capacity:
            return Response({"error": "There are no more slots. Event is at full capacity."}, status=400)

        data = request.data.copy()
        data["event"] = event.id

        if Attendee.objects.filter(event_id=event.id, email=data['email']).exists():
            return Response({"error": "This email is already registered for the event."}, status=400)

        serializer = AttendeeSerializer(data=data)
        if serializer.is_valid():
            serializer.save(event=event)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class AttendeeListView(APIView):
    @extend_schema(responses=AttendeeListSerializer(many=True),
    parameters=[OpenApiParameter(name='page', type=int, required=False, location=OpenApiParameter.QUERY,
                             description="Page number for pagination"),
    OpenApiParameter(name='size', type=int, required=False, location=OpenApiParameter.QUERY,
                             description="Page size for pagination"),])
    def get(self, request, event_id):
        try:
            Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return Response({"Event not found"}, status=404)

        attendees = Attendee.objects.filter(event_id=event_id).order_by('registered_at')
        page = int(request.GET.get('page', 1))
        size = int(request.GET.get('size', 10))
        start = (page - 1) * size
        end = start + size
        total = len(attendees)
        serializer = AttendeeListSerializer(attendees[start:end], many=True)
        return Response({
        "count": total,
        "page": page,
        "size": size,
        "results": serializer.data
    })
