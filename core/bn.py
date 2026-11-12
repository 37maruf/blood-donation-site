"""Bangla versions of every English string that Python code sends to the screen.

Templates use `{% t "English" "বাংলা" %}` for fixed text. Text created in Python (form labels,
help texts, flash messages, choice names, validation errors) is translated by the `|tr` template
filter, which looks the exact English text up here. Anything missing simply stays in English,
so adding a new message never breaks a page - add its Bangla version here when you can.
"""

BN = {
    # ---------------------------------------------------------------- page titles, buttons, intros
    "Join Surjotori": "সূর্যতরীতে যোগ দিন",
    "Create account": "অ্যাকাউন্ট খুলুন",
    "One account for everyone: donate, request blood, or both. All fields are required unless marked optional.":
        "সবার জন্য একটি অ্যাকাউন্ট: রক্ত দিন, রক্ত চান, কিংবা দুটোই। ঐচ্ছিক লেখা না থাকলে সব ঘর পূরণ করতে হবে।",
    "Edit profile": "প্রোফাইল সম্পাদনা",
    "Save changes": "পরিবর্তন সংরক্ষণ করুন",
    "Save": "সংরক্ষণ করুন",
    "Contact & privacy": "যোগাযোগ ও গোপনীয়তা",
    "Save settings": "সেটিংস সংরক্ষণ করুন",
    "Everything is OFF by default. Only what you switch on is shown, and only to logged-in members.":
        "সবকিছু শুরুতে বন্ধ থাকে। আপনি যেটি চালু করবেন শুধু সেটিই দেখা যাবে, তাও কেবল লগইন করা সদস্যদের কাছে।",
    "Donation willingness": "রক্তদানের আগ্রহ",
    "Inactive members are removed from donor lists. When reactivating, confirm your last donation.":
        "নিষ্ক্রিয় সদস্যরা রক্তদাতার তালিকা থেকে বাদ পড়েন। আবার সক্রিয় হলে আপনার সর্বশেষ রক্তদানের তথ্য নিশ্চিত করুন।",
    "Post a blood need": "রক্তের প্রয়োজন পোস্ট করুন",
    "Publish request": "অনুরোধ প্রকাশ করুন",
    "This post is PUBLIC. Patient name and contact stay hidden unless you tick the options.":
        "এই পোস্টটি সবার জন্য উন্মুক্ত। আপনি টিক না দিলে রোগীর নাম ও যোগাযোগের নম্বর গোপন থাকবে।",
    "Edit blood need": "রক্তের প্রয়োজন সম্পাদনা",
    "Request blood (private)": "রক্তের অনুরোধ (ব্যক্তিগত)",
    "Submit for review": "পর্যালোচনার জন্য পাঠান",
    "Only you and our review team can see this. We will contact you; nothing is published automatically.":
        "শুধু আপনি এবং আমাদের পর্যালোচনা দল এটি দেখতে পাবে। আমরা আপনার সঙ্গে যোগাযোগ করব; কিছুই স্বয়ংক্রিয়ভাবে প্রকাশ হবে না।",
    "Send request": "অনুরোধ পাঠান",
    "Your request is private to this donor. The donor may accept or decline.":
        "আপনার অনুরোধটি শুধু এই দাতার কাছে যাবে। দাতা গ্রহণ বা প্রত্যাখ্যান করতে পারেন।",
    "Reset your password": "পাসওয়ার্ড রিসেট করুন",
    "Send reset link": "রিসেট লিংক পাঠান",
    "Enter your account email. If it exists, we will send reset instructions.":
        "আপনার অ্যাকাউন্টের ইমেইল দিন। অ্যাকাউন্টটি থাকলে আমরা রিসেটের নির্দেশনা পাঠাব।",
    "Choose a new password": "নতুন পাসওয়ার্ড বেছে নিন",
    "Change password": "পাসওয়ার্ড পরিবর্তন করুন",
    "Check your email": "আপনার ইমেইল দেখুন",
    "If an account exists for that address, reset instructions are on their way.":
        "ওই ঠিকানায় অ্যাকাউন্ট থাকলে রিসেটের নির্দেশনা পাঠানো হচ্ছে।",
    "Password changed": "পাসওয়ার্ড পরিবর্তন হয়েছে",
    "You can now log in with your new password.": "এখন নতুন পাসওয়ার্ড দিয়ে লগইন করতে পারবেন।",

    # ---------------------------------------------------------------- flash messages
    "Too many attempts. Please try again later.": "অনেকবার চেষ্টা করা হয়েছে। পরে আবার চেষ্টা করুন।",
    "Welcome to Surjotori! Your account is ready.": "সূর্যতরীতে স্বাগতম! আপনার অ্যাকাউন্ট প্রস্তুত।",
    "Too many login attempts. Please wait a few minutes.": "অনেকবার লগইনের চেষ্টা হয়েছে। কয়েক মিনিট অপেক্ষা করুন।",
    "You have been logged out.": "আপনি লগআউট হয়েছেন।",
    "Password changed.": "পাসওয়ার্ড পরিবর্তন হয়েছে।",
    "Email updated.": "ইমেইল হালনাগাদ হয়েছে।",
    "Your account was deactivated. Contact the organization to reactivate or request data correction/deletion.":
        "আপনার অ্যাকাউন্ট নিষ্ক্রিয় করা হয়েছে। আবার চালু করতে বা তথ্য সংশোধন/মুছে ফেলার অনুরোধ জানাতে সংগঠনের সঙ্গে যোগাযোগ করুন।",
    "This account has no member profile.": "এই অ্যাকাউন্টের কোনো সদস্য প্রোফাইল নেই।",
    "Profile updated.": "প্রোফাইল হালনাগাদ হয়েছে।",
    "Contact & privacy settings saved.": "যোগাযোগ ও গোপনীয়তার সেটিংস সংরক্ষিত হয়েছে।",
    "Turn on 'I want to donate' in your profile first.": "আগে প্রোফাইলে ‘আমি রক্ত দিতে চাই’ চালু করুন।",
    "Donation settings saved.": "রক্তদানের সেটিংস সংরক্ষিত হয়েছে।",
    "Your blood need is now public and members were notified.":
        "আপনার রক্তের প্রয়োজন এখন প্রকাশিত হয়েছে এবং সদস্যদের জানানো হয়েছে।",
    "Closed posts cannot be edited.": "বন্ধ পোস্ট সম্পাদনা করা যায় না।",
    "Post updated.": "পোস্ট হালনাগাদ হয়েছে।",
    "Post closed.": "পোস্ট বন্ধ করা হয়েছে।",
    "Thank you! The owner has been notified.": "ধন্যবাদ! পোস্টদাতাকে জানানো হয়েছে।",
    "Request submitted. Our team will review it; it is not made public.":
        "অনুরোধ জমা হয়েছে। আমাদের দল এটি দেখবে; এটি প্রকাশ করা হবে না।",
    "This donor is not accepting direct requests.": "এই দাতা সরাসরি অনুরোধ নিচ্ছেন না।",
    "Request sent. The donor has been notified.": "অনুরোধ পাঠানো হয়েছে। দাতাকে জানানো হয়েছে।",
    "Request updated.": "অনুরোধ হালনাগাদ হয়েছে।",
    "You are registered. See you there!": "আপনার নিবন্ধন সম্পন্ন। সেখানে দেখা হবে!",
    "You have used many contact links recently. Please try again later.":
        "আপনি সম্প্রতি অনেকবার যোগাযোগের লিংক ব্যবহার করেছেন। পরে আবার চেষ্টা করুন।",
    "You are sending reports too quickly. Please try again later.":
        "আপনি খুব দ্রুত রিপোর্ট পাঠাচ্ছেন। পরে আবার চেষ্টা করুন।",
    "Thank you. Our team will review your report.": "ধন্যবাদ। আমাদের দল আপনার রিপোর্ট দেখবে।",
    "The report could not be submitted. Please check the details and try again.":
        "রিপোর্ট জমা দেওয়া যায়নি। তথ্য দেখে আবার চেষ্টা করুন।",
    "You are doing that too often. Please try again later.": "আপনি খুব ঘন ঘন এটি করছেন। পরে আবার চেষ্টা করুন।",

    # ---------------------------------------------------------------- service errors
    "Only the owner can close this post.": "শুধু পোস্টদাতাই এই পোস্ট বন্ধ করতে পারেন।",
    "Invalid status.": "অবৈধ অবস্থা।",
    "This post is already closed.": "এই পোস্ট আগেই বন্ধ হয়েছে।",
    "This request is no longer active.": "এই অনুরোধ আর সক্রিয় নেই।",
    "You cannot respond to your own post.": "নিজের পোস্টে সাড়া দেওয়া যায় না।",
    "You have already offered to help with this request.": "আপনি এই অনুরোধে আগেই সাহায্যের প্রস্তাব দিয়েছেন।",
    "You cannot send a request to yourself.": "নিজেকে অনুরোধ পাঠানো যায় না।",
    "This donor cannot receive requests right now.": "এই দাতা এখন অনুরোধ নিতে পারছেন না।",
    "You already have a pending request to this donor.": "এই দাতার কাছে আপনার একটি অনুরোধ আগে থেকেই অপেক্ষমাণ।",
    "Unknown action.": "অজানা কাজ।",
    "You cannot change this request.": "আপনি এই অনুরোধ পরিবর্তন করতে পারেন না।",
    "That action is not allowed in the request's current state.": "অনুরোধের বর্তমান অবস্থায় এই কাজটি করা যায় না।",
    "This campaign has already ended.": "এই কর্মসূচি শেষ হয়ে গেছে।",
    "You are already registered for this campaign.": "আপনি এই কর্মসূচিতে আগেই নিবন্ধন করেছেন।",
    "Sorry, this campaign is full.": "দুঃখিত, এই কর্মসূচিতে আর জায়গা নেই।",

    # ---------------------------------------------------------------- validation errors
    "You cannot report yourself.": "নিজেকে রিপোর্ট করা যায় না।",
    "That item could not be found.": "জিনিসটি খুঁজে পাওয়া যায়নি।",
    "A donation date cannot be in the future.": "রক্তদানের তারিখ ভবিষ্যতের হতে পারে না।",
    "Enter a valid Bangladeshi mobile number, e.g. 01XXXXXXXXX.": "সঠিক বাংলাদেশি মোবাইল নম্বর দিন, যেমন 01XXXXXXXXX।",
    "Use a link from facebook.com, fb.com, m.me or messenger.com.": "facebook.com, fb.com, m.me বা messenger.com থেকে একটি লিংক দিন।",
    "Choose at least one: 'I want to donate' or 'I may need blood'.":
        "অন্তত একটি বেছে নিন: ‘আমি রক্ত দিতে চাই’ অথবা ‘আমার রক্ত লাগতে পারে’।",
    "This upazila does not belong to the selected district.": "এই উপজেলা নির্বাচিত জেলার অন্তর্গত নয়।",
    "Blood group is required for donors.": "রক্তদাতাদের জন্য রক্তের গ্রুপ দেওয়া আবশ্যক।",
    "Choose either 'never donated' or a last donation date, not both.":
        "‘কখনো রক্ত দিইনি’ অথবা সর্বশেষ রক্তদানের তারিখ — যেকোনো একটি দিন, দুটো নয়।",
    "Tell us your last donation date, or tick 'never donated'.":
        "সর্বশেষ রক্তদানের তারিখ জানান, অথবা ‘কখনো রক্ত দিইনি’ টিক দিন।",
    "The last donation date cannot be in the future.": "সর্বশেষ রক্তদানের তারিখ ভবিষ্যতের হতে পারে না।",
    "The required date cannot be in the past.": "প্রয়োজনের তারিখ অতীতের হতে পারবে না।",
    "Units must be between 1 and 20.": "ইউনিট ১ থেকে ২০ এর মধ্যে হতে হবে।",
    "An account with this email already exists.": "এই ইমেইলে আগেই একটি অ্যাকাউন্ট আছে।",
    "The two passwords do not match.": "দুটি পাসওয়ার্ড মেলেনি।",
    "Password is incorrect.": "পাসওয়ার্ড সঠিক নয়।",
    "That email cannot be used.": "এই ইমেইলটি ব্যবহার করা যাবে না।",
    "The image must be 2 MB or smaller.": "ছবির আকার সর্বোচ্চ ২ এমবি হতে পারবে।",
    "Upload a valid JPG, PNG or WEBP image.": "সঠিক JPG, PNG বা WEBP ছবি আপলোড করুন।",
    "Image sides must be between 100px and 4000px.": "ছবির দৈর্ঘ্য ও প্রস্থ ১০০ থেকে ৪০০০ পিক্সেলের মধ্যে হতে হবে।",

    # ---------------------------------------------------------------- form labels and help
    "Full name": "পূর্ণ নাম",
    "Email": "ইমেইল",
    "Password": "পাসওয়ার্ড",
    "Confirm password": "পাসওয়ার্ড নিশ্চিত করুন",
    "Phone": "ফোন",
    "Whatsapp number": "হোয়াটসঅ্যাপ নম্বর",
    "Messenger url": "মেসেঞ্জার লিংক",
    "District": "জেলা",
    "Upazila": "উপজেলা",
    "Select upazila": "উপজেলা বেছে নিন",
    "Area / village / road": "এলাকা / গ্রাম / রাস্তা",
    "Profile image": "প্রোফাইল ছবি",
    "I want to donate blood": "আমি রক্ত দিতে চাই",
    "I may need blood": "আমার রক্ত লাগতে পারে",
    "Blood group": "রক্তের গ্রুপ",
    "I have never donated blood": "আমি কখনো রক্ত দিইনি",
    "Last donation date": "সর্বশেষ রক্তদানের তারিখ",
    "I accept the Terms of Use and have read the Privacy Notice.": "আমি ব্যবহারের শর্তে সম্মত এবং গোপনীয়তা নীতি পড়েছি।",
    "Bangladeshi mobile number, e.g. 01XXXXXXXXX.": "বাংলাদেশি মোবাইল নম্বর, যেমন 01XXXXXXXXX।",
    "Your Facebook / Messenger profile link (facebook.com, fb.com, m.me, messenger.com).":
        "আপনার ফেসবুক / মেসেঞ্জার প্রোফাইলের লিংক (facebook.com, fb.com, m.me, messenger.com)।",
    "Optional. JPG, PNG or WEBP up to 2 MB.": "ঐচ্ছিক। JPG, PNG বা WEBP, সর্বোচ্চ ২ এমবি।",
    "Required for donors unless you have never donated.": "কখনো রক্ত না দিয়ে থাকলে ছাড়া দাতাদের জন্য আবশ্যক।",
    "Show my phone number to logged-in members": "লগইন করা সদস্যদের আমার ফোন নম্বর দেখান",
    "Allow WhatsApp contact": "হোয়াটসঅ্যাপে যোগাযোগের অনুমতি দিন",
    "Allow Messenger contact": "মেসেঞ্জারে যোগাযোগের অনুমতি দিন",
    "Show my completed donations": "আমার সম্পন্ন রক্তদান দেখান",
    "Show my area (and allow area search)": "আমার এলাকা দেখান (এবং এলাকা দিয়ে খোঁজার অনুমতি দিন)",
    "Receive direct donation requests": "সরাসরি রক্তদানের অনুরোধ গ্রহণ করুন",
    "Any blood group": "যেকোনো রক্তের গ্রুপ",
    "Any upazila": "যেকোনো উপজেলা",
    "Area": "এলাকা",
    "Patient name": "রোগীর নাম",
    "Show patient name publicly": "রোগীর নাম সবার সামনে দেখান",
    "Units": "ইউনিট",
    "Hospital name": "হাসপাতালের নাম",
    "Hospital location": "হাসপাতালের অবস্থান",
    "Required date": "প্রয়োজনের তারিখ",
    "Contact phone": "যোগাযোগের ফোন",
    "Only shown to logged-in members, and only if you tick the box below.":
        "শুধু লগইন করা সদস্যদের দেখানো হবে, এবং নিচের বক্সে টিক দিলেই।",
    "Show contact number to logged-in members": "লগইন করা সদস্যদের যোগাযোগের নম্বর দেখান",
    "Urgency": "জরুরি অবস্থা",
    "Details": "বিস্তারিত",
    "Status": "অবস্থা",
    "Message": "বার্তা",
    "Optional short message to the family": "পরিবারের জন্য ঐচ্ছিক ছোট বার্তা",
    "Hospital": "হাসপাতাল",
    "Location": "অবস্থান",
    "Contact": "যোগাযোগ",
    "Current password": "বর্তমান পাসওয়ার্ড",
    "New password": "নতুন পাসওয়ার্ড",
    "Confirm new password": "নতুন পাসওয়ার্ড নিশ্চিত করুন",
    "New email": "নতুন ইমেইল",
    "I understand my account will be deactivated (my records are kept).":
        "আমি বুঝি যে আমার অ্যাকাউন্ট নিষ্ক্রিয় হবে (আমার রেকর্ড সংরক্ষিত থাকবে)।",

    # ---------------------------------------------------------------- choices
    "---------": "---------",
    "Normal": "সাধারণ", "Urgent": "জরুরি", "Critical": "অতি জরুরি",
    "Active": "সক্রিয়", "Inactive": "নিষ্ক্রিয়",
    "Fulfilled": "পূরণ হয়েছে", "Cancelled": "বাতিল", "All": "সব",
    "Pending": "অপেক্ষমাণ", "Accepted": "গৃহীত", "Rejected": "প্রত্যাখ্যাত", "Completed": "সম্পন্ন",
    "Submitted": "জমা হয়েছে", "Under review": "পর্যালোচনাধীন", "Matched": "মিলেছে",
    "Draft": "খসড়া", "Published": "প্রকাশিত", "Archived": "সংরক্ষণাগারে",
    "Spam or scam": "স্প্যাম বা প্রতারণা", "Fake or misleading": "ভুয়া বা বিভ্রান্তিকর",
    "Abusive behaviour": "অশোভন আচরণ", "Privacy concern": "গোপনীয়তা নিয়ে উদ্বেগ", "Other": "অন্যান্য",
    "Upcoming": "আসন্ন", "Past": "অতীত", "Ongoing": "চলমান", "Upcoming & ongoing": "আসন্ন ও চলমান",

    # ---------------------------------------------------------------- eligibility
    "Available to donate.": "রক্ত দিতে প্রস্তুত।",
    "Willing to donate, not currently listed under the 60-day rule.":
        "রক্ত দিতে ইচ্ছুক, তবে ৬০ দিনের নিয়মে এখন তালিকাভুক্ত নন।",
    "Set to inactive: hidden from donor lists and direct requests.":
        "নিষ্ক্রিয় করা আছে: দাতার তালিকা ও সরাসরি অনুরোধ থেকে লুকানো।",
    "Turn on 'I want to donate' in your profile to be listed.":
        "তালিকাভুক্ত হতে প্রোফাইলে ‘আমি রক্ত দিতে চাই’ চালু করুন।",
    "Confirm your donation history (never donated, or your last donation date) to be listed.":
        "তালিকাভুক্ত হতে আপনার রক্তদানের ইতিহাস (কখনো দেননি, অথবা সর্বশেষ রক্তদানের তারিখ) নিশ্চিত করুন।",
    "This account is inactive.": "এই অ্যাকাউন্ট নিষ্ক্রিয়।",
    "Availability follows this website's 60-day rule only. It is not medical clearance - blood centres decide who can donate.":
        "প্রাপ্যতা শুধু এই ওয়েবসাইটের ৬০ দিনের নিয়ম অনুসরণ করে। এটি চিকিৎসাগত ছাড়পত্র নয় — কে রক্ত দিতে পারবেন তা ব্লাড সেন্টার ঠিক করে।",

    # ---------------------------------------------------------------- organisation
    "Surjotori": "সূর্যতরী",
    "Blood Donation Organization": "রক্তদান সংগঠন",
    "Member": "সদস্য",
}


def translate(text):
    """Bangla version of `text` when Bangla is the active language, otherwise `text` unchanged."""
    from django.utils import translation

    if text is None or not (translation.get_language() or "en").startswith("bn"):
        return text
    return BN.get(str(text).strip(), text)
