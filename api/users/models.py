import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

ROLE_CHOICES = [
    ('student', 'Student'),
    ('psychologist', 'Psychologist'),
    ('admin', 'Admin'),
]

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    groups = None
    user_permissions = None
    # Gunakan email sebagai username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # still required by AbstractUser

    def __str__(self):
        return f"{self.username} ({self.role})"

class StudentProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    school_name = models.CharField(max_length=100, blank=True)
    grade_level = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    nisn = models.CharField(max_length=20, blank=True, null=True)
    homeroom_teacher = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')], blank=True, null=True)
    major = models.CharField(max_length=100, blank=True, null=True)
    address_avatar = models.URLField(blank=True, null=True)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"Profile of {self.user.username}"

class PsychologistProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='psychologist_profile')
    license_number = models.CharField(max_length=50)
    specialization = models.CharField(max_length=100, blank=True)
    biography = models.TextField(blank=True)
    address_avatar = models.URLField(blank=True, null=True)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"Psychologist: {self.user.username}"

class PsychologistAvailability(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    psychologist = models.ForeignKey('PsychologistProfile', on_delete=models.CASCADE, related_name='availabilities')
    day_of_week = models.CharField(
        max_length=10,
        choices=[
            ('Monday', 'Monday'),
            ('Tuesday', 'Tuesday'),
            ('Wednesday', 'Wednesday'),
            ('Thursday', 'Thursday'),
            ('Friday', 'Friday'),
            ('Saturday', 'Saturday'),
            ('Sunday', 'Sunday'),
        ]
    )
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.psychologist.user.username} - {self.day_of_week}: {self.start_time} to {self.end_time}"
