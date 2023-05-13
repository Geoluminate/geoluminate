from django.db import models

# from django.urls import reverse
# from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from treebeard.mp_tree import MP_Node

# from invitations.base_invitation import AbstractBaseInvitation


class ControlledVocabulary(MP_Node):
    label = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    node_order_by = ["name"]

    class Meta:
        verbose_name = _("Controlled Vocabularies")
        verbose_name_plural = _("Controlled Vocabularies")

    def __str__(self):
        return f"{self.name}"
