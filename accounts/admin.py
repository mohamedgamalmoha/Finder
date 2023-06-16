from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Profile, User
from .utils import create_profile_html


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'create_at', 'update_at']
    search_fields = ['user__first_name', 'user__last_name', 'user__nick_name', 'position', 'bio']
    date_hierarchy = 'create_at'
    readonly_fields = ['user', 'create_at', 'update_at', 'show_image', 'show_cover']
    fieldsets = (
        ('User Main Info', {'fields': (
            'user',
            'position',
            'bio',
            ('phone_number_1', 'phone_number_2'),
            'qr_code'
        )}),
        ('Address', {'fields': (
            ('city', 'country'),
            'address',
        )}),
        ('Images', {'fields': (
            ('image', 'show_image'),
            ('cover', 'show_cover'),
        )}),
    )

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


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
