from micro.jango.permissions import IsInternal
from micro.jango.views import BaseViewSet, post
from rest_framework import status
from rest_framework.response import Response

from users.serializers import UserCreateSerializer, UserCrudSerializer, UserLookupSerializer, UserSerializer
from users.services import UserService


class InternalViewSet(BaseViewSet):
    permission_classes = (IsInternal,)
    authentication_classes = ()

    @post(url_path="create")
    def create_(self, request):
        data = request.data.copy()
        serializer = UserCreateSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            validated_data: dict = serializer.validated_data
            auth_id, team_id, email = serializer.extract("auth", "team", "email")
            user = UserService.create_user(auth_id, team_id, email, data=validated_data)
            context = dict(include_profile=data.pop("include_profile", True))
            resp = dict(user=UserSerializer(user, context=context).data)
            return Response(data=resp, status=status.HTTP_200_OK)

    @post(url_path="destroy")
    def destroy_(self, request):
        data = request.data.copy()
        serializer = UserCrudSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            UserService.destroy_user(data.pop("user"))
            return Response(status=status.HTTP_200_OK)

    @post(url_path="lookup")
    def lookup(self, request):
        data = request.data.copy()
        serializer = UserLookupSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user_id, team_id, auth_id = serializer.extract("user", "team", "auth", how="get")
            if user_id:
                user = UserService.lookup_user(user_id)
            else:
                user = UserService.lookup_user(auth_id=auth_id, team_id=team_id)
            if user:
                return Response(dict(user=user), status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
