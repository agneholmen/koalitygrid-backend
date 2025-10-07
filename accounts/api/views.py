from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

DEFAULT_PROFILE_PHOTO = '/media/defaults/default.png'

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
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

class ProfilePhotoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        photo_url = (
            request.build_absolute_uri(request.user.profile_photo.url)
            if request.user.profile_photo
            else request.build_absolute_uri(DEFAULT_PROFILE_PHOTO)
        )
        return Response({'profile_photo': photo_url}, status=status.HTTP_200_OK)

    def post(self, request):
        if 'profile_photo' not in request.FILES:
            return Response({'error': 'No profile photo provided'}, status=status.HTTP_400_BAD_REQUEST)

        photo = request.FILES['profile_photo']
        user = request.user
        try:
            # Delete old photo if it exists and isn't the default
            if user.profile_photo and user.profile_photo.name != 'defaults/default.png':
                default_storage.delete(user.profile_photo.name)
            user.profile_photo = photo
            user.save()
            logger.info(f"Profile photo uploaded for user: {user.username}")
            return Response(
                {
                    'message': 'Profile photo uploaded successfully',
                    'photo_url': request.build_absolute_uri(user.profile_photo.url)
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        try:
            if user.profile_photo and user.profile_photo.name != 'defaults/default.png':
                default_storage.delete(user.profile_photo.name)
            user.profile_photo = None
            user.save()
            logger.info(f"Profile photo deleted for user: {user.username}")
            return Response(
                {
                    'message': 'Profile photo deleted',
                    'photo_url': request.build_absolute_uri(DEFAULT_PROFILE_PHOTO)
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'name': request.user.first_name if request.user.first_name else request.user.username})