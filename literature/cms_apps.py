from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


# @apphook_pool.register
class LiteratureApphook(CMSApp):
    app_name = "cms_literature"  # must match the application namespace
    name = "Literature"

    def get_urls(self, page=None, language=None, **kwargs):
        # replace this with the path to your application's URLs module
        return ["literature.urls"]
