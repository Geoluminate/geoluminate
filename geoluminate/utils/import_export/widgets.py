# from controlled_vocabulary.models import ControlledVocabulary
# from import_export.widgets import ForeignKeyWidget, ManyToManyWidget


# class VocabularyWidget(ForeignKeyWidget):
#     def __init__(self, *args, **kwargs):
#         self.type = kwargs.pop("type")
#         super().__init__(ControlledVocabulary, "code", *args, **kwargs)

#     def get_queryset(self, value, row, *args, **kwargs):
#         return self.model.objects.filter(type=self.type)

#     def clean(self, value, row=None, *args, **kwargs):
#         if value:
#             value = value.lower()
#             try:
#                 return self.get_queryset(value, row, *args, **kwargs).get(**{self.field: value})
#             except self.model.DoesNotExist as exc:
#                 raise ValueError(
#                     f"'{value}' is not a valid option for this field. Available choices are"
#                     f" [{', '.join(list(self.get_queryset(value, row).values_list('code',flat=True)))}]"
#                 ) from exc
#         else:
#             return None


# class VocabularyM2MWidget(ManyToManyWidget):
#     def __init__(self, *args, **kwargs):
#         self.type = kwargs.pop("type")
#         kwargs.update(field="code")
#         super().__init__(ControlledVocabulary, *args, **kwargs)

#     def get_queryset(self, value, row, *args, **kwargs):
#         return self.model.objects.filter(type=self.type)
