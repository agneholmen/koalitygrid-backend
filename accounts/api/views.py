from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

DEFAULT_PROFILE_PHOTO = '/media/profile_photos/default.png'

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Call the parent class to get tokens
            response = super().post(request, *args, **kwargs)
            return response
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([AllowAny])
def logout_view(request):
    # For JWT, logout is handled client-side by removing the token
    # Optionally, blacklist the token if using blacklist support
    response = Response({"detail": "Successfully logged out"}, status=status.HTTP_200_OK)
    response.delete_cookie('refresh_token')  # If using cookies
    return response

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    confirm_password = request.data.get('confirm_password')

    # Validate input
    if not all([username, email, password, confirm_password]):
        return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)
    if password != confirm_password:
        return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)

 # Create new user
    try:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password  # Hash the password
        )
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if not all([old_password, new_password]):
        return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

    user = request.user
    if not user.check_password(old_password):
        return Response({'error': 'Gammalt lösenord är felaktigt'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()
    logger.info(f"Password changed for user: {user.username}")
    return Response({'message': 'Lösenordet har ändrats'}, status=status.HTTP_200_OK)

@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def upload_profile_photo(request):
    user = request.user
    if request.method == 'POST':
        if 'profile_photo' not in request.FILES:
            return Response({'error': 'No profile photo provided'}, status=status.HTTP_400_BAD_REQUEST)

        photo = request.FILES['profile_photo']
        
        try:
            # Delete old photo if it exists and isn't the default
            if user.profile_photo and user.profile_photo.name != 'profile_photos/default.png':
                default_storage.delete(user.profile_photo.name)
            user.profile_photo = photo
            user.save()
            logger.info(f"Profile photo uploaded for user: {user.username}")
            return Response({'message': 'Profile photo uploaded successfully', 'photo_url': request.build_absolute_uri(user.profile_photo.url)}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        try:
            if user.profile_photo and user.profile_photo.name != 'profile_photos/default.png':
                default_storage.delete(user.profile_photo.name)
            user.profile_photo = None
            user.save()
            logger.info(f"Profile photo deleted for user: {request.user.username}")
            return Response({'message': 'Profile photo deleted', 'photo_url': request.build_absolute_uri(DEFAULT_PROFILE_PHOTO)}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST) 
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_photo(request):
    return Response({'profile_photo': request.build_absolute_uri(request.user.profile_photo.url) if request.user.profile_photo else request.build_absolute_uri(DEFAULT_PROFILE_PHOTO)})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    return Response({'name': request.user.first_name if request.user.first_name else request.user.username})