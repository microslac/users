from micro.jango.views import BaseViewSet, post
from rest_framework import status
from rest_framework.response import Response

from users.serializers import (
    PrepareAvatarSerializer,
    RemoveAvatarSerializer,
    SetAvatarSerializer,
    SetProfileSerializer,
    UserInfoSerializer,
    UserProfileSerializer,
    UserSerializer,
)
from users.services import UserService


class UserViewSet(BaseViewSet):
    @post(url_path="info")
    def info(self, request):
        data = request.data.copy()
        data.update(team=request.token.team)
        serializer = UserInfoSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            team_id, user_id, include_profile = serializer.extract("team", "user", "include_profile")
            user = UserService.get_user(team_id, user_id)
            user_data = UserSerializer(user, context=dict(include_profile=include_profile)).data
            return Response(data=dict(user=user_data), status=status.HTTP_200_OK)

    @post(url_path="list")
    def list_(self, request):
        pass

    @post(url_path="prepare-photo")
    def prepare_photo(self, request):
        data = request.data.copy()
        data.update(team=request.token.team, user=request.token.user)
        serializer = PrepareAvatarSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            team_id, user_id, image = serializer.extract("team", "user", "image")
            resp = UserService.prepare_avatar(team_id, user_id, image=image)
            return Response(resp, status=status.HTTP_200_OK)

    @post(url_path="set-photo")
    def set_photo(self, request):
        data = request.data.copy()
        data.update(team=request.token.team, user=request.token.user)
        serializer = SetAvatarSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            team_id, user_id, image_id = serializer.extract("team", "user", "image")
            resp = UserService.set_avatar(team_id, user_id, image_id)
            return Response(resp, status=status.HTTP_200_OK)

    @post(url_path="remove-photo")
    def remove_photo(self, request):
        data = request.data.copy()
        data.update(team=request.token.team, user=request.token.user)
        serializer = RemoveAvatarSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            team_id, user_id = serializer.extract("team", "user")
            UserService.remove_avatar(team_id, user_id)
            return Response(status=status.HTTP_200_OK)

    @post(url_path="set-profile")
    def set_profile(self, request):
        data = request.data.copy()
        data.update(team=request.token.team, user=request.token.user)
        serializer = SetProfileSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            team_id, user_id = serializer.extract("team", "user")
            updated_data: dict = serializer.validated_data
            updated_profile = UserService.set_profile(team_id, user_id, data=serializer.validated_data)
            profile_data = UserProfileSerializer(updated_profile).data
            profile_data = {k: v for k, v in profile_data.items() if k in updated_data.keys()}
            resp = dict(id=user_id, profile=profile_data)
            return Response(resp, status=status.HTTP_200_OK)
