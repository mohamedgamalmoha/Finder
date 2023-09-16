from django import template
from django.templatetags.static import static


register = template.Library()


@register.simple_tag(takes_context=True)
def absolute_static(context, path):
    request = context['request']
    return request.build_absolute_uri(static(path))
