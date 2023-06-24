from modeltranslation.translator import translator, TranslationOptions

from .models import MainInfo, FAQs, AboutUs, TermsOfService, CookiePolicy, PrivacyPolicy, HeaderImage


class MainInfoTranslationOptions(TranslationOptions):
    fields = ('why_us', )


class FAQsTranslationOptions(TranslationOptions):
    fields = ('quote', 'answer')


class TitledDescriptiveTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


class HeaderImageTranslationOptions(TranslationOptions):
    fields = ('alt', )


translator.register(FAQs, FAQsTranslationOptions)
translator.register(MainInfo, MainInfoTranslationOptions)
translator.register(HeaderImage, HeaderImageTranslationOptions)
translator.register(AboutUs, TitledDescriptiveTranslationOptions)
translator.register(CookiePolicy, TitledDescriptiveTranslationOptions)
translator.register(PrivacyPolicy, TitledDescriptiveTranslationOptions)
translator.register(TermsOfService, TitledDescriptiveTranslationOptions)
