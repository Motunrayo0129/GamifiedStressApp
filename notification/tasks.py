from celery import shared_task


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=60, retry_kwargs={"max_retries": 3})
def send_email_task(self, email_log_id):
    from .services import send_email_once
    return send_email_once(email_log_id=email_log_id)