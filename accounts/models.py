from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.timezone import localdate
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField


class GenderChoice(models.TextChoices):
    MALE = "M", _("Male")
    FEMALE = "F", _("Female")
    OTHER = "O", _("Other")


class CustomUserManager(UserManager):

    def active(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(is_active=True)

    def with_profile(self):
        return self.active().filter(profile__isnull=False)


class User(AbstractUser):
    email = models.EmailField(blank=False, unique=True, verbose_name=_('Email Address'))
    nick_name = models.CharField(max_length=150, blank=True, verbose_name=_('Nick Name'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'nick_name']

    objects = CustomUserManager()

    class Meta(AbstractUser.Meta):
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.email


class ProfilerQuerySet(models.QuerySet):

    def with_age(self):
        current_date = localdate().today()
        return self.exclude(date_of_birth__isnull=True).annotate(
            calculated_age=models.ExpressionWrapper(
                current_date.year - models.F('date_of_birth__year') -
                models.Case(
                    models.When(
                        models.Q(date_of_birth__month__gt=current_date.month) |
                        models.Q(date_of_birth__month=current_date.month, date_of_birth__day__gt=current_date.day),
                        then=models.Value(1)
                    ),
                    default=models.Value(0),
                    output_field=models.IntegerField()
                ),
                output_field=models.IntegerField()
            )
        )

    def age_range(self, start, end):
        return self.with_age().filter(calculated_age__gte=start, calculated_age__lte=end)


class ProfileManager(models.Manager):

    def get_queryset(self):
        return ProfilerQuerySet(self.model, using=self._db)

    def active(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(user__is_active=True)

    def age_range(self, start, end):
        return self.get_queryset().age_range(start, end)


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
    gender = models.CharField(choices=GenderChoice.choices, default=GenderChoice.MALE, null=True, blank=True,
                              max_length=100, verbose_name=_('Gender'))
    date_of_birth = models.DateField(null=True, blank=True, verbose_name=_('Date of Birth'))
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('Update Date'))

    objects = ProfileManager()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
        ordering = ['-create_at', '-update_at']

    @property
    def age(self) -> int:
        now = localdate().today()
        if not self.date_of_birth:
            return 0
        return now.year - self.date_of_birth.year - ((now.month, now.day) < (self.date_of_birth.month, self.date_of_birth.day))


class VisitLog(models.Model):
    visitor = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='visits',
                                verbose_name=_('Visitor'))
    profile = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE, related_name='visits',
                                verbose_name=_('Visited Profile'))
    is_scanned = models.BooleanField(default=False, blank=True, verbose_name=_('Is scanned by qr code'))
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))

    class Meta:
        verbose_name = _('Visit Log')
        verbose_name_plural = _('Visit Logs')
        ordering = ['-create_at', ]


class SocialLink(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='links', verbose_name=_('Profile'))
    url = models.URLField(blank=False, null=False, verbose_name=_('Link'))
    is_active = models.BooleanField(default=True, blank=True, verbose_name=_('Active'),
                                    help_text=_('Designates whether this link is viewed at the profile'))
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation Date'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('Update Date'))

    class Meta:
        verbose_name = _('Social Link')
        verbose_name_plural = _('Social Links')
        ordering = ('-create_at', '-update_at')

    def __str__(self):
        return self.domain

    @property
    def domain(self):
        from .utils import get_hostname_from_url
        return get_hostname_from_url(self.url)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, *args, **kwargs):
    if instance and created and not (instance.is_staff or instance.is_superuser):
        max_qr_code = Profile.objects.aggregate(models.Max('qr_code'))['qr_code__max']
        new_qr_code = 1 if max_qr_code is None else max_qr_code + 1
        instance.profile = Profile.objects.create(user=instance, qr_code=new_qr_code)
