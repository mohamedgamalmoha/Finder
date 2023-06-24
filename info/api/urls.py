from django.urls import path

from .views import (MainInfoAPIView, FAQsAPIView, AboutUsAPIView, TermsOfServiceAPIView, CookiePolicyAPIView,
                    PrivacyPolicyAPIView, ContactUsAPIView, HeaderImageAPIView)


app_name = 'info'

urlpatterns = [
    path('main-info/', MainInfoAPIView.as_view(), name='main-info'),
    path('about-us/', AboutUsAPIView.as_view(), name='about_us'),
    path('terms-of-service/', TermsOfServiceAPIView.as_view(), name='terms_of_service'),
    path('cookie-policy/', CookiePolicyAPIView.as_view(), name='cookie_policy'),
    path('privacy-policy/', PrivacyPolicyAPIView.as_view(), name='privacy_policy'),
    path('contact-us/', ContactUsAPIView.as_view(), name='contact_us'),
    path('header-image/', HeaderImageAPIView.as_view(), name='header_images'),
    path('frequently-asked-question/', FAQsAPIView.as_view(), name='fqa'),
]
