from geoluminate.contrib.contributors.views import ContributorsPlugin
from geoluminate.contrib.datasets.views import DatasetPlugin
from geoluminate.core.plugins import ActivityStream, Discussion, Overview
from geoluminate.plugins import project

project.register_page(Overview)
project.register_page(ContributorsPlugin)
project.register_page(DatasetPlugin)
project.register_page(Discussion)
project.register_page(ActivityStream)


# @project.action("flag", icon="fas fa-flag")
# @project.action("download", icon="fas fa-file-zipper")
# class XMLDownload(ProjectDetailView):
#     pass
