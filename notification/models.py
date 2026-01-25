import uuid
from django.db import models

# Create your models here.
class EmailLog(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	to = models.EmailField()
	template = models.CharField(max_length=255)
	subject = models.CharField(max_length=100)
	context = models.JSONField(default=dict)

	sent_at = models.DateTimeField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
 
	send_attempts = models.PositiveIntegerField(default=0)
	last_error = models.TextField(blank=True)

	class Meta:
		indexes = [
            models.Index(fields=["to", "template"]),
        ]