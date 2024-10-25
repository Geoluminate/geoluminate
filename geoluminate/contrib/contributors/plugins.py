from geoluminate.contrib.datasets.views import DatasetPlugin
from geoluminate.contrib.projects.views import ProjectPlugin
from geoluminate.core.plugins import ActivityStream, Overview
from geoluminate.plugins import contributor


@contributor.page("overview")
class ContributorOverview(Overview):
    template_name = "contributors/contributor_overview.html"


# contributor.register_page(Overview)
contributor.register_page(ProjectPlugin)
contributor.register_page(DatasetPlugin)
contributor.register_page(ActivityStream)
