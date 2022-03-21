from django import forms
from django.forms import CharField, ModelMultipleChoiceField, DateField
import datetime
from django.core.exceptions import ValidationError


class ListConcatField(CharField):

	def to_python(self, value):
		"""Return a string from a list."""
		if value not in self.empty_values:
			if isinstance(value, list):
				value = ''.join(value)
			value = str(value)
			if self.strip:
				value = value.strip()
		if value in self.empty_values:
			return self.empty_value
		return value

class CrossRefAuthorField(ModelMultipleChoiceField):

	def _check_values(self, value):
		"""
		Given a list of author dicts (as return by crossref), return a QuerySet of the corresponding objects. Values are queried on first, middle and family name. A new object will be created if not found in the database already.
		"""
		authors = []
		for author in value:
			create_from = {k:v for k,v in author.items() if k in [f.name for f in self.queryset.model._meta.fields]}
			try:
				obj, _ = self.queryset.get_or_create(**create_from)
			except (ValueError, TypeError):
				raise ValidationError(
                    self.error_messages['invalid_author'],
                    code='invalid_author',
                    params=author,
                )
			authors.append(obj.id)

		return self.queryset.filter(id__in=authors)


class DatePartsField(DateField):

	def to_python(self, value):	
		"""
		Validate that the input can be converted to a date. Return a Python
		datetime.date object.
		"""
		if value in self.empty_values:
			return None
		if isinstance(value, datetime.datetime):
			return value.date()
		if isinstance(value, datetime.date):
			return value
		if isinstance(value, dict):
			if 'date-parts' in value.keys():
				date_parts = value['date-parts'][0]
				while len(date_parts) < 3:
					date_parts.append(1)
				return datetime.date(*date_parts)
				# date_parts = {k: v for k,v in zip(['year','month','day'],value['date-parts'][0])}

		return super().to_python(value)

