from django.core.files.storage import default_storage
from imagekit import ImageSpec
from imagekit.processors import ResizeToFill

from image_versions.models import FocusPoint


# https://django-imagekit.readthedocs.io/en/latest/


class ImageSpecBase(ImageSpec):
    dimensions = (0, 0)

    @property
    def processors(self):
        anchor = (.5, .5)
        path = self.source.name[len(default_storage.base_location) + 1 :]
        focus_point = FocusPoint.objects.filter(path=path).first()
        if focus_point:
            anchor = focus_point.get_imagekit_anchor()
        width = type(self).dimensions[0]
        height = type(self).dimensions[1]
        return [ResizeToFill(width=width, height=height, anchor=anchor)]


class JPEGImageSpecBase(ImageSpecBase):
    format = "JPEG"
    options = {"quality": 90}
    dimensions = (0, 0)


class PNGImageSpecBase(ImageSpecBase):
    format = "PNG"
    options = {"quality": 90}
    dimensions = (0, 0)
