import random
from typing import List


def generate_random_number(lower_limit: int, upper_limit: int, exclude: List[int] = None) -> int:
    number = random.randint(lower_limit, upper_limit)
    if exclude is None:
        return number
    while number in exclude:
        number = random.randint(lower_limit, upper_limit)
    return number


def get_object_or_none(model,  *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None
