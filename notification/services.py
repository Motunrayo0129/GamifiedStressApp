from django.db import transaction
from django.db.models import F
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.timezone import now
from django.core.mail import EmailMultiAlternatives

from .models import EmailLog


def send_email_once(*, email_log_id: str) -> str:
	with transaction.atomic():
		email_log = (
			EmailLog.objects.select_for_update().get(id=email_log_id)
		)
		if email_log.sent_at is not None:
			return "already sent"
		
		template = email_log.template
		context= email_log.context
		subject = email_log.subject
		recipient = email_log.to
		
	try:
		email_body_html = render_to_string(
			template_name=template, context=context
		)
		email_body_text = strip_tags(value=email_body_html)
		email = EmailMultiAlternatives(
			subject=subject, body=email_body_text, to=[recipient]
		)
		email.attach_alternative(email_body_html, "text/html")
		email.send()
	except Exception as e:
		EmailLog.objects.filter(id=email_log_id).update(
			send_attempts=F("send_attempts") + 1, last_error=str(e)
		)
		raise
		
	with transaction.atomic():
		EmailLog.objects.filter(id=email_log_id).update(
			sent_at=now(), send_attempts=F("send_attempts") + 1
		)
	
	return "sent"