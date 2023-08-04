from django.contrib.auth.backends import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer
from rest_flex_fields.serializers import FlexFieldsSerializerMixin
from djoser.serializers import UserSerializer, UserCreateSerializer

from accounts.models import Profile, VisitLog, SocialLink, GenderChoice


User = get_user_model()


class SocialLinkSerializer(serializers.ModelSerializer):
    domain = serializers.CharField(read_only=True)

    class Meta:
        model = SocialLink
        exclude = ()
        read_only_fields = ('id', 'profile', 'domain', 'create_at', 'update_at')


class ProfileSerializer(FlexFieldsModelSerializer):
    age = serializers.IntegerField(read_only=True)

    class Meta:
        model = Profile
        exclude = ()
        read_only_fields = ('id', 'user', 'create_at', 'update_at', 'qr_code', 'age')
        expandable_fields = {
            'links': (SocialLinkSerializer, {'many': True, 'read_only': True}),
            'user': ('accounts.api.serializers.CustomUserSerializer', {'many': False, 'read_only': True,
                                                                       'omit': ['profile']}),
            'visits': ('accounts.api.serializers.VisitLogSerializer', {'many': True, 'read_only': True})
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)

        request = self.context['request']

        # Set default image based on gender
        if not instance.image:
            if instance.gender == GenderChoice.FEMALE:
                data['image'] = request.build_absolute_uri('/static/images/profile_female.png')
            else:
                data['image'] = request.build_absolute_uri('/static/images/profile_male.png')

        # Set default cover in case of being empty
        if not instance.cover:
            data['cover'] = request.build_absolute_uri('/static/images/profile_cover.png')

        return data


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta(UserCreateSerializer.Meta):
        fields = (*UserCreateSerializer.Meta.fields, 'nick_name')


class CustomUserSerializer(FlexFieldsSerializerMixin, UserSerializer):

    class Meta(UserSerializer.Meta):
        fields = (*UserSerializer.Meta.fields, 'profile')
        read_only_fields = (*UserSerializer.Meta.read_only_fields, 'profile')
        expandable_fields = {
            'profile': (ProfileSerializer, {'many': False}),
            'visits': ('accounts.api.serializers.VisitLogSerializer', {'many': True, 'read_only': True})
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

    def validate_profile(self, profile):
        user = self.context['request'].user
        if profile.user == user:
            raise serializers.ValidationError(_('Cant create visit for same profile'))
        return profile
