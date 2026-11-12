from django.contrib import admin

from .models import MemberPrivacy, MemberProfile


@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "user", "blood_group", "upazila", "wants_to_donate", "donation_willingness")
    list_filter = ("blood_group", "upazila", "wants_to_donate", "needs_blood", "donation_willingness")
    search_fields = ("full_name", "user__email", "phone", "area")
    readonly_fields = ("user",)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(MemberPrivacy)
class MemberPrivacyAdmin(admin.ModelAdmin):
    list_display = ("user", "show_phone", "show_whatsapp", "show_messenger", "allow_direct_requests")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
