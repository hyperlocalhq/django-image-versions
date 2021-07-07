from django import template
from django.core.files.storage import default_storage

register = template.Library()


@register.filter
def original_image_exists(f):
    return f and default_storage.exists(f.name)


@register.filter
def to_django_file(f):
    django_file = default_storage.open(f.name)
    return django_file
