from django.db import models
from django.contrib.auth.models import AbstractUser

ROLE_CHOICES = [
    ('student', 'Student'),
    ('psychologist', 'Psychologist'),
    ('admin', 'Admin'),
]

class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_verified = models.BooleanField(default=False)

    # Gunakan email sebagai username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # still required by AbstractUser

    def __str__(self):
        return f"{self.username} ({self.role})"

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    school_name = models.CharField(max_length=100)
    grade_level = models.CharField(max_length=20)
    birth_date = models.DateField()

    def __str__(self):
        return f"Profile of {self.user.username}"

class PsychologistProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='psychologist_profile')
    license_number = models.CharField(max_length=50)
    specialization = models.CharField(max_length=100, blank=True)
    biography = models.TextField(blank=True)

    def __str__(self):
        return f"Psychologist: {self.user.username}"
