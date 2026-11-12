# DECISIONS

| # | Decision | Why |
|---|----------|-----|
| D1 | Site is **Rajbari-only**. `District`/`Upazila` models kept, seeded with Rajbari + its 5 upazilas (Rajbari Sadar, Goalanda, Pangsha, Baliakandi, Kalukhali). Forms offer only Rajbari. | Requirement from owner; models stay generic so another district is a data change. |
| D2 | Seeding runs from a `post_migrate` handler in `content/apps.py` (+ `manage.py seed_initial`) instead of a hand-written data migration. | Migrations could not be generated offline; the handler is idempotent and also builds staff groups after all permissions exist. |
| D3 | `makemigrations` must be run once before `migrate` (no migration files are shipped). Custom `accounts.User` is in place before the first migration. | Django was not installable in the build sandbox. |
| D4 | DB credentials come only from env vars / `.env` (`DB_NAME` default `blood_donatio_site`, `DB_PASSWORD` has no default) or `DATABASE_URL`. | Never commit or print secrets. Put the local password in `.env`. |
| D5 | Email: any Django backend chosen via `EMAIL_BACKEND` (console by default). | Provider-agnostic; set the provider's backend/SMTP in Vercel env. |
| D6 | Media: S3-compatible via django-storages when `AWS_STORAGE_BUCKET_NAME` is set (private ACL, signed URLs); local `./media` otherwise. Cloudinary not wired. | Vercel has no persistent disk. |
| D7 | Profile photos are re-encoded to WEBP (<=1024px) which strips EXIF/ICC. Max 2 MB, JPG/PNG/WEBP, 100-4000px. | R1 requirement. |
| D8 | Broadcast notifications are visible only if created after the member joined. | New members are not flooded with old broadcasts; still one row per broadcast. |
| D9 | `MemberPrivacy` and `NotificationRead` hang off `User` (not profile). Donor URLs use the profile id. | Matches the model spec (1:1 User). |
| D10 | Area search only matches donors with `show_area=True`. | Prevents inferring a hidden area through search. |
| D11 | Donor-only values (blood group, never-donated, last donation date) are cleared for members who are not donors. | R1. |
| D12 | Bootstrap 5.3.3 is loaded from jsDelivr (no SRI hash, no CSP header). | No network to compute hashes; add SRI/CSP before launch. |
| D13 | Dependencies use compatible ranges; run `pip freeze > requirements.lock` after install and pin. | Exact patch versions could not be verified offline. |
| D14 | Staff statistics page at `/dashboard/staff/`; everything else staff-side uses the Django admin with group permissions. | Lean build. |
| D15 | Sample campaigns (from the two supplied photos) are seeded as editable admin data; venues are placeholders. | Owner can replace via admin. |
| D16 | Org phone/email are blank (shown only when filled). About/Home/Contact/Terms/Privacy text is original and editable in admin > Site content pages. | Avoids inventing contact details. |
| D17 | **No email verification.** Registering makes you a full member at once (listed as a donor, can post and request). The `email_verified_at` column was removed (migration `accounts.0002`). | Owner request. |
| D18 | **Language** (English / Bangla) is a cookie set by `/lang/<en|bn>/`; first visit follows the browser. Fixed template text uses `{% t "English" "বাংলা" %}`; text produced by Python is looked up in `core/bn.py` through `\|tr`. Missing entries fall back to English. | No translation toolchain needed; works for forms, flash messages and choice lists. |
| D19 | About / Terms / Privacy / Home intro and campaigns have optional `*_bn` fields, editable in admin; seeded Bangla text is added only where the English text is still the default. | Admin-edited content is never overwritten. |
| D20 | **Theme**: light/dark via Bootstrap `data-bs-theme`, saved in `localStorage` (`sj-theme`), defaults to the device setting. Fonts: Bricolage Grotesque + Hind Siliguri (Google Fonts). | |
