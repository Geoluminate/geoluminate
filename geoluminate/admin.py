from django.apps import apps
from django.contrib import admin

from geoluminate.contrib.measurements.models import Measurement
from geoluminate.contrib.samples.models import Sample

# from geoluminate.contrib.measurements.admin import MeasurementAdmin
# from geoluminate.contrib.samples.admin import SampleAdmin


class GeoluminateAdminSite(admin.AdminSite):
    site_header = "Geoluminate Admin"
    site_title = "Geoluminate"

    def get_app_list(self, request):
        app_list = super().get_app_list(request)

        sample_models = self.find_subclass_of(app_list, Sample)
        measurement_models = self.find_subclass_of(app_list, Measurement)
        app_list.append(
            {
                "name": "Sample Types",
                "app_label": "samples",
                "models": sample_models,
            }
        )
        app_list.append(
            {
                "name": "Measurements",
                "app_label": "measurements",
                "models": measurement_models,
            }
        )

        app_list = sorted(app_list, key=lambda x: x["name"])

        return app_list

    def find_subclass_of(self, app_list, base_model):
        found = []
        for app in app_list:
            models_to_append = []
            for model in app["models"]:
                model_class = apps.get_model(app["app_label"], model["object_name"])
                if issubclass(model_class, base_model):
                    models_to_append.append(model)
            for model in models_to_append:
                app["models"].remove(model)

            if not app["models"]:
                app_list.remove(app)

            found.extend(models_to_append)

        return found


# admin.site.unregister(Action)
# admin.site.unregister(Follow)

# __all__ = ["MeasurementAdmin", "SampleAdmin", "GeoluminateAdminSite"]
#
