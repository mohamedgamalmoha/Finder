from django_filters import rest_framework as filters

from accounts.models import Profile, VisitLog


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
