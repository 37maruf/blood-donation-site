from django import forms
from django.utils import timezone

from core.choices import BloodGroup
from core.forms import DATE_WIDGET, BootstrapMixin
from members.validators import normalize_phone, validate_bd_phone

from .models import BloodNeedPost, BloodNeedResponse, DonationRequest, GeneralBloodRequest


class _FutureDateMixin:
    def clean_required_date(self):
        value = self.cleaned_data["required_date"]
        if value < timezone.localdate():
            raise forms.ValidationError("The required date cannot be in the past.")
        return value


class BloodNeedForm(_FutureDateMixin, BootstrapMixin, forms.ModelForm):
    class Meta:
        model = BloodNeedPost
        fields = [
            "patient_name", "patient_name_public", "blood_group", "units", "hospital_name", "hospital_location",
            "required_date", "contact_phone", "contact_public", "urgency", "details",
        ]
        widgets = {"required_date": DATE_WIDGET, "details": forms.Textarea(attrs={"rows": 4})}
        help_texts = {"contact_phone": "Only shown to logged-in members, and only if you tick the box below."}

    def clean_units(self):
        value = self.cleaned_data["units"]
        if value < 1 or value > 20:
            raise forms.ValidationError("Units must be between 1 and 20.")
        return value

    def clean_contact_phone(self):
        validate_bd_phone(self.cleaned_data["contact_phone"])
        return normalize_phone(self.cleaned_data["contact_phone"])


class NeedFilterForm(BootstrapMixin, forms.Form):
    blood_group = forms.ChoiceField(required=False, choices=[("", "Any blood group")] + list(BloodGroup.choices))
    status = forms.ChoiceField(
        required=False,
        choices=[("ACTIVE", "Active"), ("FULFILLED", "Fulfilled"), ("CANCELLED", "Cancelled"), ("ALL", "All")],
    )


class NeedResponseForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = BloodNeedResponse
        fields = ["message"]
        widgets = {"message": forms.TextInput(attrs={"placeholder": "Optional short message to the family"})}


class GeneralBloodRequestForm(_FutureDateMixin, BootstrapMixin, forms.ModelForm):
    class Meta:
        model = GeneralBloodRequest
        fields = ["patient_name", "blood_group", "units", "hospital", "location", "required_date", "contact",
                  "urgency", "message"]
        widgets = {"required_date": DATE_WIDGET, "message": forms.Textarea(attrs={"rows": 4})}

    def clean_units(self):
        value = self.cleaned_data["units"]
        if value < 1 or value > 20:
            raise forms.ValidationError("Units must be between 1 and 20.")
        return value

    def clean_contact(self):
        validate_bd_phone(self.cleaned_data["contact"])
        return normalize_phone(self.cleaned_data["contact"])


class DirectRequestForm(_FutureDateMixin, BootstrapMixin, forms.ModelForm):
    class Meta:
        model = DonationRequest
        fields = ["hospital_location", "required_date", "message"]
        widgets = {"required_date": DATE_WIDGET, "message": forms.Textarea(attrs={"rows": 3})}
