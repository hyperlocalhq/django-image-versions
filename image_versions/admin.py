from django.contrib import admin
from django.conf import settings

from .models import FocusPoint


class FocusPointAdmin(admin.ModelAdmin):
    search_fields = ["path"]
    list_display = ["path", "x", "y", "width", "height"]
    fields = ["path", "x", "y", "width", "height"]
    readonly_fields = ["width", "height"]


if settings.DEBUG:
    admin.site.register(FocusPoint, FocusPointAdmin)
