# AdvanceMed Knowledge Base

Source-of-truth repo for **knowledge.advancemed.com.au**, published via [documentation.ai](https://advancemed.documentationai.com).

Pushes to `main` trigger an automatic build and deploy.

## Repo layout

```
.
├── documentation.json     ← navigation / IA — controls sidebar and tabs
├── introduction.mdx       ← Documentation tab — entry page
├── quickstart.mdx         ← Documentation tab — orientation
├── features.mdx           ← Documentation tab — services overview
├── coaching-guide.mdx     ← Documentation tab — full coaching flow
├── changelog.mdx          ← Changelog tab
├── private-documentation.mdx  ← Documentation tab — gated content placeholder
├── help-center.mdx        ← Help Center landing (initialRoute)
├── help-center/
│   ├── getting-started/   (4 pages — orientation, about, testimonials)
│   ├── services/          (11 pages — calls, CV, cover letters, courses, pricing)
│   ├── international-medical-graduates/  (9 pages — pathways, exams, visas)
│   ├── career-pathways/   (6 pages — psychiatry, nursing, AHPRA, sectors)
│   ├── recruitment-and-practice/  (6 pages — interviews, agencies, CPD)
│   ├── account-and-billing/  (7 pages — subs, refunds, privacy, support)
│   ├── faq/               (1 page)
│   ├── guides/            (1 page)
│   └── troubleshooting/   (1 page)
├── api-reference/
│   └── openapi.yaml       ← API tab — empty shell
└── scripts/
    └── plausible.js       ← analytics for knowledge.advancemed.com.au
```

**Total:** 53 pages, all reachable from the navigation.

## What's been done (v0.1.0 — 2026-05-09)

### Migrated from `help.advancemed.com.au` (29 → 24 pages)

Help Scout export, restructured into the topic-based Help Center IA. 5 merges:

- 30 + 31 → `become-a-psychiatrist-australia.mdx`
- 33 + 35 + 50 → `psychiatrist-income-australia.mdx`
- 18 + 47 → `img-internship.mdx`
- 6 + 34 → `cover-letters-and-selection-criteria.mdx`

See `_mapping.json` for the full source-to-destination mapping.

### Net-new pages (19)

| Section | New page |
|---|---|
| Getting Started | About Dr Anthony Llewellyn |
| Getting Started | What clients say (testimonials placeholder — needs population) |
| Services | Pricing summary |
| Services | What to expect from a coaching series |
| Services | VisualCV licence |
| Services | What a strong doctor CV looks like |
| Services | Group coaching and cohort programs |
| IMG | The Standard Pathway |
| IMG | The Competent Authority Pathway |
| IMG | Visa types relevant to doctors |
| Career Pathways | AHPRA registration timeline |
| Career Pathways | Australian specialist medical colleges |
| Career Pathways | Public vs private practice |
| Recruitment & Practice | Medical interview formats by employer |
| Account & Billing | Refund and cancellation policy |
| Account & Billing | Privacy and how we handle your data |
| Account & Billing | Contact and support |
| Account & Billing | Session recordings |
| Account & Billing | How to reschedule or rebook |

### Seed cleanup

The documentation.ai scaffold's AI-generated pages have been rewritten with real content — they previously referenced fictional URLs (`dashboard.advancemed.com`, `ai.advancemed.com.au/career-advisor`, `support@advancemed.com`) and a fabricated changelog. Pages rewritten:

- `introduction.mdx`, `quickstart.mdx`, `features.mdx`, `coaching-guide.mdx`
- `changelog.mdx` (reset to v0.1.0 launch entry)
- `help-center.mdx` (landing page, real card targets)
- `help-center/faq/how-to-access-dashboard.mdx`
- `help-center/guides/submit-your-cv.mdx`
- `help-center/troubleshooting/cannot-reset-password.mdx`

## TODOs flagged inside files

- **Testimonials** (`help-center/getting-started/testimonials.mdx`) — placeholder; live `our-fans` page renders dynamically and didn't migrate. Anthony to paste 6–8 favourite testimonials.
- **Article 49 / AMC exemptions** — original title used `"....."` as a placeholder. Page now reads as a generic Q&A; consider splitting into per-exam pages (USMLE, MRCP, PLAB, LMCC).
- **Article 36 / Immigration** — currently a stub pointing to `advancemed.com.au/migrating-to-australia-as-a-doctor`. Decide whether to inline.
- **IMG internship** — original article had an embedded video that didn't migrate. Add the video URL.
- **Group coaching** — page is a generic placeholder. Replace with current cohort programs (or convert to "register interest").

## Editorial standards

- **General advice only** — explicit caveats added on migration, registration, financial, legal, clinical topics
- **Australian English** spelling and conventions
- **Authoritative sources cited** for AMC, AHPRA, Medical Board, MARA
- **Strong "we don't do that" sections** on every page where confusion is common
- All cross-links use **absolute paths from repo root** (`/help-center/services/...`)
- Frontmatter `title` and `description` on every page (required by documentation.ai)

## Brand notes

- **Brand colours**: `#fc5708` (light), `#F98C58` (dark) — preserved from seed; please confirm against AdvanceMed brand guide
- **Logo and favicon**: real CDN URLs preserved from seed
- **Domain**: `knowledge.advancemed.com.au` (Plausible analytics already wired)
- **Template**: `atlas`
- **Initial route**: `help-center` — site lands users on the help centre, not the Documentation tab

## Local preview

Documentation.ai supports a local preview workflow — see [Code Editor docs](https://documentation.ai/docs/write-and-publish/code-editor). Verify any major change locally before pushing.

## Contributing — adding a new page

1. Create the `.mdx` file under the right section folder.
2. Add `title` + `description` to the frontmatter.
3. Add the page to `documentation.json` under the correct group.
4. Use absolute paths for internal links: `/help-center/services/<page>`.
5. Open a PR — documentation.ai builds a preview build automatically.

## Source content

- Public help: [help.advancemed.com.au](https://help.advancemed.com.au)
- Terms: [advancemed.com.au/terms](https://advancemed.com.au/terms/)
- Privacy: [advancemed.com.au/privacy](https://advancemed.com.au/privacy/)
- About: [advancemed.com.au/about](https://advancemed.com.au/about/)
- Wall of Love: [advancemed.com.au/our-fans](https://advancemed.com.au/our-fans/)
