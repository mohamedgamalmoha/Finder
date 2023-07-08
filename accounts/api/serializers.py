from django.contrib.auth.backends import get_user_model

from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer
from rest_flex_fields.serializers import FlexFieldsSerializerMixin
from djoser.serializers import UserSerializer, UserCreateSerializer

from accounts.models import Profile, VisitLog, GenderChoice


User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(read_only=True)

    class Meta:
        model = Profile
        exclude = ()
        read_only_fields = ('id', 'user', 'create_at', 'update_at', 'qr_code', 'age')

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Set default image based on gender
        if instance.gender == GenderChoice.FEMALE:
            data['image'] = '/static/images/profile_female.png'
        else:
            data['image'] = '/static/images/profile_male.png'

        # Set default cover in case of being empty
        if not instance.cover:
            data['cover'] = '/static/images/profile_cover.png'

        return data


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta(UserCreateSerializer.Meta):
        fields = (*UserCreateSerializer.Meta.fields, 'nick_name')


class CustomUserSerializer(FlexFieldsSerializerMixin, UserSerializer):

    class Meta(UserSerializer.Meta):
        fields = (*UserSerializer.Meta.fields, 'profile')
        read_only_fields = (*UserSerializer.Meta.read_only_fields, 'profile')
        expandable_fields = {
            'profile': (ProfileSerializer, {'many': False})
        }


class VisitLogSerializer(FlexFieldsModelSerializer):

    class Meta:
        model = VisitLog
        fields = '__all__'
        read_only_fields = ('visitor', 'create_at')
        expandable_fields = {
            'visitor': CustomUserSerializer,
            'profile': ProfileSerializer
        }
