from django.contrib.gis.db.models import Extent
from django.urls import reverse
from literature.models import Literature


class Publication(Literature):
    def get_absolute_url(self):
        return reverse("literature:detail", kwargs={"pk": self.pk})

    def bbox(self):
        """Calculate and return a bounding box for sites in the
        given publication.

        Returns:
            array: the bounding box
        """
        return self.sites.aggregate(Extent("geom"))["geom__extent"]

    class Meta:
        proxy = True
