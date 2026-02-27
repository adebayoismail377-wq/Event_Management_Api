# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    event_datetime = models.DateTimeField()
    location = models.CharField(max_length=255)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    capacity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    organizer = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    attendees = models.ManyToManyField(
        User,
        related_name='registered_events',
        blank=True
    )

    waitlist = models.ManyToManyField(
        User,
        related_name='waitlisted_events',
        blank=True
    )

    max_capacity = models.PositiveIntegerField(default=3)
    def is_full(self):
        return self.attendees.count() >= self.max_capacity


    def __str__(self):
        return self.title


class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'user')


