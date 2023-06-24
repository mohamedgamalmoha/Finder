from django.contrib import admin

from modeltranslation.admin import TranslationAdmin

from .models import MainInfo, FAQs, AboutUs, TermsOfService, CookiePolicy, PrivacyPolicy, ContactUs, HeaderImage


class MainInfoAdmin(TranslationAdmin):
    readonly_fields = ('whatsapp_link', )

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone_number', 'subject', 'create_at', 'update_at')
    search_fields = ('email', 'subject', 'first_name', 'last_name', 'message')


class TitledDescriptiveTranslationAdmin(TranslationAdmin):
    list_display = ('title', 'description')
    search_fields = ('title', 'description')


class FAQsAdmin(TranslationAdmin):
    list_display = ('quote', 'answer')
    search_fields = ('quote', 'answer')


admin.site.register(MainInfo, MainInfoAdmin)
admin.site.register(FAQs, FAQsAdmin)
admin.site.register(AboutUs, TitledDescriptiveTranslationAdmin)
admin.site.register(CookiePolicy, TitledDescriptiveTranslationAdmin)
admin.site.register(PrivacyPolicy, TitledDescriptiveTranslationAdmin)
admin.site.register(TermsOfService, TitledDescriptiveTranslationAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(HeaderImage)
