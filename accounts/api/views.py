from rest_framework.viewsets import ModelViewSet

from accounts.models import Profile
from .serializers import ProfileSerializer
from .permissions import IsUserWithProfile

from .mixins import (CreateMethodNotAllowedMixin, DestroyMethodNotAllowedMixin,
                     AllowAnyInSafeMethodOrCustomPermissionMixin)

from .filters import ProfileFilter


class ProfileViewSet(CreateMethodNotAllowedMixin, DestroyMethodNotAllowedMixin,
                     AllowAnyInSafeMethodOrCustomPermissionMixin, ModelViewSet):
    queryset = Profile.objects.active()
    serializer_class = ProfileSerializer
    filterset_class = ProfileFilter
    permission_classes = [IsUserWithProfile]
