
from django.db import migrations


def forwards_func(apps, schema_editor):
    import hashlib

    FocusPoint = apps.get_model("image_versions", "FocusPoint")

    for obj in FocusPoint.objects.all():
        if obj.path:
            file_path = obj.path
            hash_object = hashlib.sha256(file_path.encode("utf-8"))
            file_path_hash = hash_object.hexdigest()
            obj.file_path_hash = file_path_hash
            obj.save(update_fields=["file_path_hash"])


class Migration(migrations.Migration):
    dependencies = [
        ("image_versions", "0003_focuspoint_file_path_hash"),
    ]

    operations = [
        migrations.RunPython(
            code=forwards_func, reverse_code=migrations.RunPython.noop
        ),
    ]
