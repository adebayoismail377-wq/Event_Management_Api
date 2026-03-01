from rest_framework import serializers
from .models import Event
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import EventRegistration

User = get_user_model()


class EventSerializer(serializers.ModelSerializer):
    available_spots = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['organizer', 'created_at']

    def get_available_spots(self, obj):
        return obj.max_capacity - obj.attendees.count()

    def validate_event_datetime(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Event date cannot be in the past.")
        return value

    def validate(self, data):
        if not data.get('title'):
            raise serializers.ValidationError("Title is required.")
        if not data.get('location'):
            raise serializers.ValidationError("Location is required.")
        return data


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class EventRegistrationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = EventRegistration
        fields = ['user', 'status', 'registered_at']