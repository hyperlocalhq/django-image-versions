from django import template
from django.core.files.storage import default_storage

register = template.Library()


@register.filter
def original_image_exists(f):
    if not f:
        return False
    return default_storage.exists(f.name)
