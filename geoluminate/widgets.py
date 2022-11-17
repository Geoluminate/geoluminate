from multiprocessing.sharedctypes import Value
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from django.utils.translation import ugettext as _
from database.models import Choice


class ChoiceForeignKey(ForeignKeyWidget):

    def __init__(self, *args, **kwargs):
        self.type = kwargs.pop('type')
        super().__init__(Choice, 'code', *args, **kwargs)

    def get_queryset(self, value, row, *args, **kwargs):
        return self.model.objects.filter(type=self.type)

    def clean(self, value, row=None, *args, **kwargs):
        if value:
            value = value.lower()
            try:
                return self.get_queryset(
                    value, row, *args, **kwargs).get(**{self.field: value})
            except self.model.DoesNotExist:
                raise ValueError(
                    f"'{value}' is not a valid option for this field. Available choices are [{', '.join([v for v in self.get_queryset(value, row).values_list('code',flat=True)])}]")
        else:
            return None


class ChoiceManyToMany(ManyToManyWidget):

    def __init__(self, *args, **kwargs):
        self.type = kwargs.pop('type')
        super().__init__(Choice, field='code', *args, **kwargs)

    def get_queryset(self, value, row, *args, **kwargs):
        return self.model.objects.filter(type=self.type)
