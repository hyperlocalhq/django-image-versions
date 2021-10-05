import json
import base64

from django.http import (
    HttpResponse,
    JsonResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
)
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext_lazy as _
from django.core.files.storage import default_storage
from django.shortcuts import render

from .models import FocusPoint
from .forms import FocusPointForm, VersionForm
from .utils import create_token


PIXEL_GIF_DATA = base64.b64decode(
    "R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
)


def show_image_version(request):
    form = VersionForm(data=request.GET)
    if form.is_valid():
        result = form.generate()
        return redirect(result.url)
    json_data = json.dumps(form.errors)
    response = HttpResponse(PIXEL_GIF_DATA, content_type="image/gif")
    response["Hints"] = json_data
    return response


@csrf_exempt
def focus_point_details(request):
    path = request.POST.get("path") or request.GET.get("path")
    token = request.POST.get("token") or request.GET.get("token")
    data = {}
    errors = None
    if not path:
        data["errors"] = {"path": ["This field is required."]}
        return JsonResponse(data, status=400)
    if "../" in path:
        data["errors"] = {"path": ["Such media path is not valid."]}
        return JsonResponse(data, status=400)
    if not token:
        data["errors"] = {"path": ["Token is not defined. You don't have permission to change the focus point."]}
        return JsonResponse(data, status=400)
    if token != create_token(request.user.username, path):
        data["errors"] = {"path": ["Token is incorrect. You don't have permission to change the focus point."]}
        return JsonResponse(data, status=400)

    focus_point = FocusPoint.objects.filter(path=path).first()
    if not focus_point:
        focus_point = FocusPoint(path=path)
    if request.method == "POST":
        form = FocusPointForm(data=request.POST, instance=focus_point)
        if form.is_valid():
            focus_point = form.save()
        else:
            errors = form.errors
    data["result"] = {
        "path": path,
        "x": focus_point.x,
        "y": focus_point.y,
        "width": focus_point.get_width(),
        "height": focus_point.get_height(),
    }
    if errors:
        data["errors"] = errors
    return JsonResponse(data)


def set_focus_point(request):
    """
    Allows to set a focus point for an image.

    This view has no information about the object which has the image attached.
    But a per-user unique link to this view will be formed in a template of the
    previous page only if the current user has a permission to edit the object.

    Required GET params:
    * orig_path - full path of the original image within filebrowser's MEDIA_ROOT
    * token - encrypted string ensuring that current user can modify this file

    Optional GET params:
    * goto_next - path where to go after setting the focus point

    """

    # QUERY / PATH CHECK
    orig_path = request.GET.get("orig_path", "")
    token = request.GET.get("token", "")
    goto_next = request.GET.get("goto_next", "/")

    if not orig_path:
        return HttpResponseBadRequest(
            _("Sorry. We can't show the page. Path is not defined.")
        )

    if not default_storage.exists(orig_path):
        return HttpResponseBadRequest(
            _("Sorry. We can't show the page. Path is not correct.")
        )

    if not token:
        return HttpResponseBadRequest(
            _("Sorry. We can't show the page. Token is not defined.")
        )

    if token != create_token(request.user.username, orig_path):
        return HttpResponseForbidden(
            _("Sorry. You are not allowed to access this page. Token is incorrect.")
        )

    context = {
        "path": orig_path,
        "goto_next": goto_next,
        "token": token,
    }
    return render(request, "image_versions/set_focus_point.html", context)
