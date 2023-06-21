from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin

from drf_spectacular.utils import extend_schema

from accounts.models import Profile, VisitLog
from .permissions import IsUserWithProfile
from .filters import ProfileFilter, VisitLogFilter
from .serializers import ProfileSerializer, VisitLogSerializer
from .mixins import AllowAnyInSafeMethodOrCustomPermissionMixin


class ProfileViewSet(AllowAnyInSafeMethodOrCustomPermissionMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin,
                     GenericViewSet):
    queryset = Profile.objects.active()
    serializer_class = ProfileSerializer
    filterset_class = ProfileFilter
    permission_classes = [IsUserWithProfile]


class VisitLogViewSet(AllowAnyInSafeMethodOrCustomPermissionMixin, CreateModelMixin, RetrieveModelMixin, ListModelMixin,
                      GenericViewSet):
    queryset = VisitLog.objects.all()
    serializer_class = VisitLogSerializer
    filterset_class = VisitLogFilter
    permission_classes = [IsUserWithProfile]

    def perform_create(self, serializer):
        serializer.save(visitor=self.request.user)

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
