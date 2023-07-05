from django.db.models import ForeignKey


class SiteField(ForeignKey):
    def __init__(self, *args, **kwargs):
        kwargs["to"] = "ggis.Site"
        super().__init__(*args, **kwargs)
