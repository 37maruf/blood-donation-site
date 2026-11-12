from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm

from core.forms import BootstrapMixin
from members.forms import MemberProfileForm

from .models import User


class RegistrationForm(MemberProfileForm):
    email = forms.EmailField()
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}))
    password2 = forms.CharField(
        label="Confirm password", widget=forms.PasswordInput(attrs={"autocomplete": "new-password"})
    )
    accept_terms = forms.BooleanField(
        required=True, label="I accept the Terms of Use and have read the Privacy Notice."
    )

    field_order = [
        "full_name", "email", "password1", "password2", "phone", "whatsapp_number", "messenger_url",
        "district", "upazila", "area", "profile_image", "wants_to_donate", "needs_blood", "blood_group",
        "never_donated", "confirmed_last_donation_date", "accept_terms",
    ]

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean(self):
        cleaned = super().clean()
        p1, p2 = cleaned.get("password1"), cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "The two passwords do not match.")
        elif p1:
            try:
                password_validation.validate_password(p1, User(email=cleaned.get("email", "")))
            except forms.ValidationError as exc:
                self.add_error("password1", exc)
        return cleaned


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"autofocus": True, "autocomplete": "email"}))

    def clean_username(self):
        return self.cleaned_data["username"].strip().lower()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class _PasswordConfirm(BootstrapMixin, forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        if not self.user.check_password(self.cleaned_data["current_password"]):
            raise forms.ValidationError("Password is incorrect.")
        return self.cleaned_data["current_password"]


class ChangePasswordForm(_PasswordConfirm):
    new_password1 = forms.CharField(label="New password", widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}))
    new_password2 = forms.CharField(label="Confirm new password", widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}))

    def clean(self):
        cleaned = super().clean()
        p1, p2 = cleaned.get("new_password1"), cleaned.get("new_password2")
        if p1 and p2 and p1 != p2:
            self.add_error("new_password2", "The two passwords do not match.")
        elif p1:
            try:
                password_validation.validate_password(p1, self.user)
            except forms.ValidationError as exc:
                self.add_error("new_password1", exc)
        return cleaned


class ChangeEmailForm(_PasswordConfirm):
    new_email = forms.EmailField()

    def clean_new_email(self):
        email = self.cleaned_data["new_email"].strip().lower()
        if User.objects.filter(email__iexact=email).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError("That email cannot be used.")
        return email


class DeactivateForm(_PasswordConfirm):
    confirm = forms.BooleanField(label="I understand my account will be deactivated (my records are kept).")


class ResetRequestForm(BootstrapMixin, PasswordResetForm):
    pass


class NewPasswordForm(BootstrapMixin, SetPasswordForm):
    pass
