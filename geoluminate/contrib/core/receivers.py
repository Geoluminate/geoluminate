import logging

# import django signals and receivers
# from django.db.models import signals as django_signals
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_comments import signals
from literature.models import Literature

logger = logging.getLogger(__name__)


@receiver(signals.comment_was_posted)
def on_comment_posted(sender, comment, request, **kwargs):
    """
    Send email notification of a new comment to site staff when email notifications have been requested.
    """
    content_object = comment.content_object
    # logger.info("content_object", content_object)

    # get contributors that are subscribed to email notifications for this project

    print("content_object", content_object)


@receiver(post_save, sender=Literature)
def update_identifiers_for_new_literature(sender, instance, created, **kwargs):
    """
    Update identifier fields for new literature.
    """
    # update identifier fields
    print("update_identifiers_for_new_literature", instance, created, kwargs)

    # for field in IdentifierTypes.labels:
    #     if self.CSL.get(field):
    #         obj, new = Identifier.objects.get_or_create(
    #             ID=self.CSL.get(field), type=getattr(IdentifierTypes, field), literature=self
    #         )
    #         if new:
    #             print(f"Creating new {field}")
    #             obj.save()

    # if created:
    #     instance.update_identifiers()
