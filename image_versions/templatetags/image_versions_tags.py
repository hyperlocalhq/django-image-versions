from django.core.files.storage import default_storage
from django import template
from django.urls import reverse


register = template.Library()


### TAGS ###


@register.simple_tag(takes_context=True)
def focus_point_url(context, path_or_file_object, goto_next=None):
    """
    Returns focus-point URL for the user

    Usage:
        <a href="{% focus_point_url <path> <request> <goto_next> %}">
            Set focus point
        </a>
        or
        <a href="{% focus_point_url <file_object> <request> <goto_next> %}">
            Set focus point
        </a>

    Example:
        <a href="{% focus_point_url "test/original.png" request request.path %}">
            Set focus point
        </a>
        <a href="{% focus_point_url person.avatar request request.path %}">
            Set focus point
        </a>

    """
    from ..utils import create_token

    request = context["request"]
    if not goto_next:
        goto_next = request.path

    if not request.user.is_authenticated:
        return ""

    path = (
        path_or_file_object
        if isinstance(path_or_file_object, str)
        else path_or_file_object.name
    )

    token = create_token(request.user.username, path)

    return (
        reverse("image_versions:set_focus_point")
        + f"?orig_path={path}&token={token}&goto_next={goto_next}"
    )


### FILTERS ###


@register.filter
def original_image_exists(path_or_file_object):
    """
    Checks if a file exists in the default storage.
    path_or_file_object is a file path relative to MEDIA_URL or a file object.
    """
    return path_or_file_object and default_storage.exists(
        path_or_file_object
        if isinstance(path_or_file_object, str)
        else path_or_file_object.name
    )


@register.filter
def to_django_file(path_or_file_object):
    """
    Converts f to django.core.files.File object.
    path_or_file_object is a file path relative to MEDIA_URL or a file object.
    """
    django_file = default_storage.open(
        path_or_file_object
        if isinstance(path_or_file_object, str)
        else path_or_file_object.name
    )
    return django_file


@register.filter
def image_version_url(path_or_file_object, generator_id):
    """
    Creates an image version and returns its URL if the original file exists.
    """
    from imagekit.registry import generator_registry
    from imagekit.cachefiles import ImageCacheFile

    if original_image_exists(path_or_file_object):
        django_file = to_django_file(path_or_file_object)
        generator = generator_registry.get(generator_id, source=django_file)
        image_version = ImageCacheFile(generator)
        return image_version.url
    return ""


@register.filter
def is_image(path_or_file_object):
    """
    Checks if a file is an image.
    Assumes that the file exists in the default storage.

    path_or_file_object is a file path relative to MEDIA_URL or a file object.
    """
    from PIL import Image, UnidentifiedImageError

    django_file = to_django_file(path_or_file_object)
    try:
        Image.open(django_file)
        return True
    except (OSError, UnidentifiedImageError):
        return False
