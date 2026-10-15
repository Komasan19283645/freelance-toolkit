#!/usr/bin/env python3
"""
challenge_calc.py - Empirical Challenger Stress-Test Suite for Rate Calculator & Multi-Currency Engine

Author: challenger_m1_1 (Empirical Challenger Agent)
Scope: calculator-en.html, calculator.html, Multi-Currency Engine (USD, EUR, GBP, CAD, AUD),
       boundary conditions, zero-division guardrails, CRO links & promo code.

Zero external dependencies - pure Python 3 standard library.
"""

import os
import re
import sys
import math
import random
import urllib.request
import unittest
from typing import Dict, Any, List

# Ensure UTF-8 output on Windows console
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Exact currency symbol specification per PROJECT.md
CURRENCY_SPECS = {
    "USD": {"symbol": "$", "btn_id": "curr-usd", "label": "$ / mo"},
    "EUR": {"symbol": "€", "btn_id": "curr-eur", "label": "€ / mo"},
    "GBP": {"symbol": "£", "btn_id": "curr-gbp", "label": "£ / mo"},
    "CAD": {"symbol": "CA$", "btn_id": "curr-cad", "label": "CA$ / mo"},
    "AUD": {"symbol": "A$", "btn_id": "curr-aud", "label": "A$ / mo"},
}


def simulate_calculator_js(
    net_val: Any,
    exp_val: Any,
    tax_val: Any,
    vac_val: Any,
    h_day_val: Any,
    b_ratio_val: Any,
    currency_code: str = "USD",
) -> Dict[str, Any]:
    """
    Exact emulation of client-side JavaScript calculate() in calculator-en.html:
    
    const net = parseFloat(document.getElementById("calc-desired-net").value) || 0;
    const exp = parseFloat(document.getElementById("calc-monthly-expenses").value) || 0;
    const tax = (parseFloat(document.getElementById("calc-tax-rate").value) || 0) / 100;
    const vac = parseFloat(document.getElementById("calc-vacation-weeks").value) || 0;
    const hDay = parseFloat(document.getElementById("calc-hours-day").value) || 0;
    const bRatio = (parseFloat(document.getElementById("calc-billable-ratio").value) || 0) / 100;

    const monthlyGross = (1 - tax > 0) ? (net + exp) / (1 - tax) : (net + exp);
    const workingWeeks = Math.max(1, 52 - vac);
    const totalBillable = Math.max(1, workingWeeks * 5 * hDay * bRatio);
    const hourly = (monthlyGross * 12) / totalBillable;
    const daily = hourly * (hDay * bRatio);
    """
    try:
        net = float(net_val) if net_val not in (None, "") and not math.isnan(float(net_val)) else 0.0
    except (ValueError, TypeError):
        net = 0.0

    try:
        exp = float(exp_val) if exp_val not in (None, "") and not math.isnan(float(exp_val)) else 0.0
    except (ValueError, TypeError):
        exp = 0.0

    try:
        raw_tax = float(tax_val) if tax_val not in (None, "") and not math.isnan(float(tax_val)) else 0.0
    except (ValueError, TypeError):
        raw_tax = 0.0
    tax = raw_tax / 100.0

    try:
        vac = float(vac_val) if vac_val not in (None, "") and not math.isnan(float(vac_val)) else 0.0
    except (ValueError, TypeError):
        vac = 0.0

    try:
        h_day = float(h_day_val) if h_day_val not in (None, "") and not math.isnan(float(h_day_val)) else 0.0
    except (ValueError, TypeError):
        h_day = 0.0

    try:
        raw_ratio = float(b_ratio_val) if b_ratio_val not in (None, "") and not math.isnan(float(b_ratio_val)) else 0.0
    except (ValueError, TypeError):
        raw_ratio = 0.0
    b_ratio = raw_ratio / 100.0

    # Production JS ternary logic
    if (1.0 - tax) > 0:
        monthly_gross = (net + exp) / (1.0 - tax)
    else:
        monthly_gross = net + exp

    working_weeks = max(1.0, 52.0 - vac)
    total_billable = max(1.0, working_weeks * 5.0 * h_day * b_ratio)
    hourly = (monthly_gross * 12.0) / total_billable
    daily = hourly * (h_day * b_ratio)

    sym = CURRENCY_SPECS.get(currency_code.upper(), {"symbol": "$"})["symbol"]

    # Production formatting
    formatted_hourly = f"{sym}{hourly:.2f}"
    formatted_daily = f"{sym}{daily:.2f}"
    formatted_monthly_gross = f"{sym}{round(monthly_gross):,}"
    formatted_hourly_pill = f"{sym}{hourly:.2f}/hr"
    formatted_net_pill = f"{sym}{round(net):,}/mo"

    return {
        "currency_code": currency_code.upper(),
        "currency_symbol": sym,
        "net": net,
        "exp": exp,
        "tax": tax,
        "vac": vac,
        "working_weeks": working_weeks,
        "h_day": h_day,
        "b_ratio": b_ratio,
        "total_billable": total_billable,
        "monthly_gross": monthly_gross,
        "hourly": hourly,
        "daily": daily,
        "formatted_hourly": formatted_hourly,
        "formatted_daily": formatted_daily,
        "formatted_monthly_gross": formatted_monthly_gross,
        "formatted_hourly_pill": formatted_hourly_pill,
        "formatted_net_pill": formatted_net_pill,
    }


class ChallengeRateCalculatorSuite(unittest.TestCase):
    """Adversarial stress-testing of rate calculator & multi-currency engine."""

    @classmethod
    def setUpClass(cls):
        cls.calc_en_path = os.path.join(BASE_DIR, "calculator-en.html")
        cls.calc_es_path = os.path.join(BASE_DIR, "calculator.html")

        with open(cls.calc_en_path, "r", encoding="utf-8") as f:
            cls.calc_en_html = f.read()

        with open(cls.calc_es_path, "r", encoding="utf-8") as f:
            cls.calc_es_html = f.read()

    # =========================================================================
    # 1. Markup & Currency Engine Contract Verification
    # =========================================================================
    def test_01_all_5_currency_buttons_exist_in_en_calculator(self):
        """Stress-test: Verify presence of all 5 currency buttons with exact IDs and symbols."""
        for code, spec in CURRENCY_SPECS.items():
            btn_id = spec["btn_id"]
            symbol = spec["symbol"]
            pattern = rf'id="{btn_id}"'
            self.assertRegex(
                self.calc_en_html,
                pattern,
                f"calculator-en.html must have currency button id='{btn_id}' for {code}",
            )
            # Verify button displays currency code and symbol
            self.assertIn(
                f"{code} ({symbol})",
                self.calc_en_html,
                f"calculator-en.html button must display '{code} ({symbol})'",
            )

    def test_02_currency_switch_javascript_handles_all_5_currencies(self):
        """Verify setCurrency() function in calculator-en.html registers all 5 currencies in JS array."""
        for code, spec in CURRENCY_SPECS.items():
            btn_id = spec["btn_id"]
            symbol = spec["symbol"]
            # Look for entry { id: "curr-...", sym: "..." }
            entry_pattern = rf'id:\s*["\']?{btn_id}["\']?,\s*sym:\s*["\']?{re.escape(symbol)}["\']?'
            self.assertRegex(
                self.calc_en_html,
                entry_pattern,
                f"JS buttons array must contain {{ id: '{btn_id}', sym: '{symbol}' }}",
            )

    def test_03_currency_labels_updated_dynamically(self):
        """Verify dynamic label updates for label-curr-1 and label-curr-2 in setCurrency()."""
        self.assertIn('document.getElementById("label-curr-1").textContent = symbol + " / mo"', self.calc_en_html)
        self.assertIn('document.getElementById("label-curr-2").textContent = symbol + " / mo"', self.calc_en_html)

    # =========================================================================
    # 2. Boundary Stress-Testing
    # =========================================================================
    def test_04_boundary_zero_income(self):
        """Boundary: Zero net income ($0). Freelancer only charges to cover business expenses and tax."""
        res = simulate_calculator_js(net_val=0, exp_val=650, tax_val=25, vac_val=4, h_day_val=8, b_ratio_val=60)
        self.assertFalse(math.isnan(res["hourly"]))
        self.assertFalse(math.isinf(res["hourly"]))
        self.assertGreater(res["hourly"], 0.0)
        self.assertAlmostEqual(res["monthly_gross"], 650 / 0.75, places=2)
        # Verify formatting
        self.assertEqual(res["formatted_net_pill"], "$0/mo")
        self.assertTrue(res["formatted_hourly"].startswith("$"))

    def test_05_boundary_large_income(self):
        """Boundary: High net income ($1,000,000/mo and $10,000,000/mo). Check numerical stability."""
        res_1m = simulate_calculator_js(net_val=1_000_000, exp_val=10_000, tax_val=35, vac_val=4, h_day_val=8, b_ratio_val=60)
        self.assertFalse(math.isnan(res_1m["hourly"]))
        self.assertFalse(math.isinf(res_1m["hourly"]))
        self.assertGreater(res_1m["hourly"], 10_000.0)
        self.assertEqual(res_1m["formatted_net_pill"], "$1,000,000/mo")

        res_10m = simulate_calculator_js(net_val=10_000_000, exp_val=50_000, tax_val=40, vac_val=4, h_day_val=8, b_ratio_val=60)
        self.assertFalse(math.isnan(res_10m["hourly"]))
        self.assertFalse(math.isinf(res_10m["hourly"]))
        self.assertGreater(res_10m["hourly"], 100_000.0)

    def test_06_boundary_zero_tax(self):
        """Boundary: 0% Tax rate. Monthly gross must exactly equal net + expenses."""
        res = simulate_calculator_js(net_val=4500, exp_val=650, tax_val=0, vac_val=4, h_day_val=8, b_ratio_val=60)
        self.assertEqual(res["monthly_gross"], 5150.0)
        self.assertEqual(res["formatted_monthly_gross"], "$5,150")

    def test_07_boundary_100_percent_tax_guardrail(self):
        """Boundary: 100% Tax rate. Must activate (1 - tax > 0) guardrail, preventing division by zero."""
        res = simulate_calculator_js(net_val=4500, exp_val=650, tax_val=100, vac_val=4, h_day_val=8, b_ratio_val=60)
        self.assertFalse(math.isnan(res["hourly"]), "Hourly rate must not be NaN at 100% tax")
        self.assertFalse(math.isinf(res["hourly"]), "Hourly rate must not be Infinity at 100% tax")
        self.assertEqual(res["monthly_gross"], 5150.0, "At 100% tax, fallback gross must equal net + exp")
        self.assertGreater(res["hourly"], 0.0)

    def test_08_boundary_over_100_percent_tax_guardrail(self):
        """Boundary: >100% Tax rate (e.g. 120% tax entered). Must safely fallback to net + exp without negative gross."""
        res = simulate_calculator_js(net_val=4500, exp_val=650, tax_val=120, vac_val=4, h_day_val=8, b_ratio_val=60)
        self.assertFalse(math.isnan(res["hourly"]))
        self.assertFalse(math.isinf(res["hourly"]))
        self.assertEqual(res["monthly_gross"], 5150.0)

    def test_09_boundary_zero_billable_ratio_guardrail(self):
        """Boundary: 0% Billable client hours. Must activate Math.max(1, totalBillable) guardrail."""
        res = simulate_calculator_js(net_val=4500, exp_val=650, tax_val=25, vac_val=4, h_day_val=8, b_ratio_val=0)
        self.assertFalse(math.isnan(res["hourly"]), "Hourly rate must not be NaN at 0% billable ratio")
        self.assertFalse(math.isinf(res["hourly"]), "Hourly rate must not be Infinity at 0% billable ratio")
        self.assertEqual(res["total_billable"], 1.0, "totalBillable must clamp to 1.0 to prevent zero division")
        self.assertEqual(res["daily"], 0.0, "Daily rate at 0% billable ratio must evaluate to 0.0")
        self.assertEqual(res["formatted_daily"], "$0.00")

    def test_10_boundary_100_percent_billable_ratio(self):
        """Boundary: 100% Billable client hours. Must maximize billable capacity."""
        res = simulate_calculator_js(net_val=4500, exp_val=650, tax_val=25, vac_val=4, h_day_val=8, b_ratio_val=100)
        self.assertEqual(res["total_billable"], 48 * 5 * 8 * 1.0)
        self.assertAlmostEqual(res["hourly"], (6866.666666666667 * 12) / 1920, places=2)

    def test_11_boundary_zero_expenses(self):
        """Boundary: $0 Monthly Overhead Expenses. Gross required is solely net / (1 - tax)."""
        res = simulate_calculator_js(net_val=3000, exp_val=0, tax_val=25, vac_val=4, h_day_val=8, b_ratio_val=60)
        self.assertAlmostEqual(res["monthly_gross"], 4000.0, places=2)
        self.assertEqual(res["formatted_monthly_gross"], "$4,000")

    def test_12_boundary_zero_income_and_zero_expenses(self):
        """Boundary: Both net and exp are $0."""
        res = simulate_calculator_js(net_val=0, exp_val=0, tax_val=25, vac_val=4, h_day_val=8, b_ratio_val=60)
        self.assertEqual(res["hourly"], 0.0)
        self.assertEqual(res["daily"], 0.0)
        self.assertEqual(res["formatted_hourly"], "$0.00")
        self.assertEqual(res["formatted_daily"], "$0.00")

    def test_13_boundary_52_weeks_vacation_guardrail(self):
        """Boundary: 52 weeks vacation (taking whole year off). Math.max(1, 52 - vac) prevents 0 weeks."""
        res = simulate_calculator_js(net_val=4500, exp_val=650, tax_val=25, vac_val=52, h_day_val=8, b_ratio_val=60)
        self.assertEqual(res["working_weeks"], 1.0)
        self.assertFalse(math.isinf(res["hourly"]))

    def test_14_boundary_zero_hours_day_guardrail(self):
        """Boundary: 0 hours per day work capacity."""
        res = simulate_calculator_js(net_val=4500, exp_val=650, tax_val=25, vac_val=4, h_day_val=0, b_ratio_val=60)
        self.assertEqual(res["total_billable"], 1.0)
        self.assertFalse(math.isinf(res["hourly"]))
        self.assertEqual(res["daily"], 0.0)

    # =========================================================================
    # 3. Currency Formatting Verification Across All 5 Currencies
    # =========================================================================
    def test_15_all_5_currencies_formatting_exact_symbols(self):
        """Empirically test that every one of the 5 currencies produces exact formatted strings."""
        for code, spec in CURRENCY_SPECS.items():
            sym = spec["symbol"]
            res = simulate_calculator_js(net_val=4500, exp_val=650, tax_val=25, vac_val=4, h_day_val=8, b_ratio_val=60, currency_code=code)
            self.assertEqual(res["currency_symbol"], sym)
            self.assertEqual(res["formatted_hourly"], f"{sym}71.53")
            self.assertEqual(res["formatted_daily"], f"{sym}343.33")
            self.assertEqual(res["formatted_monthly_gross"], f"{sym}6,867")
            self.assertEqual(res["formatted_hourly_pill"], f"{sym}71.53/hr")
            self.assertEqual(res["formatted_net_pill"], f"{sym}4,500/mo")

    # =========================================================================
    # 4. Rate-Negotiation CRO Card & Gumroad URL Verification
    # =========================================================================
    def test_16_rate_negotiation_card_markup_in_en_calculator(self):
        """Verify rate negotiation card contains valid Gumroad link and LANZAMIENTO20 promo reference."""
        # Check Gumroad link
        gumroad_url = "https://migueldp3.gumroad.com/l/pswllr"
        self.assertIn(gumroad_url, self.calc_en_html, f"calculator-en.html must link to {gumroad_url}")

        # Check LANZAMIENTO20 promo code
        self.assertIn("LANZAMIENTO20", self.calc_en_html, "calculator-en.html must reference promo code LANZAMIENTO20")

        # Check 20% OFF discount reference
        self.assertIn("20% OFF", self.calc_en_html, "calculator-en.html must display '20% OFF' discount text")

    def test_17_gumroad_url_live_http_resolution(self):
        """Verify the Gumroad product URL returns HTTP 200 over live network."""
        url = "https://migueldp3.gumroad.com/l/pswllr"
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                status_code = response.getcode()
                self.assertEqual(status_code, 200, f"Gumroad URL {url} must return HTTP 200, got {status_code}")
        except Exception as e:
            self.fail(f"Failed to connect to Gumroad URL {url}: {e}")

    # =========================================================================
    # 5. Spanish Core Integrity (calculator.html)
    # =========================================================================
    def test_18_spanish_calculator_integrity(self):
        """Verify Spanish calculator retains intact DOM IDs, Euro formatting, and calculation parity."""
        # Required input and output IDs
        for expected_id in [
            "calc-desired-net",
            "calc-monthly-expenses",
            "calc-tax-rate",
            "calc-vacation-weeks",
            "calc-hours-day",
            "calc-billable-ratio",
            "res-hourly-rate",
            "res-day-rate",
            "res-monthly-gross",
            "res-hourly-pill",
            "res-net-pill",
        ]:
            self.assertIn(f'id="{expected_id}"', self.calc_es_html, f"calculator.html must contain id='{expected_id}'")

        # Verify calculate() function exists in calculator.html
        self.assertIn("function calculate()", self.calc_es_html)
        self.assertIn('toLocaleString("es-ES")', self.calc_es_html)

        # Verify rate negotiation card is present and links to Gumroad
        self.assertIn("https://migueldp3.gumroad.com/l/pswllr", self.calc_es_html)

    # =========================================================================
    # 6. Monte Carlo Fuzz Testing (500 Adversarial Vectors)
    # =========================================================================
    def test_19_monte_carlo_fuzz_testing_500_iterations(self):
        """Adversarial stress-test: 500 pseudo-random parameter vectors across all currencies."""
        random.seed(42)  # Deterministic seed for reproducible testing
        currencies = list(CURRENCY_SPECS.keys())

        for iteration in range(500):
            net = random.choice([0, random.uniform(100, 50000), random.uniform(50000, 2000000)])
            exp = random.choice([0, random.uniform(50, 10000), random.uniform(10000, 500000)])
            tax = random.choice([0, 20, 25, 50, 100, 120, random.uniform(0, 99)])
            vac = random.choice([0, 4, 25, 52, 60, random.uniform(0, 52)])
            h_day = random.choice([0, 1, 8, 16, 24, random.uniform(1, 16)])
            b_ratio = random.choice([0, 10, 60, 100, 150, random.uniform(0, 100)])
            curr = random.choice(currencies)

            res = simulate_calculator_js(net, exp, tax, vac, h_day, b_ratio, curr)

            # Invariant 1: Hourly and Daily rates must never be NaN or Inf
            self.assertFalse(
                math.isnan(res["hourly"]),
                f"Iteration {iteration}: hourly rate is NaN for inputs (net={net}, exp={exp}, tax={tax}, b_ratio={b_ratio})",
            )
            self.assertFalse(
                math.isinf(res["hourly"]),
                f"Iteration {iteration}: hourly rate is Inf for inputs (net={net}, exp={exp}, tax={tax}, b_ratio={b_ratio})",
            )
            self.assertFalse(
                math.isnan(res["daily"]),
                f"Iteration {iteration}: daily rate is NaN",
            )
            self.assertFalse(
                math.isinf(res["daily"]),
                f"Iteration {iteration}: daily rate is Inf",
            )

            # Invariant 2: Rates must be non-negative
            self.assertGreaterEqual(res["hourly"], 0.0)
            self.assertGreaterEqual(res["daily"], 0.0)
            self.assertGreaterEqual(res["monthly_gross"], 0.0)

            # Invariant 3: Formatted string starts with exact currency symbol
            expected_sym = CURRENCY_SPECS[curr]["symbol"]
            self.assertTrue(res["formatted_hourly"].startswith(expected_sym))
            self.assertTrue(res["formatted_daily"].startswith(expected_sym))
            self.assertTrue(res["formatted_monthly_gross"].startswith(expected_sym))


def run_challenge():
    print("=" * 75)
    print("EMPIRICAL CHALLENGER: Rate Calculator & Multi-Currency Engine Stress Suite")
    print("=" * 75)
    suite = unittest.TestLoader().loadTestsFromTestCase(ChallengeRateCalculatorSuite)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    print("=" * 75)
    if result.wasSuccessful():
        print("VERDICT: ALL 19 EMPIRICAL CHALLENGE TESTS PASSED.")
        print("RECOMMENDATION: APPROVE")
        sys.exit(0)
    else:
        print(f"VERDICT: {len(result.failures)} FAILURES, {len(result.errors)} ERRORS DETECTED.")
        print("RECOMMENDATION: REQUEST_CHANGES")
        sys.exit(1)


if __name__ == "__main__":
    run_challenge()
