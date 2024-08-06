from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ReviewsConfig(AppConfig):
    name = "geoluminate.contrib.reviews"
    label = "reviews"
    verbose_name = _("Reviews")

    def ready(self):
        from actstream import registry

        registry.register(self.get_model("Review"))
        return super().ready()
