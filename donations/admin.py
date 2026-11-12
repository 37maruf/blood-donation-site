from django.contrib import admin

from .models import DonationRecord
from .services.records import audit_record_change, snapshot


@admin.register(DonationRecord)
class DonationRecordAdmin(admin.ModelAdmin):
    """Only staff with model permissions manage records; members can never self-complete."""

    list_display = ("donation_date", "donor", "status", "location", "created_by")
    list_filter = ("status", "donation_date")
    search_fields = ("donor__email", "donor__profile__full_name", "location")
    raw_id_fields = ("donor",)
    readonly_fields = ("created_by",)

    def has_delete_permission(self, request, obj=None):
        return False  # history is never deleted; cancel instead

    def save_model(self, request, obj, form, change):
        old = None
        if change:
            old = snapshot(DonationRecord.objects.get(pk=obj.pk))
        else:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
        audit_record_change(request, obj, old)
