from auto_datatables.views import AutoTableMixin, DataTableBaseView
from django.conf import settings
from django.shortcuts import render


def placeholder_view(request):
    """This is a placeholder view that can be used to add dummy urls to the
    project. Use it as a placeholder to design things like toolbars, menus,
    navigation, etc. without having to worry about the underlying view."""
    return render(request, "geoluminate/placeholder.html")


class GeoluminateTableView(DataTableBaseView):
    debug = settings.DEBUG
