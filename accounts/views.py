from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordResetConfirmView, PasswordResetView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

from core import throttle
from moderation.services import audit

from . import services
from .forms import (
    ChangeEmailForm,
    ChangePasswordForm,
    DeactivateForm,
    EmailAuthenticationForm,
    NewPasswordForm,
    RegistrationForm,
    ResetRequestForm,
)


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard:index")
    if request.method == "POST":
        if not throttle.allow("register", throttle.client_ip(request), 10, 3600):
            messages.error(request, "Too many attempts. Please try again later.")
            return redirect("accounts:register")
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            user = services.register_member(form.cleaned_data, profile)
            auth_login(request, user)
            messages.success(request, "Welcome to Surjotori! Your account is ready.")
            return redirect("dashboard:index")
    else:
        form = RegistrationForm()
    return render(
        request,
        "generic_form.html",
        {"form": form, "title": "Join Surjotori", "submit_label": "Create account", "multipart": True, "aside": True,
         "intro": "One account for everyone: donate, request blood, or both. All fields are required unless marked optional."},
    )


class ThrottledLoginView(LoginView):
    authentication_form = EmailAuthenticationForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

    def post(self, request, *args, **kwargs):
        if not throttle.allow("login", throttle.client_ip(request), 15, 900):
            messages.error(request, "Too many login attempts. Please wait a few minutes.")
            return redirect("accounts:login")
        return super().post(request, *args, **kwargs)


@require_POST
def logout_view(request):
    auth_logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("core:home")


class ThrottledPasswordResetView(PasswordResetView):
    form_class = ResetRequestForm
    template_name = "generic_form.html"
    email_template_name = "registration/password_reset_email.txt"
    subject_template_name = "registration/password_reset_subject.txt"
    success_url = reverse_lazy("accounts:password_reset_done")
    extra_context = {"title": "Reset your password", "submit_label": "Send reset link",
                     "intro": "Enter your account email. If it exists, we will send reset instructions."}

    def form_valid(self, form):
        if not throttle.allow("reset", throttle.client_ip(self.request), 5, 3600):
            return redirect(self.success_url)  # generic response, nothing sent
        return super().form_valid(form)


class ConfirmView(PasswordResetConfirmView):
    form_class = NewPasswordForm
    template_name = "generic_form.html"
    success_url = reverse_lazy("accounts:password_reset_complete")
    extra_context = {"title": "Choose a new password", "submit_label": "Change password"}


@login_required
def security(request):
    user = request.user
    forms_map = {
        "password": ChangePasswordForm(user, prefix="pw"),
        "email": ChangeEmailForm(user, prefix="em"),
        "deactivate": DeactivateForm(user, prefix="dx"),
    }
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "password":
            form = ChangePasswordForm(user, request.POST, prefix="pw")
            if form.is_valid():
                user.set_password(form.cleaned_data["new_password1"])
                user.save(update_fields=["password", "updated_at"])
                update_session_auth_hash(request, user)
                audit(user, "password.changed", "USER", user.pk, request=request)
                messages.success(request, "Password changed.")
                return redirect("accounts:security")
            forms_map["password"] = form
        elif action == "email":
            form = ChangeEmailForm(user, request.POST, prefix="em")
            if form.is_valid():
                services.change_email(request, user, form.cleaned_data["new_email"])
                messages.success(request, "Email updated.")
                return redirect("accounts:security")
            forms_map["email"] = form
        elif action == "deactivate":
            form = DeactivateForm(user, request.POST, prefix="dx")
            if form.is_valid():
                services.deactivate_account(request, user)
                auth_logout(request)
                messages.info(request, "Your account was deactivated. Contact the organization to reactivate or request data correction/deletion.")
                return redirect("core:home")
            forms_map["deactivate"] = form
    return render(request, "accounts/security.html", {"forms": forms_map})
