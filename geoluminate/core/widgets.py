from django_select2 import forms


class ModelFieldSelect2Base:
    def __init__(self, *args, **kwargs):
        kwargs.update(
            {
                "attrs": {
                    "data-minimum-input-length": 0,
                    "data-minimum-results-or-search": 0,
                },
                "data_view": "geoluminate_select2",
            }
        )
        # super().__init__(data_view="geoluminate_select2", *args, **kwargs)
        super().__init__(*args, **kwargs)


class ModelFieldSelect2Widget(ModelFieldSelect2Base, forms.ModelSelect2Widget):
    """An extension of  `django_select2.forms.ModelSelect2Widget` that
    allows searching of distinct values in a model field for use in
    a standard choice select. Data view is hard coded to a view that
    returns the field value as both the text and id value in the
    JSONResponse.
    """


class ModelFieldSelect2MultiWidget(ModelFieldSelect2Base, forms.ModelSelect2MultipleWidget):
    """An extension of `django_select2.forms.ModelSelect2MultipleWidget`  that allows searching of distinct values in a model field for use in
    a standard choice select. Data view is hard coded to a view that
    returns the field value as both the text and id value in the
    JSONResponse.
    """
