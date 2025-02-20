from contextlib import suppress

from django.apps import apps
from django.contrib import admin


class FairDMRegistry:
    """
    A registry to manage and retrieve all model classes that subclass fairdm.core.models.sample.Sample and fairdm.core.models.measurement.Measurement along with associated metadata.

    This class allows models to be registered with associated metadata and categorized
    by type. It provides methods for retrieving models based on their app label and
    model name, as well as properties to filter registered models by type.
    """

    def __init__(self):
        self._registry = {}
        self.all = []

    def get(self, app_label=None, model_name=None):
        """
        Retrieves models from the registry based on the provided app label and/or model name.

        Args:
            app_label (str, optional): The app label of the models to retrieve.
            model_name (str, optional): The model name of the models to retrieve.

        Returns:
            list[dict]: A list of matching models, each represented as a dictionary.
        """
        return [
            item
            for item in self.all
            if (app_label is None or item["app_label"] == app_label)
            and (model_name is None or item["model"] == model_name)
        ]

    @property
    def samples(self):
        """
        Retrieves all registered models categorized as 'sample'.

        Returns:
            list[dict]: A list of models with type 'sample'.
        """
        return [item for item in self.all if item["type"] == "sample"]

    @property
    def measurements(self):
        """
        Retrieves all registered models categorized as 'measurement'.

        Returns:
            list[dict]: A list of models with type 'measurement'.
        """
        return [item for item in self.all if item["type"] == "measurement"]

    def register(self, model_class, config=None):
        """
        Registers a model class in the registry with associated metadata.

        Args:
            model_class (django.db.models.Model): The Django model class to register.
            mtype (str, optional): A classification type for the model (e.g., 'sample', 'measurement').

        The registered model metadata includes:
        - `app_label`: The app label of the model.
        - `model`: The model name.
        - `class`: The model class itself.
        - `verbose_name`: The human-readable name of the model.
        - `verbose_name_plural`: The plural version of the verbose name.
        - `type`: The classification type of the model (if provided).
        """

        # config = self.get_config(model_class, config)
        self.register_actstream(model_class)
        self.register_admin(model_class)
        mtype = getattr(model_class, "base_class", None)
        if mtype is not None:
            mtype = mtype().__name__.lower()
        item = {
            "app_label": model_class._meta.app_label,
            "model": model_class._meta.model_name,
            "full_name": f"{model_class._meta.app_label}.{model_class._meta.model_name}",
            "class": model_class,
            "path": f"{model_class.__module__}.{model_class.__name__}",
            "verbose_name": model_class._meta.verbose_name,
            "verbose_name_plural": model_class._meta.verbose_name_plural,
            "config": config(model_class),
            # "metadata": model_class._fairdm.meta,
            "type": mtype,
        }
        self._registry[model_class] = item
        self.all.append(item)

    def register_actstream(self, model_class):
        from actstream import registry as actstream_registry

        actstream_registry.register(model_class)

    def register_admin(self, model_class):
        from .admin import SampleAdmin

        with suppress(admin.sites.AlreadyRegistered):
            admin.site.register(model_class, SampleAdmin)

    def get_model(self, model_cls):
        """Retrieve the registered config class for a model."""
        if isinstance(model_cls, str):
            model_cls = apps.get_model(*model_cls.split("."))
        return self._registry.get(model_cls)

    def get_config(self, model_class, config):
        """
        Builds a configuration instance from the registered config class.
        """
        if config is None:
            config = getattr(model_class, "_fairdm", None)
        return config


# Global registry instance
registry = FairDMRegistry()


def register(model_class, **kwargs):
    def _register(config):
        registry.register(model_class, config, **kwargs)
        return config

    return _register
