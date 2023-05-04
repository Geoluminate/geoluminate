# class BaseSite(AbstractSite):
#     """A concrete base model for GIS enabled databases. 'geoluminate.contrib.gis'
#     must be in your installed apps to utilize this model in your application.

#     .. note:

#         Inherit from this class if you plan on working with multiple object types
#         for a given site. If you are working with only a single data type, for
#         performance reasons you may wish to consider inheriting directly from
#         `geoluminate.contrib.gis.BaseGIS`.
#     """

#     class Meta:
#         verbose_name = _("Geographic site")
#         verbose_name_plural = _("Geographic sites")
#         default_related_name = "site"
