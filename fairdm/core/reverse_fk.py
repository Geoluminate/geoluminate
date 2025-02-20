import sys

from django.db import models


def create_reverse_fk_model(related_class, Description, related_name, meta, attrs):
    """
    Dynamically create the reverse foreign key related model.

    :param related_class: The model to which the related model should be linked via ForeignKey.
    :param related_name: The related name for the reverse FK from the related model.
    :param fields: Additional fields to add to the related model (in addition to the abstract model fields).

    A single field is enforced on the Description:
        - `master`: A ForeignKey back to the shared model.
    """

    if related_class._meta.abstract:
        raise TypeError(f"Can't create ReverseForeignKey model for abstract class {related_class.__name__}")

    # Define the inner Meta class
    meta = {
        "app_label": related_class._meta.app_label,
        "db_tablespace": related_class._meta.db_tablespace,
        "managed": related_class._meta.managed,
        "db_table": f"{related_class._meta.db_table}_{related_name}",
    }

    # Define fields for the reverse related model
    name = f"{related_class.__name__}{Description.__name__}"

    attrs = attrs or None
    attrs["Meta"] = type("Meta", (Description.Meta,), meta)
    attrs["__module__"] = related_class.__module__
    attrs["objects"] = models.Manager()

    # add the foreign key to the shared model
    attrs["related"] = models.ForeignKey(
        related_class,
        related_name=related_name,
        on_delete=models.CASCADE,
        editable=False,
        null=True,
    )

    # Dynamically create the model
    related_model = type(name, (Description,), attrs)

    # Register it as a global in the shared model's module.
    # This is needed so that Translation model instances, and objects which refer to them, can be properly pickled and unpickled.
    # The Django session and caching frameworks, in particular, depend on this behaviour.
    mod = sys.modules[related_class.__module__]
    setattr(mod, name, related_model)

    return related_model


class OneToManyField(models.Field):
    """
    A field that dynamically creates a related model based on an abstract model.
    """

    def __init__(self, to, meta=None, attrs=None, *args, **kwargs):
        self.to = to
        self.meta = meta
        self.attrs = attrs
        super().__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name, **kwargs):
        # Create the related model dynamically
        self.name = name
        self.related_model = create_reverse_fk_model(cls, self.to, self.name, self.meta, attrs=self.attrs)

        setattr(cls, f"{name}_model", self.related_model)
