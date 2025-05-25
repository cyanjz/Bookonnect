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
    

class UserProfileSerializer(serializers.ModelSerializer):
    num_followers = serializers.SerializerMethodField()
    num_followings = serializers.SerializerMethodField()
    num_comments = serializers.SerializerMethodField()
    num_threads = serializers.SerializerMethodField()

    def get_num_followers(self, obj):
        return obj.followers.count()
    
    def get_num_followings(self, obj):
        return obj.followings.count()
    
    def get_num_comments(self, obj):
        return obj.comment_set.count()
    
    def get_num_threads(self, obj):
        return obj.thread_set.count()

    class Meta:
        model = get_user_model()
        fields = [
            'username', 
            'user_profile_img', 
            'user_introduction', 
            'user_banner_img', 
            'num_followers',
            'num_followings',
            'num_comments',
            'num_threads',
            ]
        
class UserUpdateSerializer(serializers.ModelSerializer):
    user_profile_img = serializers.ImageField(required=False)
    user_banner_img = serializers.ImageField(required=False)
    class Meta:
        model = get_user_model()
        fields = ['username', 'user_profile_img', 'user_banner_img', 'user_introduction']