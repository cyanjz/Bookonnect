from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from .serializers import (
    UserProfileSerializer,
    UserUpdateSerializer
)


# Create your views here.
@api_view(['GET'])
def get_user_info(request, user_pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=user_pk)
    serializer = UserProfileSerializer(user)
    user_data = serializer.data
    if request.user.is_authenticated:
        user_data['isFollowed'] = user.followers.filter(user=request.user).exists()
    else:
        user_data['isFollowed'] = False
    return Response(user_data)


@api_view(['GET'])
def get_my_info(request):
    return Response({'pk': request.user.pk})


@api_view(['POST'])
def follow(request, user_pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=user_pk)
    if (request.user in user.followers.all()):
        user.followers.remove(request.user)
        resp = {
            'removed' : True,
            'numFollowers' : user.followers.count()
        }
        return Response(resp)
    else:
        user.followers.add(request.user)
        resp = {
            'removed' : False,
            'numFollowers' : user.followers.count()
        }
        return Response(resp)
    

@api_view(['PUT'])
def update_profile(request, user_pk):
    User = get_user_model()
    profile_user = User.objects.get(pk=user_pk)
    if profile_user != request.user:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        serializer = UserUpdateSerializer(profile_user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            resp_serializer = UserProfileSerializer(profile_user)
            return Response(resp_serializer.data)