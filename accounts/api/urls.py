from django.urls import path
from .views import (
    ChangePasswordView, ProfilePhotoView, UserInfoView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('profile-photo/', ProfilePhotoView.as_view(), name='profile_photo'),
    path('user-info/', UserInfoView.as_view(), name='user_info'),
]