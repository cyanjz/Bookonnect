from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

class CustomRegisterSerializer(RegisterSerializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        value = super().validate_email(email)
        if get_user_model().objects.filter(email=value).exists():
            raise serializers.ValidationError("이미 사용 중인 이메일입니다.")
        return value
    