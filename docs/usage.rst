=====
Usage
=====

To use Geoluminate in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'geoluminate',
        ...
    )

Add Geoluminate's URL patterns:

.. code-block:: python

    from geoluminate import urls as geoluminate_urls


    urlpatterns = [
        ...
        url(r'^', include(geoluminate_urls)),
        ...
    ]
