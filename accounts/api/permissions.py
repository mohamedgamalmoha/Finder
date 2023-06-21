from rest_framework.permissions import BasePermission, SAFE_METHODS

from accounts.models import Profile, VisitLog


class ReadOnly(BasePermission):

    def has_permission(self, request, view) -> bool:
        return request.method in SAFE_METHODS


class IsUserWithProfile(BasePermission):

    def has_permission(self, request, view) -> bool:
        return request.user.is_authenticated and hasattr(request.user, 'profile')

    def has_object_permission(self, request, view, obj) -> bool:
        if isinstance(obj, Profile):
            return request.user == obj.user
        if isinstance(obj, VisitLog):
            return request.user == obj.visitor
        return False
