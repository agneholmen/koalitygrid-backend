from django.urls import path
from .views import (
    ChangePasswordView, CustomTokenObtainPairView, LogoutView, 
    ProfilePhotoView, RegisterView, UserInfoView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('profile-photo/', ProfilePhotoView.as_view(), name='profile_photo'),
    path('user-info/', UserInfoView.as_view(), name='user_info'),
]