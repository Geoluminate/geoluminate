from django.utils.decorators import classonlymethod
from polymorphic.showfields import ShowFieldType

from geoluminate.core.utils import get_inheritance_chain, get_subclasses


class PolymorphicMixin(ShowFieldType):
    # steplen = 5
    # alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"  # 62 characters
    # node_order_by = ["created"]

    @classonlymethod
    def get_subclasses(cls):
        return get_subclasses(cls)

    @classonlymethod
    def get_polymorphic_choices(cls, include_self=False, pluralize_labels=False):
        label = lambda x: x.verbose_name_plural if pluralize_labels else x.verbose_name
        choices = []
        if include_self:
            opts = cls._meta
            choices.append((f"{opts.app_label}.{opts.model_name}", label(opts)))
        for subclass in cls.get_subclasses():
            opts = subclass._meta
            choices.append((f"{opts.app_label}.{opts.model_name}", label(opts)))
        return choices

    def get_type(self):
        return {
            "class": self.__class__.__name__,
            "app_label": self._meta.app_label,
            "model_name": self._meta.model_name,
            "verbose_name": self._meta.verbose_name,
            "verbose_name_plural": self._meta.verbose_name_plural,
        }

    @classmethod
    def get_metadata(cls):
        metadata = {}

        # for k in inheritance:
        # if cls._metadata is not None:
        # metadata.update(**cls._metadata.as_dict())
        metadata.update(**cls.Config.metadata.as_dict())

        inheritance = [
            k.get_metadata() for k in cls.mro()[:0:-1] if issubclass(k, cls.base_class()) and k != cls.base_class()
        ]

        metadata.update(
            name=cls._meta.verbose_name,
            name_plural=cls._meta.verbose_name_plural,
            inheritance=inheritance,
        )

        return metadata

    @classonlymethod
    def get_inheritance_chain(cls):
        return get_inheritance_chain(cls, cls.base_class())
