from partial_date import PartialDateField as BasePartialDateField

from geoluminate.forms import PartialDateFormField


class PartialDateField(BasePartialDateField):
    def formfield(self, **kwargs):
        # Specify the form field to use for this model field
        defaults = {"form_class": PartialDateFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)
