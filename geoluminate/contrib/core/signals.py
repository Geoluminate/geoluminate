import logging

from django.dispatch import receiver
from django_comments import signals

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
