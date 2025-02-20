from import_export import fields
from import_export.resources import ModelResource
from import_export.widgets import ForeignKeyWidget

from fairdm.core.models import Sample


class BaseFairDMResource(ModelResource):
    """Shared base class for Sample and Measurement resources."""

    def __init__(self, dataset, *args, **kwargs):
        # always require that the dataset is passed in to the model resource so that we can attribute
        # uploaded data to the current dataset
        self.dataset = dataset
        super().__init__(*args, **kwargs)

    def for_delete(self, row, instance):
        return row.get("delete") == "1"

    def before_import_row(self, row, **kwargs):
        row["dataset"] = self.dataset.pk
        return super().before_import_row(row, **kwargs)

    def get_import_order(self):
        return [*super().get_import_order(), "dataset", "sample"]

    def get_export_order(self):
        # Exclude 'field_to_exclude' from export but keep it for import
        fields = list(super().get_export_order())  # Get all fields
        if "dataset" in fields:
            fields.remove("dataset")  # Remove the field you don't want to export
        return fields

    def _get_ordered_field_names(self, order_field):
        fields = list(super()._get_ordered_field_names(order_field))
        if "id" not in fields:
            fields = ["id", *fields]
        if "dataset" not in fields:
            fields = ["dataset", *fields]

        return fields


class SampleResource(BaseFairDMResource):
    class Meta:
        fields = (
            "dataset",
            "id",
            "local_id",
            "name",
            "char_field",
        )

    def get_instance(self, instance_loader, row):
        dataset_id = row.get("dataset")
        obj_id = row.get("id")
        local_id = row.get("local_id")

        if obj_id:
            return self.model.objects.filter(id=obj_id).first()
        elif local_id and dataset_id:
            return self.model.objects.filter(local_id=local_id, dataset_id=dataset_id).first()

        return None  # No existing instance found


class SampleWidget(ForeignKeyWidget):
    def __init__(self, model=None, **kwargs):
        super().__init__(model=model or Sample, **kwargs)

    def clean(self, value, row=None, *args, **kwargs):
        # if the value looks like a shortuuid and startswith "s"
        # e.g. snu96wFe33UFqnYBFnZDbUn
        if value and value.startswith("s") and len(value) == 23:
            return self.model.objects.filter(pk=value).first()

        elif value:
            return self.model.objects.filter(name=value, dataset=row["dataset"]).first()
        return None


class MeasurementResource(BaseFairDMResource):
    sample = fields.Field(attribute="sample", column_name="sample", widget=SampleWidget())

    # class Meta:
    #     # class Meta:
    #     fields = ("dataset", "id", "local_id", "name", "char_field", "sample")

    def get_instance(self, instance_loader, row):
        dataset = row.get("dataset")
        obj_id = row.get("id")
        name = row.get("name")
        sample = row.get("sample")

        if obj_id:
            return self._meta.model.objects.filter(id=obj_id).first()

        elif name and dataset:
            # check for an object with the provided name within the dataset
            # if it exists, update it
            # if multiple objects exist in the dataset with the same name, an error will be raised
            # NOTE: I think we will have to add sample here as well.
            obj = self._meta.model.objects.get(name=name, dataset=dataset)
            if obj:
                # because id is blank, the default behavior would assign a new random id to the object which would create a new instance. As we want to update the instance we found, we prevent this by removing the id field from the row.
                del row["id"]
                return obj
        return None  # No existing instance found
