from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import *
from .serializers import *
from .permissions import *
from api.users.models import User

# Create your views here.

class SessionViewSet(viewsets.ModelViewSet):
    serializer_class = SessionSerializer
    permission_classes = [IsStudentOrPsychologist]

    def get_queryset(self):
        user = self.request.user
        return Session.objects.filter(models.Q(student=user) | models.Q(psychologist=user))

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)
class SessionCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'student':
            return Response({'detail': 'Hanya siswa yang dapat membuat sesi.'}, status=403)

        serializer = SessionSerializer(data=request.data)

        if serializer.is_valid():
            # Sisipkan student langsung sebagai argumen
            session = serializer.save(student=request.user)

            # Buat log
            SessionLog.objects.create(
                session=session,
                action='created',
                description=f'Sesi dibuat oleh siswa {request.user.username}'
            )

            # Kirim notifikasi ke psikolog
            Notification.objects.create(
                user=session.psychologist,
                message=f'Ada permintaan sesi baru dari {request.user.username}'
            )

            return Response(SessionSerializer(session).data, status=201)

        return Response(serializer.errors, status=400)
class MySessionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role == 'student':
            sessions = Session.objects.filter(student=user)
        elif user.role == 'psychologist':
            sessions = Session.objects.filter(psychologist=user)
        else:
            sessions = Session.objects.all()  # admin

        serializer = SessionSerializer(sessions, many=True)
        return Response(serializer.data)
class SessionStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, session_id):
        if request.user.role != 'psychologist':
            return Response({'detail': 'Hanya psikolog yang dapat mengubah status sesi.'}, status=403)

        try:
            session = Session.objects.get(id=session_id, psychologist=request.user)
        except Session.DoesNotExist:
            return Response({'detail': 'Sesi tidak ditemukan atau Anda tidak memiliki akses.'}, status=404)

        new_status = request.data.get('status')
        if new_status not in ['accepted', 'rejected', 'completed']:
            return Response({'detail': 'Status tidak valid.'}, status=400)

        session.status = new_status
        session.save()

        SessionLog.objects.create(
            session=session,
            action=new_status,
            description=f'Sesi {new_status} oleh psikolog {request.user.username}'
        )

        Notification.objects.create(
            user=session.student,
            message=f'Sesi Anda telah {new_status} oleh psikolog {request.user.username}'
        )

        return Response({'message': f'Status sesi diperbarui menjadi {new_status}.'}, status=200)
class SessionLogListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, session_id):
        try:
            session = Session.objects.get(id=session_id)
        except Session.DoesNotExist:
            return Response({'detail': 'Sesi tidak ditemukan.'}, status=404)

        # Hanya siswa/psikolog yang terkait atau admin
        if request.user.role == 'student' and session.student != request.user:
            return Response({'detail': 'Tidak memiliki akses ke log sesi ini.'}, status=403)
        if request.user.role == 'psychologist' and session.psychologist != request.user:
            return Response({'detail': 'Tidak memiliki akses ke log sesi ini.'}, status=403)

        logs = session.logs.all().order_by('created_at')
        serializer = SessionLogSerializer(logs, many=True)
        return Response(serializer.data)

class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifs = Notification.objects.filter(user=request.user).order_by('-created_at')
        serializer = NotificationSerializer(notifs, many=True)
        return Response(serializer.data)


class MarkNotificationReadView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            notif = Notification.objects.get(id=pk, user=request.user)
        except Notification.DoesNotExist:
            return Response({'detail': 'Notifikasi tidak ditemukan.'}, status=404)

        notif.is_read = True
        notif.save()
        return Response({'message': 'Notifikasi ditandai sebagai telah dibaca.'})