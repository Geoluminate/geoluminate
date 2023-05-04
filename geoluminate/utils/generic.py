def choices_from_qs(qs, field):
    return [(k, k) for k in (qs.order_by(field).values_list(field, flat=True).distinct())]


def get_choices(model, field):
    def func():
        return [(k, k) for k in (model.objects.order_by(field).values_list(field, flat=True).distinct())]

    return func
