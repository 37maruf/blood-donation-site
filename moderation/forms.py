from django import forms

from blood_requests.models import BloodNeedPost
from members.models import MemberProfile

from .models import Report


class ReportForm(forms.Form):
    target_type = forms.ChoiceField(choices=Report.TargetType.choices)
    target_id = forms.UUIDField()
    reason = forms.ChoiceField(choices=Report.Reason.choices)
    details = forms.CharField(required=False, max_length=1000)

    def __init__(self, *args, reporter=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.reporter = reporter

    def clean(self):
        cleaned = super().clean()
        ttype, tid = cleaned.get("target_type"), cleaned.get("target_id")
        if ttype and tid:
            if ttype == Report.TargetType.USER:
                exists = MemberProfile.objects.filter(user_id=tid, user__is_active=True).exists()
                if tid == self.reporter.pk:
                    raise forms.ValidationError("You cannot report yourself.")
            else:
                exists = BloodNeedPost.objects.filter(pk=tid, is_hidden=False).exists()
            if not exists:
                raise forms.ValidationError("That item could not be found.")
        return cleaned
