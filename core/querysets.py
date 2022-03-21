from django.db.models.query import QuerySet
from io import StringIO
import csv

class QuerySetExtra(QuerySet):

    def explode(self, on='data', *args):
        if not args:
            args = self.export_field_names
        return self.prefetch_related(on).values(*args)

    def explode_values(self, on='data', *args):
        if not args:
            args = self.export_field_names
        return self.prefetch_related(on).values_list(*args)
    
    @property
    def export_field_names(self):
        return self.field_names+self.data_field_names

    @property
    def verbose_export_field_names(self):
        return self.verbose_field_names+self.data_verbose_field_names

    @property
    def data_fields(self):
        """Returns the fields of the related data model"""
        fields = self.model._meta.related_objects[0].related_model._meta.fields
        return [f for f in fields if f.name not in ['id','log']]

    @property
    def data_field_names(self):
        return [f"data__{f.name}" for f in self.data_fields] 

    @property
    def data_verbose_field_names(self):
        return [f.verbose_name for f in self.data_fields] 

    @property
    def model_fields(self):
        fields = self.model._meta.fields
        return [f for f in fields if f.name not in ['added']]

    @property
    def field_names(self):
        return [f.name for f in self.model_fields] 

    @property
    def verbose_field_names(self):
        return [f.verbose_name for f in self.model_fields] 

    def to_csv(self):
        writer = csv.writer()

        # write the header row;
        writer.writerow(self.verbose_export_field_names)

        # write the rows to the csv file
        for i in self:
            writer.writerow(i)

        return writer

    def to_csv_buffer(self):

        csv_buffer = StringIO()
        writer = csv.writer(csv_buffer)

        # write the header row;
        writer.writerow(self.verbose_export_field_names)

        # write the rows to the csv file
        for i in self:
            writer.writerow(i)

        return csv_buffer.getvalue()