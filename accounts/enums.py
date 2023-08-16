from django.db import models
from django.utils.translation import gettext_lazy as _


class GenderChoice(models.TextChoices):
    MALE = "M", _("Male")
    FEMALE = "F", _("Female")
    OTHER = "O", _("Other")


class SocialLinkIconChoice(models.TextChoices):
    FACEBOOK = 'facebook.com', 'facebook-square'
    TWITTER = 'twitter.com', 'twitter-square'
    LINKEDIN = 'linkedin.com', 'linkedin-square'
    SNAPCHAT = 'snapchat.com', 'snapchat-square'
    BEHANCE = 'behance.com', 'behance-square'
    GITHUB = 'github.com', 'github-square'
    PINTEREST = 'pinterest.com', 'pinterest-square'
    WHATSAPP = 'whatsapp.com', 'whatsapp'
    INSTAGRAM = 'instagram.com', 'instagram'
    TIKTOK = 'tiktok.com', 'tiktok'
    DISCORD = 'discord.com', 'discord'
    TELEGRAM = 'telegram.com', 'telegram'
    YOUTUBE = 'youtube.com', 'youtube-play'
    DRIBBBLE = 'dribbble.com', 'dribbble'
    TWITCH = 'twitch.com', 'twitch'
    OTHER = 'globe', ''
