from rest_framework import serializers

from django.contrib.auth.backends import get_user_model
from djoser.serializers import UserSerializer, UserCreateSerializer

from accounts.models import Profile


User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        exclude = ()
        read_only_fields = ('id', 'user', 'create_at', 'update_at', 'qr_code')


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta(UserCreateSerializer.Meta):
        fields = (*UserCreateSerializer.Meta.fields, 'nick_name')


class CustomUserSerializer(UserSerializer):
    profile = ProfileSerializer(many=False, read_only=True)

    class Meta(UserSerializer.Meta):
        fields = (*UserSerializer.Meta.fields, 'profile')
        read_only_fields = (*UserSerializer.Meta.read_only_fields, 'profile')
