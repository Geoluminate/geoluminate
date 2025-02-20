from django.forms import modelform_factory
from django_filters.filterset import filterset_factory
from django_tables2 import table_factory
from import_export.resources import ModelDeclarativeMetaclass, ModelResource

__all__ = [
    "filterset_factory",
    "modelform_factory",
    "modelresource_factory",
    "serializer_factory",
    "table_factory",
]


def modelresource_factory(model, resource_class=ModelResource, **kwargs):
    """
    Factory for creating ``ModelResource`` class for given Django model.
    """
    meta = type("Meta", (object,), {"model": model, **kwargs})
    metaclass = ModelDeclarativeMetaclass
    return metaclass(
        f"{model.__name__}Resource",
        (resource_class,),
        {
            "Meta": meta,
        },
    )


def serializer_factory(model, base_serializer, **kwargs):
    meta = type("Meta", (base_serializer.Meta,), {"model": model, **kwargs})
    return type(f"{model.__name__}Serializer", (base_serializer,), {"Meta": meta})
