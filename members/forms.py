from django import forms
from django.core.files.uploadedfile import UploadedFile
from django.utils import timezone

from core.forms import DATE_WIDGET, BootstrapMixin
from core.images import process_profile_image
from core.choices import BloodGroup
from core.models import District, Upazila
from django.conf import settings

from .models import MemberPrivacy, MemberProfile, Willingness
from .validators import (
    donor_history_errors,
    normalize_phone,
    validate_bd_phone,
    validate_messenger_url,
)


def default_district():
    return District.objects.filter(name=settings.DEFAULT_DISTRICT_NAME).first()


class MemberProfileForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = MemberProfile
        fields = [
            "full_name", "phone", "whatsapp_number", "messenger_url", "district", "upazila", "area",
            "profile_image", "wants_to_donate", "needs_blood", "blood_group", "never_donated",
            "confirmed_last_donation_date",
        ]
        widgets = {"confirmed_last_donation_date": DATE_WIDGET}
        help_texts = {
            "messenger_url": "Your Facebook / Messenger profile link (facebook.com, fb.com, m.me, messenger.com).",
            "phone": "Bangladeshi mobile number, e.g. 01XXXXXXXXX.",
            "profile_image": "Optional. JPG, PNG or WEBP up to 2 MB.",
            "confirmed_last_donation_date": "Required for donors unless you have never donated.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        district = default_district()
        self.fields["district"].queryset = District.objects.filter(pk=district.pk) if district else District.objects.none()
        self.fields["district"].empty_label = None
        self.fields["upazila"].queryset = Upazila.objects.filter(district=district) if district else Upazila.objects.none()
        self.fields["upazila"].empty_label = "Select upazila"
        if district and not self.instance.pk:
            self.fields["district"].initial = district.pk
        self.fields["blood_group"].required = False
        self.fields["profile_image"].required = False

    def clean_phone(self):
        value = self.cleaned_data["phone"]
        validate_bd_phone(value)
        return normalize_phone(value)

    def clean_whatsapp_number(self):
        value = self.cleaned_data["whatsapp_number"]
        validate_bd_phone(value)
        return normalize_phone(value)

    def clean_messenger_url(self):
        value = self.cleaned_data["messenger_url"].strip()
        validate_messenger_url(value)
        return value

    def clean_profile_image(self):
        value = self.cleaned_data.get("profile_image")
        if isinstance(value, UploadedFile):
            return process_profile_image(value)
        return value

    def clean(self):
        cleaned = super().clean()
        donor, needs = cleaned.get("wants_to_donate"), cleaned.get("needs_blood")
        if not donor and not needs:
            raise forms.ValidationError("Choose at least one: 'I want to donate' or 'I may need blood'.")
        district, upazila = cleaned.get("district"), cleaned.get("upazila")
        if district and upazila and upazila.district_id != district.pk:
            self.add_error("upazila", "This upazila does not belong to the selected district.")
        if donor:
            if not cleaned.get("blood_group"):
                self.add_error("blood_group", "Blood group is required for donors.")
            for field, msg in donor_history_errors(
                cleaned.get("never_donated"), cleaned.get("confirmed_last_donation_date"), timezone.localdate()
            ):
                self.add_error(field, msg)
        else:  # donor-only values are cleared server-side
            cleaned["blood_group"] = ""
            cleaned["never_donated"] = False
            cleaned["confirmed_last_donation_date"] = None
        return cleaned


class DonationSettingsForm(BootstrapMixin, forms.Form):
    donation_willingness = forms.ChoiceField(choices=Willingness.choices, label="Donation willingness")
    never_donated = forms.BooleanField(required=False, label="I have never donated blood")
    confirmed_last_donation_date = forms.DateField(required=False, widget=DATE_WIDGET, label="Last donation date")

    def __init__(self, *args, profile, **kwargs):
        self.profile = profile
        kwargs.setdefault("initial", {
            "donation_willingness": profile.donation_willingness,
            "never_donated": profile.never_donated,
            "confirmed_last_donation_date": profile.confirmed_last_donation_date,
        })
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        for field, msg in donor_history_errors(
            cleaned.get("never_donated"), cleaned.get("confirmed_last_donation_date"), timezone.localdate()
        ):
            self.add_error(field, msg)
        return cleaned


class PrivacyForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = MemberPrivacy
        fields = ["show_phone", "show_whatsapp", "show_messenger", "show_donation_history", "show_area", "allow_direct_requests"]


class DonorSearchForm(BootstrapMixin, forms.Form):
    blood_group = forms.ChoiceField(required=False, choices=[("", "Any blood group")] + list(BloodGroup.choices))
    upazila = forms.ModelChoiceField(required=False, queryset=Upazila.objects.none(), empty_label="Any upazila")
    area = forms.CharField(required=False, max_length=80)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        district = default_district()
        if district:
            self.fields["upazila"].queryset = Upazila.objects.filter(district=district)
