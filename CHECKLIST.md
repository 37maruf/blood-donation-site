# CHECKLIST (ID | feature | status)
Status: WRITTEN = code present, NOT YET RUN (Django could not be installed in the build sandbox). Verify with the steps in README.

| ID | Feature | Status |
|----|---------|--------|
| R1 | Registration (one account, validation, atomic create, image processing) | WRITTEN |
| R2 | Eligibility (Python + SQL, shared tests) | WRITTEN |
| R3 | Willingness + audit | WRITTEN |
| R4 | Blood Need / General request / Direct request kept distinct | WRITTEN |
| R5 | Blood Need posts (public summary, respond, close, never delete) | WRITTEN |
| R6 | Direct requests + locked state machine + notifications + audit | WRITTEN |
| R7 | Contact via POST redirect, ContactAttempt, no hidden values in HTML | WRITTEN |
| R8 | Masked public list, detailed profile for logged-in members, filters | WRITTEN |
| R9 | Donation records (staff only, audited) | WRITTEN |
| R10 | Campaigns (list/detail/register/capacity/notify/archive) | WRITTEN |
| R11 | Home (stats cached 5 min, campaigns, About/Contact from admin content) | WRITTEN |
| R12 | Member dashboard + staff groups | WRITTEN |
| R13 | Auth (email login, instant membership - no email verification, reset, throttles, POST logout) | WRITTEN |
| R14 | Reports + DB throttling | WRITTEN |
| R15 | In-site notifications | WRITTEN |
| R16 | Terms/Privacy pages, deactivation, staff activate/deactivate, hide posts | WRITTEN |
| SEC | Prod settings, 403/404/500, /health/, cron endpoint | WRITTEN |
| TEST | pytest suite (eligibility parity, registration, privacy/contact, requests) | WRITTEN, NOT RUN |
| MIG | Migrations generated and applied | DONE (accounts 0002 drops email_verified_at; content/campaigns add Bangla fields) |
| UI | Redesign, English/Bangla switch (cookie), light/dark theme | DONE |
