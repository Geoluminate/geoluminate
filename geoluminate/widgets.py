from django import forms
from quantityfield.fields import QuantityFormFieldMixin
from quantityfield.widgets import QuantityWidget


class QuantityFieldWidget(QuantityWidget):
    template_name = "forms/widgets/quantity_field.html"


class QuantityFormField(QuantityFormFieldMixin, forms.FloatField):
    to_number_type = float

    def __init__(self, *args, **kwargs):
        kwargs.update(
            widget=QuantityFieldWidget,
        )
        super().__init__(*args, **kwargs)
        self.widget = QuantityFieldWidget(base_units=self.base_units, allowed_types=self.units)
