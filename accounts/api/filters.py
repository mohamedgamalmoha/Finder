from django_filters import rest_framework as filters

from accounts.models import Profile


class ProfileFilter(filters.FilterSet):

    class Meta:
        model = Profile
        exclude = ('user', 'image', 'cover', 'create_at', 'update_at')
