from urllib.parse import quote

from django.contrib.gis.db.models import Extent
from django.urls import reverse
from django.utils.safestring import mark_safe
from literature.models import Literature


class Publication(Literature):
    def get_data(self, data_type=None):
        return {
            "intervals": self.intervals.all(),
            "temperature": self.temperature_logs.all(),
            "conductivity": self.conductivity_logs.all(),
        }

    def get_absolute_url(self):
        return reverse("literature:detail", kwargs={"pk": self.pk})

    def file_download(self):
        if self.file:
            return mark_safe(  # noqa: S308
                f'<a href="https://doi.org/{self.DOI}"><i class="fas fa-globe fa-lg"></i></a>'
            )
        else:
            return ""

    def keywords_escaped(self):
        return [(keyword.strip(), quote(keyword.strip())) for keyword in self.keywords.split(",")]

    def bbox(self):
        """Calculate and return a bounding box for sites in the
        given publication.

        Returns:
            array: the bounding box
        """
        return self.sites.aggregate(Extent("geom"))["geom__extent"]

    class Meta:
        proxy = True
