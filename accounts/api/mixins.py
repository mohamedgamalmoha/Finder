from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import AllowAny, SAFE_METHODS


class RetrieveMethodNotAllowedMixin:

    def retrieve(self, request, *args, **kwargs):
        # Raise an exception to deny GET request to get a specific object by ID
        raise MethodNotAllowed(request.method)


class ListMethodNotAllowedMixin:

    def list(self, request, *args, **kwargs):
        # Raise an exception to deny GET request to get a list of objects
        raise MethodNotAllowed(request.method)


class PutMethodNotAllowedMixin:

    def put(self, request, *args, **kwargs):
        # Raise an exception to deny PUT request to update a specific object by ID
        raise MethodNotAllowed(request.method)


class PatchMethodNotAllowedMixin:

    def put(self, request, *args, **kwargs):
        # Raise an exception to deny PATCH request to partially update a specific object by ID
        raise MethodNotAllowed(request.method)


class UpdateMethodNotAllowedMixin(PutMethodNotAllowedMixin, PatchMethodNotAllowedMixin):
    # Raise an exception to deny PATCH / PUT request to update a specific object by ID
    ...


class CreateMethodNotAllowedMixin:

    def create(self, request, *args, **kwargs):
        # Raise an exception to deny CREATE request to create a new object
        raise MethodNotAllowed(request.method)


class DestroyMethodNotAllowedMixin:

    def destroy(self, request, *args, **kwargs):
        # Raise an exception to deny DELETE request to delete a specific object by ID
        raise MethodNotAllowed(request.method)


class AllowAnyInSafeMethodOrCustomPermissionMixin:
    """
    Mixin to allow safe methods (GET, HEAD, OPTIONS) for any user,
    while applying permission classes for other methods.
    """
    save_method_permission_classes = [AllowAny]

    def get_permission_classes(self, request):
        if request.method in SAFE_METHODS:
            return self.save_method_permission_classes
        return super().get_permission_classes(request)
