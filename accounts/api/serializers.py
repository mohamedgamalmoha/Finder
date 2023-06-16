from django.contrib.auth.backends import get_user_model

from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer
from djoser.serializers import UserSerializer, UserCreateSerializer

from accounts.models import Profile, VisitLog


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


class VisitLogSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = VisitLog
        fields = '__all__'
        read_only_fields = ('visitor', 'create_at')
        expandable_fields = {
            'profile': ProfileSerializer
        }
