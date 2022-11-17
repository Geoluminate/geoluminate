import django_filters as df
from .select2.widgets import (
    ModelFieldSelect2MultiWidget,
    ModelFieldSelect2Widget
)
from django.utils.translation import gettext as _
from django_filters import rest_framework as df
from crispy_forms.helper import FormHelper
from crispy_bootstrap5.bootstrap5 import FloatingField, BS5Accordion
from crispy_forms.layout import Layout, ButtonHolder, Row, Column, Button, Div
from crispy_forms.bootstrap import AccordionGroup
from geoluminate.utils import DATABASE


class MapFilter(df.FilterSet):
    name = df.CharFilter(lookup_expr='icontains', label='Site Name')
    lat_gt = df.NumberFilter(
        field_name='lat',
        lookup_expr='gt',
        label='Latitude')
    lat_lt = df.NumberFilter(
        field_name='lat',
        lookup_expr='lt',
        label='Latitude')
    lng_gt = df.NumberFilter(
        field_name='lng',
        lookup_expr='gt',
        label='Longitude')
    lng_lt = df.NumberFilter(
        field_name='lng',
        lookup_expr='lt',
        label='Longitude')
    elevation_gt = df.NumberFilter(
        field_name='elevation',
        lookup_expr='gt',
        label='Elevation (m)')
    elevation_lt = df.NumberFilter(
        field_name='elevation',
        lookup_expr='lt',
        label='Elevation (m)')

    class Meta:
        model = DATABASE
        fields = ["name", 'id']

    helper = FormHelper()
    helper.form_method = 'GET'
    helper.form_id = 'map-filter-form'
    helper.layout = Layout(
        BS5Accordion(
            AccordionGroup('Geographic',
                           FloatingField('name', placeholder='Site name'),
                           Row(
                               Div(FloatingField('lat_lt'), css_class='w-50'),
                               css_class='justify-content-center'
                           ),
                           Row(
                               Column(FloatingField('lng_gt')),
                               Column(FloatingField('lng_lt')),
                           ),
                           Row(
                               Div(FloatingField('lat_gt'), css_class='w-50'),
                               css_class='justify-content-center'
                           ),

                           Row(
                               Column(FloatingField('elevation_gt')),
                               Column(FloatingField('elevation_lt')),
                               css_class='justify-content-center'
                           ),
                           ),
            AccordionGroup('Geology',
                           FloatingField('plate'),
                           FloatingField('crust_type'),
                           ),
            flush=True,
        ),
        ButtonHolder(
            Button(
                'button',
                'Search',
                onclick='updateMap()',
                css_class='button solid large'),
        )
    )


class Select2ChoiceFilterBase:

    def __init__(self, model, field, *args, **kwargs):
        super().__init__(
            queryset=model.objects.filter(
                **{f'{field}__isnull': False}),
            to_field_name=field,
            widget=self.widget(
                search_fields=[
                    f"{field}__{kwargs.pop('select2_lookup_expr','icontains')}", ]
            ), *args, **kwargs)


class Select2ChoiceFilter(
        Select2ChoiceFilterBase, df.ModelChoiceFilter):
    """A subclass of `django_filters.ModelChoiceFilter` that supports
    Select2 querying of possible values."""
    widget = ModelFieldSelect2Widget


class Select2MultipleChoiceFilter(
        Select2ChoiceFilterBase, df.ModelMultipleChoiceFilter):
    """Same as `Select2ChoiceFilter` but allows selection of multiple values"""
    widget = ModelFieldSelect2MultiWidget
