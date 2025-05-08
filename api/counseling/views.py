from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Session
from .serializers import SessionSerializer
from .permissions import IsStudentOrPsychologist

# Create your views here.

class SessionViewSet(viewsets.ModelViewSet):
    serializer_class = SessionSerializer
    permission_classes = [IsStudentOrPsychologist]

    def get_queryset(self):
        user = self.request.user
        return Session.objects.filter(models.Q(student=user) | models.Q(psychologist=user))

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)
