# import tzinfo from datetime

import factory
from django.contrib.gis.geos import Point
from faker.providers import BaseProvider

from geoluminate.contrib.controlled_vocabulary.models import ControlledVocabulary

# ALL_FIELDS = "__all__"


class VocabularyIterator(factory.Iterator):
    def __init__(self, label, *args, **kwargs):
        iterator = ControlledVocabulary.objects.get(label=label).get_descendants()
        super().__init__(iterator, *args, **kwargs)


class GeoDjangoPointProvider(BaseProvider):
    def geo_point(self, **kwargs):
        faker = factory.faker.faker.Faker()
        coords = faker.latlng(**kwargs)
        return Point(x=float(coords[1]), y=float(coords[0]), srid=4326)


factory.Faker.add_provider(GeoDjangoPointProvider)


# class AutoFactory(factory.django.DjangoModelFactory):
#     serializer_field_mapping = {
#         # models.AutoField: IntegerField,
#         models.BigIntegerField: "pyint",
#         models.BooleanField: "pybool",
#         models.CharField: "pystr",
#         # models.CommaSeparatedIntegerField: CharField,
#         # models.DateField: DateField,
#         # models.DateTimeField: DateTimeField,
#         models.DecimalField: "pydecimal",
#         # models.DurationField: DurationField,
#         # models.EmailField: factory.LazyAttribute(lambda o: f"{o.first_name}.{o.last_name}@fakeuser.org"),
#         # models.Field: ModelField,
#         models.FileField: FileField,
#         models.FloatField: "pyfloat",
#         models.ImageField: ImageField,
#         models.IntegerField: "pyint",
#         # models.NullBooleanField: BooleanField,
#         models.PositiveIntegerField: "pyint",
#         models.PositiveSmallIntegerField: "pyint",
#         # models.SlugField: SlugField,
#         # models.SmallIntegerField: IntegerField,
#         models.TextField: "text",
#         # models.TimeField: TimeField,
#         # models.URLField: URLField,
#         # models.UUIDField: UUIDField,
#         # models.GenericIPAddressField: IPAddressField,
#         # models.FilePathField: FilePathField,
#     }

#     class Meta:
#         abstract = True

#     def __init__(self, model, fields) -> None:
#         self.Meta.model = model
#         if fields == "__all__":
#             self.fields = model._meta.fields
#         else:
#             self.fields = [model._meta.get_field(f) for f in fields]

#     def get_fields(self):
#         """
#         Return the dict of field names -> field instances that should be
#         used for `self.fields` when instantiating the serializer.
#         """
#         if self.url_field_name is None:
#             self.url_field_name = api_settings.URL_FIELD_NAME

#         assert hasattr(self, 'Meta'), (
#             'Class {serializer_class} missing "Meta" attribute'.format(
#                 serializer_class=self.__class__.__name__
#             )
#         )
#         assert hasattr(self.Meta, 'model'), (
#             'Class {serializer_class} missing "Meta.model" attribute'.format(
#                 serializer_class=self.__class__.__name__
#             )
#         )
#         if model_meta.is_abstract_model(self.Meta.model):
#             raise ValueError(
#                 'Cannot use ModelSerializer with Abstract Models.'
#             )

#         declared_fields = copy.deepcopy(self._declared_fields)
#         model = getattr(self.Meta, 'model')
#         depth = getattr(self.Meta, 'depth', 0)

#         if depth is not None:
#             assert depth >= 0, "'depth' may not be negative."
#             assert depth <= 10, "'depth' may not be greater than 10."

#         # Retrieve metadata about fields & relationships on the model class.
#         info = model_meta.get_field_info(model)
#         field_names = self.get_field_names(declared_fields, info)

#         # Determine any extra field arguments and hidden fields that
#         # should be included
#         extra_kwargs = self.get_extra_kwargs()
#         extra_kwargs, hidden_fields = self.get_uniqueness_extra_kwargs(
#             field_names, declared_fields, extra_kwargs
#         )

#         # Determine the fields that should be included on the serializer.
#         fields = OrderedDict()

#         for field_name in field_names:
#             # If the field is explicitly declared on the class then use that.
#             if field_name in declared_fields:
#                 fields[field_name] = declared_fields[field_name]
#                 continue

#             extra_field_kwargs = extra_kwargs.get(field_name, {})
#             source = extra_field_kwargs.get('source', '*')
#             if source == '*':
#                 source = field_name

#             # Determine the serializer field class and keyword arguments.
#             field_class, field_kwargs = self.build_field(
#                 source, info, model, depth
#             )

#             # Include any kwargs defined in `Meta.extra_kwargs`
#             field_kwargs = self.include_extra_kwargs(
#                 field_kwargs, extra_field_kwargs
#             )

#             # Create the serializer field.
#             fields[field_name] = field_class(**field_kwargs)

#         # Add in any hidden fields.
#         fields.update(hidden_fields)

#         return fields

#     def get_field_names(self, declared_fields, info):
#         """
#         Returns the list of all field names that should be created when
#         instantiating this serializer class. This is based on the default
#         set of fields, but also takes into account the `Meta.fields` or
#         `Meta.exclude` options if they have been specified.
#         """
#         fields = getattr(self.Meta, 'fields', None)
#         exclude = getattr(self.Meta, 'exclude', None)

#         if fields and fields != ALL_FIELDS and not isinstance(fields, (list, tuple)):
#             raise TypeError(
#                 'The `fields` option must be a list or tuple or "__all__". '
#                 'Got %s.' % type(fields).__name__
#             )

#         if exclude and not isinstance(exclude, (list, tuple)):
#             raise TypeError(
#                 'The `exclude` option must be a list or tuple. Got %s.' %
#                 type(exclude).__name__
#             )

#         assert not (fields and exclude), (
#             "Cannot set both 'fields' and 'exclude' options on "
#             "serializer {serializer_class}.".format(
#                 serializer_class=self.__class__.__name__
#             )
#         )

#         assert not (fields is None and exclude is None), (
#             "Creating a ModelSerializer without either the 'fields' attribute "
#             "or the 'exclude' attribute has been deprecated since 3.3.0, "
#             "and is now disallowed. Add an explicit fields = '__all__' to the "
#             "{serializer_class} serializer.".format(
#                 serializer_class=self.__class__.__name__
#             ),
#         )

#         if fields == ALL_FIELDS:
#             fields = None

#         if fields is not None:
#             # Ensure that all declared fields have also been included in the
#             # `Meta.fields` option.

#             # Do not require any fields that are declared in a parent class,
#             # in order to allow serializer subclasses to only include
#             # a subset of fields.
#             required_field_names = set(declared_fields)
#             for cls in self.__class__.__bases__:
#                 required_field_names -= set(getattr(cls, '_declared_fields', []))

#             for field_name in required_field_names:
#                 assert field_name in fields, (
#                     "The field '{field_name}' was declared on serializer "
#                     "{serializer_class}, but has not been included in the "
#                     "'fields' option.".format(
#                         field_name=field_name,
#                         serializer_class=self.__class__.__name__
#                     )
#                 )
#             return fields

#         # Use the default set of field names if `Meta.fields` is not specified.
#         fields = self.get_default_field_names(declared_fields, info)

#         if exclude is not None:
#             # If `Meta.exclude` is included, then remove those fields.
#             for field_name in exclude:
#                 assert field_name not in self._declared_fields, (
#                     "Cannot both declare the field '{field_name}' and include "
#                     "it in the {serializer_class} 'exclude' option. Remove the "
#                     "field or, if inherited from a parent serializer, disable "
#                     "with `{field_name} = None`."
#                     .format(
#                         field_name=field_name,
#                         serializer_class=self.__class__.__name__
#                     )
#                 )

#                 assert field_name in fields, (
#                     "The field '{field_name}' was included on serializer "
#                     "{serializer_class} in the 'exclude' option, but does "
#                     "not match any model field.".format(
#                         field_name=field_name,
#                         serializer_class=self.__class__.__name__
#                     )
#                 )
#                 fields.remove(field_name)

#         return fields

#     def get_default_field_names(self, declared_fields, model_info):
#         """
#         Return the default list of field names that will be used if the
#         `Meta.fields` option is not specified.
#         """
#         return (
#             [model_info.pk.name] +
#             list(declared_fields) +
#             list(model_info.fields) +
#             list(model_info.forward_relations)
#         )
