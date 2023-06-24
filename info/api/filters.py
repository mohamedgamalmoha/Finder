from django.db import models
from django_filters import rest_framework as filters

from info.models import FAQs, AboutUs, TermsOfService, CookiePolicy, PrivacyPolicy


class CustomSearchFilter(filters.FilterSet):
    search = filters.CharFilter(method='custom_search', label="Search in title & description")

    def custom_search(self, queryset, name, value):
        """Search in both title and description"""
        return queryset.filter(models.Q(title__icontains=value) | models.Q(description__icontains=value))


class AboutUsFilter(CustomSearchFilter):

    class Meta:
        model = AboutUs
        fields = ('title', 'description', 'search')


class TermsOfServiceFilter(CustomSearchFilter):

    class Meta:
        model = TermsOfService
        fields = ('title', 'description', 'search')


class CookiePolicyFilter(CustomSearchFilter):

    class Meta:
        model = CookiePolicy
        fields = ('title', 'description', 'search')


class PrivacyPolicyFilter(CustomSearchFilter):

    class Meta:
        model = PrivacyPolicy
        fields = ('title', 'description', 'search')


class FAQsFilter(filters.FilterSet):
    search = filters.CharFilter(method='custom_search', label="Search in title & description")

    class Meta:
        model = FAQs
        fields = ('quote', 'answer', 'search')

    def custom_search(self, queryset, name, value):
        """Search in both title and description"""
        return queryset.filter(models.Q(quote__icontains=value) | models.Q(answer__icontains=value))
