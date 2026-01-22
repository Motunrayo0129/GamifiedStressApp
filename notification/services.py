from django.db import transaction
from django.utils.timezone import now
from django.core.mail import send_mail

from .models import EmailLog


def send_email_once(*, email_log_id: str) -> str:
    with transaction.atomic():
        email_log = (
            EmailLog.objects.select_for_update().get(id=email_log_id)
        )

        if email_log.sent_at is not None:
            return "already_sent"

        send_mail(
            subject=email_log.subject, message=email_log.body,
            from_email=None, recipient_list=[email_log.to],
            fail_silently=False,
        )

        email_log.sent_at = now()
        email_log.save(update_fields=["sent_at"])

    return "sent"