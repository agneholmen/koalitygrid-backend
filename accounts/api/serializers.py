from rest_framework import serializers
from dj_rest_auth.serializers import PasswordChangeSerializer

class CustomPasswordChangeSerializer(PasswordChangeSerializer):
    def validate_old_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError('Gammalt lösenord är felaktigt')
        return value

    def validate(self, data):
        if not all([data.get('new_password1'), data.get('new_password2')]):
            raise serializers.ValidationError('Fälten för nytt lösenord är obligatoriska.')
        if data.get('new_password1') != data.get('new_password2'):
            raise serializers.ValidationError('Nya lösenorden matchar inte.')
        return super().validate(data)