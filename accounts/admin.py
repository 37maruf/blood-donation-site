from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import BaseUserCreationForm, UserChangeForm
from django.utils import timezone

from moderation.services import audit

from .models import User


class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ("email",)


class UserChangeAdminForm(UserChangeForm):
    class Meta:
        model = User
        fields = "__all__"


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    add_form = UserCreationForm
    form = UserChangeAdminForm
    ordering = ("email",)
    list_display = ("email", "is_active", "is_staff", "date_joined")
    list_filter = ("is_active", "is_staff", "groups")
    search_fields = ("email", "profile__full_name", "profile__phone")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Status", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Consent", {"fields": ("terms_version", "terms_accepted_at")}),
        ("Permissions", {"fields": ("groups", "user_permissions")}),
        ("Dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2", "is_staff", "groups")}),
    )
    readonly_fields = ("last_login", "date_joined")
    actions = ["deactivate_users", "activate_users"]

    @admin.action(description="Deactivate selected members (records are kept)")
    def deactivate_users(self, request, queryset):
        for user in queryset.exclude(pk=request.user.pk):
            user.is_active = False
            user.save(update_fields=["is_active", "updated_at"])
            audit(request.user, "user.deactivated", "USER", user.pk, {"by": "staff"}, request)
        self.message_user(request, "Selected members deactivated.", messages.SUCCESS)

    @admin.action(description="Activate selected members")
    def activate_users(self, request, queryset):
        for user in queryset:
            user.is_active = True
            user.save(update_fields=["is_active", "updated_at"])
            audit(request.user, "user.activated", "USER", user.pk, {"by": "staff"}, request)
        self.message_user(request, "Selected members activated.", messages.SUCCESS)
