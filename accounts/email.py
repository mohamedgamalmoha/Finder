from templated_mail.mail import BaseEmailMessage


class UserDeleteEmail(BaseEmailMessage):
    template_name = "email/delete.html"
