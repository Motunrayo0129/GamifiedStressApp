from django.contrib import admin

from .models import EmailLog

# Register your models here.
@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ["to", "template", "sent_at", "created_at"]
    list_per_page = 10
    list_filter = ["template", "sent_at", "created_at"]
    ordering = ["-created_at"]
    search_fields = ["to", "template", "subject"]
    readonly_fields = ["id", "created_at", "sent_at", "send_attempts", "last_error", "context"]