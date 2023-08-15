from rest_framework.permissions import BasePermission, SAFE_METHODS

from accounts.models import Profile, VisitLog, SocialLink
from .utils import user_has_profile


class ReadOnly(BasePermission):

    def has_permission(self, request, view) -> bool:
        return request.method in SAFE_METHODS


class IsUserWithProfile(BasePermission):

    def has_permission(self, request, view) -> bool:
        return request.method in SAFE_METHODS or (request.user.is_authenticated and user_has_profile(request.user))

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in SAFE_METHODS:
            return True
        if isinstance(obj, Profile):
            return request.user == obj.user
        if isinstance(obj, VisitLog):
            return request.user == obj.visitor or request.user == obj.profile.user
        if isinstance(obj, SocialLink):
            return request.user.profile == obj.profile
        return False


class DenyDelete(BasePermission):

    def has_permission(self, request, view):
        return not request.method == 'DELETE'
