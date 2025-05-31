# serializers.py
from rest_framework import serializers
from .models import *

from rest_framework import serializers
from .models import Session

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'student', 'psychologist', 'schedule_time', 'status', 'notes']
        read_only_fields = ['id', 'student', 'status']  # student diisi otomatis
class SessionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionLog
        fields = ['id', 'session', 'action', 'description', 'created_at']
        read_only_fields = ['id', 'session', 'action', 'description', 'created_at']
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'is_read', 'created_at']
        read_only_fields = ['id', 'message', 'is_read', 'created_at']