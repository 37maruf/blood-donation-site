# Surjotori Blood Donation Platform (Rajbari district)

Django 5.2 + PostgreSQL + Bootstrap 5. One district: **Rajbari**.

## Local setup
```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env          # then edit: DEBUG=True, DJANGO_SECRET_KEY, DB_PASSWORD
createdb blood_donatio_site   # or create it in pgAdmin
python manage.py migrate      # also seeds Rajbari, staff groups, site pages, 2 sample campaigns
python manage.py createsuperuser
python manage.py check
pytest
python manage.py runserver
```
Admin: `/admin/`. Give staff the groups Content Manager, Campaign Manager, Donation Manager,
Request Moderator, User Support (tick *Staff status* on the user). Edit About/Home/Contact/Terms/Privacy
under *Site content pages* and phone/email/social links under *Organization settings*.

## Language and theme
Visitors switch **EN / বাং** and light / dark in the header. To translate new Python-side text, add it to `core/bn.py`; fixed text in templates uses `{% t "English" "বাংলা" %}`. Bangla page content is edited in admin (fields ending *(Bangla)*).

## Deploy (Vercel + external Postgres)
* Env vars: `DEBUG=False`, `DJANGO_SECRET_KEY`, `DATABASE_URL`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`,
  email vars, S3 vars (media), `CRON_SECRET`, optional `SENTRY_DSN`. Use a separate DB for previews.
* Build: `build_files.sh` runs `collectstatic` (WhiteNoise). Migrations are a separate release step:
  `python manage.py migrate --noinput` (never on cold start).
* `vercel.json` rewrites everything to `api/index.py` and registers a daily cron on
  `/internal/cron/cleanup/` (needs `CRON_SECRET`). Verify current Vercel plan/cron limits.
* Run `python manage.py check --deploy` with production env before launch; raise `SECURE_HSTS_SECONDS` gradually.
* Back up PostgreSQL and the media bucket, and test a restore.

## Data correction / deletion
Members can edit data, hide themselves (inactive) or deactivate. Correction/deletion requests are
handled by staff after identity confirmation (see Contact page text).

See `DECISIONS.md` and `CHECKLIST.md`.
