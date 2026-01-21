import os
from celery import Celery

#set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GamifiedStressApp.settings")

app = Celery("GamifiedStressApp")

#namespace='CELERY' means all celery configuration keys should have a `CELERY_` prefix in settings.py.
app.config_from_object("django.conf:settings", namespace="CELERY")

#load task modules from all registered Django app configurations
app.autodiscover_tasks()