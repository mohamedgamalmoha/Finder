import random
from typing import List
from django.utils.safestring import mark_safe


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
    return mark_safe(f"""<a href='{image.url}'><img src="{image.url}" style="height:60%; border-radius: 50%; border: 6px solid gray;"></a>""")
