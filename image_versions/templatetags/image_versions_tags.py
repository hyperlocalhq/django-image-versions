from django import template
from django.core.files.storage import default_storage

register = template.Library()


@register.filter
def original_image_exists(f):
    """
    Checks if a file exists in the default storage.
    f is a file path relative to MEDIA_URL or a file object.
    """
    return f and default_storage.exists(f if isinstance(f, str) else f.name)


@register.filter
def to_django_file(f):
    """
    Converts f to django.core.files.File object.
    f is a file path relative to MEDIA_URL or a file object.
    """
    django_file = default_storage.open(f if isinstance(f, str) else f.name)
    return django_file
