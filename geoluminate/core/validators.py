import tldextract
from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class RangeValidator(BaseValidator):
    message = _("Ensure this value is within the range %(limit_value)s.")
    code = "range_value"

    def compare(self, a, b):
        min_is_valid = self.validate(a[0], b)
        max_is_valid = self.validate(a[1], b)

        return min_is_valid and max_is_valid

    def validate(self, a, b):
        val, allow_equals = self.parse_val(a)
        if allow_equals:
            return val <= b
        return val < b

    def parse_val(self, val):
        allow_equals = False
        try:
            float(val)
        except ValueError as exc:
            if val.startswith("="):
                val = float(val.strip("="))
                allow_equals = True
            else:
                raise ValueError('String values must only contain a prepended "=".') from exc
        return val, allow_equals


@deconstructible
class DomainValidator(BaseValidator):
    message = _("The provided domain is not allowed: %(limit_value)s.")
    code = "domain"

    def compare(self, a, b):
        a = tldextract.extract(a).domain
        return super().compare(a, b)
