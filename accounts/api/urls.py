from django.urls import path
from .views import CustomTokenObtainPairView, change_password_view, get_user_info, get_user_photo, logout_view, register_view, upload_profile_photo
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('change-password/', change_password_view, name='change_password'),
    path('upload-profile-photo/', upload_profile_photo, name='upload_profile_photo'),
    path('user-profile/', get_user_photo, name='get_user_photo'),
    path('user-info', get_user_info, name='get_user_info'),
]