from time import sleep
from django.core.mail import send_mail
from celery import shared_task

# EXAMPLE ONLY - DOES NOTHING


@shared_task()
def send_feedback_email_task(email_address, message):
    """Sends an email when the feedback form has been submitted."""
    sleep(20)  # Simulate expensive operation(s) that freeze Django
    send_mail(
        "Your Feedback",
        f"\t{message}\n\nThank you!",
        "support@example.com",
        [email_address],
        fail_silently=False,
    )


def dump_database():
    """Dumps the entire database to a storage location.

    Raises:
        NotImplementedError: _description_
    """
    raise NotImplementedError
