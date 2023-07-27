from accounts.model import Profile


def user_has_profile(user):
    return isinstance(getattr(user, 'profile', None), Profile)
