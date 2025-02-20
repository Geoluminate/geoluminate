import django_tables2 as tables
from django.utils.translation import gettext_lazy as _
from easy_icons import icon


class BaseTable(tables.Table):
    id = tables.Column(verbose_name="UUID", visible=False)
    dataset = tables.Column(linkify=True, orderable=False, verbose_name=False)

    def render_dataset(self, value):
        return icon("dataset")

    def render_location(self, record):
        return icon("location")

    def value_dataset(self, value):
        return value.pk

    def before_render(self, request):
        """
        A way to hook into the moment just before rendering the template.

        Can be used to hide a column.

        Arguments:
            request: contains the `WGSIRequest` instance, containing a `user` attribute if
                `.django.contrib.auth.middleware.AuthenticationMiddleware` is added to
                your `MIDDLEWARE_CLASSES`.

        Example::

            class Table(tables.Table):
                name = tables.Column(orderable=False)
                country = tables.Column(orderable=False)

                def before_render(self, request):
                    if request.user.has_perm("foo.delete_bar"):
                        self.columns.hide("country")
                    else:
                        self.columns.show("country")
        """
        return


class SampleTable(BaseTable):
    name = tables.Column(linkify=True)
    latitude = tables.Column(accessor="location.x", verbose_name=_("Latitude"))
    longitude = tables.Column(accessor="location.y", verbose_name=_("Longitude"))
    location = tables.Column(accessor="location", linkify=True, verbose_name=False, orderable=False)


class MeasurementTable(BaseTable):
    sample = tables.Column(linkify=True)
    latitude = tables.Column(accessor="sample.location.x", verbose_name=_("Latitude"))
    longitude = tables.Column(accessor="sample.location.y", verbose_name=_("Longitude"))
    location = tables.Column(accessor="sample.location", linkify=True, verbose_name=False, orderable=False)

    def __init__(self, data=None, *args, **kwargs):
        # modify the queryset (data) here if required
        data = data.prefetch_related("sample")
        super().__init__(*args, data=data, **kwargs)

    def render_sample(self, value):
        sample_type = value.get_real_instance_class()
        return sample_type._meta.verbose_name
