from rest_framework.throttling import UserRateThrottle


UPDATE_METHODS = ('PUT', 'PATCH')


class UpdateRateThrottle(UserRateThrottle):
    scope = 'update'

    def allow_request(self, request, view):
        if request.method not in UPDATE_METHODS:
            return True
        return super().allow_request(request, view)
