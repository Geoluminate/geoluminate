class FieldSetMixin:
    """Tries to imitate the functionality of viewsets in the django admin."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["fieldset"] = self.get_fieldset()
        return context

    def get_fieldset(self):
        obj = self.get_object()
        fieldset = {}
        for fset in self.fieldset:
            fieldset[fset[0]] = []
            for k in fset[1]["fields"]:
                if isinstance(k, str):
                    fieldset[fset[0]].append({obj._meta.get_field(k).verbose_name: getattr(obj, k)})
                else:
                    fieldset[fset[0]].append(
                        {obj._meta.get_field(sub_k).verbose_name: getattr(obj, sub_k) for sub_k in k}
                    )

        return fieldset
