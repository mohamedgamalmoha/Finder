from django import forms
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _

from accounts.api.views import UserViewSet


class BaseUidAndTokenForm(forms.Form):
    field_name: str
    action_name: str
    uid = forms.CharField(widget=forms.HiddenInput)
    token = forms.CharField(widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def get_viewset(self):
        return UserViewSet.as_view({'post': self.action_name})

    def clean(self):
        cleaned_data = super().clean()
        ViewSet = self.get_viewset()
        response = ViewSet(self.request)
        if response.data:
            for err in response.data.get(self.field_name):
                self.add_error(self.field_name, err)
        return cleaned_data


class ActivationForm(BaseUidAndTokenForm):
    action_name = 'activation'


class ResetUsernameForm(BaseUidAndTokenForm):
    field_name = 'new_email'
    action_name = 'reset_username_confirm'
    new_email = forms.EmailField(
        label=_("New Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )


class ResetPasswordForm(BaseUidAndTokenForm):
    field_name = 'new_password'
    action_name = 'reset_password_confirm'
    new_password = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
        required=True
    )
