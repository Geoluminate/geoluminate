# Geoluminate 

[![Github Build](https://github.com/Geoluminate/geoluminate/actions/workflows/build.yml/badge.svg)](https://github.com/Geoluminate/geoluminate/actions/workflows/build.yml)
[![Github Docs](https://github.com/Geoluminate/geoluminate/actions/workflows/docs.yml/badge.svg)](https://github.com/Geoluminate/geoluminate/actions/workflows/docs.yml)
[![CodeCov](https://codecov.io/gh/Geoluminate/geoluminate/branch/main/graph/badge.svg?token=0Q18CLIKZE)](https://codecov.io/gh/Geoluminate/geoluminate)
![GitHub](https://img.shields.io/github/license/Geoluminate/geoluminate)
![GitHub last commit](https://img.shields.io/github/last-commit/Geoluminate/geoluminate)
![PyPI](https://img.shields.io/pypi/v/geoluminate)
<!-- [![RTD](https://readthedocs.org/projects/geoluminate/badge/?version=latest)](https://geoluminate.readthedocs.io/en/latest/readme.html) -->
<!-- [![Documentation](https://github.com/Geoluminate/geoluminate/actions/workflows/build-docs.yml/badge.svg)](https://github.com/Geoluminate/geoluminate/actions/workflows/build-docs.yml) -->
<!-- [![PR](https://img.shields.io/github/issues-pr/Geoluminate/geoluminate)](https://github.com/Geoluminate/geoluminate/pulls)
[![Issues](https://img.shields.io/github/issues-raw/Geoluminate/geoluminate)](https://github.com/Geoluminate/geoluminate/pulls) -->
<!-- ![PyPI - Downloads](https://img.shields.io/pypi/dm/geoluminate) -->
<!-- ![PyPI - Status](https://img.shields.io/pypi/status/geoluminate) -->

A Django application for managing collections of scientific instruments

Documentation
-------------

The full documentation is at https://ssjenny90.github.io/geoluminate/

Quickstart
----------

Install Geoluminate::

    pip install geoluminate

Add it to your `INSTALLED_APPS`:


    INSTALLED_APPS = (
        ...
        'geoluminate',
        ...
    )

Add Geoluminate's URL patterns:

    urlpatterns = [
        ...
        path('', include("geoluminate.urls")),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


Development commands
---------------------

    pip install -r requirements_dev.txt
    invoke -l


Credits
-------

