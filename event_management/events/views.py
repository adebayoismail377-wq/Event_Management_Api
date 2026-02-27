from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from django.contrib.auth.models import User

from .models import Event
from .serializers import EventSerializer, UserSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Event.objects.filter(organizer=self.request.user)
        return Event.objects.none()

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.organizer != self.request.user:
            raise PermissionDenied("You can only edit your own events.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.organizer != self.request.user:
            raise PermissionDenied("You can only delete your own events.")
        instance.delete()

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

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def register(self, request, pk=None):
        event = self.get_object()

        if request.user in event.attendees.all():
            return Response(
                {"message": "You are already registered."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if event.is_full():
            if request.user in event.waitlist.all():
                return Response(
                    {"message": "You are already on the waitlist."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            event.waitlist.add(request.user)
            return Response(
                {"message": "Event is full. You have been added to the waitlist."},
                status=status.HTTP_200_OK
            )

        event.attendees.add(request.user)
        return Response(
            {"message": "Successfully registered!"},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def cancel_registration(self, request, pk=None):
        event = self.get_object()

        if request.user in event.attendees.all():
            event.attendees.remove(request.user)

            if event.waitlist.exists():
                next_user = event.waitlist.first()
                event.waitlist.remove(next_user)
                event.attendees.add(next_user)

            return Response(
                {"message": "Registration cancelled successfully."},
                status=status.HTTP_200_OK
            )

        return Response(
            {"error": "You are not registered for this event."},
            status=status.HTTP_400_BAD_REQUEST
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]