# Project: FreelanceToolkit Global Scaling & Organic Distribution

## Architecture
- **Platform Stack**: Zero-dependency, pure static HTML5 / Modern CSS (Vanilla + Tailwind utilities) / Client-side JavaScript / Browser-native Print-to-PDF / LocalStorage persistence.
- **Hosting & Infrastructure**: GitHub Pages deployment (`https://komasan19283645.github.io/freelance-toolkit/`), synchronized with GitHub repository `komasan19283645/freelance-toolkit`.
- **Commerce & Checkout Engine**: Gumroad digital products (`https://migueldp3.gumroad.com/l/...`) with promo code `LANZAMIENTO20` support.
- **International Architecture**:
  - Spanish Core: `index.html`, `calculator.html`, `store.html`, `contracts.html`, and guides (`como-hacer-factura-autonomo-irpf-iva.html`, `ventas-vinted-wallapop-hacienda-dac7.html`, `metodo-50-30-20-presupuesto-espanol.html`).
  - English Platform: `index-en.html`, `calculator-en.html`, `store-en.html`.
  - Multi-Currency: USD ($), EUR (€), GBP (£), CAD (CA$), AUD (A$).
  - Pricing Engine: $9 individual systems, $39 8-in-1 Suite, $0 Free Starter Pack.
  - SEO Layer: `sitemap.xml` with `xmlns:xhtml`, `robots.txt`, bidirectional hreflang alternates, canonical tags, Open Graph and Twitter Card tags (`@Komaleon37`).
- **Distribution & Marketing Layer**:
  - Multi-channel educational acquisition across authorized pseudonym channels: Reddit (`u/Komaleon`), X/Twitter (`@Komaleon37`), Pinterest (`@migueldpsp`).
  - Strict zero-commercial links on Reddit (educational GitHub Pages only).
  - Human-like pacing distribution engine (45–90s delays).
- **Identity Shielding & Privacy Guardrail**:
  - Total shielding of personal email, real names, academic records, and personal LinkedIn.
  - Commits configured with `komasan19283645@users.noreply.github.com`.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| F1 | English Web Core | Fully functioning `index-en.html`, `calculator-en.html`, `store-en.html` | M1 | R1 |
| F2 | Multi-Currency Engine | USD ($), EUR (€), GBP (£), CAD (CA$), AUD (A$) support in calculator and invoice | M1 | R1 |
| F3 | International Pricing Model | $9 individual products, $39 8-in-1 Suite, $0 Free Starter Pack with LANZAMIENTO20 promo | M1 | R1 |
| F4 | High-Converting CRO Elements | Post-PDF generation download modal for Finance Hub ($9) and rate-negotiation cards linking to Email Swipe File Pro | M1 | R1 |
| F5 | Bidirectional Language Switchers | `[ 🇪🇸 ES | 🇬🇧 EN ]` in desktop headers and mobile drawer menus across all 10 pages | M1 | R1 |
| F6 | Invoice Print & Persistence Fix | Fix `#printable-document` print CSS selector in `index-en.html` and implement localStorage persistence | M1 | R1 |
| F7 | Programmatic Sitemap Architecture | `sitemap.xml` with 10 endpoints, `xmlns:xhtml`, and bidirectional `xhtml:link` alternates | M2 | R2 |
| F8 | Canonical & International Hreflang | `<link rel="canonical">` and `<link rel="alternate" hreflang="...">` across all 10 HTML files | M2 | R2 |
| F9 | Meta & Social Tag Validation | `<meta name="description">` on `calculator.html`, `twitter:creator` (`@Komaleon37`), Open Graph tags | M2 | R2 |
| F10 | Synchronized Bilingual README | Synchronized `README.md` with Spanish & English sections, live English links, USD pricing, topic badges | M2 | R2 |
| F11 | Reddit Organic Distribution Engine | `marketing/reddit_campaign_distribution.md` with 4 educational blueprints and zero direct Gumroad links | M3 | R3 |
| F12 | X / Twitter Thread Campaign | `marketing/x_twitter_campaign_threads.md` with 4 value threads, preview cards, `@Komaleon37` branding | M3 | R3 |
| F13 | International Pinterest Pins | `marketing/pinterest_campaign_pins_international.md` with 10 vertical 2:3 pins for ES and EN queries | M3 | R3 |
| F14 | Marketing Copy Quarantine & Cleanup | Purge Gumroad links in Reddit copy and quarantine LinkedIn in `marketing/posts_redes_sociales.md` | M3 | R3 & R4 |
| F15 | Distribution Automation Script | `scripts/distribute_organic_campaign.py` with 45–90s pacing simulation and zero-Gumroad validation | M3 | R3 |
| F16 | Automated Link & Page Validator | Automated test script verifying internal links, language switches, stylesheets, zero 404s | Test Track | R1 & R2 |
| F17 | Sitemap XML Schema Validator | Automated test script verifying well-formed XML and complete 10-URL enumeration | Test Track | R2 |
| F18 | Dynamic Calculator & Currency Tests | Automated tests verifying calculations across all 5 currencies ($/€/£/CA$/A$) | Test Track | R1 |
| F19 | Privacy Audit & Git Shielding | Automated privacy scanner checking outgoing payload, git user.email configuration, and push to origin/main | M4 / Final | R4 |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| E2E | E2E Testing Track | Test infra (`TEST_INFRA.md`), test scripts (links, sitemap, calc, privacy), Tiers 1-4 tests -> `TEST_READY.md` | Survey | DONE (`TEST_READY.md` published, 241 tests) |
| M1 | Bilingual Web & Currency Engine | F1, F2, F3, F4, F5, F6: English pages, AUD currency, CRO modals, print fix, language switchers | Survey | DONE (Gate passed, 5/5 approvals) |
| M2 | Programmatic SEO & Sitemap | F7, F8, F9, F10: sitemap.xml, robots.txt, canonical/hreflang tags, README.md | M1 | IN_PROGRESS |
| M3 | Distribution Engine & Marketing | F11, F12, F13, F14, F15: Reddit, X, Pinterest campaigns, LinkedIn quarantine, distribution script | Survey | PLANNED |
| M4 / Final | E2E Pass, Hardening & Git Push | F19 + 100% E2E test pass (Tiers 1-4) + Tier 5 adversarial hardening + privacy audit + git commit & push to origin/main | E2E, M1, M2, M3 | PLANNED |

## Interface Contracts
### Web Navigation & Language Switching Contract
- Desktop Header: `<div class="language-switcher ..."><a href="<target-page>" class="...">[ 🇪🇸 ES | 🇬🇧 EN ]</a></div>`
- Mobile Drawer: `<a href="<target-page>" class="...">[ 🇪🇸 ES | 🇬🇧 EN ]</a>`
- Target mappings:
  - `index.html` <-> `index-en.html`
  - `calculator.html` <-> `calculator-en.html`
  - `store.html` <-> `store-en.html`
  - `contracts.html` -> `index-en.html` (with tooltip / notice)
  - Spanish guides -> `index-en.html` / `store-en.html`

### Currency Engine Contract
- Currency values: `'USD' | 'EUR' | 'GBP' | 'CAD' | 'AUD'`
- Symbols: `USD: '$'`, `EUR: '€'`, `GBP: '£'`, `CAD: 'CA$'`, `AUD: 'A$'`
- Function signature in calculator: `setCurrency(currCode, symbol)` updates active button CSS, updates all display symbols, recalculates hourly and daily rates dynamically.

### CRO & Upsell Contract
- Post-PDF Download Modal: triggers immediately on `downloadPdf()` / `window.print()` callback in `index-en.html`.
- Offer: Freelance Finance Hub ($9) linking to `https://migueldp3.gumroad.com/l/bszbzj` with `LANZAMIENTO20` reference.
- Negotiation Callout: Card beneath hourly rate in `calculator-en.html` linking to Email Swipe File Pro (`https://migueldp3.gumroad.com/l/email-swipe-file-pro` or store anchor).

### SEO Contract
- Canonical: `<link rel="canonical" href="https://komasan19283645.github.io/freelance-toolkit/<page>">`
- Hreflang:
  - `<link rel="alternate" hreflang="es" href="https://komasan19283645.github.io/freelance-toolkit/<es-page>">`
  - `<link rel="alternate" hreflang="en" href="https://komasan19283645.github.io/freelance-toolkit/<en-page>">`
  - `<link rel="alternate" hreflang="x-default" href="https://komasan19283645.github.io/freelance-toolkit/">`

## Code Layout
- Root: HTML platform files (`index.html`, `index-en.html`, `calculator.html`, `calculator-en.html`, `store.html`, `store-en.html`, `contracts.html`, guide HTML files).
- `css/`: `custom.css` (global styles, print media rules, CRO modal styles).
- `js/`: `app.js` (invoice generation, math, local storage, CRO triggers).
- `scripts/`: Test and verification scripts (`verify_links.py`, `verify_sitemap.py`, `test_calc.py`, `verify_privacy.py`, `distribute_organic_campaign.py`).
- `tests/`: Automated test suite runner and test case definitions across Tiers 1-5.
- `marketing/`: Campaign strategies, threads, pins, and distribution content.
- `sitemap.xml`, `robots.txt`, `README.md`.
