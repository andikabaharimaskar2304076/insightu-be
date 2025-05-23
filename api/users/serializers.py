from rest_framework import serializers
from .models import *

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    birth_date = serializers.DateField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'birth_date']

    def validate(self, attrs):
        role = attrs.get('role')
        birth_date = attrs.get('birth_date')

        if role == 'student' and not birth_date:
            raise serializers.ValidationError({'birth_date': 'This field is required for students.'})

        return attrs

    def create(self, validated_data):
        role = validated_data.pop('role')
        birth_date = validated_data.pop('birth_date', None)

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=role
        )

        if role == 'admin':
            user.is_verified = True
            user.save()

        if role == 'student':
            StudentProfile.objects.create(user=user, birth_date=birth_date)
        elif role == 'psychologist':
            license_number = validated_data.pop('license_number', 'UNKNOWN')
            PsychologistProfile.objects.create(user=user, license_number=license_number)

        return user
class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ['school_name', 'grade_level', 'birth_date', 'nisn', 'homeroom_teacher', 'gender', 'major', 'address_avatar']
class PsychologistProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PsychologistProfile
        fields = ['license_number', 'specialization', 'biography', 'address_avatar']
class UserSummarySerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'is_verified']

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PsychologistAvailability
        fields = '__all__'
