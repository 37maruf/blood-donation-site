"""Demo/test data for every feature. Safe to run more than once.

Put this file at:  core/management/commands/seed_demo.py
Run:               python manage.py seed_demo
Use a TEST database only. All demo users share one password (printed at the end).
"""
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from accounts.models import User
from blood_requests.models import BloodNeedPost, DonationRequest, GeneralBloodRequest
from campaigns.models import Campaign, CampaignRegistration
from core.models import District, Upazila
from donations.models import DonationRecord
from members.models import MemberPrivacy, MemberProfile
from moderation.models import Report
from notifications import services as notifications
from notifications.models import Notification

PASSWORD = "Demo-pass-12345!"
today = timezone.localdate


class Command(BaseCommand):
    help = "Create demo members, donors, records, blood needs, requests, registrations, reports."

    @transaction.atomic
    def handle(self, *args, **options):
        self.district = District.objects.get(name="Rajbari")
        self.ups = {u.name: u for u in Upazila.objects.filter(district=self.district)}

        rahim = self.member("rahim@demo.test", "Rahim Uddin", "01711000001", "Rajbari Sadar", "A+",
                            never=True, privacy=dict(show_phone=True, show_whatsapp=True, show_messenger=True,
                                                     show_donation_history=True, show_area=True,
                                                     allow_direct_requests=True))
        karim = self.member("karim@demo.test", "Karim Hossain", "01711000002", "Goalanda", "O+",
                            last=today() - timedelta(days=100),
                            privacy=dict(show_whatsapp=True, show_messenger=True, show_area=True,
                                         allow_direct_requests=True))
        self.member("salma@demo.test", "Salma Akter", "01711000003", "Pangsha", "B+",
                    last=today() - timedelta(days=20))                    # NOT listed: 60-day rule
        self.member("nusrat@demo.test", "Nusrat Jahan", "01711000004", "Baliakandi", "AB-",
                    never=True, willingness="INACTIVE")                   # NOT listed: inactive
        tanvir = self.member("tanvir@demo.test", "Tanvir Ahmed", "01711000005", "Kalukhali", "",
                             donor=False)                                 # needs blood: posts and requests
        history = self.member("jamal@demo.test", "Jamal Mia", "01711000007", "Pangsha", "O-",
                              last=today() - timedelta(days=75),
                              privacy=dict(show_donation_history=True, show_phone=True, allow_direct_requests=True))

        # Donation records (staff-managed in real life)
        self.record(history.user, 70, "COMPLETED", "Rajbari Sadar Hospital")
        self.record(history.user, 200, "COMPLETED", "Blood donation camp")
        self.record(rahim.user, 3, "PENDING", "Planned donation")        # PENDING is ignored by the rule
        self.record(karim.user, 400, "CANCELLED", "Cancelled visit")      # CANCELLED is ignored

        # Public blood needs (+ one broadcast notification each)
        self.need(tanvir.user, "A+", 2, "Rajbari Sadar Hospital", "URGENT", 2, public_patient=True, public_contact=True,
                  details="Operation scheduled. Please contact as soon as possible.")
        self.need(tanvir.user, "O-", 1, "Pangsha Upazila Health Complex", "CRITICAL", 1)
        self.need(tanvir.user, "B+", 3, "Goalanda Clinic", "NORMAL", 7, status="FULFILLED")

        # Private general request (staff reviews it in /admin/)
        if not GeneralBloodRequest.objects.filter(requester=tanvir.user).exists():
            GeneralBloodRequest.objects.create(
                requester=tanvir.user, patient_name="Mother of Tanvir", blood_group="AB+", units=2,
                hospital="Rajbari Sadar Hospital", location="Rajbari", required_date=today() + timedelta(days=4),
                contact="01711000005", message="Need AB+ donors, please help.", urgency="URGENT")

        # Direct request tanvir -> rahim (log in as rahim to accept/reject)
        if not DonationRequest.objects.filter(requester=tanvir.user, donor=rahim.user).exists():
            req = DonationRequest.objects.create(
                requester=tanvir.user, donor=rahim.user, blood_group="A+", hospital_location="Rajbari Sadar Hospital",
                required_date=today() + timedelta(days=2), message="Can you donate this week?")
            notifications.notify(rahim.user, Notification.Kind.DIRECT_REQUEST_RECEIVED, "New donation request",
                                 "A member asked for A+ blood.", "requests_received", req.pk, tanvir.user)

        # Campaign registration + a site announcement + a report
        campaign = Campaign.objects.filter(status="PUBLISHED", ends_at__gte=timezone.now()).first()
        if campaign:
            CampaignRegistration.objects.get_or_create(campaign=campaign, member=tanvir.user)
        if not Notification.objects.filter(kind="ANNOUNCEMENT", title="Welcome to Surjotori").exists():
            notifications.broadcast(Notification.Kind.ANNOUNCEMENT, "Welcome to Surjotori",
                                    "Thank you for joining our Rajbari blood donation community.")
        Report.objects.get_or_create(reporter=tanvir.user, target_type="USER", target_id=karim.user_id,
                                     defaults={"reason": "OTHER", "details": "Demo report for moderation testing."})

        self.stdout.write(self.style.SUCCESS("Demo data ready."))
        self.stdout.write(f"All demo logins use password: {PASSWORD}")
        self.stdout.write("rahim@demo.test (donor, everything public) | karim@demo.test (donor, 100 days ago)\n"
                          "salma@demo.test (20 days ago, hidden) | nusrat@demo.test (inactive, hidden)\n"
                          "tanvir@demo.test (needs blood: posts/requests)\n"
                          "jamal@demo.test (donor with public donation history)")

    # ------------------------------------------------------------------ helpers
    def member(self, email, name, phone, upazila, blood, donor=True, never=False, last=None,
               willingness="ACTIVE", privacy=None):
        user, created = User.objects.get_or_create(email=email)
        if created:
            user.set_password(PASSWORD)
            user.terms_version, user.terms_accepted_at = "demo", timezone.now()
            user.save()
        profile, _ = MemberProfile.objects.get_or_create(user=user, defaults=dict(
            full_name=name, phone=phone, whatsapp_number=phone, messenger_url="https://m.me/" + email.split("@")[0],
            district=self.district, upazila=self.ups[upazila], area=f"{upazila} town area",
            wants_to_donate=donor, needs_blood=not donor, blood_group=blood if donor else "",
            never_donated=never if donor else False, confirmed_last_donation_date=last if donor else None,
            donation_willingness=willingness))
        MemberPrivacy.objects.get_or_create(user=user, defaults=privacy or {})
        return profile

    def record(self, user, days_ago, status, location):
        date = today() - timedelta(days=days_ago)
        DonationRecord.objects.get_or_create(donor=user, donation_date=date, status=status,
                                             defaults={"location": location})

    def need(self, owner, group, units, hospital, urgency, days, status="ACTIVE", public_patient=False,
             public_contact=False, details=""):
        if BloodNeedPost.objects.filter(owner=owner, hospital_name=hospital, blood_group=group).exists():
            return
        post = BloodNeedPost.objects.create(
            owner=owner, patient_name="Demo Patient", patient_name_public=public_patient, blood_group=group,
            units=units, hospital_name=hospital, hospital_location="Rajbari", required_date=today() + timedelta(days=days),
            contact_phone="01711000005", contact_public=public_contact, details=details, urgency=urgency,
            status=status, closed_at=timezone.now() if status != "ACTIVE" else None)
        if status == "ACTIVE":
            notifications.broadcast(Notification.Kind.NEW_BLOOD_NEED, f"{urgency.title()}: {group} blood needed",
                                    f"{units} unit(s) at {hospital}.", "need", post.pk, owner)
