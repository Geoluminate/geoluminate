from geoluminate.contrib.contributors.models import Contribution, Contributor
from geoluminate.contrib.datasets.models import Dataset
from geoluminate.contrib.projects.models import Project
from geoluminate.contrib.reviews.models import Review
from geoluminate.contrib.samples.models import Location, Sample

# class GlobalConfiguration(SingletonModel):
#     site = models.OneToOneField(Site, blank=True, null=True, on_delete=models.SET_NULL)  # type: ignore[var-annotated]
#     logo = FilerImageField(
#         related_name="+",
#         verbose_name=_("Logo"),
#         null=True,
#         blank=True,
#         on_delete=models.SET_NULL,
#     )
#     icon = FilerImageField(
#         related_name="+",
#         verbose_name=_("Icon"),
#         null=True,
#         blank=True,
#         on_delete=models.SET_NULL,
#     )

#     custodian = models.OneToOneField(
#         to=settings.AUTH_USER_MODEL,
#         limit_choices_to={
#             "is_staff": True,
#         },
#         verbose_name=_("custodian"),
#         related_name="custodian",
#         blank=True,
#         null=True,
#         on_delete=models.SET_NULL,
#     )

#     class Meta:
#         db_table = "global_config"
#         verbose_name = _("Configuration")

#     def __str__(self):
#         return force_str(_("Configuration"))

__all__ = [
    "Contributor",
    "Contribution",
    "Dataset",
    "Project",
    "Review",
    "Sample",
    "Location",
    # GlobalConfiguration,
]
