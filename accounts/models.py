from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from .utils import generate_random_number, get_object_or_none


class User(AbstractUser):
    email = models.EmailField(blank=False, unique=True, verbose_name=_('Email Address'))
    nick_name = models.CharField(max_length=150, blank=True, verbose_name=_('Nick Name'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'nick_name']

    class Meta(AbstractUser.Meta):
        ...

    def __str__(self):
        return self.email


class ProfileManager(models.Manager):

    def active(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(user__is_active=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('User'), related_name='profile')
    position = models.CharField(null=True, blank=True, max_length=100, verbose_name=_('Position'))
    bio = models.TextField(null=True, blank=True, verbose_name=_('Bio'))
    phone_number_1 = PhoneNumberField(null=True, blank=True, verbose_name=_('Phone Number 1'))
    phone_number_2 = PhoneNumberField(null=True, blank=True, verbose_name=_('Phone Number 2'))
    city = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('City'))
    country = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Country'))
    address = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Address'))
    image = models.URLField(null=True, blank=True, verbose_name=_('Image'))
    cover = models.URLField(null=True, blank=True, verbose_name=_('Cover Image'))
    qr_code = models.PositiveIntegerField(unique=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('Update Date'))

    objects = ProfileManager()

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['-create_at', '-update_at']


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, *args, **kwargs):
    if instance and created:
        exclude = sender.objects.values_list('qr_code')
        number = generate_random_number(0, 10_000, exclude)
        instance.profile = sender.objects.create(user=instance, qr_code=number)


@receiver(pre_save, sender=Profile)
def change_profile(sender, instance, raw, using, update_fields, **kwargs):
    # Ignore if the qr_code value is not changes
    if 'qr_code' not in update_fields:
        return

    # Get instance tht have the same value of qr_code
    another_instance = get_object_or_none(sender, qr_code=instance.qr_code)
    if another_instance is None:
        return

    # Get the pre values of instance
    pre_instance = get_object_or_none(sender, pk=instance.pk)

    # Update the another instance with the pre qr_Code value
    another_instance.qr_code = pre_instance.qr_code
    another_instance.save()
