# TEST INFRASTRUCTURE SPECIFICATION: FREELANCETOOLKIT

**Project**: FreelanceToolkit Global Scaling & Organic Distribution  
**Document**: `TEST_INFRA.md`  
**Test Philosophy**: Opaque-box, requirement-driven, zero dependency on implementation internals  
**Test Suite Target**: >= 11 * N + max(5, N/2) test cases across 4 tiers (N=19 -> >= 219 test cases)  
**Track**: E2E Testing Track  

---

## 1. Test Philosophy & Architecture

### 1.1 Opaque-Box, Requirement-Driven Principles
The FreelanceToolkit test architecture is strictly **opaque-box** and **specification-grounded**:
1. **Zero Dependency on Implementation Internals**: Tests assert externally observable behavior, interface contracts, DOM structures, mathematical invariants, HTTP/HTML payloads, XML schema specifications, and security policies—never private implementation details.
2. **Authoritative Source of Truth**: All expected values and boundary behaviors are derived directly from `PROJECT.md`, `ORIGINAL_REQUEST.md`, and established international standards (W3C HTML5, XML Sitemap 0.9, ISO currency codes).
3. **Progressive Testability**: The test infrastructure is designed for multi-milestone orchestration. Tests automatically detect feature completion status and execute comprehensive assertions as deliverables land in M1 (Bilingual Web), M2 (SEO & Sitemap), M3 (Distribution Engine), and M4 (Final Hardening).
4. **Zero-Flake & Deterministic**: Tests rely purely on the Python 3 standard library (`unittest`, `html.parser`, `xml.etree.ElementTree`, `re`, `subprocess`, `pathlib`) requiring no external dependencies, no network calls, and executing deterministically in < 5 seconds.

---

## 2. Four-Tier Testing Methodology

```
+------------------------------------------------------------------------------+
|                          TIER 4: APPLICATION SCENARIOS                       |
|   End-to-end freelancer workflows (US, UK, ES, CA, AU personas, DAC7, etc.)  |
+------------------------------------------------------------------------------+
|                     TIER 3: CROSS-FEATURE COMBINATIONS                       |
|  Pairwise interactions (Currency + Print, Language + Modal, Storage + Math)  |
+------------------------------------------------------------------------------+
|                     TIER 2: BOUNDARY & CORNER CASES                          |
|  Zero tax, extreme expenses, 52wk vacation, promo edge cases, XSS escaping    |
+------------------------------------------------------------------------------+
|                          TIER 1: FEATURE COVERAGE                            |
|       >= 5 unit/contract tests per feature across F1 to F19 (101+ tests)     |
+------------------------------------------------------------------------------+
```

### Tier 1: Feature Coverage (F1 to F19)
- **Target**: Exhaustive verification of primary functional requirements across all 19 defined features in `PROJECT.md`.
- **Requirement**: Minimum 5 dedicated test cases per feature (19 * 5 = 95 minimum; implemented: 101 tests).
- **Scope**:
  - `F1`: English Web Core (`index-en.html`, `calculator-en.html`, `store-en.html`)
  - `F2`: Multi-Currency Engine (USD $, EUR €, GBP £, CAD CA$, AUD A$)
  - `F3`: International Pricing Model ($9 individual, $39 Suite, $0 Starter, LANZAMIENTO20)
  - `F4`: High-Converting CRO Elements (Post-PDF modal, negotiation callout cards)
  - `F5`: Bidirectional Language Switchers (`[ 🇪🇸 ES | 🇬🇧 EN ]` across 10 pages)
  - `F6`: Invoice Print & Persistence Fix (`#printable-document`, LocalStorage draft)
  - `F7`: Programmatic Sitemap Architecture (`sitemap.xml` with 10 endpoints & xmlns:xhtml)
  - `F8`: Canonical & International Hreflang (Canonical, hreflang es/en/x-default)
  - `F9`: Meta & Social Tag Validation (Open Graph, Twitter Cards, @Komaleon37)
  - `F10`: Synchronized Bilingual README (`README.md` in ES & EN, live links, topics)
  - `F11`: Reddit Organic Distribution Engine (`marketing/reddit_campaign_distribution.md`)
  - `F12`: X / Twitter Thread Campaign (`marketing/x_twitter_campaign_threads.md`)
  - `F13`: International Pinterest Pins (`marketing/pinterest_campaign_pins_international.md`)
  - `F14`: Marketing Copy Quarantine & Cleanup (Quarantine LinkedIn, zero-Gumroad Reddit)
  - `F15`: Distribution Automation Script (`scripts/distribute_organic_campaign.py`)
  - `F16`: Automated Link & Page Validator (`scripts/verify_links.py`)
  - `F17`: Sitemap XML Schema Validator (`scripts/verify_sitemap.py`)
  - `F18`: Dynamic Calculator & Currency Tests (`scripts/test_calc.py`)
  - `F19`: Privacy Audit & Git Shielding (`scripts/verify_privacy.py`, git noreply)

### Tier 2: Boundary & Corner Cases
- **Target**: Stress-testing domain limits, numerical boundaries, empty inputs, extreme rates, and encoding fidelity.
- **Scope**: 50+ test cases covering:
  - Rate Calculator numerical limits: Tax 0%, Tax 60%, Tax 99%, Expenses $0, Expenses $50,000/mo.
  - Vacation bounds: 0 weeks (52 working weeks), 26 weeks, 51 weeks (1 working week), 52 weeks clamped to minimum 1 week to prevent division by zero.
  - Workday & billable bounds: 1 hr/day, 16 hrs/day, 10% billable ratio, 100% billable ratio.
  - Invoice limits: 0 items, 50 items, fractional quantities (0.25h), rate $0.00, high value ($50,000.00).
  - Tax combinations: IVA 21%, 10%, 4%, 0%; IRPF 15%, 7%, 0%; Discount 0%, 100%.
  - Promo code boundaries: `LANZAMIENTO20`, case-insensitivity, whitespace trimming, invalid codes (`PROMO`, empty).
  - Special characters and XSS sanitization: `<script>`, `"`, `'`, `&`, `ñ`, `á` in invoice notes and client descriptions.
  - Date boundaries: invoice due date before issue date, same day, 365 days out.

### Tier 3: Cross-Feature Combinations
- **Target**: Pairwise and systemic interactions between independent features.
- **Scope**: 50+ test cases covering:
  - Currency Toggle x Rate Calculation: USD, EUR, GBP, CAD, AUD symbol updates and real-time recalculation.
  - Currency Toggle x Invoice Totals: Preserving row data while updating currency symbols in table and summaries.
  - Language Switch x Route Integrity: 10-page bidirectional traversal (`index.html` <-> `index-en.html`, etc.).
  - Language Switch x Localized Pricing: EUR pricing on Spanish pages vs USD pricing on English pages.
  - Print Trigger x CRO Modal: Generating PDF prompts the Finance Hub download modal without disrupting print stream.
  - Calculator Rate x Negotiation Upsell: High-rate calculation triggers contextual callout linking to Email Swipe File Pro.
  - LocalStorage Serialization x Schema Evolution: Draft save/restore, handling malformed/corrupted localStorage JSON.
  - Sitemap x Canonical x Hreflang Alignment: Perfect triangular consistency between sitemap URL, canonical URL, and hreflang alternate.
  - Marketing Channels x Privacy Guardrail: Reddit copy has zero commercial links AND zero personal identifiers.

### Tier 4: Real-World Application Scenarios
- **Target**: Holistic end-to-end user journeys replicating real freelancer and solopreneur workflows.
- **Scope**: 40+ test cases covering:
  - Persona 1: US Full-Stack Developer ($6,000 net, $800 overhead, 25% tax, USD invoice, PDF export, CRO upsell).
  - Persona 2: Spanish Graphic Designer Autónomo (2,200 € net, 350 € overhead, 20% tax, 21% IVA, 15% IRPF, legal clauses).
  - Persona 3: UK Content Strategist (£3,500 net, £400 overhead, 20% tax, 20% VAT, GBP invoicing).
  - Persona 4: Canadian Mobile App Engineer (CA$5,500 net, CA$600 overhead, 28% tax, CAD invoicing).
  - Persona 5: Australian Consultant (A$7,000 net, A$900 overhead, 30% tax, AUD rate calculation).
  - Persona 6: Discovery & Navigation Journey (Bilingual switching, browsing pro store, applying launch promo).
  - Persona 7: E-commerce Reseller DAC7 Journey (DAC7 guide, 30-sale / 2,000 € threshold, Profit Tracker).
  - Persona 8: Personal Finance 50/30/20 Journey (Needs 50%, Wants 30%, Savings 20% allocation).
  - Persona 9: Zero-Trust Identity Shielding Journey (Git email verification, privacy scanner execution).

---

## 3. Test Metric Thresholds & Formulas

| Metric | Minimum Threshold | Implemented |
|---|---|---|
| **Total Test Cases** | $\ge 11 \times N + \max(5, \lceil N/2 \rceil) = 219$ | **241** |
| **Tier 1 Feature Coverage** | $\ge 5$ tests per feature ($19 \times 5 = 95$) | **101** |
| **Tier 2 Boundary Cases** | $\ge 40$ boundary tests | **50** |
| **Tier 3 Combinations** | $\ge 40$ pairwise combination tests | **50** |
| **Tier 4 Scenarios** | $\ge 30$ persona workflow tests | **40** |
| **Automated Verification Scripts** | 4 standalone validation scripts | **4** |
| **Pass Rate Requirement** | 100% of runnable tests must pass | **100%** |
| **Execution Speed** | Full suite under 10 seconds | **< 3s** |

---

## 4. Test Infrastructure Directory Layout

```
freelance-toolkit-saas/
├── TEST_INFRA.md                   # This specification document
├── TEST_READY.md                   # Execution summary & track readiness sign-off
├── run_tests.py                    # Unified test runner (scripts + tiers 1-4)
│
├── scripts/                        # Standalone verification utilities
│   ├── verify_links.py             # Validates links, assets & language switchers
│   ├── verify_sitemap.py           # Validates XML schema, 10 URLs & hreflang
│   ├── test_calc.py                # Evaluates rate calculator math across 5 currencies
│   └── verify_privacy.py           # Verifies identity shielding & git user.email
│
└── tests/                          # 4-Tier Test Suite
    ├── __init__.py
    ├── test_tier1_features.py      # Tier 1: F1 through F19 coverage (101 tests)
    ├── test_tier2_boundaries.py    # Tier 2: Boundary & corner cases (50 tests)
    ├── test_tier3_combinations.py  # Tier 3: Cross-feature combinations (50 tests)
    └── test_tier4_scenarios.py     # Tier 4: Real-world user journeys (40 tests)
```

---

## 5. Execution Protocols & Runner Usage

### 5.1 Run Everything (Scripts + All Tiers)
```powershell
python run_tests.py
```

### 5.2 Run Specific Tiers
```powershell
python run_tests.py --tier 1       # Run Tier 1 Feature Coverage only
python run_tests.py --tier 2       # Run Tier 2 Boundary Tests only
python run_tests.py --tier 3       # Run Tier 3 Combinations only
python run_tests.py --tier 4       # Run Tier 4 Application Scenarios only
python run_tests.py --scripts      # Run the 4 verification scripts only
```

### 5.3 Run Individual Verification Scripts
```powershell
python scripts/verify_links.py
python scripts/verify_sitemap.py [--strict]
python scripts/test_calc.py
python scripts/verify_privacy.py
```

### 5.4 Native Unittest Discovery
```powershell
python -m unittest discover tests -p "test_*.py" -v
```

---

## 6. Progressive Testability Lifecycle

1. **Milestone E2E (Current)**:
   - Full test infrastructure, runner, 4 verification scripts, and 4 test tiers are deployed.
   - Tests run immediately and pass with 0 errors. Prerequisites for downstream milestones (M1, M2, M3) are gracefully handled via progressive assertions and prerequisite skips.
2. **Milestone M1 (Bilingual Web & Currency Engine)**:
   - M1 implementer runs `python run_tests.py --tier 1` to verify F1-F6 (English pages, AUD currency, CRO modals, print fix, language switchers).
3. **Milestone M2 (SEO & Sitemap)**:
   - M2 implementer runs `python scripts/verify_sitemap.py --strict` and `python run_tests.py --tier 1` to verify F7-F10 (sitemap with 10 URLs and hreflang, README).
4. **Milestone M3 (Distribution Engine)**:
   - M3 implementer runs `python run_tests.py --tier 1` and `python scripts/verify_privacy.py` to verify F11-F15 (Reddit zero-Gumroad, Twitter threads, Pinterest pins, distribution automation).
5. **Milestone M4 / Final (Full Pass & Hardening)**:
   - Final agent executes `python run_tests.py` with 100% pass across all 241 tests and zero skipped tests, confirming complete end-to-end readiness.
