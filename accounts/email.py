from django.forms.models import model_to_dict
from templated_mail.mail import BaseEmailMessage
from djoser.email import (ActivationEmail, ConfirmationEmail, PasswordResetEmail, PasswordChangedConfirmationEmail,
                          UsernameChangedConfirmationEmail, UsernameResetEmail)

from info.models import MainInfo


class AttachMainInfoEmailMixin:
    main_info_context_name = 'main_info'

    def get_main_info_data(self):
        main_info = MainInfo.objects.first()
        return model_to_dict(main_info) if main_info else {}

    def get_context_data(self):
        context = super().get_context_data()
        context[self.main_info_context_name] = self.get_main_info_data()
        return context


class UserDeleteEmail(AttachMainInfoEmailMixin, BaseEmailMessage):
    template_name = "email/delete.html"


class CustomActivationEmail(AttachMainInfoEmailMixin, ActivationEmail):
    ...


class CustomConfirmationEmail(AttachMainInfoEmailMixin, ConfirmationEmail):
    ...


class CustomPasswordResetEmail(AttachMainInfoEmailMixin, PasswordResetEmail):
    ...


class CustomPasswordChangedConfirmationEmail(AttachMainInfoEmailMixin, PasswordChangedConfirmationEmail):
    ...


class CustomUsernameChangedConfirmationEmail(AttachMainInfoEmailMixin, UsernameChangedConfirmationEmail):
    ...


class CustomUsernameResetEmail(AttachMainInfoEmailMixin, UsernameResetEmail):
    ...
