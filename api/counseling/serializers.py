# serializers.py
from rest_framework import serializers
from .models import *

from rest_framework import serializers
from .models import Session

class SessionSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()
    psychologist = serializers.SerializerMethodField()

    class Meta:
        model = Session
        fields = ['id', 'student', 'psychologist', 'schedule_time', 'notes', 'status']

    def get_student(self, obj):
        return {
            "id": str(obj.student.id),
            "username": obj.student.username,
        }

    def get_psychologist(self, obj):
        return {
            "id": str(obj.psychologist.id),
            "username": obj.psychologist.username,
        }
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