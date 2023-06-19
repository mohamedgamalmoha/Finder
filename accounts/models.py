from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    email = models.EmailField(blank=False, unique=True, verbose_name=_('Email Address'))
    nick_name = models.CharField(max_length=150, blank=True, verbose_name=_('Nick Name'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'nick_name']

    class Meta(AbstractUser.Meta):
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.email


class ProfileManager(models.Manager):

    def active(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(user__is_active=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name=_('User'))
    position = models.CharField(null=True, blank=True, max_length=100, verbose_name=_('Position'))
    bio = models.TextField(null=True, blank=True, verbose_name=_('Bio'))
    phone_number_1 = PhoneNumberField(null=True, blank=True, verbose_name=_('Phone Number 1'))
    phone_number_2 = PhoneNumberField(null=True, blank=True, verbose_name=_('Phone Number 2'))
    city = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('City'))
    country = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Country'))
    address = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Address'))
    image = models.ImageField(null=True, blank=True, upload_to='images/', verbose_name=_('Image'))
    cover = models.ImageField(null=True, blank=True, upload_to='covers/', verbose_name=_('Cover Image'))
    qr_code = models.PositiveIntegerField(unique=True, default=0, verbose_name=_('QR Code'))
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('Update Date'))

    objects = ProfileManager()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
        ordering = ['-create_at', '-update_at']


class VisitLog(models.Model):
    visitor = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='visits',
                                verbose_name=_('Visitor'))
    profile = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE, related_name='visits',
                                verbose_name=_('Visited Profile'))
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))

    class Meta:
        verbose_name = _('Visit Log')
        verbose_name_plural = _('Visit Logs')
        ordering = ['-create_at', ]


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, *args, **kwargs):
    if instance and created and not (instance.is_staff or instance.is_superuser):
        qr_codes = Profile.objects.values_list('qr_code')
        new_qr_code = max(qr_codes) + 1 if qr_codes else 0
        instance.profile = Profile.objects.create(user=instance, qr_code=new_qr_code)
