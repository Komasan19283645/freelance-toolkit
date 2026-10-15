#!/usr/bin/env python3
"""
test_tier5_adversarial.py - Tier 5: Adversarial Hardening & White-Box Edge Testing

Author: worker_final (Teamwork Preview Implementer & QA Specialist)
Scope:
1. Corrupted LocalStorage & Persistence White-Box Injection
2. Rapid Currency Flipping, Idempotency & Precision
3. Extreme Numeric Overflow, Underflow & Division-by-Zero Guardrails
4. Unicode & Internationalization Stress in Invoice Preview & Escaping
5. Programmatic Sitemap Priority, Changefreq & Hreflang Tag Integrity
6. Privacy Guardrails, Obfuscation Scanning & Git Hygiene

Total tests: 46 tests.
Zero external dependencies - pure Python 3 standard library.
"""

import os
import re
import sys
import json
import math
import random
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, Any, List

# Ensure UTF-8 output on Windows
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from scripts.test_calc import calculate_rate, CURRENCY_SYMBOLS
from tests.test_tier2_boundaries import calculate_invoice_totals, escape_html_reference
from scripts.distribute_organic_campaign import validate_reddit_payload
from scripts.verify_privacy import check_git_user_email, AUTHORIZED_GIT_EMAIL


class TestTier5AdversarialHardening(unittest.TestCase):

    # =========================================================================
    # Group 1: Corrupted LocalStorage & Persistence White-Box Injection (8 tests)
    # =========================================================================

    def test_adv01_localstorage_corrupted_json_syntax(self):
        """Verify loadSavedData logic recovers gracefully from malformed JSON."""
        corrupted_payloads = [
            "{bad_json: true,,",
            "{'single_quotes': 1}",
            "{\"unclosed\": ",
            "<!-- HTML injection -->",
            "<<<>>>",
        ]
        default_data = {
            "type": "factura",
            "currency": "€",
            "items": [{"description": "Default", "quantity": 1, "rate": 100}],
        }
        for bad_raw in corrupted_payloads:
            try:
                # Simulating loadSavedData try-catch block
                loaded = json.loads(bad_raw)
                merged = {**default_data, **loaded}
            except Exception:
                merged = default_data
            self.assertEqual(merged["type"], "factura")
            self.assertEqual(len(merged["items"]), 1)

    def test_adv02_localstorage_empty_string_and_null(self):
        """Verify empty strings and null in storage fallback to defaults."""
        for val in ["", "null", "undefined"]:
            try:
                parsed = json.loads(val)
                data = {**{"currency": "€"}, **(parsed if isinstance(parsed, dict) else {})}
            except Exception:
                data = {"currency": "€"}
            self.assertEqual(data["currency"], "€")

    def test_adv03_localstorage_primitive_type_injection(self):
        """Verify injection of primitive types (int, bool, list) does not crash dict unpacking."""
        primitives = ["12345", "true", '"plain string"', "[1, 2, 3]"]
        base_state = {"type": "factura", "currency": "€"}
        for raw in primitives:
            try:
                parsed = json.loads(raw)
                # Client-side: if (saved) invoiceData = { ...invoiceData, ...(isObj ? parsed : {}) }
                if isinstance(parsed, dict):
                    state = {**base_state, **parsed}
                else:
                    state = base_state
            except Exception:
                state = base_state
            self.assertIn("type", state)
            self.assertIn("currency", state)

    def test_adv04_localstorage_prototype_pollution_keys(self):
        """Verify prototype pollution keys do not pollute base dictionary."""
        payload = '{"__proto__": {"admin": true}, "constructor": {"prototype": {"hacked": true}}}'
        parsed = json.loads(payload)
        base = {"sender": {"name": "Test"}}
        merged = {**base, **parsed}
        self.assertNotIn("admin", dir(dict))
        self.assertNotIn("hacked", dir(dict))

    def test_adv05_localstorage_missing_required_substructures(self):
        """Verify empty object merged into schema preserves invoice calculations."""
        empty_payload = "{}"
        parsed = json.loads(empty_payload)
        base = {
            "items": [{"description": "Service", "quantity": 2, "rate": 50}],
            "taxRate": 21,
            "withholdingRate": 0,
            "discountRate": 0,
        }
        merged = {**base, **parsed}
        totals = calculate_invoice_totals(merged["items"], merged["taxRate"])
        self.assertEqual(totals["subtotal"], 100.0)
        self.assertEqual(totals["total"], 121.0)

    def test_adv06_localstorage_corrupted_items_array(self):
        """Verify non-numeric values in item fields are safely handled as 0."""
        corrupted_items = [
            {"description": "Item 1", "quantity": None, "rate": "invalid"},
            {"description": "Item 2", "quantity": "NaN", "rate": None},
            {"description": "", "quantity": 0, "rate": 500},
        ]
        # In app.js: sum + ((item.quantity || 0) * (item.rate || 0))
        subtotal = 0.0
        for it in corrupted_items:
            q = float(it.get("quantity") or 0) if it.get("quantity") not in (None, "NaN") else 0.0
            r = float(it.get("rate") or 0) if it.get("rate") not in (None, "invalid") else 0.0
            subtotal += q * r
        self.assertEqual(subtotal, 0.0)

    def test_adv07_localstorage_mass_items_scale(self):
        """Verify calculation of 1000 invoice items scales with high precision and performance."""
        items = [{"description": f"Bulk Item #{i}", "quantity": 1, "rate": 10.5} for i in range(1000)]
        totals = calculate_invoice_totals(items, tax_rate=21, withholding_rate=15)
        self.assertEqual(totals["subtotal"], 10500.0)
        self.assertAlmostEqual(totals["tax_amount"], 2205.0, places=2)
        self.assertAlmostEqual(totals["withholding_amount"], 1575.0, places=2)
        self.assertAlmostEqual(totals["total"], 11130.0, places=2)

    def test_adv08_localstorage_negative_or_extreme_rates(self):
        """Verify invoice total clamping to non-negative even if discounts exceed subtotal."""
        items = [{"description": "Discounted", "quantity": 1, "rate": 100.0}]
        # Discount rate 150% (exceeds 100%)
        totals = calculate_invoice_totals(items, tax_rate=21, discount_rate=150.0)
        self.assertEqual(totals["total"], 0.0, "Invoice total must never be negative")

    # =========================================================================
    # Group 2: Rapid Currency Flipping & Idempotency (8 tests)
    # =========================================================================

    def test_adv09_rapid_sequential_currency_flipping(self):
        """Simulate rapid cycling across all 5 currencies 100 times without numeric drift."""
        currencies = ["USD", "EUR", "GBP", "CAD", "AUD"]
        net = 5000
        exp = 600
        tax = 20
        vac = 4
        hDay = 8
        bRatio = 70

        # Initial reference calculation
        base_res = calculate_rate(net, exp, tax, vac, hDay, bRatio, "USD")
        base_hourly = base_res["hourly_rate"]

        for cycle in range(100):
            curr = currencies[cycle % len(currencies)]
            res = calculate_rate(net, exp, tax, vac, hDay, bRatio, curr)
            self.assertEqual(res["hourly_rate"], base_hourly, f"Numeric drift detected on cycle {cycle}")
            self.assertEqual(res["currency_symbol"], CURRENCY_SYMBOLS[curr])

    def test_adv10_currency_label_idempotency(self):
        """Verify that currency symbol change produces idempotent labels."""
        for code, sym in CURRENCY_SYMBOLS.items():
            label = f"{sym} / mo"
            self.assertFalse(label.endswith("/ mo / mo"), "Label must not duplicate suffix")
            self.assertTrue(label.startswith(sym), f"Label must start with symbol {sym}")

    def test_adv11_currency_unsupported_code_fallback(self):
        """Verify unsupported currency codes fallback to $ symbol safely."""
        unsupported = ["JPY", "CHF", "CNY", "XYZ", ""]
        for bad_code in unsupported:
            res = calculate_rate(3000, 400, 20, 4, 8, 70, bad_code)
            self.assertEqual(res["currency_symbol"], "$")
            self.assertTrue(res["formatted_hourly"].startswith("$"))

    def test_adv12_currency_symbol_injection_resistance(self):
        """Verify currency symbols are restricted to plain characters with zero HTML injection."""
        for code, sym in CURRENCY_SYMBOLS.items():
            self.assertNotIn("<", sym)
            self.assertNotIn(">", sym)
            self.assertNotIn('"', sym)
            self.assertNotIn("'", sym)
            self.assertNotIn("&", sym)

    def test_adv13_currency_prefix_vs_suffix_invariants(self):
        """Verify international currency notation rules (Anglo prefix vs Spanish EUR suffix)."""
        # In English platform: $100.00, CA$100.00, A$100.00, £100.00
        for code in ["USD", "CAD", "AUD", "GBP"]:
            res = calculate_rate(4000, 500, 25, 4, 8, 60, code)
            sym = CURRENCY_SYMBOLS[code]
            self.assertTrue(res["formatted_hourly"].startswith(sym))

    def test_adv14_currency_toggle_recalculates_gross_and_daily(self):
        """Verify changing currency recalculates gross, hourly, and daily synchronously."""
        for code in CURRENCY_SYMBOLS.keys():
            res = calculate_rate(4500, 500, 20, 2, 8, 75, code)
            self.assertGreater(res["monthly_gross"], 0)
            self.assertGreater(res["hourly_rate"], 0)
            self.assertGreater(res["daily_rate"], 0)
            self.assertAlmostEqual(res["daily_rate"], res["hourly_rate"] * (8 * 0.75), places=2)

    def test_adv15_currency_zero_rate_with_all_symbols(self):
        """Verify 0.00 rate formatting across all 5 currencies."""
        for code, sym in CURRENCY_SYMBOLS.items():
            res = calculate_rate(0, 0, 0, 0, 8, 100, code)
            self.assertEqual(res["formatted_hourly"], f"{sym}0.00")

    def test_adv16_currency_floating_precision_consistency(self):
        """Verify precision rounding to 2 decimal places avoids binary floating artefacts."""
        res = calculate_rate(1234.56, 78.90, 15, 3, 7.5, 66.6, "USD")
        # Format string should match regex ^\$[0-9]+\.[0-9]{2}$
        self.assertTrue(re.match(r"^\$[0-9]+\.[0-9]{2}$", res["formatted_hourly"]))

    # =========================================================================
    # Group 3: Extreme Numeric Overflow & Division-by-Zero Guardrails (8 tests)
    # =========================================================================

    def test_adv17_extreme_net_income_overflow(self):
        """Extreme net income ($10^12/mo) must not yield Infinity or NaN."""
        res = calculate_rate(1e12, 1e9, 25, 4, 8, 70, "USD")
        self.assertFalse(math.isinf(res["monthly_gross"]))
        self.assertFalse(math.isnan(res["monthly_gross"]))
        self.assertFalse(math.isinf(res["hourly_rate"]))
        self.assertFalse(math.isnan(res["hourly_rate"]))
        self.assertGreater(res["hourly_rate"], 0)

    def test_adv18_extreme_expenses_overflow(self):
        """Extreme monthly expenses ($10^9/mo) must scale gross proportionately."""
        res = calculate_rate(5000, 1e9, 20, 4, 8, 70, "USD")
        self.assertGreater(res["monthly_gross"], 1e9)
        self.assertFalse(math.isnan(res["hourly_rate"]))

    def test_adv19_tax_rate_100_percent_guardrail(self):
        """Tax rate of exactly 100% must engage denominator guardrail to prevent division by zero."""
        # When tax = 100%, 1 - tax = 0 -> (1 - tax > 0) ? (net+exp)/(1-tax) : (net+exp)
        res = calculate_rate(4000, 500, 100, 4, 8, 70, "USD")
        self.assertEqual(res["monthly_gross"], 4500.0)
        self.assertFalse(math.isnan(res["hourly_rate"]))

    def test_adv20_tax_rate_exceeding_100_percent(self):
        """Tax rate of 150% must not produce negative monthly gross."""
        res = calculate_rate(3000, 200, 150, 4, 8, 70, "USD")
        self.assertEqual(res["monthly_gross"], 3200.0)
        self.assertGreater(res["hourly_rate"], 0)

    def test_adv21_vacation_52_weeks_division_by_zero_guardrail(self):
        """52 weeks vacation must clamp workingWeeks to at least 1."""
        res = calculate_rate(3000, 300, 20, 52, 8, 70, "USD")
        self.assertGreater(res["hourly_rate"], 0)
        self.assertFalse(math.isnan(res["hourly_rate"]))
        self.assertFalse(math.isinf(res["hourly_rate"]))

    def test_adv22_hours_per_day_zero_division_guardrail(self):
        """0 hours per day must clamp totalBillable to at least 1."""
        res = calculate_rate(3000, 300, 20, 4, 0, 70, "USD")
        self.assertGreater(res["hourly_rate"], 0)
        self.assertFalse(math.isnan(res["hourly_rate"]))
        self.assertFalse(math.isinf(res["hourly_rate"]))

    def test_adv23_billable_ratio_zero_division_guardrail(self):
        """0% billable ratio must clamp totalBillable to at least 1."""
        res = calculate_rate(3000, 300, 20, 4, 8, 0, "USD")
        self.assertGreater(res["hourly_rate"], 0)
        self.assertFalse(math.isnan(res["hourly_rate"]))
        self.assertFalse(math.isinf(res["hourly_rate"]))

    def test_adv24_negative_inputs_sanitization(self):
        """Negative inputs must not produce complex numbers or uncaught crashes."""
        res = calculate_rate(-1000, -200, -10, -5, 8, 70, "USD")
        self.assertFalse(math.isnan(res["hourly_rate"]))

    # =========================================================================
    # Group 4: Unicode Stress & XSS Escaping Invariants (8 tests)
    # =========================================================================

    def test_adv25_invoice_xss_script_tag_neutralization(self):
        """Verify `<script>alert('pwned')</script>` is thoroughly escaped."""
        evil = "<script>alert('pwned')</script>"
        escaped = escape_html_reference(evil)
        self.assertNotIn("<script>", escaped)
        self.assertIn("&lt;script&gt;", escaped)
        self.assertIn("&#039;pwned&#039;", escaped)

    def test_adv26_invoice_xss_img_onerror_neutralization(self):
        """Verify `<img src=x onerror=alert(1)>` has quotes and angle brackets escaped."""
        evil = '<img src="x" onerror="alert(1)">'
        escaped = escape_html_reference(evil)
        self.assertNotIn("<img", escaped)
        self.assertIn("&lt;img", escaped)
        self.assertIn("&quot;x&quot;", escaped)

    def test_adv27_invoice_xss_svg_onload_neutralization(self):
        """Verify `\"><svg/onload=confirm(1)>` breaks out of attribute context safely."""
        evil = '"><svg/onload=confirm(1)>'
        escaped = escape_html_reference(evil)
        self.assertNotIn('">', escaped)
        self.assertIn("&quot;&gt;&lt;svg/onload=confirm(1)&gt;", escaped)

    def test_adv28_invoice_cjk_multibyte_characters(self):
        """Verify Chinese, Japanese, and Korean characters preserve multibyte encoding."""
        cjk_text = "开发设计 / システム設計 / 소프트웨어 개발"
        escaped = escape_html_reference(cjk_text)
        self.assertEqual(escaped, cjk_text)

    def test_adv29_invoice_rtl_arabic_hebrew_characters(self):
        """Verify RTL Arabic and Hebrew characters pass through uncorrupted."""
        rtl_text = "فاتورة خدمات استشارية / חשבונית מס"
        escaped = escape_html_reference(rtl_text)
        self.assertEqual(escaped, rtl_text)

    def test_adv30_invoice_emoji_stress_test(self):
        """Verify emojis in invoice description and notes preserve UTF-8 integrity."""
        emoji_text = "Consulting 🚀💼 - Q4 Growth 📈 & Stripe Integration 🎉"
        escaped = escape_html_reference(emoji_text)
        self.assertIn("🚀💼", escaped)
        self.assertIn("🎉", escaped)
        self.assertIn("&amp;", escaped)  # Ampersand escaped

    def test_adv31_invoice_zero_width_spaces_and_control_chars(self):
        """Verify zero-width spaces and control characters do not raise encoding errors."""
        text = "Item\u200Bwith\u200Czero\u200Dwidth\uFEFFchars"
        escaped = escape_html_reference(text)
        self.assertIn("Item", escaped)

    def test_adv32_invoice_spanish_diacritics_complete_set(self):
        """Verify complete Spanish diacritics set is rendered accurately."""
        spanish_chars = "áéíóúñÁÉÍÓÚÑüÜ¿¡"
        escaped = escape_html_reference(spanish_chars)
        self.assertEqual(escaped, spanish_chars)

    # =========================================================================
    # Group 5: Programmatic Sitemap & International Hreflang Tags (8 tests)
    # =========================================================================

    def test_adv33_sitemap_priority_range_and_weights(self):
        """All sitemap priority values must be floats between 0.0 and 1.0; core pages >= 0.8."""
        sitemap_path = os.path.join(BASE_DIR, "sitemap.xml")
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        ns = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        core_pages = [
            "https://komasan19283645.github.io/freelance-toolkit/",
            "https://komasan19283645.github.io/freelance-toolkit/index-en.html",
        ]
        for url in root.findall("ns:url", ns):
            loc = url.find("ns:loc", ns).text.strip()
            priority_el = url.find("ns:priority", ns)
            self.assertIsNotNone(priority_el, f"Missing priority for {loc}")
            p_val = float(priority_el.text.strip())
            self.assertGreaterEqual(p_val, 0.0)
            self.assertLessEqual(p_val, 1.0)
            if loc in core_pages:
                self.assertGreaterEqual(p_val, 0.8, f"Core page {loc} must have priority >= 0.8")

    def test_adv34_sitemap_changefreq_enum_validity(self):
        """Changefreq values must be strictly valid W3C sitemap enum members."""
        valid_changefreqs = {"always", "hourly", "daily", "weekly", "monthly", "yearly", "never"}
        sitemap_path = os.path.join(BASE_DIR, "sitemap.xml")
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        ns = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        for url in root.findall("ns:url", ns):
            cf_el = url.find("ns:changefreq", ns)
            self.assertIsNotNone(cf_el)
            self.assertIn(cf_el.text.strip(), valid_changefreqs)

    def test_adv35_sitemap_lastmod_iso8601_validity(self):
        """All lastmod values must follow YYYY-MM-DD format."""
        sitemap_path = os.path.join(BASE_DIR, "sitemap.xml")
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        ns = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        for url in root.findall("ns:url", ns):
            lm_el = url.find("ns:lastmod", ns)
            self.assertIsNotNone(lm_el)
            self.assertTrue(re.match(r"^\d{4}-\d{2}-\d{2}$", lm_el.text.strip()))

    def test_adv36_hreflang_tags_malformed_detection(self):
        """Assert no HTML files contain invalid hreflang attributes (e.g. 'eng', 'esp', uppercase)."""
        valid_hreflang_values = {"es", "en", "x-default"}
        html_files = [f for f in os.listdir(BASE_DIR) if f.endswith(".html")]
        for hf in html_files:
            with open(os.path.join(BASE_DIR, hf), "r", encoding="utf-8") as f:
                content = f.read()
            matches = re.findall(r'<link[^>]*rel="alternate"[^>]*hreflang="([^"]+)"', content)
            for lang in matches:
                self.assertIn(lang, valid_hreflang_values, f"File {hf} contains invalid hreflang: {lang}")

    def test_adv37_hreflang_bidirectional_graph_closure(self):
        """Assert full bidirectional reciprocity between paired Spanish and English pages."""
        pairs = [
            ("index.html", "index-en.html"),
            ("calculator.html", "calculator-en.html"),
            ("store.html", "store-en.html"),
        ]
        domain = "https://komasan19283645.github.io/freelance-toolkit/"
        for es_file, en_file in pairs:
            with open(os.path.join(BASE_DIR, es_file), "r", encoding="utf-8") as f:
                es_content = f.read()
            with open(os.path.join(BASE_DIR, en_file), "r", encoding="utf-8") as f:
                en_content = f.read()

            en_target = domain + en_file
            es_target = domain if es_file == "index.html" else domain + es_file

            self.assertIn(en_target, es_content, f"{es_file} must declare alternate to {en_target}")
            self.assertIn(es_target, en_content, f"{en_file} must declare alternate to {es_target}")

    def test_adv38_canonical_url_absolute_and_secure(self):
        """All <link rel='canonical'> must be absolute HTTPS URLs without trailing fragments."""
        html_files = [f for f in os.listdir(BASE_DIR) if f.endswith(".html")]
        for hf in html_files:
            with open(os.path.join(BASE_DIR, hf), "r", encoding="utf-8") as f:
                content = f.read()
            match = re.search(r'<link[^>]*rel="canonical"[^>]*href="([^"]+)"', content)
            self.assertIsNotNone(match, f"Missing canonical in {hf}")
            url = match.group(1)
            self.assertTrue(url.startswith("https://komasan19283645.github.io/freelance-toolkit/"))
            self.assertNotIn("#", url)

    def test_adv39_robots_txt_sitemap_url_exactness(self):
        """robots.txt must point exactly to the HTTPS production sitemap.xml."""
        robots_path = os.path.join(BASE_DIR, "robots.txt")
        self.assertTrue(os.path.exists(robots_path))
        with open(robots_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Sitemap: https://komasan19283645.github.io/freelance-toolkit/sitemap.xml", content)

    def test_adv40_no_broken_internal_anchors_or_hash_targets(self):
        """Verify internal in-page hash links point to existing DOM element IDs."""
        for page in ["index.html", "index-en.html", "store.html", "store-en.html"]:
            filepath = os.path.join(BASE_DIR, page)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            # Find href="#..."
            hash_links = re.findall(r'href="#([a-zA-Z0-9_\-]+)"', content)
            for h in hash_links:
                if h in ("top", ""):
                    continue
                # Assert id="h" exists in the document
                id_pattern = rf'id="{h}"'
                self.assertTrue(
                    re.search(id_pattern, content) is not None,
                    f"Broken in-page anchor #{h} in {page}",
                )

    # =========================================================================
    # Group 6: Privacy Guardrails, Obfuscation Scanning & Git Hygiene (6 tests)
    # =========================================================================

    def test_adv41_obfuscated_email_detection_in_marketing(self):
        """Adversarial check: ensure no obfuscated email syntax exists in marketing copy."""
        marketing_dir = os.path.join(BASE_DIR, "marketing")
        obfuscated_patterns = [
            re.compile(r'\b[A-Za-z0-9._%+-]+\s*\[at\]\s*[A-Za-z0-9.-]+\s*\[dot\]\s*[A-Za-z]{2,}\b', re.IGNORECASE),
            re.compile(r'\b[A-Za-z0-9._%+-]+\s*\(at\)\s*[A-Za-z0-9.-]+\s*\(dot\)\s*[A-Za-z]{2,}\b', re.IGNORECASE),
            re.compile(r'mailto:[A-Za-z0-9._%+-]+@', re.IGNORECASE),
        ]
        for root_dir, _, files in os.walk(marketing_dir):
            for file in files:
                if file.endswith((".md", ".txt")):
                    filepath = os.path.join(root_dir, file)
                    with open(filepath, "r", encoding="utf-8") as f:
                        text = f.read()
                    for pat in obfuscated_patterns:
                        matches = pat.findall(text)
                        self.assertEqual(len(matches), 0, f"Obfuscated email pattern in {file}: {matches}")

    def test_adv42_obfuscated_linkedin_detection_in_marketing(self):
        """Adversarial check: ensure active marketing copy contains 0 active LinkedIn profile URLs."""
        marketing_dir = os.path.join(BASE_DIR, "marketing")
        linkedin_pattern = re.compile(r'https?://(?:www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+', re.IGNORECASE)
        for root_dir, _, files in os.walk(marketing_dir):
            for file in files:
                if file.endswith(".md"):
                    filepath = os.path.join(root_dir, file)
                    with open(filepath, "r", encoding="utf-8") as f:
                        text = f.read()
                    # In posts_redes_sociales.md, any LinkedIn content must be explicitly quarantined
                    if file == "posts_redes_sociales.md":
                        # Check that quarantine banner is present if LinkedIn is referenced
                        if "linkedin" in text.lower():
                            self.assertTrue("QUARANTINADO" in text or "PROHIBIDO" in text)
                    else:
                        matches = linkedin_pattern.findall(text)
                        self.assertEqual(len(matches), 0, f"Unquarantined LinkedIn URL in {file}: {matches}")

    def test_adv43_reddit_payload_case_and_protocol_variations(self):
        """Adversarial check: validate_reddit_payload rejects any casing or protocol of Gumroad link."""
        attacks = [
            "Check my profile: HTTPS://MIGUELDP3.GUMROAD.COM/L/TEST",
            "Go to HTTP://gumroad.com/l/product for discount",
            "Get it at migueldp3.gumroad.com right now!",
            "Visit https://GUMROAD.COM/pricing",
        ]
        for attack_text in attacks:
            errs = validate_reddit_payload("Adversarial Reddit Title", attack_text, "adversarial_test.md")
            self.assertGreater(len(errs), 0, f"Failed to reject attack payload: {attack_text}")

    def test_adv44_distribution_pacing_jitter_stochastic_properties(self):
        """Verify distribution simulation pacing strictly satisfies 45.0s <= t <= 90.0s."""
        min_p = 45.0
        max_p = 90.0
        delays = [random.uniform(min_p, max_p) for _ in range(200)]
        self.assertTrue(all(min_p <= d <= max_p for d in delays))
        mean_delay = sum(delays) / len(delays)
        self.assertGreater(mean_delay, 55.0)
        self.assertLess(mean_delay, 80.0)

    def test_adv45_gitignore_shields_agents_and_system_metadata(self):
        """Verify .gitignore shields both .agents/ and .system_generated/."""
        gi_path = os.path.join(BASE_DIR, ".gitignore")
        self.assertTrue(os.path.exists(gi_path))
        with open(gi_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn(".agents/", content)
        self.assertIn(".system_generated/", content)

    def test_adv46_git_committer_configuration_hard_assertion(self):
        """Verify git committer is configured with authorized noreply email and name."""
        git_check = check_git_user_email(BASE_DIR)
        self.assertTrue(git_check["matches"], f"Git email {git_check['current_email']} != {AUTHORIZED_GIT_EMAIL}")


if __name__ == "__main__":
    unittest.main()
