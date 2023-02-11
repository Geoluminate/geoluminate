=============================
Geoluminate
=============================

.. image:: https://badge.fury.io/py/geoluminate.svg
    :target: https://badge.fury.io/py/geoluminate

.. image:: https://travis-ci.org/SSJenny90/geoluminate.svg?branch=master
    :target: https://travis-ci.org/SSJenny90/geoluminate

.. image:: https://codecov.io/gh/SSJenny90/geoluminate/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/SSJenny90/geoluminate

A highly-opinionated, batteries included Django app for jump-starting the creation of bespoke research databases.

Documentation
-------------

You can find the full documentation at https://geoluminate.readthedocs.io.

About
-----




Quickstart
----------

The recommended way of getting started with Geoluminate and building your own research database is to use `cookiecutter <Cookiecutter_>`_ with the geoluminate-project cookiecutter template.

 
To quickly get started creating your own modern research database using the latest release, take a look at the geoluminate-project cookiecutter template which will get you started in no time.


Install Geoluminate::

    pip install geoluminate

Add it to your `INSTALLED_APPS`:

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
        path('', include('geoluminate.urls')),
        ...
    ]

Features
--------

* Part CMS, part data-driven


Frontend
-----------
* CMS capabilites
* Map viewer
* Literature catalogue
* Author tracking
* RESTful API
* User comments application
* Login and account management
* Localization
* Automatic glossary
* Automatic API docs
* Datables.js integration with serverside processing for large datasets

Administration
---------------
* CRUD style admin interface
* Object level user permissions
* Import/export capable
* Invitation system
* Object history tracking
* Newsletters
* Literature management
* ORCID based user authentication
* Site lockdown capabilities
* User organisations

Application
-------------
* PostgreSQL with PostGIS 
* Redis integration for caching peformance
* Celery for task management
* Remote storage support (FTP or Amazon S3)

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
