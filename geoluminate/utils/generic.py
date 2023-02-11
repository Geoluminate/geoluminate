from django.apps import apps
from django.utils.translation import gettext_lazy as _


def choices_from_qs(qs, field):
    return [
        (k, k) for k in (qs.order_by(field).values_list(field, flat=True).distinct())
    ]


def get_choices(model, field):
    def func():
        return [
            (k, k)
            for k in (
                model.objects.order_by(field).values_list(field, flat=True).distinct()
            )
        ]

    return func


def get_form_class(forms, form_id, default_form):
    form_class = forms.get(form_id, default_form)
    if isinstance(form_class, str):
        form_class = import_attribute(form_class)
    return form_class
