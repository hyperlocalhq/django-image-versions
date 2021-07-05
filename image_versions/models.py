import sys

from django.db import models
from django.core.files.storage import default_storage
from django.core.validators import MinValueValidator, MaxValueValidator

if "makemigrations" in sys.argv:
    from django.utils.translation import ugettext_noop as _
else:
    from django.utils.translation import ugettext_lazy as _


class FocusPointManager(models.Manager):
    def copy_focus_point(self, path_source, path_target, transfer=False):
        focus_point_source = self.filter(path=path_source).first()
        if focus_point_source:
            focus_point_target, created = self.update_or_create(
                path=path_target,
                defaults={
                    "x": focus_point_source.x,
                    "y": focus_point_source.y,
                },
            )
            if transfer:
                focus_point_source.delete()
            return focus_point_target

    def transfer_focus_point(self, path_source, path_target):
        return self.copy_focus_point(
            path_source=path_source, path_target=path_target, transfer=True
        )

    def delete_ghost_focus_points(self, verbose=False):
        for focus_point in self.all():
            if not focus_point.image_exists():
                if verbose:
                    print(f"File {focus_point.path} doesn't exist.")
                focus_point.delete()


class FocusPoint(models.Model):
    path = models.CharField(
        _("Image path inside the media directory"),
        max_length=255,
        unique=True,
        db_index=True,
    )
    x = models.FloatField(
        "X",
        help_text="From -1.0 (left) to 1.0 (right)",
        default=0,
        validators=[MinValueValidator(-1.0), MaxValueValidator(1.0)],
    )
    y = models.FloatField(
        "Y",
        help_text="From -1.0 (bottom) to 1.0 (top)",
        default=0,
        validators=[MinValueValidator(-1.0), MaxValueValidator(1.0)],
    )
    width = models.PositiveIntegerField(_("Width"), default=0, editable=False)
    height = models.PositiveIntegerField(
        _("Height"), default=0, editable=False
    )

    objects = FocusPointManager()

    class Meta:
        verbose_name = _("Focus Point")
        verbose_name_plural = _("Focus Points")
        ordering = ["path"]

    def __str__(self):
        return self.path

    def image_exists(self):
        return default_storage.exists(self.path)

    def update_dimensions(self):
        from PIL import Image

        if not self.image_exists():
            return 0, 0
        fp = default_storage.open(self.path, "rb")
        image = Image.open(fp)
        width, height = image.size
        self.width = width
        self.height = height
        self.save()
        return width, height

    def get_width(self):
        if not self.width:
            self.update_dimensions()
        return self.width

    def get_height(self):
        if not self.height:
            self.update_dimensions()
        return self.height

    def get_imagekit_anchor(self):
        """
        Imagekit <-> Focus Point
        (0, 0)       (-1, 1)
        (0.5, 0.5)   (0, 0)
        (1, 1)       (1, -1)
        :return:
        """
        return (self.x + 1.0) / 2.0, (1.0 - self.y) / 2.0
