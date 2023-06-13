from rest_framework.permissions import BasePermission, SAFE_METHODS


class ReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsUserWithProfile(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'profile')

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
