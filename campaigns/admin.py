from django.contrib import admin

from . import services
from .models import Campaign, CampaignRegistration

WATCHED = {"starts_at": "date/time", "ends_at": "end time", "venue": "venue", "status": "status"}


class RegistrationInline(admin.TabularInline):
    model = CampaignRegistration
    extra = 0
    can_delete = False
    readonly_fields = ("member", "status", "created_at")

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ("title", "starts_at", "venue", "status", "capacity")
    list_filter = ("status",)
    search_fields = ("title", "venue")
    inlines = [RegistrationInline]
    actions = ["archive_selected"]
    readonly_fields = ("created_by",)

    def has_delete_permission(self, request, obj=None):
        # archive instead of delete once registrations exist
        if obj is not None and obj.registrations.exists():
            return False
        return super().has_delete_permission(request, obj)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
        if change:
            changed = [label for field, label in WATCHED.items() if field in form.changed_data]
            if changed:
                services.notify_registrants(obj, ", ".join(changed), request.user)

    @admin.action(description="Archive selected campaigns")
    def archive_selected(self, request, queryset):
        for campaign in queryset.exclude(status=Campaign.Status.ARCHIVED):
            campaign.status = Campaign.Status.ARCHIVED
            campaign.save(update_fields=["status", "updated_at"])
            services.notify_registrants(campaign, "status (archived)", request.user)
