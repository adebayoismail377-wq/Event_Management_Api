from django.db import models
from django.conf import settings


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    event_datetime = models.DateTimeField()
    location = models.CharField(max_length=255)

    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="organized_events"
    )

    max_capacity = models.PositiveIntegerField()

    attendees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="EventRegistration",
        related_name="registered_events"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def is_full(self):
        confirmed_count = self.registrations.filter(status="confirmed").count()
        return confirmed_count >= self.max_capacity

    def __str__(self):
        return self.title


class EventRegistration(models.Model):

    STATUS_CHOICES = (
        ("confirmed", "Confirmed"),
        ("waitlisted", "Waitlisted"),
        ("cancelled", "Cancelled"),
    )

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="registrations"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="event_registrations"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="confirmed"
    )

    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("event", "user")

    def __str__(self):
        return f"{self.user.username} - {self.event.title} ({self.status})"