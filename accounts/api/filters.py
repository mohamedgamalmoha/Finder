from django.db import models

from django_filters import rest_framework as filters

from accounts.models import User, Profile, VisitLog


class UserFilter(filters.FilterSet):
    search = filters.CharFilter(method='custom_search', label="Search first & last & nick name, and email")

    def custom_search(self, queryset, name, value):
        """Search first & last & nick name, and email"""
        return queryset.filter(
            models.Q(first_name__icontains=value) | models.Q(last_name__icontains=value) |
            models.Q(nick_name__icontains=value) | models.Q(email__icontains=value) |
            models.Q(username__icontains=value)
        )

    class Meta:
        model = User
        fields = ('search', )


class ProfileFilter(filters.FilterSet):

    class Meta:
        model = Profile
        exclude = ('user', 'image', 'cover', 'create_at', 'update_at')


class VisitLogFilter(filters.FilterSet):
    before = filters.DateTimeFilter(field_name='create_at', lookup_expr='gte')
    after = filters.DateTimeFilter(field_name='create_at', lookup_expr='lte')

    class Meta:
        model = VisitLog
        fields = ('visitor', 'profile', 'before', 'after')
