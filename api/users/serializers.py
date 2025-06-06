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
class UserSummarySerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'is_verified', 'avatar']
class PsychologistProfileSerializer(serializers.ModelSerializer):
    user = UserSummarySerializer(read_only=True)

    class Meta:
        model = PsychologistProfile
        fields = ['id', 'user', 'license_number', 'specialization', 'biography', 'address_avatar', 'is_complete']
class AvailabilitySerializer(serializers.ModelSerializer):
    psychologist = PsychologistProfileSerializer(read_only=True)

    class Meta:
        model = PsychologistAvailability
        fields = ['id', 'psychologist', 'day_of_week', 'start_time', 'end_time']
class PsychologistAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PsychologistAvailability
        fields = ['day_of_week', 'start_time', 'end_time']
class PsychologistWithUserSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    avatar = serializers.ImageField(source='user.avatar', read_only=True)
    is_verified = serializers.BooleanField(source='user.is_verified')
    availabilities = PsychologistAvailabilitySerializer(many=True, read_only=True)

    class Meta:
        model = PsychologistProfile
        fields = [
            'id',               # ini id dari PsychologistProfile
            'user_id',          # ini yang digunakan saat booking
            'username',
            'email',
            'avatar',
            'is_verified',
            'license_number',
            'specialization',
            'biography',
            'address_avatar',
            'availabilities',
        ]
class AdminVerificationListSerializer(serializers.ModelSerializer):
    role = serializers.CharField()
    is_complete = serializers.SerializerMethodField()
    profile_data = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'is_verified', 'is_complete', 'profile_data']

    def get_is_complete(self, obj):
        if obj.role == 'student' and hasattr(obj, 'studentprofile'):
            return obj.studentprofile.is_complete
        elif obj.role == 'psychologist' and hasattr(obj, 'psychologistprofile'):
            return obj.psychologistprofile.is_complete
        return False

    def get_profile_data(self, obj):
        if obj.role == 'student' and hasattr(obj, 'studentprofile'):
            return {
                "nisn": obj.studentprofile.nisn,
                "gender": obj.studentprofile.gender,
                "major": obj.studentprofile.major,
                "homeroom_teacher": obj.studentprofile.homeroom_teacher,
            }
        elif obj.role == 'psychologist' and hasattr(obj, 'psychologistprofile'):
            return {
                "license_number": obj.psychologistprofile.license_number,
                "specialization": obj.psychologistprofile.specialization,
                "biography": obj.psychologistprofile.biography,
            }
        return {}
