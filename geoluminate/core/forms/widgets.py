from django.forms.widgets import SelectMultiple, TextInput


class DynamicArrayWidget(TextInput):
    template_name = "forms/widgets/postgres_array_widget.html"

    class Media:
        js = ("js/django_better_admin_arrayfield.min.js",)
        css = {"all": ("css/django_better_admin_arrayfield.min.css",)}

    def __init__(self, *args, **kwargs):
        self.subwidget_form = kwargs.pop("subwidget_form", TextInput)
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context_value = value or [""]
        context = super().get_context(name, context_value, attrs)
        final_attrs = context["widget"]["attrs"]
        id_ = context["widget"]["attrs"].get("id")
        context["widget"]["is_none"] = value is None

        subwidgets = []
        for index, item in enumerate(context["widget"]["value"]):
            widget_attrs = final_attrs.copy()
            if id_:
                widget_attrs["id"] = f"{id_}_{index}"
            widget = self.subwidget_form()
            widget.is_required = self.is_required
            subwidgets.append(widget.get_context(name, item, widget_attrs)["widget"])

        context["widget"]["subwidgets"] = subwidgets
        return context

    def value_from_datadict(self, data, files, name):
        try:
            getter = data.getlist
            return [value for value in getter(name) if value]
        except AttributeError:
            return data.get(name)

    def value_omitted_from_data(self, data, files, name):
        return False

    def format_value(self, value):
        return value or []

    def clean_field(self):
        data = self.cleaned_data["field"]
        return data


class ArraySelect2Widget(SelectMultiple):
    template_name = "forms/widgets/array_select2.html"

    def __init__(self, *args, **kwargs):
        attrs = kwargs.pop("attrs", {})
        attrs.update({"data-tags": "true"})
        kwargs["attrs"] = attrs
        super().__init__(*args, **kwargs)

    # class Media:
    #     css = {
    #         "all": (
    #             "https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css",
    #             "https://cdn.jsdelivr.net/npm/select2-bootstrap-5-theme@1.3.0/dist/select2-bootstrap-5-theme.min.css",
    #         )
    #     }
    # js = (
    #     "ror/js/select2.min.js",
    # "admin/js/array_select2_tags.js",
    # )

    def value_from_datadict(self, data, files, name):
        try:
            getter = data.getlist
        except AttributeError:
            getter = data.get
        return getter(name)

    def value_omitted_from_data(self, data, files, name):
        # An unselected <select multiple> doesn't appear in POST data, so it's
        # never known if the value is actually omitted.
        return False
