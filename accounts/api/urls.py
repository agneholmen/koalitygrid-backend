from django.urls import path
from .views import (
    ProfilePhotoView, UserInfoView
)

urlpatterns = [
    path('profile-photo/', ProfilePhotoView.as_view(), name='profile_photo'),
    path('user-info/', UserInfoView.as_view(), name='user_info'),
]