from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.exceptions import PermissionDenied
from rest_framework.mixins import (CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin,
                                   DestroyModelMixin)

from rest_flex_fields import is_expanded
from drf_spectacular.utils import extend_schema
from djoser.conf import settings
from djoser.views import UserViewSet as DjoserUserViewSet
from djoser.compat import get_user_email, get_user_email_field_name

from accounts import signals
from accounts.models import User, Profile, VisitLog, SocialLink
from .utils import user_has_profile
from .throttling import UpdateRateThrottle
from .permissions import IsUserWithProfile
from .filters import ProfileFilter, VisitLogFilter, UserFilter
from .serializers import ProfileSerializer, VisitLogSerializer, SocialLinkSerializer
from .mixins import AllowAnyInSafeMethodOrCustomPermissionMixin, ThrottleActionsWithMethodsMixin


class ProfileViewSet(AllowAnyInSafeMethodOrCustomPermissionMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin,
                     GenericViewSet):
    queryset = Profile.objects.active()
    serializer_class = ProfileSerializer
    filterset_class = ProfileFilter
    filterset_fields = ('links',)
    permission_classes = [IsUserWithProfile]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'list':
            queryset = queryset.exclude(is_public=False)
            if is_expanded(self.request, 'links'):
                queryset = queryset.prefetch_related(
                    models.Prefetch('links', queryset=SocialLink.objects.filter(is_active=True))
                )
        return queryset

    def get_permission_classes(self, request):
        if self.action == 'me':
            return self.permission_classes
        return super().get_permission_classes(request)

    def get_object(self):
        if self.action == 'me':
            return self.request.user.profile
        return super(ProfileViewSet, self).get_object()

    @action(detail=False, methods=["GET", "PUT", "PATCH"], name='Get My Profile')
    def me(self, request, *args, **kwargs):
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        elif request.method == "PUT":
            return self.update(request, *args, **kwargs)
        elif request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class VisitLogViewSet(AllowAnyInSafeMethodOrCustomPermissionMixin, CreateModelMixin, RetrieveModelMixin, ListModelMixin,
                      GenericViewSet):
    queryset = VisitLog.objects.all()
    serializer_class = VisitLogSerializer
    filterset_class = VisitLogFilter
    permission_classes = [IsUserWithProfile]

    def perform_create(self, serializer):
        serializer.save(visitor=self.request.user)

    def get_permission_classes(self, request):
        if self.action in ('my_visits', 'my_views'):
            return self.permission_classes
        return super().get_permission_classes(request)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'my_visits':
            return queryset.filter(visitor=self.request.user).exclude(hide_from_visitor=True)
        elif self.action == 'my_views':
            return queryset.filter(profile=self.request.user.profile).exclude(hide_from_profile=True)
        return queryset

    @extend_schema(responses={200: VisitLogSerializer(many=True)})
    @action(detail=False, methods=['GET'], name='Get My Visits', url_path='my-visits')
    def my_visits(self, request, *args, **kwargs):
        """Get list of visits that user made"""
        return self.list(request, *args, **kwargs)

    @extend_schema(responses={200: VisitLogSerializer(many=True)})
    @action(detail=False, methods=['GET'], name='Get My Views', url_path='my-views')
    def my_views(self, request,  *args, **kwargs):
        """Get list of user profile visits that others have made"""
        return self.list(request, *args, **kwargs)

    @extend_schema(request=None, responses={200: None, 403: None},
                   description="Hide visits from user\n"
                               "\t-200: The visit is updated successfully.\n"
                               "\t-403: The user is neither the visitor nor the profile belongs to him.\n")
    @action(detail=True, methods=['POST'], name='Hide Visit', url_path='hide')
    def hide(self, request,  *args, **kwargs):
        user = request.user
        profile = getattr(user, 'profile', None)
        instance = self.get_object()
        if instance.visitor == user:
            instance.hide_from_visitor = True
        elif instance.profile == profile:
            instance.hide_from_profile = True
        else:
            raise PermissionDenied(detail=_('You do not have permission to perform this action. '
                                            'You are neither the visitor nor the profile belongs to you.'))
        instance.save()
        return Response(status.HTTP_200_OK)


class UserViewSet(ThrottleActionsWithMethodsMixin, DjoserUserViewSet):
    queryset = User.objects.with_profile()
    filterset_class = UserFilter
    throttle_classes = [UpdateRateThrottle]
    throttle_actions = [
        ('me', 'PUT'),
        ('me', 'PATCH')
    ]

    def get_queryset(self):
        user = self.request.user
        queryset = super(UserViewSet, self).get_queryset()
        if self.action == 'list' and user_has_profile(user):
            queryset = queryset.exclude(id=user.id)
        return queryset

    @action(["post"], detail=False, url_path=f"set_{User.USERNAME_FIELD}")
    def set_username(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        new_username = serializer.data["new_" + User.USERNAME_FIELD]

        setattr(user, User.USERNAME_FIELD, new_username)
        email_field_name = get_user_email_field_name(user)
        # deactivate user to reactivate it again throw email
        if User.USERNAME_FIELD == email_field_name:
            user.is_active = False
            # send deactivate signal
            signals.user_deactivated.send(
                sender=self.__class__, user=user, request=self.request
            )
        user.save()

        context = {"user": user}
        to = [get_user_email(user)]

        if settings.USERNAME_CHANGED_EMAIL_CONFIRMATION:
            settings.EMAIL.username_changed_confirmation(self.request, context).send(to)

        # send activation mail in case of being not activated, to guarantee that he owns this email
        if settings.SEND_ACTIVATION_EMAIL and not user.is_active:
            settings.EMAIL.activation(self.request, context).send(to)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["post"], detail=False, url_path=f"reset_{User.USERNAME_FIELD}_confirm")
    def reset_username_confirm(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_username = serializer.data["new_" + User.USERNAME_FIELD]

        setattr(serializer.user, User.USERNAME_FIELD, new_username)
        if hasattr(serializer.user, "last_login"):
            serializer.user.last_login = now()

        user = serializer.user
        email_field_name = get_user_email_field_name(user)
        # deactivate user to reactivate it again throw email
        if User.USERNAME_FIELD == email_field_name:
            user.is_active = False
            # send deactivate signal
            signals.user_deactivated.send(
                sender=self.__class__, user=user, request=self.request
            )
        user.save()

        context = {"user": user}
        to = [get_user_email(user)]

        if settings.USERNAME_CHANGED_EMAIL_CONFIRMATION:
            settings.EMAIL.username_changed_confirmation(self.request, context).send(to)

        # send activation mail in case of being not activated, to guarantee that he owns this email
        if settings.SEND_ACTIVATION_EMAIL and not user.is_active:
            settings.EMAIL.activation(self.request, context).send(to)

        return Response(status=status.HTTP_204_NO_CONTENT)


class SocialLinkViewSet(AllowAnyInSafeMethodOrCustomPermissionMixin, CreateModelMixin, UpdateModelMixin,
                        DestroyModelMixin, ListModelMixin, GenericViewSet):
    queryset = SocialLink.objects.all()
    serializer_class = SocialLinkSerializer
    permission_classes = [IsUserWithProfile]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_authenticated and user_has_profile(user):
            queryset = queryset.filter(profile=user.profile)
        return queryset

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)
