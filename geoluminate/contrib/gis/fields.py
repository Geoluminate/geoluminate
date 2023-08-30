from django.db.models import ForeignKey


class SiteField(ForeignKey):
    def __init__(self, *args, **kwargs):
        kwargs["to"] = "project.Site"
        super().__init__(*args, **kwargs)
