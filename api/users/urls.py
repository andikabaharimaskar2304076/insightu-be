from django.urls import path
from .views import *
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register_user'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', CurrentUserView.as_view(), name='current_user'),
    path('psychologist-profile/', PsychologistProfileView.as_view(), name='psychologist_profile'),
    path('student-profile/', StudentProfileView.as_view(), name='student_profile'),
    path('verify/<str:user_id>/', VerifyUserView.as_view(), name='verify_user'),
    path('users-all/', UserListView.as_view(), name='user_list'),
    path('find/<str:username>/', UserByUsernameView.as_view(), name='find_user_by_username'),
    path('admin/users/unverified/', UnverifiedUserListView.as_view(), name='admin_unverified_users'),
    path('users/upload-avatar/', UploadAvatarView.as_view(), name='upload_avatar'),
    path('availabilities/', AvailabilityListAPIView.as_view(), name='availability-list'),
] 
