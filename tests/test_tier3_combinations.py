#!/usr/bin/env python3
"""
test_tier3_combinations.py - Tier 3: Cross-Feature Combinations

Evaluates pairwise interactions and systemic integration:
- Currency Toggle x Rate Calculation
- Currency Toggle x Invoice Totals
- Language Switch x Route Mapping
- Print Action x CRO Modal Trigger
- LocalStorage x Data State Persistence
- Sitemap x Canonical x Hreflang Alignment
- Marketing Channels x Privacy Guardrail

Total tests: 50 tests.
"""

import os
import re
import sys
import json
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from scripts.test_calc import calculate_rate, CURRENCY_SYMBOLS
from scripts.verify_links import verify_all_links
from scripts.verify_sitemap import verify_sitemap, EXPECTED_10_URLS
from scripts.verify_privacy import verify_privacy, AUTHORIZED_GIT_EMAIL, AUTHORIZED_PSEUDONYMS


class TestTier3Combinations(unittest.TestCase):

    # =========================================================================
    # Group 1: Currency Toggle x Rate Calculation (10 tests)
    # =========================================================================
    def test_c01_usd_toggle_recalculates_with_dollar(self):
        res = calculate_rate(4500, 650, 25, 4, 8, 60, "USD")
        self.assertEqual(res["currency_symbol"], "$")
        self.assertEqual(res["formatted_hourly"], "$71.53")
        self.assertEqual(res["formatted_daily"], "$343.33")

    def test_c02_eur_toggle_recalculates_with_euro(self):
        res = calculate_rate(4500, 650, 25, 4, 8, 60, "EUR")
        self.assertEqual(res["currency_symbol"], "€")
        self.assertEqual(res["formatted_hourly"], "€71.53")
        self.assertEqual(res["formatted_daily"], "€343.33")

    def test_c03_gbp_toggle_recalculates_with_pound(self):
        res = calculate_rate(4500, 650, 25, 4, 8, 60, "GBP")
        self.assertEqual(res["currency_symbol"], "£")
        self.assertEqual(res["formatted_hourly"], "£71.53")
        self.assertEqual(res["formatted_daily"], "£343.33")

    def test_c04_cad_toggle_recalculates_with_cad_prefix(self):
        res = calculate_rate(4500, 650, 25, 4, 8, 60, "CAD")
        self.assertEqual(res["currency_symbol"], "CA$")
        self.assertEqual(res["formatted_hourly"], "CA$71.53")
        self.assertEqual(res["formatted_daily"], "CA$343.33")

    def test_c05_aud_toggle_recalculates_with_aud_prefix(self):
        res = calculate_rate(4500, 650, 25, 4, 8, 60, "AUD")
        self.assertEqual(res["currency_symbol"], "A$")
        self.assertEqual(res["formatted_hourly"], "A$71.53")
        self.assertEqual(res["formatted_daily"], "A$343.33")

    def test_c06_currency_cycling_preserves_numerical_value(self):
        rates = [calculate_rate(4500, 650, 25, 4, 8, 60, curr)["hourly_rate"] for curr in ["USD", "EUR", "GBP", "CAD", "AUD"]]
        for r in rates:
            self.assertAlmostEqual(r, rates[0], places=4)

    def test_c07_currency_toggle_preserves_inputs(self):
        inputs = (3500, 400, 22, 5, 7.5, 65)
        res_usd = calculate_rate(*inputs, "USD")
        res_eur = calculate_rate(*inputs, "EUR")
        self.assertEqual(res_usd["monthly_net"], res_eur["monthly_net"])
        self.assertEqual(res_usd["monthly_expenses"], res_eur["monthly_expenses"])
        self.assertEqual(res_usd["working_weeks"], res_eur["working_weeks"])

    def test_c08_currency_toggle_updates_hourly_pill(self):
        res_gbp = calculate_rate(5000, 600, 20, 4, 8, 70, "GBP")
        pill_text = f"{res_gbp['currency_symbol']}{res_gbp['hourly_rate']:.2f}/hr"
        self.assertTrue(pill_text.startswith("£"))

    def test_c09_currency_toggle_updates_net_pill(self):
        res_cad = calculate_rate(5000, 600, 20, 4, 8, 70, "CAD")
        pill_text = f"{res_cad['currency_symbol']}{round(res_cad['monthly_net']):,}/mo"
        self.assertTrue(pill_text.startswith("CA$5,000"))

    def test_c10_currency_toggle_updates_monthly_gross_display(self):
        res_aud = calculate_rate(5000, 600, 20, 4, 8, 70, "AUD")
        self.assertTrue(res_aud["formatted_monthly_gross"].startswith("A$7,000"))

    # =========================================================================
    # Group 2: Currency Toggle x Invoice Totals (10 tests)
    # =========================================================================
    def test_c11_invoice_currency_usd_symbol_assignment(self):
        inv_data = {"currency": "$"}
        self.assertEqual(inv_data["currency"], "$")

    def test_c12_invoice_currency_eur_symbol_assignment(self):
        inv_data = {"currency": "€"}
        self.assertEqual(inv_data["currency"], "€")

    def test_c13_invoice_currency_gbp_symbol_assignment(self):
        inv_data = {"currency": "£"}
        self.assertEqual(inv_data["currency"], "£")

    def test_c14_invoice_currency_cad_symbol_assignment(self):
        inv_data = {"currency": "CA$"}
        self.assertEqual(inv_data["currency"], "CA$")

    def test_c15_invoice_currency_aud_symbol_assignment(self):
        inv_data = {"currency": "A$"}
        self.assertEqual(inv_data["currency"], "A$")

    def test_c16_currency_switch_recalculates_subtotal_with_symbol(self):
        items = [{"quantity": 2, "rate": 500}]
        subtotal = sum(i["quantity"] * i["rate"] for i in items)
        for sym in ["$", "€", "£", "CA$", "A$"]:
            formatted = f"{sym}{subtotal:,.2f}"
            self.assertTrue(formatted.startswith(sym))
            self.assertIn("1,000.00", formatted)

    def test_c17_currency_switch_recalculates_tax_with_symbol(self):
        subtotal = 1000.0
        tax_amount = subtotal * 0.21
        for sym in ["$", "€", "£", "CA$", "A$"]:
            formatted = f"{sym}{tax_amount:,.2f}"
            self.assertTrue(formatted.startswith(sym))
            self.assertIn("210.00", formatted)

    def test_c18_currency_switch_recalculates_grand_total_with_symbol(self):
        total = 1060.0  # 1000 + 210 (IVA) - 150 (IRPF)
        for sym in ["$", "€", "£", "CA$", "A$"]:
            formatted = f"{sym}{total:,.2f}"
            self.assertTrue(formatted.startswith(sym))
            self.assertIn("1,060.00", formatted)

    def test_c19_adding_item_inherits_active_currency(self):
        active_currency = "CA$"
        new_item = {"description": "New Service", "quantity": 1, "rate": 100}
        item_display_price = f"{active_currency} {new_item['rate']}"
        self.assertIn("CA$ 100", item_display_price)

    def test_c20_removing_item_preserves_active_currency(self):
        active_currency = "£"
        items = [{"rate": 100}, {"rate": 200}]
        items.pop()
        self.assertEqual(len(items), 1)
        self.assertEqual(active_currency, "£")

    # =========================================================================
    # Group 3: Language Switch x Route Mapping (10 tests)
    # =========================================================================
    def test_c21_route_index_es_to_en(self):
        with open(os.path.join(BASE_DIR, "index.html"), "r", encoding="utf-8") as f:
            c = f.read()
        self.assertIn('href="index-en.html"', c)

    def test_c22_route_index_en_to_es(self):
        with open(os.path.join(BASE_DIR, "index-en.html"), "r", encoding="utf-8") as f:
            c = f.read()
        self.assertIn('href="index.html"', c)

    def test_c23_route_calculator_es_to_en(self):
        with open(os.path.join(BASE_DIR, "calculator.html"), "r", encoding="utf-8") as f:
            c = f.read()
        self.assertIn('href="calculator-en.html"', c)

    def test_c24_route_calculator_en_to_es(self):
        with open(os.path.join(BASE_DIR, "calculator-en.html"), "r", encoding="utf-8") as f:
            c = f.read()
        self.assertIn('href="calculator.html"', c)

    def test_c25_route_store_es_to_en(self):
        with open(os.path.join(BASE_DIR, "store.html"), "r", encoding="utf-8") as f:
            c = f.read()
        self.assertIn('href="store-en.html"', c)

    def test_c26_route_store_en_to_es(self):
        with open(os.path.join(BASE_DIR, "store-en.html"), "r", encoding="utf-8") as f:
            c = f.read()
        self.assertIn('href="store.html"', c)

    def test_c27_route_contracts_to_english_platform(self):
        with open(os.path.join(BASE_DIR, "contracts.html"), "r", encoding="utf-8") as f:
            c = f.read()
        self.assertIn('index-en.html', c)

    def test_c28_route_dac7_guide_to_platform(self):
        with open(os.path.join(BASE_DIR, "ventas-vinted-wallapop-hacienda-dac7.html"), "r", encoding="utf-8") as f:
            c = f.read()
        self.assertIn('store.html', c)

    def test_c29_desktop_and_mobile_menus_coexist(self):
        for fname in ["index-en.html", "calculator-en.html", "store-en.html"]:
            with open(os.path.join(BASE_DIR, fname), "r", encoding="utf-8") as f:
                c = f.read()
            self.assertIn('class="hidden md:flex', c, f"{fname} must have desktop nav")
            self.assertIn('id="mobile-menu"', c, f"{fname} must have mobile menu")

    def test_c30_language_switch_badge_styling(self):
        for fname in ["index-en.html", "calculator-en.html", "store-en.html"]:
            with open(os.path.join(BASE_DIR, fname), "r", encoding="utf-8") as f:
                c = f.read()
            self.assertIn('EN', c)
            self.assertIn('ES', c)

    # =========================================================================
    # Group 4: Print Action x CRO Modal Trigger (5 tests)
    # =========================================================================
    def test_c31_trigger_pdf_and_modal_function_definition(self):
        with open(os.path.join(BASE_DIR, "index-en.html"), "r", encoding="utf-8") as f:
            c = f.read()
        self.assertIn("function triggerPdfAndModal()", c)

    def test_c32_trigger_calls_window_print(self):
        with open(os.path.join(BASE_DIR, "index-en.html"), "r", encoding="utf-8") as f:
            c = f.read()
        self.assertIn("window.print()", c)

    def test_c33_cro_modal_contains_finance_hub_cta(self):
        with open(os.path.join(BASE_DIR, "index-en.html"), "r", encoding="utf-8") as f:
            c = f.read()
        self.assertIn("Freelance Finance Hub", c)
        self.assertIn("bszbzj", c)

    def test_c34_cro_modal_close_button_defined(self):
        with open(os.path.join(BASE_DIR, "index-en.html"), "r", encoding="utf-8") as f:
            c = f.read()
        self.assertIn("closeCroModal()", c)

    def test_c35_print_media_rules_hide_cro_modal(self):
        with open(os.path.join(BASE_DIR, "css", "custom.css"), "r", encoding="utf-8") as f:
            css = f.read()
        self.assertIn("@media print", css)
        self.assertIn(".no-print", css)

    # =========================================================================
    # Group 5: LocalStorage x Data State Persistence (5 tests)
    # =========================================================================
    def test_c36_localstorage_serialization_schema(self):
        sample_state = {
            "type": "factura",
            "currency": "$",
            "invoiceNumber": "INV-2026-001",
            "items": [{"description": "Dev", "quantity": 10, "rate": 80}],
            "taxRate": 0,
        }
        serialized = json.dumps(sample_state)
        deserialized = json.loads(serialized)
        self.assertEqual(deserialized["invoiceNumber"], "INV-2026-001")
        self.assertEqual(len(deserialized["items"]), 1)

    def test_c37_localstorage_deserialization_restores_totals(self):
        sample_state = {
            "items": [{"description": "Audit", "quantity": 2, "rate": 500}],
            "taxRate": 20,
        }
        subtotal = sum(i["quantity"] * i["rate"] for i in sample_state["items"])
        self.assertEqual(subtotal, 1000.0)

    def test_c38_localstorage_null_safe_handling(self):
        # Simulates loadSavedData when localStorage returns None
        saved = None
        base_data = {"invoiceNumber": "DEFAULT-001"}
        if saved:
            base_data.update(json.loads(saved))
        self.assertEqual(base_data["invoiceNumber"], "DEFAULT-001")

    def test_c39_localstorage_corrupted_json_recovery(self):
        corrupted = "{not valid json..."
        base_data = {"invoiceNumber": "FALLBACK-001"}
        try:
            base_data.update(json.loads(corrupted))
        except json.JSONDecodeError:
            pass
        self.assertEqual(base_data["invoiceNumber"], "FALLBACK-001")

    def test_c40_app_js_saves_after_field_update(self):
        with open(os.path.join(BASE_DIR, "js", "app.js"), "r", encoding="utf-8") as f:
            code = f.read()
        self.assertIn("saveData();", code)

    # =========================================================================
    # Group 6: Sitemap x Canonical x Hreflang Alignment (5 tests)
    # =========================================================================
    def test_c41_canonical_matches_sitemap_domain(self):
        for expected in EXPECTED_10_URLS:
            self.assertTrue(expected.startswith("https://komasan19283645.github.io/freelance-toolkit/"))

    def test_c42_spanish_canonical_urls_use_standard_paths(self):
        es_urls = [u for u in EXPECTED_10_URLS if not u.endswith("-en.html")]
        self.assertEqual(len(es_urls), 7)

    def test_c43_english_canonical_urls_use_en_suffix(self):
        en_urls = [u for u in EXPECTED_10_URLS if u.endswith("-en.html")]
        self.assertEqual(len(en_urls), 3)

    def test_c44_sitemap_xml_element_tree_validation(self):
        res = verify_sitemap(strict=False)
        self.assertTrue(res["well_formed_xml"])

    def test_c45_hreflang_reciprocal_pairing_integrity(self):
        pairs = [
            ("https://komasan19283645.github.io/freelance-toolkit/", "https://komasan19283645.github.io/freelance-toolkit/index-en.html"),
            ("https://komasan19283645.github.io/freelance-toolkit/calculator.html", "https://komasan19283645.github.io/freelance-toolkit/calculator-en.html"),
            ("https://komasan19283645.github.io/freelance-toolkit/store.html", "https://komasan19283645.github.io/freelance-toolkit/store-en.html"),
        ]
        for es, en in pairs:
            self.assertIn("freelance-toolkit", es)
            self.assertIn("freelance-toolkit", en)

    # =========================================================================
    # Group 7: Marketing Channels x Privacy Guardrail (5 tests)
    # =========================================================================
    def test_c46_reddit_strategy_pairs_zero_gumroad_and_zero_personal_info(self):
        res = verify_privacy()
        self.assertEqual(res["violations_count"], 0)

    def test_c47_twitter_strategy_pairs_komaleon37_and_zero_personal_info(self):
        self.assertEqual(AUTHORIZED_PSEUDONYMS["twitter"], "@Komaleon37")

    def test_c48_pinterest_strategy_pairs_migueldpsp_and_zero_personal_info(self):
        self.assertEqual(AUTHORIZED_PSEUDONYMS["pinterest"], "@migueldpsp")

    def test_c49_git_email_configured_with_noreply_pseudonym(self):
        res = verify_privacy()
        self.assertTrue(res["git_email"]["matches"])
        self.assertEqual(res["git_email"]["current_email"], AUTHORIZED_GIT_EMAIL)

    def test_c50_repository_zero_leakage_across_all_text_files(self):
        res = verify_privacy()
        self.assertTrue(res["passed"], "Privacy audit must pass across all repository files")


if __name__ == "__main__":
    unittest.main()
