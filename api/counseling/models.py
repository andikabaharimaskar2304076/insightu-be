from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Session(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_sessions')
    psychologist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='psychologist_sessions')
    schedule_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Session with {self.psychologist.username} by {self.student.username} at {self.schedule_time}"