from django.dispatch import Signal

# User has deactivated his or her account. Args: user, request.
user_deactivated = Signal()
