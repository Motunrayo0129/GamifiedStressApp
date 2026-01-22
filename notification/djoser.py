from djoser.email import (
	ActivationEmail as BaseActivationEmail,
	ConfirmationEmail as BaseConfirmationEmail,
	PasswordResetEmail as BasePasswordResetEmail,
)

from .models import EmailLog
from .tasks import send_email_task


class ActivationEmail(BaseActivationEmail):
	def send(self, to, *args, **kwargs):
		context = self.get_context_data()
		email_log = EmailLog.objects.create(
			to=to[0],
			template="activation",
			subject=self.subject,
			body=self.render(),
			body_html=self.render(),
		)

		send_email_task.delay(str(email_log.id))


class ConfirmationEmail(BaseConfirmationEmail):
	def send(self, to, *args, **kwargs):
		context = self.get_context_data()

		email_log = EmailLog.objects.create(
			to=to[0],
			template="confirmation",
			subject=self.subject,
			body=self.render(),
			body_html=self.render(),
		)

		send_email_task.delay(str(email_log.id))
	

class PasswordResetEmail(BasePasswordResetEmail):
	def send(self, to, *args, **kwargs):
		context = self.get_context_data()

		email_log = EmailLog.objects.create(
			to=to[0],
			template="password_reset",
			subject=self.subject,
			body=self.render(),
			body_html=self.render(),
		)

		send_email_task.delay(str(email_log.id))