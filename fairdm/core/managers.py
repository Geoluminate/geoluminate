from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from polymorphic import managers


class PolymorphicManager(managers.PolymorphicManager):
    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     qs.
    #     if self.model._meta.proxy:
    #         qs = qs.instance_of(self.model)
    #     return qs

    def get_type_counts(self):
        """Returns a dictionary with counts of each polymorphic child type in the queryset."""
        type_counts = self.get_queryset().values("polymorphic_ctype").annotate(count=Count("id")).order_by()

        # Get all unique ContentType IDs
        content_type_ids = [entry["polymorphic_ctype"] for entry in type_counts]

        # Fetch all related ContentType objects in a single query
        content_types = ContentType.objects.filter(id__in=content_type_ids).in_bulk()

        # Build a mapping {content_type_id: model_class}
        content_type_map = {ct_id: content_types[ct_id].model_class() for ct_id in content_type_ids}

        # Replace content type IDs with actual model classes
        return {content_type_map[entry["polymorphic_ctype"]]: entry["count"] for entry in type_counts}
