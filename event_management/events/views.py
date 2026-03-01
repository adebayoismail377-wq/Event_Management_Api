from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from .models import Event
from .serializers import EventSerializer, UserSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    # Users can only see their own events
    def get_queryset(self):
        return Event.objects.filter(organizer=self.request.user)

    # Allow organizers (staff users) to create events
    def perform_create(self, serializer):
        if self.request.user.role != "organizer":
            raise PermissionDenied("Only organizers can create events.")

        serializer.save(organizer=self.request.user)

    # Only event owner can update event
    def perform_update(self, serializer):
        if serializer.instance.organizer != self.request.user:
            raise PermissionDenied("You can only edit your own events.")

        serializer.save()

    # Only event owner can delete event
    def perform_destroy(self, instance):
        if instance.organizer != self.request.user:
            raise PermissionDenied("You can only delete your own events.")

        instance.delete()

    # Upcoming events with filtering
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def upcoming(self, request):
        events = Event.objects.filter(event_datetime__gt=timezone.now())

        title = request.query_params.get('title')
        location = request.query_params.get('location')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if title:
            events = events.filter(title__icontains=title)

        if location:
            events = events.filter(location__icontains=location)

        if start_date and end_date:
            events = events.filter(event_datetime__range=[start_date, end_date])

        page = self.paginate_queryset(events)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]