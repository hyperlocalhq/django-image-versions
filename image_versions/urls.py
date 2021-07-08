from django.urls import path

from . import views

app_name = "image_versions"

urlpatterns = [
    path("set-focus-point/", views.set_focus_point, name="set_focus_point"),
    path("focus-point/", views.focus_point_details, name="focus_point_details"),
]
