from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _, ngettext

from social_django.models import UserSocialAuth, Nonce, Association
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

from .models import Profile, User, SocialLink
from .utils import create_profile_html, get_change_admin_url, send_activation_mail


class AgeProfileListFilter(admin.SimpleListFilter):
    title = _('Age')
    parameter_name = 'age'

    def lookups(self, request, model_admin):
        return (
            ('0, 18', _('Under Aage')),
            ('18,30', _('In the twenties')),
            ('30,40', _('In the thirties')),
            ('40,50', _('In the forties')),
            ('50,60', _('In the fifties')),
            ('60,70', _('In the sixties')),
            ('70,80', _('In the seventies')),
        )

    def queryset(self, request, queryset):
        val = self.value()
        if val is None:
            return queryset
        start_age, end_age = self.value().split(',')
        return queryset.age_range(start_age, end_age)


class ProfileInlineAdmin(admin.TabularInline):
    model = Profile
    extra = 0
    can_delete = False


class SocialLinkInlineAdmin(admin.TabularInline):
    model = SocialLink
    extra = 0
    can_delete = False
    readonly_fields = ('domain', 'create_at', 'update_at')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'create_at', 'update_at']
    search_fields = ['user__first_name', 'user__last_name', 'user__nick_name', 'position', 'bio']
    date_hierarchy = 'create_at'
    list_filter = ['gender', AgeProfileListFilter]
    readonly_fields = ['user', 'create_at', 'update_at', 'show_image', 'show_cover', 'age']
    fieldsets = (
        ('User Main Info', {'fields': (
            'user',
            'position',
            'bio',
            ('phone_number_1', 'phone_number_2'),
        )}),
        ('Address', {'fields': (
            ('city', 'country'),
            'address',
        )}),
        ('Images', {'fields': (
            ('image', 'show_image'),
            ('cover', 'show_cover'),
        )}),
        ('Extra', {'fields': (
            'gender',
            ('date_of_birth', 'age'),
            'qr_code'
        )}),
    )
    inlines = [SocialLinkInlineAdmin]

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        """
        Show a link to the model with this field already exists.
        """

        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.unique:
            try:
                model = db_field.model.objects.get(qr_code=request.POST.get('qr_code'))
                url = get_change_admin_url(model)
            except db_field.model.DoesNotExist:
                ...
            except Exception as e:
                messages.error(request, e)
            else:
                messages.info(request, mark_safe(
                    _(f"If you wanna edit the duplicate instance, <a style='color: white;' href='{url}'>Go here</a>")))
        return field

    def show_image(self, obj):
        if obj.image:
            return create_profile_html(obj.image)
        return ''

    show_image.short_description = ''

    def show_cover(self, obj):
        if obj.cover:
            return create_profile_html(obj.cover)
        return ''

    show_cover.short_description = ''


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    actions = ['activate_users', 'deactivate_users', 'send_users_activation_mail']
    inlines = [ProfileInlineAdmin]

    def get_inlines(self, request, obj):
        if not obj or (obj and (obj.is_staff or obj.is_superuser)):
            return []
        return self.inlines

    def deactivate_users(self, request, queryset):
        updated = queryset.filter(is_active=True).update(is_active=False)
        self.message_user(
            request,
            _(
                ngettext(
                    "%d user was successfully deactivated.",
                    "%d users were successfully deactivated.",
                    updated,
                ) % updated
            ),
            messages.SUCCESS,
        )

    deactivate_users.short_description = _('Deactivate selected Users')

    def activate_users(self, request, queryset):
        updated = queryset.filter(is_active=False).update(is_active=True)
        self.message_user(
            request,
            _(
                ngettext(
                    "%d user was successfully activated.",
                    "%d users were successfully activated.",
                    updated,
                ) % updated
            ),
            messages.SUCCESS,
        )

    activate_users.short_description = _('Activate selected Users')

    def send_users_activation_mail(self, request, queryset):
        queryset = queryset.filter(is_active=False)
        for user in queryset:
            send_activation_mail(request, user)
        self.message_user(
            request,
            _(
                ngettext(
                    "%d user has successfully received the email.",
                    "%d users have successfully received the email.",
                    queryset,
                ) % queryset
            ),
            messages.SUCCESS,
        )

    send_users_activation_mail.short_description = _('Send activation mail')


admin.site.unregister(Nonce)
admin.site.unregister(Association)
admin.site.unregister(UserSocialAuth)
admin.site.unregister(BlacklistedToken)
admin.site.unregister(OutstandingToken)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
