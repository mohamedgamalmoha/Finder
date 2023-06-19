from rest_framework.viewsets import ModelViewSet

from accounts.models import Profile, VisitLog
from .permissions import IsUserWithProfile
from .filters import ProfileFilter, VisitLogFilter
from .serializers import ProfileSerializer, VisitLogSerializer
from .mixins import (CreateMethodNotAllowedMixin, DestroyMethodNotAllowedMixin, UpdateMethodNotAllowedMixin,
                     AllowAnyInSafeMethodOrCustomPermissionMixin)


class ProfileViewSet(CreateMethodNotAllowedMixin, DestroyMethodNotAllowedMixin,
                     AllowAnyInSafeMethodOrCustomPermissionMixin, ModelViewSet):
    queryset = Profile.objects.active()
    serializer_class = ProfileSerializer
    filterset_class = ProfileFilter
    permission_classes = [IsUserWithProfile]


class VisitLogViewSet(DestroyMethodNotAllowedMixin, UpdateMethodNotAllowedMixin,
                      AllowAnyInSafeMethodOrCustomPermissionMixin, ModelViewSet):
    queryset = VisitLog.objects.all()
    serializer_class = VisitLogSerializer
    filterset_class = VisitLogFilter
    permission_classes = [IsUserWithProfile]

    def perform_create(self, serializer):
        serializer.save(visitor=self.request.user)
