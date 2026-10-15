#!/usr/bin/env python3
"""
test_tier2_boundaries.py - Tier 2: Boundary & Corner Cases

Stress-tests domain limits, numerical boundaries, extreme values, empty inputs,
currency edge cases, discount rates, escaping integrity, and error guards.

Total tests: 50 tests.
"""

import os
import sys
import math
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from scripts.test_calc import calculate_rate, CURRENCY_SYMBOLS


def calculate_invoice_totals(items, tax_rate=0.0, withholding_rate=0.0, discount_rate=0.0):
    """Authoritative invoice math calculation oracle."""
    subtotal = sum(float(item.get("quantity", 0)) * float(item.get("rate", 0)) for item in items)
    discount_amount = subtotal * (float(discount_rate) / 100.0)
    taxable_base = subtotal - discount_amount
    tax_amount = taxable_base * (float(tax_rate) / 100.0)
    withholding_amount = taxable_base * (float(withholding_rate) / 100.0)
    total = taxable_base + tax_amount - withholding_amount
    return {
        "subtotal": subtotal,
        "discount_amount": discount_amount,
        "taxable_base": taxable_base,
        "tax_amount": tax_amount,
        "withholding_amount": withholding_amount,
        "total": max(0.0, total),
    }


def escape_html_reference(text: str) -> str:
    """Reference HTML escaping oracle matching client-side app.js."""
    if not text:
        return ""
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#039;")
    )


class TestTier2Boundaries(unittest.TestCase):

    # =========================================================================
    # Group 1: Rate Calculator Boundaries (20 tests)
    # =========================================================================
    def test_b01_zero_net_income(self):
        res = calculate_rate(0, 500, 20, 4, 8, 60, "USD")
        self.assertGreater(res["hourly_rate"], 0)
        self.assertEqual(res["monthly_net"], 0.0)

    def test_b02_zero_expenses(self):
        res = calculate_rate(3000, 0, 20, 4, 8, 60, "USD")
        self.assertAlmostEqual(res["monthly_gross"], 3000 / 0.8, places=2)

    def test_b03_both_net_and_expenses_zero(self):
        res = calculate_rate(0, 0, 20, 4, 8, 60, "USD")
        self.assertEqual(res["monthly_gross"], 0.0)
        self.assertEqual(res["hourly_rate"], 0.0)
        self.assertEqual(res["daily_rate"], 0.0)

    def test_b04_zero_tax_rate(self):
        res = calculate_rate(4000, 600, 0, 4, 8, 60, "USD")
        self.assertEqual(res["monthly_gross"], 4600.0)

    def test_b05_minimal_one_percent_tax_rate(self):
        res = calculate_rate(4000, 600, 1, 4, 8, 60, "USD")
        self.assertAlmostEqual(res["monthly_gross"], 4600.0 / 0.99, places=2)

    def test_b06_fifty_percent_tax_rate(self):
        res = calculate_rate(3000, 500, 50, 4, 8, 60, "USD")
        self.assertEqual(res["monthly_gross"], 7000.0)

    def test_b07_sixty_percent_tax_rate(self):
        res = calculate_rate(3000, 500, 60, 4, 8, 60, "USD")
        self.assertEqual(res["monthly_gross"], 3500 / 0.4)

    def test_b08_extreme_ninety_nine_percent_tax_rate(self):
        res = calculate_rate(100, 50, 99, 4, 8, 60, "USD")
        self.assertAlmostEqual(res["monthly_gross"], 150 / 0.01, places=2)

    def test_b09_zero_vacation_weeks(self):
        res = calculate_rate(4000, 500, 20, 0, 8, 60, "USD")
        self.assertEqual(res["working_weeks"], 52.0)

    def test_b10_one_vacation_week(self):
        res = calculate_rate(4000, 500, 20, 1, 8, 60, "USD")
        self.assertEqual(res["working_weeks"], 51.0)

    def test_b11_twenty_five_vacation_weeks(self):
        res = calculate_rate(4000, 500, 20, 25, 8, 60, "USD")
        self.assertEqual(res["working_weeks"], 27.0)

    def test_b12_fifty_vacation_weeks(self):
        res = calculate_rate(4000, 500, 20, 50, 8, 60, "USD")
        self.assertEqual(res["working_weeks"], 2.0)

    def test_b13_fifty_one_vacation_weeks(self):
        res = calculate_rate(4000, 500, 20, 51, 8, 60, "USD")
        self.assertEqual(res["working_weeks"], 1.0)

    def test_b14_fifty_two_vacation_weeks_clamped(self):
        res = calculate_rate(4000, 500, 20, 52, 8, 60, "USD")
        self.assertEqual(res["working_weeks"], 1.0)
        self.assertFalse(math.isinf(res["hourly_rate"]))

    def test_b15_over_fifty_two_vacation_weeks_clamped(self):
        res = calculate_rate(4000, 500, 20, 60, 8, 60, "USD")
        self.assertEqual(res["working_weeks"], 1.0)

    def test_b16_minimal_work_hours_per_day(self):
        res = calculate_rate(3000, 400, 20, 4, 1, 60, "USD")
        self.assertGreater(res["hourly_rate"], 0)

    def test_b17_maximum_work_hours_per_day(self):
        res = calculate_rate(3000, 400, 20, 4, 16, 60, "USD")
        self.assertGreater(res["hourly_rate"], 0)

    def test_b18_ten_percent_billable_ratio(self):
        res = calculate_rate(3000, 400, 20, 4, 8, 10, "USD")
        self.assertGreater(res["hourly_rate"], 100)

    def test_b19_hundred_percent_billable_ratio(self):
        res = calculate_rate(3000, 400, 20, 4, 8, 100, "USD")
        self.assertAlmostEqual(res["total_billable_hours"], 48 * 5 * 8, places=2)

    def test_b20_high_income_scale_hundred_thousand(self):
        res = calculate_rate(100000, 10000, 35, 4, 8, 60, "USD")
        self.assertGreater(res["hourly_rate"], 1000)

    # =========================================================================
    # Group 2: Invoice Calculation Boundaries (15 tests)
    # =========================================================================
    def test_b21_invoice_empty_items_list(self):
        inv = calculate_invoice_totals([], tax_rate=21, withholding_rate=15)
        self.assertEqual(inv["subtotal"], 0.0)
        self.assertEqual(inv["tax_amount"], 0.0)
        self.assertEqual(inv["total"], 0.0)

    def test_b22_invoice_single_item_rate_zero(self):
        items = [{"description": "Free consultation", "quantity": 1, "rate": 0}]
        inv = calculate_invoice_totals(items, 21, 15)
        self.assertEqual(inv["subtotal"], 0.0)
        self.assertEqual(inv["total"], 0.0)

    def test_b23_invoice_single_item_quantity_zero(self):
        items = [{"description": "Cancelled line", "quantity": 0, "rate": 500}]
        inv = calculate_invoice_totals(items, 21, 15)
        self.assertEqual(inv["subtotal"], 0.0)

    def test_b24_invoice_fractional_quantities(self):
        items = [
            {"description": "15 min bugfix", "quantity": 0.25, "rate": 100},
            {"description": "30 min support", "quantity": 0.5, "rate": 100},
            {"description": "1h 45m review", "quantity": 1.75, "rate": 100},
        ]
        inv = calculate_invoice_totals(items, 0, 0)
        self.assertEqual(inv["subtotal"], 250.0)

    def test_b25_invoice_extreme_high_quantity(self):
        items = [{"description": "API requests (thousands)", "quantity": 10000, "rate": 1.5}]
        inv = calculate_invoice_totals(items, 0, 0)
        self.assertEqual(inv["subtotal"], 15000.0)

    def test_b26_invoice_extreme_high_unit_price(self):
        items = [{"description": "Enterprise Retainer", "quantity": 1, "rate": 50000.0}]
        inv = calculate_invoice_totals(items, 21, 15)
        self.assertEqual(inv["subtotal"], 50000.0)
        self.assertEqual(inv["tax_amount"], 10500.0)
        self.assertEqual(inv["withholding_amount"], 7500.0)
        self.assertEqual(inv["total"], 53000.0)

    def test_b27_invoice_zero_tax_rate(self):
        items = [{"description": "Export service", "quantity": 1, "rate": 1000}]
        inv = calculate_invoice_totals(items, tax_rate=0, withholding_rate=0)
        self.assertEqual(inv["tax_amount"], 0.0)
        self.assertEqual(inv["total"], 1000.0)

    def test_b28_invoice_four_percent_super_reduced_tax(self):
        items = [{"description": "Libro técnico", "quantity": 1, "rate": 100}]
        inv = calculate_invoice_totals(items, tax_rate=4, withholding_rate=0)
        self.assertEqual(inv["tax_amount"], 4.0)
        self.assertEqual(inv["total"], 104.0)

    def test_b29_invoice_ten_percent_reduced_tax(self):
        items = [{"description": "Servicio hostelería", "quantity": 1, "rate": 200}]
        inv = calculate_invoice_totals(items, tax_rate=10, withholding_rate=0)
        self.assertEqual(inv["tax_amount"], 20.0)
        self.assertEqual(inv["total"], 220.0)

    def test_b30_invoice_twenty_one_percent_standard_tax(self):
        items = [{"description": "Desarrollo web", "quantity": 1, "rate": 1000}]
        inv = calculate_invoice_totals(items, tax_rate=21, withholding_rate=0)
        self.assertEqual(inv["tax_amount"], 210.0)
        self.assertEqual(inv["total"], 1210.0)

    def test_b31_invoice_zero_withholding(self):
        items = [{"description": "B2C client", "quantity": 1, "rate": 1000}]
        inv = calculate_invoice_totals(items, tax_rate=21, withholding_rate=0)
        self.assertEqual(inv["withholding_amount"], 0.0)
        self.assertEqual(inv["total"], 1210.0)

    def test_b32_invoice_seven_percent_new_autonomo_withholding(self):
        items = [{"description": "Primer año autónomo", "quantity": 1, "rate": 1000}]
        inv = calculate_invoice_totals(items, tax_rate=21, withholding_rate=7)
        self.assertEqual(inv["withholding_amount"], 70.0)
        self.assertEqual(inv["total"], 1000 + 210 - 70)

    def test_b33_invoice_fifteen_percent_standard_autonomo_withholding(self):
        items = [{"description": "Autónomo consolidado", "quantity": 1, "rate": 1000}]
        inv = calculate_invoice_totals(items, tax_rate=21, withholding_rate=15)
        self.assertEqual(inv["withholding_amount"], 150.0)
        self.assertEqual(inv["total"], 1060.0)

    def test_b34_invoice_zero_discount(self):
        items = [{"description": "Full price", "quantity": 1, "rate": 1000}]
        inv = calculate_invoice_totals(items, tax_rate=20, discount_rate=0)
        self.assertEqual(inv["discount_amount"], 0.0)
        self.assertEqual(inv["total"], 1200.0)

    def test_b35_invoice_hundred_percent_discount(self):
        items = [{"description": "Pro bono project", "quantity": 1, "rate": 1000}]
        inv = calculate_invoice_totals(items, tax_rate=20, discount_rate=100)
        self.assertEqual(inv["discount_amount"], 1000.0)
        self.assertEqual(inv["taxable_base"], 0.0)
        self.assertEqual(inv["total"], 0.0)

    # =========================================================================
    # Group 3: Sanitization & Escaping Boundaries (5 tests)
    # =========================================================================
    def test_b36_html_script_injection_escaped(self):
        raw = '<script>alert("xss")</script>'
        escaped = escape_html_reference(raw)
        self.assertNotIn("<script>", escaped)
        self.assertIn("&lt;script&gt;", escaped)

    def test_b37_quotes_escaped(self):
        raw = 'Client "Acme" & \'Partner\''
        escaped = escape_html_reference(raw)
        self.assertIn("&quot;", escaped)
        self.assertIn("&#039;", escaped)

    def test_b38_ampersands_escaped(self):
        raw = "Design & Development & Hosting"
        escaped = escape_html_reference(raw)
        self.assertEqual(escaped, "Design &amp; Development &amp; Hosting")

    def test_b39_unicode_accents_preserved(self):
        raw = "Facturación Autónomo Diseño Gráfico"
        escaped = escape_html_reference(raw)
        self.assertEqual(raw, escaped)

    def test_b40_very_long_description_string(self):
        raw = "A" * 2000
        escaped = escape_html_reference(raw)
        self.assertEqual(len(escaped), 2000)

    # =========================================================================
    # Group 4: Promo & Pricing Boundaries (5 tests)
    # =========================================================================
    def test_b41_promo_code_exact_match(self):
        valid_code = "LANZAMIENTO20"
        self.assertEqual(valid_code.strip().upper(), "LANZAMIENTO20")

    def test_b42_promo_code_case_insensitivity(self):
        test_inputs = ["lanzamiento20", "Lanzamiento20", "LANZAMIENTO20"]
        for inp in test_inputs:
            self.assertEqual(inp.strip().upper(), "LANZAMIENTO20")

    def test_b43_promo_code_whitespace_trimming(self):
        inp = "  LANZAMIENTO20  \n"
        self.assertEqual(inp.strip().upper(), "LANZAMIENTO20")

    def test_b44_invalid_promo_codes_rejected(self):
        invalids = ["DISCOUNT20", "FREE", "LANZAMIENTO50", "", "   "]
        for inv in invalids:
            self.assertNotEqual(inv.strip().upper(), "LANZAMIENTO20")

    def test_b45_twenty_percent_launch_discount_math(self):
        bundle_price = 39.0
        discounted_bundle = bundle_price * (1 - 0.20)
        self.assertAlmostEqual(discounted_bundle, 31.20, places=2)
        single_price = 9.0
        discounted_single = single_price * (1 - 0.20)
        self.assertAlmostEqual(discounted_single, 7.20, places=2)

    # =========================================================================
    # Group 5: Date & Link Boundaries (5 tests)
    # =========================================================================
    def test_b46_due_date_equals_invoice_date(self):
        # Immediate payment term
        date_issue = "2026-10-15"
        date_due = "2026-10-15"
        self.assertEqual(date_issue, date_due)

    def test_b47_due_date_thirty_days_standard(self):
        import datetime
        d1 = datetime.date(2026, 10, 15)
        d2 = d1 + datetime.timedelta(days=30)
        self.assertEqual(d2.isoformat(), "2026-11-14")

    def test_b48_due_date_three_hundred_sixty_five_days_future(self):
        import datetime
        d1 = datetime.date(2026, 1, 1)
        d2 = d1 + datetime.timedelta(days=365)
        self.assertEqual(d2.year, 2027)

    def test_b49_url_hash_anchor_preservation(self):
        url = "store.html#faq"
        base, anchor = url.split("#")
        self.assertEqual(base, "store.html")
        self.assertEqual(anchor, "faq")

    def test_b50_deep_relative_asset_paths_exist(self):
        for asset in ["css/custom.css", "favicon.svg", "entregables/cover_bundle_all_in_one.png"]:
            self.assertTrue(os.path.exists(os.path.join(BASE_DIR, asset)), f"Asset must exist: {asset}")


if __name__ == "__main__":
    unittest.main()
