from rest_framework.throttling import UserRateThrottle
from rest_framework.settings import api_settings


UPDATE_METHODS = ('PUT', 'PATCH')


class UpdateRateThrottle(UserRateThrottle):
    scope = 'update'
    rate = api_settings.DEFAULT_THROTTLE_RATES.update

    def allow_request(self, request, view):
        if request.method not in UPDATE_METHODS:
            return True
        return super().allow_request(request, view)
