"""Datatables populates a `drf_auto_endpoint.router` with relevant
API viewsets that can be accessed by `datatables.js`. The urls
generated by the router MUST be included in your project urls or
the application will not work. You can include the urls by placing
the following in your project `urlspatterns`:

.. code:: python

    urlspattern = [
        ...
        path('datatables/', include('datatables.urls')),
        ...
    ]

"""

from django.urls import path, include
from drf_auto_endpoint.router import router

urlpatterns = [
    path('', include(router.urls)),
]
