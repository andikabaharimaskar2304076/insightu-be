from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "is_verified": user.is_verified
        })
class StudentProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = request.user.student_profile
            serializer = StudentProfileSerializer(profile)
            return Response(serializer.data)
        except StudentProfile.DoesNotExist:
            return Response({"detail": "Student profile not found."}, status=404)
        
    def post(self, request):
        if request.user.role != 'student':
            return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        # Cek jika sudah punya profil
        if hasattr(request.user, 'student_profile'):
            return Response({'detail': 'Profile already exists.'}, status=400)

        serializer = StudentProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # penting: ikat ke user yang login
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request):
        try:
            profile = request.user.student_profile
        except StudentProfile.DoesNotExist:
            return Response({"detail": "Student profile not found."}, status=404)

        serializer = StudentProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
class PsychologistProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'psychologist':
            return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        try:
            profile = request.user.psychologist_profile
            serializer = PsychologistProfileSerializer(profile)
            return Response(serializer.data)
        except PsychologistProfile.DoesNotExist:
            return Response({"detail": "Psychologist profile not found."}, status=404)

    def put(self, request):
        if request.user.role != 'psychologist':
            return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        try:
            profile = request.user.psychologist_profile
        except PsychologistProfile.DoesNotExist:
            return Response({"detail": "Psychologist profile not found."}, status=404)

        serializer = PsychologistProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
class VerifyUserView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, user_id):
        if request.user.role != 'admin':
            return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        user.is_verified = True
        user.save()
        return Response({'message': f'User {user.email} has been verified.'}, status=status.HTTP_200_OK)
class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'admin':
            return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        users = User.objects.all()
        serializer = UserSummarySerializer(users, many=True)
        return Response(serializer.data, status=200)
class UserByUsernameView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        if request.user.role != 'admin':
            return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'id': str(user.id),
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'is_verified': user.is_verified
        }, status=200)
class UnverifiedUserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'admin':
            return Response({'detail': 'Permission denied'}, status=403)

        users = User.objects.filter(is_verified=False)
        serializer = UserSummarySerializer(users, many=True)
        return Response(serializer.data)
class UploadAvatarView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        avatar_file = request.FILES.get('avatar')

        if not avatar_file:
            return Response({'error': 'No avatar uploaded'}, status=400)

        # Simpan avatar ke user.avatar
        user.avatar = avatar_file
        user.save()

        # Buat URL absolut dari gambar
        avatar_url = request.build_absolute_uri(user.avatar.url)

        # Simpan ke profil
        if hasattr(user, 'student_profile'):
            profile = user.student_profile
            profile.address_avatar = avatar_url
            profile.save()
        elif hasattr(user, 'psychologist_profile'):
            profile = user.psychologist_profile
            profile.address_avatar = avatar_url
            profile.save()

        return Response({'avatar_url': avatar_url}, status=200)
