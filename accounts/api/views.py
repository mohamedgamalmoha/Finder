from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin

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
