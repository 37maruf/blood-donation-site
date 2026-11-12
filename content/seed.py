"""Idempotent seed: Rajbari district + upazilas, staff groups, default pages, sample campaigns.

Runs automatically after `migrate` (see content/apps.py) and via `manage.py seed_initial`.
Existing admin-edited content is never overwritten.
"""
from datetime import timedelta

from django.contrib.auth.models import Group, Permission
from django.utils import timezone

RAJBARI_UPAZILAS = [
    ("Rajbari Sadar", "রাজবাড়ী সদর"),
    ("Goalanda", "গোয়ালন্দ"),
    ("Pangsha", "পাংশা"),
    ("Baliakandi", "বালিয়াকান্দি"),
    ("Kalukhali", "কালুখালী"),
]

GROUPS = {
    "Content Manager": [
        ("content", "sitecontent", "add change view"),
        ("content", "organizationsettings", "change view"),
        ("notifications", "notification", "add view"),
    ],
    "Campaign Manager": [
        ("campaigns", "campaign", "add change delete view"),
        ("campaigns", "campaignregistration", "view"),
    ],
    "Donation Manager": [
        ("donations", "donationrecord", "add change view"),
        ("members", "memberprofile", "view"),
    ],
    "Request Moderator": [
        ("blood_requests", "bloodneedpost", "change view"),
        ("blood_requests", "generalbloodrequest", "change view"),
        ("blood_requests", "donationrequest", "view change"),
        ("moderation", "report", "change view"),
    ],
    "User Support": [
        ("accounts", "user", "change view"),
        ("members", "memberprofile", "change view"),
        ("members", "memberprivacy", "view"),
    ],
}

PAGES = {
    "home_intro": (
        "Every drop connects a neighbour",
        "Surjotori is a volunteer blood donation organization serving Rajbari district. We bring together "
        "people who are ready to donate and families who urgently need blood, so that a call for help in "
        "Rajbari Sadar, Goalanda, Pangsha, Baliakandi or Kalukhali reaches willing hands quickly.\n\n"
        "Join as a donor, post a blood need, or simply spread the word. One account does it all.",
    ),
    "about": (
        "About Surjotori",
        "Surjotori means the sun-bearer, and the name reflects what we hope to be for Rajbari: a steady "
        "source of light for families on the hardest day of their year. We are a community-run blood "
        "donation organization working only within Rajbari district.\n\n"
        "What we do\n"
        "We keep a district-level register of voluntary donors, help families publish urgent blood needs, "
        "arrange blood group testing and awareness sessions at schools and community spaces, and "
        "encourage regular, safe, voluntary donation.\n\n"
        "How this website helps\n"
        "Members choose exactly what to share. Phone numbers, WhatsApp, Messenger, area and donation "
        "history stay private unless a donor switches them on. The public only ever sees a shortened name, "
        "blood group, upazila and availability.\n\n"
        "Our promise\n"
        "Blood must never be sold through this platform. Donation is voluntary, and the final decision on "
        "medical fitness always belongs to the blood centre or doctor. Our 60-day availability rule is a "
        "simple website guideline, not medical clearance.",
    ),
    "contact": (
        "Contact us",
        "Have a question, want to volunteer, or need help with your account? Reach out using the details "
        "on this page. For a medical emergency, please contact a hospital or blood bank directly first.\n\n"
        "To correct or delete your personal data, write to us from the email address on your account and "
        "describe what you would like changed. We will confirm your identity before acting.\n\n"
        "Organizations, schools and clubs in Rajbari that would like us to run a blood group testing camp "
        "or an awareness session are warmly invited to get in touch.",
    ),
    "terms": (
        "Terms of Use",
        "By creating an account you agree to the following.\n\n"
        "1. You will give accurate information and keep it up to date.\n"
        "2. Blood donation through this platform is voluntary. You will not ask for, offer or accept "
        "payment for blood.\n"
        "3. Availability shown on this site follows a simple 60-day rule and is not medical clearance. "
        "Always follow the advice of the blood centre or a doctor.\n"
        "4. You will not misuse other members' contact details, harass anyone, or post false requests.\n"
        "5. Surjotori cannot verify that a message was delivered or answered, and is not responsible for "
        "arrangements made between members.\n"
        "6. We may hide posts or deactivate accounts that break these terms.\n"
        "7. We may update these terms. The version you accepted is recorded with your account.",
    ),
    "privacy": (
        "Privacy Notice",
        "What we collect\n"
        "Your name, email, phone and WhatsApp numbers, Messenger link, location within Rajbari, blood "
        "group, donation history, optional profile photo, and records of your activity on the site "
        "(for example requests and audit entries).\n\n"
        "Who can see it\n"
        "Visitors see only a shortened name, blood group, upazila and availability. Logged-in "
        "members can open a detailed profile, but each contact field and your area and donation history "
        "appear only if you switched that setting on. All settings are off by default and you can change "
        "them at any time under Contact & Privacy.\n\n"
        "Why we use it\n"
        "To match donors with people who need blood, to keep the community safe, and to run the "
        "organization.\n\n"
        "Your choices\n"
        "You can edit your details, hide yourself from donor lists, or deactivate your account. "
        "Deactivation keeps donation and request records for safety and audit purposes. You may also ask "
        "us to correct or delete your personal data - see the Contact page for the process.",
    ),
}

PAGES_BN = {
    "home_intro": (
        "প্রতিটি ফোঁটা একজন প্রতিবেশীকে জুড়ে দেয়",
        "সূর্যতরী রাজবাড়ী জেলায় কাজ করা একটি স্বেচ্ছাসেবী রক্তদান সংগঠন। যাঁরা রক্ত দিতে প্রস্তুত এবং যে পরিবারগুলোর "
        "জরুরি রক্ত দরকার, আমরা তাঁদের এক জায়গায় আনি, যাতে রাজবাড়ী সদর, গোয়ালন্দ, পাংশা, বালিয়াকান্দি বা কালুখালী "
        "থেকে সাহায্যের ডাক দ্রুত ইচ্ছুক হাতে পৌঁছায়।\n\nদাতা হিসেবে যোগ দিন, রক্তের প্রয়োজন জানান, কিংবা কথাটা ছড়িয়ে দিন। "
        "একটি অ্যাকাউন্টেই সবকিছু।",
    ),
    "about": (
        "সূর্যতরী সম্পর্কে",
        "সূর্যতরী মানে সূর্যবাহক। রাজবাড়ীর জন্য আমরা এটাই হতে চাই: বছরের সবচেয়ে কঠিন দিনে পরিবারগুলোর জন্য আলোর এক স্থির "
        "উৎস। আমরা একটি কমিউনিটি-চালিত রক্তদান সংগঠন, যা শুধু রাজবাড়ী জেলায় কাজ করে।\n\n"
        "আমরা যা করি\n"
        "আমরা স্বেচ্ছায় রক্তদাতাদের একটি জেলা-পর্যায়ের তালিকা রাখি, পরিবারগুলোকে জরুরি রক্তের প্রয়োজন প্রকাশ করতে সাহায্য করি, "
        "স্কুল ও কমিউনিটি স্থানে রক্তের গ্রুপ পরীক্ষা ও সচেতনতামূলক অনুষ্ঠানের আয়োজন করি, এবং নিয়মিত, নিরাপদ ও স্বেচ্ছায় "
        "রক্তদানে উৎসাহ দিই।\n\n"
        "এই ওয়েবসাইট কীভাবে সাহায্য করে\n"
        "সদস্যরা নিজেরাই ঠিক করেন কী প্রকাশ করবেন। দাতা নিজে চালু না করলে ফোন নম্বর, হোয়াটসঅ্যাপ, মেসেঞ্জার, এলাকা ও "
        "রক্তদানের ইতিহাস গোপন থাকে। সাধারণ দর্শক শুধু সংক্ষিপ্ত নাম, রক্তের গ্রুপ, উপজেলা ও প্রাপ্যতা দেখতে পান।\n\n"
        "আমাদের অঙ্গীকার\n"
        "এই প্ল্যাটফর্মে রক্ত কখনো বিক্রি করা যাবে না। রক্তদান স্বেচ্ছায়, এবং শারীরিক উপযুক্ততার চূড়ান্ত সিদ্ধান্ত সবসময় "
        "ব্লাড সেন্টার বা চিকিৎসকের। আমাদের ৬০ দিনের প্রাপ্যতার নিয়মটি একটি সাধারণ ওয়েবসাইট-নির্দেশনা, চিকিৎসাগত ছাড়পত্র নয়।",
    ),
    "contact": (
        "যোগাযোগ করুন",
        "কোনো প্রশ্ন আছে, স্বেচ্ছাসেবক হতে চান, বা অ্যাকাউন্ট নিয়ে সাহায্য দরকার? এই পাতার তথ্য ব্যবহার করে যোগাযোগ করুন। "
        "চিকিৎসা-জরুরি অবস্থায় আগে সরাসরি হাসপাতাল বা ব্লাড ব্যাংকে যোগাযোগ করুন।\n\n"
        "আপনার ব্যক্তিগত তথ্য সংশোধন বা মুছে ফেলতে চাইলে অ্যাকাউন্টের ইমেইল থেকে আমাদের লিখুন এবং কী বদলাতে চান জানান। "
        "কাজ করার আগে আমরা আপনার পরিচয় নিশ্চিত করব।\n\n"
        "রাজবাড়ীর যেসব প্রতিষ্ঠান, স্কুল বা ক্লাব রক্তের গ্রুপ পরীক্ষা শিবির বা সচেতনতামূলক অনুষ্ঠান চায়, তাদের যোগাযোগের "
        "জন্য আন্তরিক আমন্ত্রণ।",
    ),
    "terms": (
        "ব্যবহারের শর্তাবলি",
        "অ্যাকাউন্ট খুললে আপনি নিচের শর্তে সম্মত হচ্ছেন।\n\n"
        "1. আপনি সঠিক তথ্য দেবেন এবং তা হালনাগাদ রাখবেন।\n"
        "2. এই প্ল্যাটফর্মের মাধ্যমে রক্তদান স্বেচ্ছায়। রক্তের জন্য আপনি অর্থ চাইবেন না, দেবেন না বা নেবেন না।\n"
        "3. এই সাইটে দেখানো প্রাপ্যতা একটি সাধারণ ৬০ দিনের নিয়ম অনুসরণ করে, এটি চিকিৎসাগত ছাড়পত্র নয়। সবসময় ব্লাড সেন্টার "
        "বা চিকিৎসকের পরামর্শ মানুন।\n"
        "4. আপনি অন্য সদস্যদের যোগাযোগের তথ্যের অপব্যবহার করবেন না, কাউকে হয়রানি করবেন না, এবং ভুয়া অনুরোধ পোস্ট করবেন না।\n"
        "5. কোনো বার্তা পৌঁছেছে বা উত্তর পেয়েছে কি না তা সূর্যতরী যাচাই করতে পারে না, এবং সদস্যদের মধ্যকার ব্যবস্থার দায় নেয় না।\n"
        "6. শর্ত ভাঙলে আমরা পোস্ট লুকিয়ে দিতে বা অ্যাকাউন্ট নিষ্ক্রিয় করতে পারি।\n"
        "7. আমরা এই শর্ত হালনাগাদ করতে পারি। আপনি যে সংস্করণে সম্মত হয়েছেন তা আপনার অ্যাকাউন্টের সঙ্গে সংরক্ষিত থাকে।",
    ),
    "privacy": (
        "গোপনীয়তা নীতি",
        "আমরা কী সংগ্রহ করি\n"
        "আপনার নাম, ইমেইল, ফোন ও হোয়াটসঅ্যাপ নম্বর, মেসেঞ্জার লিংক, রাজবাড়ীর মধ্যে অবস্থান, রক্তের গ্রুপ, রক্তদানের ইতিহাস, "
        "ঐচ্ছিক প্রোফাইল ছবি, এবং সাইটে আপনার কার্যকলাপের রেকর্ড (যেমন অনুরোধ ও অডিট এন্ট্রি)।\n\n"
        "কারা দেখতে পারেন\n"
        "সাধারণ দর্শক শুধু সংক্ষিপ্ত নাম, রক্তের গ্রুপ, উপজেলা ও প্রাপ্যতা দেখতে পান। লগইন করা সদস্যরা বিস্তারিত প্রোফাইল "
        "খুলতে পারেন, তবে প্রতিটি যোগাযোগের তথ্য, আপনার এলাকা ও রক্তদানের ইতিহাস কেবল তখনই দেখা যায় যখন আপনি সেই সেটিং "
        "চালু করেছেন। সব সেটিং শুরুতে বন্ধ থাকে এবং আপনি যেকোনো সময় ‘যোগাযোগ ও গোপনীয়তা’ থেকে বদলাতে পারেন।\n\n"
        "কেন ব্যবহার করি\n"
        "রক্তদাতাদের সঙ্গে রক্তপ্রত্যাশীদের মেলাতে, কমিউনিটিকে নিরাপদ রাখতে এবং সংগঠন চালাতে।\n\n"
        "আপনার পছন্দ\n"
        "আপনি আপনার তথ্য সম্পাদনা করতে, দাতার তালিকা থেকে নিজেকে লুকাতে, বা অ্যাকাউন্ট নিষ্ক্রিয় করতে পারেন। নিরাপত্তা ও "
        "অডিটের জন্য নিষ্ক্রিয় করার পরও রক্তদান ও অনুরোধের রেকর্ড রাখা হয়। ব্যক্তিগত তথ্য সংশোধন বা মুছে ফেলার অনুরোধও "
        "করতে পারেন; প্রক্রিয়ার জন্য যোগাযোগ পাতা দেখুন।",
    ),
}

RETENTION_BN = (
    "সংরক্ষণের মেয়াদ সংগঠন নির্ধারণ করে। অ্যাকাউন্ট থাকা পর্যন্ত এবং পরে অডিটের প্রয়োজনে অ্যাকাউন্ট ও রক্তদানের রেকর্ড "
    "রাখা হয়। সংশোধন বা মুছে ফেলার অনুরোধ জানাতে সংগঠনের সঙ্গে যোগাযোগ করুন।"
)

CAMPAIGNS_BN = {
    "School Blood Group Testing Camp": (
        "স্কুলে রক্তের গ্রুপ পরীক্ষা শিবির",
        "শিক্ষার্থী ও শিক্ষকরা বন্ধুত্বপূর্ণ, তত্ত্বাবধানে থাকা একটি আয়োজনে নিজের রক্তের গ্রুপ জানতে পারবেন। স্বেচ্ছাসেবকরা "
        "বুঝিয়ে বলবেন রক্তের গ্রুপ জানা কেন জরুরি এবং স্বেচ্ছায় রক্তদান কীভাবে জীবন বাঁচায়। এটি সচেতনতা ও পরীক্ষার কার্যক্রম; "
        "কোনো রক্ত সংগ্রহ করা হবে না।",
        "রাজবাড়ী সদর (স্কুলের নাম পরে জানানো হবে)",
    ),
    "Blood Donation Awareness Programme": (
        "রক্তদান সচেতনতা কর্মসূচি",
        "নিরাপদ, নিয়মিত ও স্বেচ্ছায় রক্তদান এবং দায়িত্বশীলভাবে দাতা খোঁজা নিয়ে ছোট আলোচনা, পোস্টার ও প্রশ্নোত্তরের একটি "
        "কমিউনিটি সমাবেশ।",
        "রাজবাড়ী সদরের কমিউনিটি ভেন্যু",
    ),
}

CAMPAIGNS = [
    {
        "title": "School Blood Group Testing Camp",
        "description": (
            "Students and teachers can learn their blood group in a friendly, supervised session. "
            "Volunteers explain why knowing your blood group matters and how voluntary donation "
            "saves lives. This is an awareness and testing activity; no blood is collected."
        ),
        "start_offset": timedelta(days=14), "hours": 4, "venue": "Rajbari Sadar (exact school to be announced)",
        "static_image": "img/campaign-school-blood-group-testing.svg",
    },
    {
        "title": "Blood Donation Awareness Programme",
        "description": (
            "A community gathering with short talks, posters and a question-and-answer session on safe, "
            "regular and voluntary blood donation, and on how to find a donor responsibly."
        ),
        "start_offset": timedelta(days=-45), "hours": 3, "venue": "Rajbari Sadar community venue",
        "static_image": "img/campaign-awareness-programme.svg",
    },
]


def seed_district():
    from core.models import District, Upazila

    district, _ = District.objects.get_or_create(name="Rajbari", defaults={"name_bn": "রাজবাড়ী"})
    for name, name_bn in RAJBARI_UPAZILAS:
        Upazila.objects.get_or_create(district=district, name=name, defaults={"name_bn": name_bn})
    return district


def seed_groups():
    for group_name, entries in GROUPS.items():
        group, _ = Group.objects.get_or_create(name=group_name)
        perms = []
        for app_label, model, actions in entries:
            codenames = [f"{action}_{model}" for action in actions.split()]
            perms += list(Permission.objects.filter(content_type__app_label=app_label, codename__in=codenames))
        if perms:
            group.permissions.add(*perms)


def seed_content():
    from .models import OrganizationSettings, SiteContent

    if not OrganizationSettings.objects.exists():
        OrganizationSettings.objects.create(
            name="Surjotori",
            tagline="Blood Donation Organization",
            address="Rajbari, Bangladesh",
            retention_note=(
                "Retention periods are set by the organization. Account and donation records are kept while "
                "the account exists and for audit purposes afterwards. Contact the organization to request "
                "correction or deletion."
            ),
        )
    for key, (title, body) in PAGES.items():
        obj, _ = SiteContent.objects.get_or_create(key=key, defaults={"title": title, "body": body})
        # Add the Bangla text only while the English page is still the untouched default.
        if key in PAGES_BN and not obj.title_bn and not obj.body_bn and obj.body == body:
            obj.title_bn, obj.body_bn = PAGES_BN[key]
            obj.save(update_fields=["title_bn", "body_bn", "updated_at"])
    org = OrganizationSettings.objects.first()
    if org and not org.retention_note_bn and org.retention_note.startswith("Retention periods are set by the organization"):
        org.retention_note_bn = RETENTION_BN
        org.save()


def seed_campaigns(district):
    from campaigns.models import Campaign

    for title, (title_bn, desc_bn, venue_bn) in CAMPAIGNS_BN.items():
        Campaign.objects.filter(title=title, title_bn="").update(
            title_bn=title_bn, description_bn=desc_bn, venue_bn=venue_bn)
    if Campaign.objects.exists():
        return
    base = timezone.localtime().replace(minute=0, second=0, microsecond=0)
    for item in CAMPAIGNS:
        start = (base + item["start_offset"]).replace(hour=10)
        Campaign.objects.create(
            title=item["title"], description=item["description"], starts_at=start,
            ends_at=start + timedelta(hours=item["hours"]), venue=item["venue"], district=district,
            static_image=item["static_image"], status=Campaign.Status.PUBLISHED,
        )
    for title, (title_bn, desc_bn, venue_bn) in CAMPAIGNS_BN.items():
        Campaign.objects.filter(title=title, title_bn="").update(
            title_bn=title_bn, description_bn=desc_bn, venue_bn=venue_bn)


def seed_all():
    district = seed_district()
    seed_groups()
    seed_content()
    seed_campaigns(district)
