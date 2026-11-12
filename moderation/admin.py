from django.contrib import admin, messages

from blood_requests.models import BloodNeedPost

from .models import AuditLog, Report
from .services import hide_post, mark_reviewed


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("created_at", "target_type", "reason", "status", "reporter")
    list_filter = ("status", "target_type", "reason")
    readonly_fields = ("reporter", "target_type", "target_id", "reason", "details", "reviewed_by", "reviewed_at")
    actions = ["mark_dismissed", "mark_actioned", "hide_reported_posts"]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.action(description="Dismiss selected reports")
    def mark_dismissed(self, request, queryset):
        for report in queryset:
            mark_reviewed(report, request.user, Report.Status.DISMISSED)

    @admin.action(description="Mark selected reports as 'action taken'")
    def mark_actioned(self, request, queryset):
        for report in queryset:
            mark_reviewed(report, request.user, Report.Status.ACTIONED)

    @admin.action(description="Hide the reported blood-need posts (reason recorded and audited)")
    def hide_reported_posts(self, request, queryset):
        count = 0
        for report in queryset.filter(target_type=Report.TargetType.POST):
            post = BloodNeedPost.objects.filter(pk=report.target_id).first()
            if post and not post.is_hidden:
                hide_post(post, request.user, f"Hidden after report ({report.get_reason_display()})", request)
                mark_reviewed(report, request.user, Report.Status.ACTIONED)
                count += 1
        self.message_user(request, f"{count} post(s) hidden.", messages.SUCCESS)


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "action", "actor", "target_type", "target_id")
    list_filter = ("action", "target_type")
    search_fields = ("action", "target_id", "actor__email")
    readonly_fields = [f.name for f in AuditLog._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
