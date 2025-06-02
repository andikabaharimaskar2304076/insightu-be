from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import render, get_object_or_404
from django.utils.dateparse import parse_datetime
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

        data = request.data.copy()
        data['student'] = str(request.user.id)

        # Validasi data wajib
        schedule_time_str = data.get('schedule_time')
        psychologist_id = data.get('psychologist')
        if not schedule_time_str or not psychologist_id:
            return Response({'detail': 'Data tidak lengkap.'}, status=400)

        # Konversi waktu
        schedule_time = parse_datetime(schedule_time_str)
        if not schedule_time:
            return Response({'detail': 'Format tanggal tidak valid.'}, status=400)

        # Cek apakah sudah ada sesi pada waktu tersebut untuk psikolog yang sama
        conflict_exists = Session.objects.filter(
            psychologist_id=psychologist_id,
            schedule_time=schedule_time,
            status__in=['pending', 'accepted']
        ).exists()

        if conflict_exists:
            return Response(
                {'detail': 'Waktu ini sudah digunakan oleh sesi lain. Silakan pilih waktu lain.'},
                status=400
            )

        # Buat sesi jika tidak ada konflik
        serializer = SessionSerializer(data=data)
        if serializer.is_valid():
            session = serializer.save(student=request.user)

            # Log dan notifikasi
            SessionLog.objects.create(
                session=session,
                action='created',
                description=f'Sesi dibuat oleh siswa {request.user.username}'
            )

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
class ChatMessageListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = request.user
        messages = ChatMessage.objects.filter(
            models.Q(sender=user, receiver_id=user_id) |
            models.Q(sender_id=user_id, receiver=user)
        ).order_by('timestamp')
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request, user_id):
        sender = request.user
        receiver = get_object_or_404(User, id=user_id)

        message = request.data.get("message")
        if not message:
            return Response({"detail": "Message cannot be empty."}, status=400)

        chat = ChatMessage.objects.create(sender=sender, receiver=receiver, message=message)
        return Response(ChatMessageSerializer(chat).data, status=201)
