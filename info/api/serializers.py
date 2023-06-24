from rest_framework import serializers

from info.models import MainInfo, AboutUs, TermsOfService, CookiePolicy, PrivacyPolicy, FAQs, ContactUs, HeaderImage


class MainInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = MainInfo
        exclude = ()


class AboutUsSerializer(serializers.ModelSerializer):

    class Meta:
        model = AboutUs
        exclude = ()


class TermsOfServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = TermsOfService
        exclude = ()


class CookiePolicySerializer(serializers.ModelSerializer):

    class Meta:
        model = CookiePolicy
        exclude = ()


class PrivacyPolicySerializer(serializers.ModelSerializer):

    class Meta:
        model = PrivacyPolicy
        exclude = ()


class FAQsSerializer(serializers.ModelSerializer):

    class Meta:
        model = FAQs
        exclude = ()


class ContactUsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactUs
        exclude = ('create_at', 'update_at')


class HeaderImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeaderImage
        exclude = ()
