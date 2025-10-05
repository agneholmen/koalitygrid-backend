from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True, default='defaults/default.png')