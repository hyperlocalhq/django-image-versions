import json
import base64

from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseForbidden

from .models import FocusPoint
from .forms import FocusPointForm, VersionForm


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
    data = {}
    errors = None
    if not path:
        data["errors"] = {"path": ["This field is required."]}
        return JsonResponse(data, status=400)
    if "../" in path:
        data["errors"] = {"path": ["Such media path is not valid."]}
        return JsonResponse(data, status=400)
    focus_point = FocusPoint.objects.filter(path=path).first()
    if not focus_point:
        focus_point = FocusPoint(path=path)
    if request.method == "POST":
        if not request.user.is_staff:
            err = "You don't have permission to change focus points."
            return HttpResponseForbidden(err)
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
