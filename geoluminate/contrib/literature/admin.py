from django.contrib import admin
from literature.admin import LiteratureAdmin
from literature.models import Literature

admin.site.unregister(Literature)


@admin.register(Literature)
class GeoLiteratureAdmin(LiteratureAdmin):
    class Media:
        css = {
            "all": (
                "https://cdn.datatables.net/v/bs4/jszip-2.5.0/dt-1.13.4/af-2.5.3/b-2.3.6/b-colvis-2.3.6/b-html5-2.3.6/b-print-2.3.6/cr-1.6.2/date-1.4.1/fc-4.2.2/fh-3.3.2/kt-2.9.0/r-2.4.1/rg-1.3.1/rr-1.3.3/sc-2.1.1/sb-1.4.2/sp-2.1.2/sl-1.6.2/sr-1.2.2/datatables.min.css",
            )
        }
