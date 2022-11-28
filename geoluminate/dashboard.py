from django import forms
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from pydoc import locate


def get_dashboard(name):
    """Utility function to get the appropriate dashboard class
    as specified by the user.

    Args:
        name (str): The key of the dasboard as specified in settings under
        DASHBOARD = {}

    Returns:
        class: The specified Dashboard class
    """
    dashboard = getattr(settings, 'DASHBOARDS')[name]
    return locate(dashboard)


class Dashboard(metaclass=forms.MediaDefiningClass):
    """
    Base class for dashboards. The Dashboard class is a simple
    python list that has two additional properties:

    ``text``
        The text displayed in list elements on the dashboard page

    ``url_name``
        A valid url name that can be reversed by Django in order to fill out
        content in the main application windown

    """

    template = 'user/dashboard.html'
    children = None

    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])
        self.children = self.children or []

    def init_with_context(self, context):
        """
        Sometimes you may need to access context or request variables to build
        your dashboard, this is what the ``init_with_context()`` method is for.
        This method is called just before the display with a
        ``django.template.RequestContext`` as unique argument, so you can
        access to all context variables and to the ``django.http.HttpRequest``.
        """
        pass

    def __iter__(self):
        return self.children.__iter__()

    def __next__(self):
        return self.children.__next__()


class App(object):

    def __init__(self, text, url_name, **kwargs):
        self.text = text

        # placing this here so it raises an error if it's not a valid url
        reverse(url_name)
        self.url_name = url_name

        for key in kwargs:
            setattr(self, key, kwargs[key])
