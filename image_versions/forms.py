from django import forms
from django.core.files.storage import default_storage
from django.utils.translation import gettext

from .models import FocusPoint
from .imagegenerators import VERSIONS

VERSION_CHOICES = [(key, key) for key in VERSIONS.keys()]


class VersionForm(forms.Form):
    image_path = forms.CharField(required=True)
    version = forms.ChoiceField(required=True, choices=VERSION_CHOICES)

    def clean_image_path(self):
        image_path = self.cleaned_data["image_path"]
        if image_path.startswith("http") or ".." in image_path:
            raise forms.ValidationError(gettext("Invalid image path"))
        if not default_storage.exists(image_path):
            raise forms.ValidationError(gettext("Image does not exist"))
        if default_storage.size(image_path) > 1024 * 1024 * 10:
            raise forms.ValidationError(
                gettext("Original image is too big. It should be less than 10 MB.")
            )
        return image_path

    def get_generator_class(self):
        return VERSIONS[self.cleaned_data["version"]]

    def generate(self):
        from imagekit.cachefiles import ImageCacheFile

        image_path = self.cleaned_data["image_path"]
        VersionGenerator = self.get_generator_class()
        with default_storage.open(image_path) as source_file:
            image_generator = VersionGenerator(source=source_file)
            cached = ImageCacheFile(image_generator)
            cached.generate()
            return cached


class FocusPointForm(forms.ModelForm):
    class Meta:
        model = FocusPoint
        fields = ["path", "x", "y"]
