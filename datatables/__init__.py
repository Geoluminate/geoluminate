"""A standalone Django app that makes it easy integrate the
wonderful and free `Datatables.js`_ package into your Django front end
using a combination of server side processing and ajax.

It relies on the following key packages to make it work:

* `django-rest-framework`_
    For serving API views that `Datatables.js`_ can interact with via ajax.

* `DRF-schema-adapter`_
    For automated creation and registration of serializers and endpoints used
    by django-rest-framework. Also for structuring API metadata (via `OPTIONS`
    requests) into a format suitable for Datatables.js

* `django-rest-framework-datatables-editor`_
    For providing an appropriate renderer to be used with django-rest-framework
    that outputs the API in a format known to Datatables.js.

.. _django-rest-framework-datatables-editor: link: https://github.com/vertliba/django-rest-framework-datatables-editor
.. _django-rest-framework: link: https://www.django-rest-framework.org
.. _DRF-schema-adapter: link: https://drf-schema-adapter.readthedocs.io/en/latest/drf_auto_endpoint/metadata/
.. _Datatables.js: link: https://datatables.net

"""
from drf_auto_endpoint import router

register = router.register
