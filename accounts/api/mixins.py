from rest_framework.exceptions import MethodNotAllowed


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


class CreateMethodNotAllowedMixin:

    def create(self, request, *args, **kwargs):
        # Raise an exception to deny CREATE request to create a new object
        raise MethodNotAllowed(request.method)


class DestroyMethodNotAllowedMixin:

    def destroy(self, request, *args, **kwargs):
        # Raise an exception to deny DELETE request to delete a specific object by ID
        raise MethodNotAllowed(request.method)
