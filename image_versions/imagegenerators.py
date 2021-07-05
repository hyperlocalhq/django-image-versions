from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFill, ResizeToFit

from image_versions.models import FocusPoint


# https://django-imagekit.readthedocs.io/en/latest/


class ImageSpecBase(ImageSpec):
    dimensions = (0, 0)

    @property
    def processors(self):
        anchor = (.5, .5)
        focus_point = FocusPoint.objects.filter(path=self.source.name).first()
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
