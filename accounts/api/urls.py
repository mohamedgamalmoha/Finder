from django.urls import path, re_path, include

from rest_framework import routers
from djoser.social.views import ProviderAuthView

from .views import ProfileViewSet, VisitLogViewSet, UserViewSet, SocialLinkViewSet


app_name = 'accounts'

router = routers.DefaultRouter()
router.register(r'profile', ProfileViewSet, basename='profile')
router.register(r'visit', VisitLogViewSet, basename='visit')
router.register(r'auth/users', UserViewSet, basename='user')
router.register(r'social-link', SocialLinkViewSet, basename='social_link')

urlpatterns = [
    path('auth/', include('djoser.urls.jwt'), name='jwt'),
    re_path(r"^auth/social/(?P<provider>\S+)/$", ProviderAuthView.as_view(), name="social-auth-provider"),
    path('', include(router.urls), name='routes'),
]
