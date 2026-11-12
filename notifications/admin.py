from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Staff use this to publish site-wide ANNOUNCEMENT broadcasts."""

    list_display = ("created_at", "kind", "title", "recipient")
    list_filter = ("kind",)
    fields = ("title", "body")

    def save_model(self, request, obj, form, change):
        if not change:
            obj.kind = Notification.Kind.ANNOUNCEMENT
            obj.recipient = None
            obj.actor = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
