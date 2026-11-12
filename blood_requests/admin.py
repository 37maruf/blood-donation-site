from django.contrib import admin

from . import services
from .models import BloodNeedPost, DonationRequest, GeneralBloodRequest


@admin.register(BloodNeedPost)
class BloodNeedPostAdmin(admin.ModelAdmin):
    list_display = ("created_at", "blood_group", "units", "hospital_name", "urgency", "status", "is_hidden")
    list_filter = ("status", "urgency", "blood_group", "is_hidden")
    search_fields = ("hospital_name", "owner__email")
    readonly_fields = ("owner", "closed_at")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(GeneralBloodRequest)
class GeneralBloodRequestAdmin(admin.ModelAdmin):
    list_display = ("created_at", "blood_group", "units", "hospital", "urgency", "status", "requester")
    list_filter = ("status", "urgency", "blood_group")
    search_fields = ("patient_name", "hospital", "requester__email")
    readonly_fields = ("requester",)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        old = GeneralBloodRequest.objects.get(pk=obj.pk).status if change else None
        super().save_model(request, obj, form, change)
        if change and old != obj.status:
            services.notify_general_status_change(obj, request.user, old)


@admin.register(DonationRequest)
class DonationRequestAdmin(admin.ModelAdmin):
    list_display = ("created_at", "requester", "donor", "blood_group", "status")
    list_filter = ("status",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
