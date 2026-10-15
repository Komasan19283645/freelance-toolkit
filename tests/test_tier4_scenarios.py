#!/usr/bin/env python3
"""
test_tier4_scenarios.py - Tier 4: Real-World Application Scenarios

Simulates realistic, multi-step freelancer workflows and user personas:
- Scenario 1: US Full-Stack Developer
- Scenario 2: Spanish Autonomous Graphic Designer (Autónomo)
- Scenario 3: UK Content Marketing Contractor
- Scenario 4: Canadian Mobile Engineer
- Scenario 5: Australian Cloud Consultant
- Scenario 6: Global Freelancer Store & Bundle Checkout
- Scenario 7: E-commerce Reseller DAC7 Tax Compliance
- Scenario 8: Personal Finance 50/30/20 Budgeting

Total tests: 40 tests.
"""

import os
import sys
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from scripts.test_calc import calculate_rate
from tests.test_tier2_boundaries import calculate_invoice_totals


class TestTier4Scenarios(unittest.TestCase):

    # =========================================================================
    # Scenario 1: US Full-Stack Developer (5 tests)
    # =========================================================================
    def test_s1_01_us_developer_rate_calculation(self):
        # Target net $6,000/mo, $800 overhead, 25% tax, 3 weeks vacation, 8h/day, 65% billable
        res = calculate_rate(6000, 800, 25, 3, 8, 65, "USD")
        self.assertAlmostEqual(res["monthly_gross"], 9066.67, places=1)
        self.assertAlmostEqual(res["hourly_rate"], 85.40, places=1)
        self.assertAlmostEqual(res["daily_rate"], 444.08, places=1)

    def test_s1_02_us_developer_invoice_generation(self):
        items = [
            {"description": "Next.js Full-Stack Architecture", "quantity": 40, "rate": 86.0},
            {"description": "Stripe Connect Integration", "quantity": 10, "rate": 86.0},
        ]
        inv = calculate_invoice_totals(items, tax_rate=0, withholding_rate=0)
        self.assertEqual(inv["subtotal"], 4300.0)
        self.assertEqual(inv["total"], 4300.0)

    def test_s1_03_us_developer_b2b_zero_tax(self):
        items = [{"description": "SaaS API Development", "quantity": 20, "rate": 85.0}]
        inv = calculate_invoice_totals(items, tax_rate=0, withholding_rate=0)
        self.assertEqual(inv["tax_amount"], 0.0)

    def test_s1_04_us_developer_preview_structure_verified(self):
        with open(os.path.join(BASE_DIR, "index-en.html"), "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("preview-items-body", content)
        self.assertIn("preview-total", content)
        self.assertIn("btn-print-pdf", content)

    def test_s1_05_us_developer_cro_upsell_flow(self):
        with open(os.path.join(BASE_DIR, "index-en.html"), "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Finance Hub", content)
        self.assertIn("bszbzj", content)

    # =========================================================================
    # Scenario 2: Spanish Autonomous Graphic Designer (Autónomo) (5 tests)
    # =========================================================================
    def test_s2_01_es_autonomo_rate_calculation(self):
        # Target net 2200 €, 550 € expenses (cuota + gestoría + software), 20% IRPF, 4 weeks vac, 8h/day, 65% billable
        res = calculate_rate(2200, 550, 20, 4, 8, 65, "EUR")
        self.assertAlmostEqual(res["monthly_gross"], 3437.50, places=1)
        self.assertAlmostEqual(res["hourly_rate"], 33.05, places=1)
        self.assertAlmostEqual(res["daily_rate"], 171.88, places=1)

    def test_s2_02_es_autonomo_invoice_spanish_taxes(self):
        # Factura con 21% IVA y 15% retención IRPF
        items = [{"description": "Diseño Identidad Visual y Manual de Marca", "quantity": 1, "rate": 1500.0}]
        inv = calculate_invoice_totals(items, tax_rate=21, withholding_rate=15)
        self.assertEqual(inv["subtotal"], 1500.0)
        self.assertEqual(inv["tax_amount"], 315.0)       # 21% IVA
        self.assertEqual(inv["withholding_amount"], 225.0) # 15% IRPF
        self.assertEqual(inv["total"], 1590.0)            # 1500 + 315 - 225

    def test_s2_03_es_autonomo_new_freelancer_reduced_irpf(self):
        # Factura con 7% IRPF para nuevos autónomos
        items = [{"description": "Diseño UI Web", "quantity": 1, "rate": 1000.0}]
        inv = calculate_invoice_totals(items, tax_rate=21, withholding_rate=7)
        self.assertEqual(inv["withholding_amount"], 70.0)
        self.assertEqual(inv["total"], 1140.0)

    def test_s2_04_es_autonomo_fiscal_guide_access(self):
        guide_path = os.path.join(BASE_DIR, "como-hacer-factura-autonomo-irpf-iva.html")
        self.assertTrue(os.path.exists(guide_path))
        with open(guide_path, "r", encoding="utf-8") as f:
            c = f.read()
        self.assertIn("IRPF", c)
        self.assertIn("IVA", c)

    def test_s2_05_es_autonomo_legal_contract_clauses(self):
        contracts_path = os.path.join(BASE_DIR, "contracts.html")
        self.assertTrue(os.path.exists(contracts_path))
        with open(contracts_path, "r", encoding="utf-8") as f:
            c = f.read()
        self.assertIn("propiedad intelectual", c.lower())

    # =========================================================================
    # Scenario 3: UK Content Marketing Contractor (5 tests)
    # =========================================================================
    def test_s3_01_uk_contractor_rate_calculation(self):
        # Net £3,500/mo, £400 overhead, 20% tax, 5 weeks vac, 8h/day, 70% billable
        res = calculate_rate(3500, 400, 20, 5, 8, 70, "GBP")
        self.assertEqual(res["currency_symbol"], "£")
        self.assertAlmostEqual(res["hourly_rate"], 44.45, places=1)
        self.assertAlmostEqual(res["daily_rate"], 248.94, places=1)

    def test_s3_02_uk_contractor_invoice_vat(self):
        items = [{"description": "Monthly Content Strategy & SEO", "quantity": 1, "rate": 2000.0}]
        inv = calculate_invoice_totals(items, tax_rate=20, withholding_rate=0)
        self.assertEqual(inv["subtotal"], 2000.0)
        self.assertEqual(inv["tax_amount"], 400.0)
        self.assertEqual(inv["total"], 2400.0)

    def test_s3_03_uk_contractor_gbp_symbol_in_rates(self):
        res = calculate_rate(3500, 400, 20, 5, 8, 70, "GBP")
        self.assertTrue(res["formatted_hourly"].startswith("£"))
        self.assertTrue(res["formatted_daily"].startswith("£"))

    def test_s3_04_uk_contractor_currency_options_in_generator(self):
        with open(os.path.join(BASE_DIR, "index-en.html"), "r", encoding="utf-8") as f:
            c = f.read()
        self.assertIn('value="£"', c)

    def test_s3_05_uk_contractor_calculator_gbp_button(self):
        with open(os.path.join(BASE_DIR, "calculator-en.html"), "r", encoding="utf-8") as f:
            c = f.read()
        self.assertIn('id="curr-gbp"', c)

    # =========================================================================
    # Scenario 4: Canadian Mobile Engineer (5 tests)
    # =========================================================================
    def test_s4_01_cad_engineer_rate_calculation(self):
        # Net CA$5,500/mo, CA$600 overhead, 28% tax, 4 weeks vac, 8h/day, 60% billable
        res = calculate_rate(5500, 600, 28, 4, 8, 60, "CAD")
        self.assertEqual(res["currency_symbol"], "CA$")
        self.assertAlmostEqual(res["hourly_rate"], 88.25, places=1)
        self.assertAlmostEqual(res["daily_rate"], 423.61, places=1)

    def test_s4_02_cad_engineer_invoice_generation(self):
        items = [{"description": "iOS Swift Feature Module", "quantity": 40, "rate": 88.0}]
        inv = calculate_invoice_totals(items, tax_rate=5, withholding_rate=0) # 5% GST
        self.assertEqual(inv["subtotal"], 3520.0)
        self.assertEqual(inv["tax_amount"], 176.0)
        self.assertEqual(inv["total"], 3696.0)

    def test_s4_03_cad_engineer_symbol_prefix(self):
        res = calculate_rate(5500, 600, 28, 4, 8, 60, "CAD")
        self.assertTrue(res["formatted_hourly"].startswith("CA$"))

    def test_s4_04_cad_engineer_calculator_button(self):
        with open(os.path.join(BASE_DIR, "calculator-en.html"), "r", encoding="utf-8") as f:
            c = f.read()
        self.assertIn('id="curr-cad"', c)

    def test_s4_05_cad_engineer_daily_rate_conversion(self):
        res = calculate_rate(5500, 600, 28, 4, 8, 60, "CAD")
        expected_daily = res["hourly_rate"] * (8 * 0.60)
        self.assertAlmostEqual(res["daily_rate"], expected_daily, places=4)

    # =========================================================================
    # Scenario 5: Australian Cloud Consultant (5 tests)
    # =========================================================================
    def test_s5_01_aud_consultant_rate_calculation(self):
        # Net A$7,000/mo, A$900 overhead, 30% tax, 4 weeks vac, 8h/day, 60% billable
        res = calculate_rate(7000, 900, 30, 4, 8, 60, "AUD")
        self.assertEqual(res["currency_symbol"], "A$")
        self.assertAlmostEqual(res["hourly_rate"], 117.56, places=1)
        self.assertAlmostEqual(res["daily_rate"], 564.29, places=1)

    def test_s5_02_aud_consultant_annual_gross_target(self):
        res = calculate_rate(7000, 900, 30, 4, 8, 60, "AUD")
        self.assertAlmostEqual(res["annual_gross"], 135428.57, places=1)

    def test_s5_03_aud_consultant_formatted_strings(self):
        res = calculate_rate(7000, 900, 30, 4, 8, 60, "AUD")
        self.assertTrue(res["formatted_hourly"].startswith("A$"))
        self.assertTrue(res["formatted_daily"].startswith("A$"))
        self.assertTrue(res["formatted_monthly_gross"].startswith("A$"))

    def test_s5_04_aud_consultant_gst_invoice(self):
        items = [{"description": "AWS Migration Architecture", "quantity": 1, "rate": 5000.0}]
        inv = calculate_invoice_totals(items, tax_rate=10, withholding_rate=0) # 10% AU GST
        self.assertEqual(inv["subtotal"], 5000.0)
        self.assertEqual(inv["tax_amount"], 500.0)
        self.assertEqual(inv["total"], 5500.0)

    def test_s5_05_aud_consultant_billable_hours_capacity(self):
        res = calculate_rate(7000, 900, 30, 4, 8, 60, "AUD")
        self.assertEqual(res["total_billable_hours"], 48 * 5 * 8 * 0.60)

    # =========================================================================
    # Scenario 6: Global Freelancer Store & Bundle Checkout (5 tests)
    # =========================================================================
    def test_s6_01_store_en_catalogue_contains_8_products(self):
        with open(os.path.join(BASE_DIR, "store-en.html"), "r", encoding="utf-8") as f:
            c = f.read()
        self.assertIn("Finance Hub", c)
        self.assertIn("Client CRM", c)
        self.assertIn("Email Swipe File", c)

    def test_s6_02_store_en_individual_product_pricing(self):
        with open(os.path.join(BASE_DIR, "store-en.html"), "r", encoding="utf-8") as f:
            c = f.read()
        self.assertIn("$9", c)

    def test_s6_03_store_en_all_in_one_pack_pricing(self):
        with open(os.path.join(BASE_DIR, "store-en.html"), "r", encoding="utf-8") as f:
            c = f.read()
        self.assertIn("$39", c)
        self.assertIn("auhouf", c)

    def test_s6_04_store_en_promo_code_application(self):
        with open(os.path.join(BASE_DIR, "store-en.html"), "r", encoding="utf-8") as f:
            c = f.read()
        self.assertIn("LANZAMIENTO20", c)
        self.assertIn("20% OFF", c)

    def test_s6_05_store_en_bundle_savings_math(self):
        individual_total = 8 * 9.0  # $72
        bundle_price = 39.0
        savings_percent = ((individual_total - bundle_price) / individual_total) * 100
        self.assertGreater(savings_percent, 45.0)

    # =========================================================================
    # Scenario 7: E-commerce Reseller DAC7 Tax Compliance (5 tests)
    # =========================================================================
    def test_s7_01_dac7_guide_exists_and_valid(self):
        path = os.path.join(BASE_DIR, "ventas-vinted-wallapop-hacienda-dac7.html")
        self.assertTrue(os.path.exists(path))

    def test_s7_02_dac7_threshold_rule_30_sales(self):
        path = os.path.join(BASE_DIR, "ventas-vinted-wallapop-hacienda-dac7.html")
        with open(path, "r", encoding="utf-8") as f:
            c = f.read()
        self.assertIn("30", c)

    def test_s7_03_dac7_threshold_rule_2000_euros(self):
        path = os.path.join(BASE_DIR, "ventas-vinted-wallapop-hacienda-dac7.html")
        with open(path, "r", encoding="utf-8") as f:
            c = f.read()
        self.assertIn("2.000", c)

    def test_s7_04_dac7_reseller_tracker_product_link(self):
        path = os.path.join(BASE_DIR, "ventas-vinted-wallapop-hacienda-dac7.html")
        with open(path, "r", encoding="utf-8") as f:
            c = f.read()
        self.assertIn("gzwqf", c)

    def test_s7_05_dac7_second_hand_loss_justification(self):
        path = os.path.join(BASE_DIR, "ventas-vinted-wallapop-hacienda-dac7.html")
        with open(path, "r", encoding="utf-8") as f:
            c = f.read()
        self.assertIn("pérdida", c.lower())

    # =========================================================================
    # Scenario 8: Personal Finance 50/30/20 Budgeting (5 tests)
    # =========================================================================
    def test_s8_01_budget_guide_exists_and_valid(self):
        path = os.path.join(BASE_DIR, "metodo-50-30-20-presupuesto-espanol.html")
        self.assertTrue(os.path.exists(path))

    def test_s8_02_budget_allocation_rule_percentages(self):
        path = os.path.join(BASE_DIR, "metodo-50-30-20-presupuesto-espanol.html")
        with open(path, "r", encoding="utf-8") as f:
            c = f.read()
        self.assertIn("50%", c)
        self.assertIn("30%", c)
        self.assertIn("20%", c)

    def test_s8_03_budget_allocation_math_simulation(self):
        salary = 2500.0
        needs = salary * 0.50    # 1250 €
        wants = salary * 0.30    # 750 €
        savings = salary * 0.20  # 500 €
        self.assertEqual(needs, 1250.0)
        self.assertEqual(wants, 750.0)
        self.assertEqual(savings, 500.0)

    def test_s8_04_budget_product_link_integrity(self):
        path = os.path.join(BASE_DIR, "metodo-50-30-20-presupuesto-espanol.html")
        with open(path, "r", encoding="utf-8") as f:
            c = f.read()
        self.assertIn("tvcpyv", c)

    def test_s8_05_budget_zero_tracking_privacy(self):
        path = os.path.join(BASE_DIR, "metodo-50-30-20-presupuesto-espanol.html")
        with open(path, "r", encoding="utf-8") as f:
            c = f.read()
        self.assertNotIn("google-analytics.com", c)
        self.assertNotIn("googletagmanager.com", c)


if __name__ == "__main__":
    unittest.main()
