import sys

from django.db import models
from django.core.files.storage import default_storage
from django.core.validators import MinValueValidator, MaxValueValidator

if "makemigrations" in sys.argv:
    from django.utils.translation import gettext_noop as _
else:
    from django.utils.translation import gettext_lazy as _


class FocusPointQuerySet(models.QuerySet):
    def _modify_kwargs(self, kwargs):
        import hashlib

        if "path" in kwargs:
            path = kwargs.pop("path") or ""
            hash_object = hashlib.sha256(path.encode("utf-8"))
            kwargs["file_path_hash"] = hash_object.hexdigest()

    def filter(self, *args, **kwargs):
        self._modify_kwargs(kwargs)
        return super().filter(*args, **kwargs)

    def exclude(self, *args, **kwargs):
        self._modify_kwargs(kwargs)
        return super().exclude(*args, **kwargs)

    def get(self, *args, **kwargs):
        self._modify_kwargs(kwargs)
        return super().get(*args, **kwargs)


class FocusPointManager(models.Manager):
    def get_queryset(self):
        return FocusPointQuerySet(
            self.model, using=self._db
        )  # Important!

    def update_all_hashes(self):
        for obj in self.all():
            obj.save()

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
    file_path_hash = models.CharField(
        max_length=64,
        db_index=True,
        blank=True,
        editable=False,
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

    def save(self, *args, **kwargs):
        self.set_file_path_hash()
        super().save(*args, **kwargs)

    def set_file_path_hash(self):
        import hashlib

        file_path_hash = ""
        if self.path:
            file_path = self.path
            hash_object = hashlib.sha256(file_path.encode("utf-8"))
            file_path_hash = hash_object.hexdigest()

        self.file_path_hash = file_path_hash

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
