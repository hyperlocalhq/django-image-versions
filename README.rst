=============================
django-image-versions
=============================

.. image:: https://badge.fury.io/py/django-image-versions.svg
    :target: https://badge.fury.io/py/django-image-versions

.. image:: https://travis-ci.org/archatas/django-image-versions.svg?branch=master
    :target: https://travis-ci.org/archatas/django-image-versions

.. image:: https://codecov.io/gh/archatas/django-image-versions/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/archatas/django-image-versions

An extension of django-imagekit using image versions with focus points.

Documentation
-------------

The full documentation is at https://django-image-versions.readthedocs.io.

Quickstart
----------

Install django-image-versions::

    pip install django-image-versions

Add it to your `INSTALLED_APPS`:

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

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


Development commands
---------------------

::

    pip install -r requirements_dev.txt
    invoke -l


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
