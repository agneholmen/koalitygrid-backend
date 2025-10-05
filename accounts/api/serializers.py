from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({'confirm_password': 'Passwords do not match'})
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({'username': 'Username already taken'})
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': 'Email already registered'})
        return data