from django.db import models
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.utils.timezone import localdate
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .models import Profile, User
from .utils import create_profile_html, get_change_admin_url


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
        current_year = localdate().today().year
        start_year, end_year = current_year - int(end_age), current_year - int(start_age)
        return queryset.filter(
            models.Q(date_of_birth__year__gte=start_year) & models.Q(date_of_birth__year__lte=end_year)
        )


class ProfileInlineAdmin(admin.TabularInline):
    model = Profile
    extra = 0
    can_delete = False


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
                messages.info(request, mark_safe(_(f"If you wanna edit the duplicate instance, <a style='color: white;' href='{url}'>Go here</a>")))
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
    inlines = [ProfileInlineAdmin]

    def get_inlines(self, request, obj):
        if not obj or (obj and (obj.is_staff or obj.is_superuser)):
            return []
        return self.inlines


admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
