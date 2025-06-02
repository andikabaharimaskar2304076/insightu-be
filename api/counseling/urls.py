# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'sessions', SessionViewSet, basename='session')

urlpatterns = [
    path('api/', include(router.urls)),
    path('create/', SessionCreateView.as_view(), name='create_session'),
    path('my-sessions/', MySessionListView.as_view(), name='my_sessions'),
    path('update-status/<uuid:session_id>/', SessionStatusUpdateView.as_view(), name='update_session_status'),
    path('<uuid:session_id>/logs/', SessionLogListView.as_view(), name='session_logs'),
    path('notifications/', NotificationListView.as_view(), name='notifications'),
    path('notifications/<uuid:pk>/read/', MarkNotificationReadView.as_view(), name='read_notification'),
    path('sessions/create/', SessionCreateView.as_view(), name='session-create'),
    path('sessions/history/', MySessionListView.as_view(), name='student_session_history'),
    path('messages/<uuid:user_id>/', ChatMessageListCreateView.as_view(), name='chat_messages'),
]
