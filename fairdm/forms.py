import datetime
import json

from client_side_image_cropping import ClientsideCroppingWidget
from django import forms
from partial_date import PartialDate


class ImageCroppingWidget(ClientsideCroppingWidget):
    def __init__(self, width: int, height: int, config, result, empty_text=None, *args, **kwargs):
        self.config = config
        self.result = result
        self.empty_text = empty_text
        super().__init__(width, height, width, height, *args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"].update(
            {
                "config": json.dumps(self.config),
                "result": json.dumps(self.result),
                "empty_text": self.empty_text,
            }
        )
        return context

    class Media:
        css = {
            "all": (
                "client_side_image_cropping/croppie.css",
                # "client_side_image_cropping/cropping_widget.css",
                # "cropping_widget/cropping.css",
            ),
        }
        js = (
            "client_side_image_cropping/croppie.min.js",
            # "cropping_widget/cropping.js",
            # "client_side_image_cropping/cropping_widget.js",
        )


class PartialDateWidget(forms.SelectDateWidget):
    def __init__(self, attrs=None, years=None, months=None, empty_label=None):
        super().__init__(attrs, years, months, empty_label)
        if not years:
            this_year = datetime.date.today().year
            self.years = list(range(1900, this_year + 1))
            self.years.reverse()

    def get_context(self, name, value, attrs):
        # reorder the subwidgets to year, month, day
        context = super().get_context(name, value, attrs)
        m, d, y = context["widget"]["subwidgets"]
        context["widget"]["subwidgets"] = [y, m, d]
        return context

    def format_value(self, value):
        # convert PartialDate to dict for SelectDateWidget
        if isinstance(value, PartialDate):
            return {
                "year": value.date.year,
                "month": value.date.month if value.precision >= PartialDate.MONTH else None,
                "day": value.date.day if value.precision == PartialDate.DAY else None,
            }
        return {"year": None, "month": None, "day": None}

    def value_from_datadict(self, data, files, name):
        # build a PartialDate from the separate fields

        y = data.get(self.year_field % name)
        m = data.get(self.month_field % name)
        d = data.get(self.day_field % name)
        if y == m == d == "":
            return None

        # build the date string
        value = y
        if m:
            value += f"-{m}"
        if m and d:
            value += f"-{d}"

        return value


class PartialDateFormField(forms.CharField):
    """A form field that provides separate fields for day, month, and year. Values from the separate fields are combined into a value suitable for a partial_date.PartialDateField."""

    widget = PartialDateWidget


class PartialDateField(forms.CharField):
    widget = forms.TextInput(attrs={"x-mask": "****-**-**", "placeholder": "yyyy-mm-dd"})

    def clean(self, value):
        if value:
            # Remove leading and trailing hyphens
            return value.strip("-")
        return None
