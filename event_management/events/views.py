from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Event, EventRegistration
from .serializers import EventSerializer, UserSerializer

User = get_user_model()


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    # Users can only see events they organize
    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
           return Event.objects.none()

    # Only event creator (organizer) can view their event
        return Event.objects.filter(organizer=user)
    def retrieve(self, request, *args, **kwargs):
        event = self.get_object()

        if event.organizer != request.user:
          raise PermissionDenied("You are not allowed to view this event.")

        return super().retrieve(request, *args, **kwargs)
    
    # Event creation restricted to organizers
    def perform_create(self, serializer):
        if self.request.user.role != "organizer":
            raise PermissionDenied("Only organizers can create events.")

        serializer.save(organizer=self.request.user)

    # Event update security
    def perform_update(self, serializer):
        if serializer.instance.organizer != self.request.user:
            raise PermissionDenied("You can only edit your own events.")

        serializer.save()

    # Event delete security
    def perform_destroy(self, instance):
        if instance.organizer != self.request.user:
            raise PermissionDenied("You can only delete your own events.")

        instance.delete()

    # Upcoming events endpoint
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

    # Event registration endpoint
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def register(self, request, pk=None):

        event = self.get_object()
        user = request.user

        if event.organizer == user:
            raise ValidationError("Organizer cannot register for own event.")

        if EventRegistration.objects.filter(event=event, user=user).exists():
            raise ValidationError("You are already registered.")

        # Waitlist or confirm registration
        if event.is_full():
            status_value = "waitlisted"
        else:
            status_value = "confirmed"

        EventRegistration.objects.create(
            event=event,
            user=user,
            status=status_value
        )

        return Response({
            "message": f"Registration successful ({status_value})."
        })
    
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def cancel_registration(self, request, pk=None):

      event = self.get_object()
      user = request.user

        # Find registration
      registration = EventRegistration.objects.filter(
        event=event,
        user=user
      ).first()

      if not registration:
        raise ValidationError("You are not registered for this event.")

    # Cancel user registration
      registration.status = "cancelled"
      registration.save()

    # ⭐ AUTO PROMOTION LOGIC (Very Important)
      if not event.is_full():

        next_waitlisted = EventRegistration.objects.filter(
            event=event,
            status="waitlisted"
        ).order_by("registered_at").first()

        if next_waitlisted:
            next_waitlisted.status = "confirmed"
            next_waitlisted.save()

        return Response({
        "message": "Registration cancelled and waitlist promoted if available."
    })

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def browse(self, request):

        events = Event.objects.filter(event_datetime__gt=timezone.now())

        title = request.query_params.get('title')
        location = request.query_params.get('location')

        if title:
            events = events.filter(title__icontains=title)

        if location:
           events = events.filter(location__icontains=location)

         # Pagination support
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
        if not self.request.user.is_authenticated:
            return User.objects.none()

        return User.objects.filter(id=self.request.user.id)

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]