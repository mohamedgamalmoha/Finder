from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin

from djoser.views import UserViewSet as DjoserUserViewSet
from drf_spectacular.utils import extend_schema, OpenApiResponse

from accounts.models import User, Profile, VisitLog
from .permissions import IsUserWithProfile
from .filters import ProfileFilter, VisitLogFilter, UserFilter
from .serializers import ProfileSerializer, VisitLogSerializer
from .mixins import AllowAnyInSafeMethodOrCustomPermissionMixin, DestroyMethodNotAllowedMixin


class ProfileViewSet(AllowAnyInSafeMethodOrCustomPermissionMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin,
                     GenericViewSet):
    queryset = Profile.objects.active()
    serializer_class = ProfileSerializer
    filterset_class = ProfileFilter
    permission_classes = [IsUserWithProfile]

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
            return queryset.filter(visitor=self.request.user)
        elif self.action == 'my_views':
            return queryset.filter(profile=self.request.user.profile)
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


class UserViewSet(DestroyMethodNotAllowedMixin, DjoserUserViewSet):
    queryset = User.objects.with_profile()
    filterset_class = UserFilter

    def get_queryset(self):
        user = self.request.user
        queryset = super(UserViewSet, self).get_queryset()
        if self.action == 'list' and hasattr(user, 'profile'):
            queryset.exclude(user)
        return queryset

    @extend_schema(responses={status.HTTP_405_METHOD_NOT_ALLOWED:
                              OpenApiResponse(description='Delete user is not allowed')})
    def destroy(self, request, *args, **kwargs):
        return super(UserViewSet, self).destroy(request, *args, **kwargs)

    @action(["get", "put", "patch"], detail=False)
    def me(self, request, *args, **kwargs):
        return super().me(request, *args, **kwargs)
