import random
from typing import List
from urllib.parse import urlparse

from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType

from djoser.conf import settings
from djoser.compat import get_user_email


def generate_random_number(lower_limit: int, upper_limit: int, exclude: List[int] = None) -> int:
    number = random.randint(lower_limit, upper_limit)
    if exclude is None:
        return number
    while number in exclude:
        number = random.randint(lower_limit, upper_limit)
    return number


def get_object_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None


def create_profile_html(image):
    return mark_safe(
        f"""<a href='{image.url}'><img src="{image.url}" style="height:60%; border-radius: 50%; border: 6px solid gray;"></a>""")


def get_change_admin_url(model_instance):
    content_type = ContentType.objects.get_for_model(model_instance.__class__)
    admin_url = reverse("admin:{}_{}_change".format(content_type.app_label, content_type.model),
                        args=(model_instance.pk,))
    return admin_url


def send_activation_mail(request, user):
    context = {"user": user}
    to = [get_user_email(user)]
    settings.EMAIL.activation(request, context).send(to)


def get_hostname_from_url(url):
    return urlparse(url).hostname
