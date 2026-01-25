from typing import Any

from djoser.email import (
	ActivationEmail as BaseActivationEmail,
	ConfirmationEmail as BaseConfirmationEmail,
	PasswordResetEmail as BasePasswordResetEmail,
)

from .models import EmailLog
from .tasks import send_email_task


class ActivationEmail(BaseActivationEmail):
	def send(self, to, *args, **kwargs):
		raw_context = self.get_context_data()
		context = _extract_context(raw_context)
		
		email_log = EmailLog.objects.create(
			to=to[0], template="djoser/email/activation.html",
			subject="Account Activation",
			context=context,
		)

		send_email_task.delay(str(email_log.id))


class ConfirmationEmail(BaseConfirmationEmail):
	def send(self, to, *args, **kwargs):
		raw_context = self.get_context_data()
		context = _extract_context(raw_context)
		
		email_log = EmailLog.objects.create(
			to=to[0], template="djoser/email/confirmation.html",
			subject="Email Confirmed!", context=context,
		)

		send_email_task.delay(str(email_log.id))
	

class PasswordResetEmail(BasePasswordResetEmail):
	def send(self, to, *args, **kwargs):
		raw_context = self.get_context_data()
		context = _extract_context(raw_context)
		
		email_log = EmailLog.objects.create(
			to=to[0], template="djoser/email/password_reset.html",
			subject="Password Reset Request", context=context,
		)

		send_email_task.delay(str(email_log.id))
		
	
def _extract_context(raw_context:  dict[str, Any]) ->  dict[str, Any]:
	user = raw_context['user']
	return {
		"domain": raw_context["domain"],
		"protocol": raw_context["protocol"],
		"uid": raw_context["uid"],
		"token": raw_context["token"],
		"url": raw_context["url"],
		"user": {
			"username": user.username,
			"email": user.email,
		},
	}