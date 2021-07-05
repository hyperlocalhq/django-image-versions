=====
Usage
=====

To use django-image-versions in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'image_versions.apps.ImageVersionsConfig',
        ...
    )

Add django-image-versions's URL patterns:

.. code-block:: python

    from image_versions import urls as image_versions_urls


    urlpatterns = [
        ...
        url(r'^', include(image_versions_urls)),
        ...
    ]
