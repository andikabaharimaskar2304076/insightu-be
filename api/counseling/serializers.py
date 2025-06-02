# serializers.py
from rest_framework import serializers
from .models import *

from rest_framework import serializers
from .models import Session

class SessionSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField(read_only=True)
    psychologist = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='psychologist'),
        write_only=True
    )
    psychologist_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Session
        fields = ['id', 'student', 'psychologist', 'psychologist_info', 'schedule_time', 'notes', 'status']
        read_only_fields = ['id', 'student', 'status']

    def get_student(self, obj):
        return {
            "id": str(obj.student.id),
            "username": obj.student.username,
        }

    def get_psychologist_info(self, obj):
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