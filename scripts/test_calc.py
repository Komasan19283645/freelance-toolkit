#!/usr/bin/env python3
"""
test_calc.py - Programmatic Rate Calculator Math & Multi-Currency Evaluator

Evaluates the mathematical models, formulas, and currency formatting of the
Freelance Rate Calculator across all 5 supported currencies:
USD ($), EUR (€), GBP (£), CAD (CA$), and AUD (A$).

Zero external dependencies - pure Python 3.
"""

import os
import re
import sys
import math
from typing import Dict, Any

# Fix Windows console UTF-8 output if needed
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

CURRENCY_SYMBOLS = {
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "CAD": "CA$",
    "AUD": "A$",
}


def calculate_rate(
    net_monthly: float,
    expenses_monthly: float,
    tax_rate_percent: float,
    vacation_weeks: float,
    hours_per_day: float,
    billable_ratio_percent: float,
    currency_code: str = "USD",
) -> Dict[str, Any]:
    """
    Authoritative mathematical implementation of the Freelance Rate Calculator.
    Matches formula in calculator.html and calculator-en.html.
    """
    net = float(net_monthly) if net_monthly is not None else 0.0
    exp = float(expenses_monthly) if expenses_monthly is not None else 0.0
    tax = (float(tax_rate_percent) if tax_rate_percent is not None else 0.0) / 100.0
    vac = float(vacation_weeks) if vacation_weeks is not None else 0.0
    h_day = float(hours_per_day) if hours_per_day is not None else 0.0
    b_ratio = (float(billable_ratio_percent) if billable_ratio_percent is not None else 0.0) / 100.0

    # 1. Monthly Gross required to hit target net after expenses and tax
    if 1.0 - tax > 0:
        monthly_gross = (net + exp) / (1.0 - tax)
    else:
        monthly_gross = net + exp

    annual_gross = monthly_gross * 12.0

    # 2. Total annual billable hours
    working_weeks = max(1.0, 52.0 - vac)
    total_billable_hours = max(1.0, working_weeks * 5.0 * h_day * b_ratio)

    # 3. Minimum recommended rates
    hourly_rate = annual_gross / total_billable_hours
    daily_rate = hourly_rate * (h_day * b_ratio)

    sym = CURRENCY_SYMBOLS.get(currency_code.upper(), "$")

    return {
        "currency_code": currency_code.upper(),
        "currency_symbol": sym,
        "monthly_net": net,
        "monthly_expenses": exp,
        "monthly_gross": monthly_gross,
        "annual_gross": annual_gross,
        "working_weeks": working_weeks,
        "total_billable_hours": total_billable_hours,
        "hourly_rate": hourly_rate,
        "daily_rate": daily_rate,
        # Formatted UI strings
        "formatted_hourly": f"{sym}{hourly_rate:.2f}",
        "formatted_daily": f"{sym}{daily_rate:.2f}",
        "formatted_monthly_gross": f"{sym}{round(monthly_gross):,}",
    }


def run_math_evaluation_suite() -> Dict[str, Any]:
    """Runs the comprehensive rate calculator test suite."""
    tests = []

    def test(name: str, passed: bool, details: str = ""):
        tests.append({"name": name, "passed": passed, "details": details})

    # Test 1: English UI Defaults ($71.53/hr, $343.33/day, $6,867/mo)
    r1 = calculate_rate(4500, 650, 25, 4, 8, 60, "USD")
    test(
        "English Defaults (USD): Exact match with UI hardcoded values",
        abs(r1["hourly_rate"] - 71.5277) < 0.01
        and abs(r1["daily_rate"] - 343.333) < 0.01
        and round(r1["monthly_gross"]) == 6867
        and r1["formatted_hourly"] == "$71.53"
        and r1["formatted_daily"] == "$343.33"
        and r1["formatted_monthly_gross"] == "$6,867",
        f"Hourly={r1['formatted_hourly']}, Daily={r1['formatted_daily']}, Gross={r1['formatted_monthly_gross']}",
    )

    # Test 2: Spanish UI Inputs (Net 2200, Exp 550, Tax 20%, Vac 4, Hours 8, Ratio 65%)
    r2 = calculate_rate(2200, 550, 20, 4, 8, 65, "EUR")
    test(
        "Spanish Inputs (EUR): Evaluates dynamically to €33.05/hr, €171.88/day, €3,438/mo",
        abs(r2["hourly_rate"] - 33.0528) < 0.01
        and abs(r2["daily_rate"] - 171.875) < 0.01
        and round(r2["monthly_gross"]) == 3438
        and r2["currency_symbol"] == "€",
        f"Hourly={r2['formatted_hourly']}, Daily={r2['formatted_daily']}, Gross={r2['formatted_monthly_gross']}",
    )

    # Tests 3-7: All 5 Currencies Symbol and Code Validation
    for code, sym in CURRENCY_SYMBOLS.items():
        res = calculate_rate(3000, 500, 20, 4, 8, 60, code)
        test(
            f"Currency {code}: Proper symbol prefix '{sym}'",
            res["currency_symbol"] == sym and res["formatted_hourly"].startswith(sym),
            f"Code={code}, Symbol={sym}, Formatted={res['formatted_hourly']}",
        )

    # Test 8: Zero Tax Boundary (tax=0)
    r_zt = calculate_rate(4000, 500, 0, 4, 8, 60, "USD")
    test(
        "Boundary: 0% Tax rate gives gross equal to net + expenses",
        r_zt["monthly_gross"] == 4500.0,
        f"Monthly gross={r_zt['monthly_gross']}, expected 4500.0",
    )

    # Test 9: Zero Expenses Boundary (exp=0)
    r_ze = calculate_rate(3000, 0, 25, 4, 8, 60, "USD")
    test(
        "Boundary: $0 Expenses gives gross equal to net / (1 - tax)",
        abs(r_ze["monthly_gross"] - 4000.0) < 0.001,
        f"Monthly gross={r_ze['monthly_gross']}, expected 4000.0",
    )

    # Test 10: High Tax Rate Boundary (60%)
    r_ht = calculate_rate(4000, 500, 60, 4, 8, 60, "USD")
    test(
        "Boundary: 60% Tax rate calculates cleanly without overflow",
        abs(r_ht["monthly_gross"] - 11250.0) < 0.01,
        f"Monthly gross={r_ht['monthly_gross']}, expected 11250.0",
    )

    # Test 11: Zero Vacation Weeks (52 working weeks)
    r_zv = calculate_rate(4500, 650, 25, 0, 8, 60, "USD")
    test(
        "Boundary: 0 Vacation weeks gives 52 working weeks",
        r_zv["working_weeks"] == 52.0 and r_zv["total_billable_hours"] == 52 * 5 * 8 * 0.60,
        f"Working weeks={r_zv['working_weeks']}, hours={r_zv['total_billable_hours']}",
    )

    # Test 12: High Vacation Weeks (26 weeks)
    r_hv = calculate_rate(4500, 650, 25, 26, 8, 60, "USD")
    test(
        "Boundary: 26 Vacation weeks gives 26 working weeks",
        r_hv["working_weeks"] == 26.0,
        f"Working weeks={r_hv['working_weeks']}",
    )

    # Test 13: 52 Weeks Vacation Edge Case (Clamped to 1 min to prevent zero division)
    r_ev = calculate_rate(4500, 650, 25, 52, 8, 60, "USD")
    test(
        "Boundary: 52 Vacation weeks clamped to >= 1 working week (no div-by-zero)",
        r_ev["working_weeks"] == 1.0 and not math.isnan(r_ev["hourly_rate"]) and not math.isinf(r_ev["hourly_rate"]),
        f"Working weeks={r_ev['working_weeks']}, hourly={r_ev['hourly_rate']:.2f}",
    )

    # Test 14: 100% Billable Ratio Boundary
    r_fb = calculate_rate(4500, 650, 25, 4, 8, 100, "USD")
    test(
        "Boundary: 100% Billable ratio uses full 8h daily capacity",
        r_fb["total_billable_hours"] == 48 * 5 * 8,
        f"Hours={r_fb['total_billable_hours']}, expected {48 * 5 * 8}",
    )

    # Test 15: Low Billable Ratio Boundary (10%)
    r_lb = calculate_rate(4500, 650, 25, 4, 8, 10, "USD")
    test(
        "Boundary: 10% Billable ratio dramatically increases required rate",
        r_lb["hourly_rate"] > r_fb["hourly_rate"] * 9.5,
        f"Hourly at 10%={r_lb['hourly_rate']:.2f} vs 100%={r_fb['hourly_rate']:.2f}",
    )

    # Test 16: Minimum Work Hours Boundary (1 hr/day)
    r_1h = calculate_rate(2000, 200, 20, 4, 1, 60, "USD")
    test(
        "Boundary: 1 hr/day work capacity calculates properly",
        r_1h["hourly_rate"] > 0 and not math.isinf(r_1h["hourly_rate"]),
        f"Hourly={r_1h['formatted_hourly']}",
    )

    # Test 17: Maximum Work Hours Boundary (16 hrs/day)
    r_16h = calculate_rate(5000, 1000, 25, 4, 16, 60, "USD")
    test(
        "Boundary: 16 hrs/day calculates properly",
        r_16h["hourly_rate"] > 0 and not math.isinf(r_16h["hourly_rate"]),
        f"Hourly={r_16h['formatted_hourly']}",
    )

    # Test 18: High Income Freelancer ($25,000/mo net)
    r_hi = calculate_rate(25000, 4000, 35, 6, 8, 65, "USD")
    test(
        "Scale: High income target ($25,000 net) scales accurately",
        r_hi["hourly_rate"] > 300,
        f"Hourly={r_hi['formatted_hourly']}, Gross={r_hi['formatted_monthly_gross']}",
    )

    # Test 19: Micro Income Starter ($500/mo net)
    r_mi = calculate_rate(500, 50, 15, 2, 4, 50, "USD")
    test(
        "Scale: Micro starter target ($500 net) calculates accurately",
        r_mi["hourly_rate"] > 5,
        f"Hourly={r_mi['formatted_hourly']}",
    )

    # Test 20: Mathematical Identity: Daily Rate == Hourly * (Hours * Billable Ratio)
    for test_case in [(4500, 650, 25, 4, 8, 60), (3000, 400, 20, 5, 7, 70), (6000, 1200, 30, 3, 9, 50)]:
        res = calculate_rate(*test_case, "USD")
        expected_daily = res["hourly_rate"] * (test_case[4] * (test_case[5] / 100.0))
        test(
            f"Mathematical Identity: Daily == Hourly * (Hours * Ratio) for inputs {test_case[:3]}",
            abs(res["daily_rate"] - expected_daily) < 1e-6,
            f"Daily={res['daily_rate']:.4f}, Expected={expected_daily:.4f}",
        )

    # Test 21: Monotonicity - Increasing Tax Strictly Increases Required Hourly Rate
    base = calculate_rate(4000, 500, 20, 4, 8, 60, "USD")
    higher_tax = calculate_rate(4000, 500, 30, 4, 8, 60, "USD")
    test(
        "Monotonicity: Higher tax strictly increases required rate",
        higher_tax["hourly_rate"] > base["hourly_rate"],
        f"Tax 20%: {base['formatted_hourly']} -> Tax 30%: {higher_tax['formatted_hourly']}",
    )

    # Test 22: Monotonicity - Increasing Expenses Strictly Increases Required Hourly Rate
    higher_exp = calculate_rate(4000, 1500, 20, 4, 8, 60, "USD")
    test(
        "Monotonicity: Higher expenses strictly increases required rate",
        higher_exp["hourly_rate"] > base["hourly_rate"],
        f"Exp $500: {base['formatted_hourly']} -> Exp $1500: {higher_exp['formatted_hourly']}",
    )

    # Test 23: Monotonicity - Increasing Vacation Strictly Increases Required Hourly Rate
    more_vac = calculate_rate(4000, 500, 20, 8, 8, 60, "USD")
    test(
        "Monotonicity: More vacation strictly increases required rate",
        more_vac["hourly_rate"] > base["hourly_rate"],
        f"Vac 4w: {base['formatted_hourly']} -> Vac 8w: {more_vac['formatted_hourly']}",
    )

    # Test 24: Monotonicity - Decreasing Billable Ratio Strictly Increases Required Hourly Rate
    lower_ratio = calculate_rate(4000, 500, 20, 4, 8, 40, "USD")
    test(
        "Monotonicity: Lower billable ratio strictly increases required rate",
        lower_ratio["hourly_rate"] > base["hourly_rate"],
        f"Ratio 60%: {base['formatted_hourly']} -> Ratio 40%: {lower_ratio['formatted_hourly']}",
    )

    # Test 25: Source Code Audit: Inspect Production JS in calculator-en.html
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    calc_en_path = os.path.join(base_dir, "calculator-en.html")
    has_formula = False
    if os.path.exists(calc_en_path):
        with open(calc_en_path, "r", encoding="utf-8") as f:
            code = f.read()
        has_formula = (
            "monthlyGross = (1 - tax > 0) ? (net + exp) / (1 - tax) : (net + exp)" in code
            and "totalBillable = Math.max(1, workingWeeks * 5 * hDay * bRatio)" in code
            and "hourly = (monthlyGross * 12) / totalBillable" in code
            and "daily = hourly * (hDay * bRatio)" in code
        )
    test(
        "Source Code Parity: calculator-en.html JS matches mathematical model",
        has_formula,
        "Production JavaScript code matches reference formulas verbatim",
    )

    all_passed = all(t["passed"] for t in tests)
    return {
        "total_tests": len(tests),
        "passed_tests": sum(1 for t in tests if t["passed"]),
        "failed_tests": sum(1 for t in tests if not t["passed"]),
        "tests": tests,
        "all_passed": all_passed,
    }


def main():
    print("=" * 70)
    print("FreelanceToolkit - Rate Calculator Math & Multi-Currency Suite")
    print("=" * 70)

    res = run_math_evaluation_suite()

    for idx, t in enumerate(res["tests"], start=1):
        status = "[PASS]" if t["passed"] else "[FAIL]"
        print(f"{status} #{idx:02d}: {t['name']}")
        if t["details"]:
            print(f"       Details: {t['details']}")

    print("=" * 70)
    print(f"Total Tests Evaluated: {res['total_tests']}")
    print(f"Passed:                {res['passed_tests']}")
    print(f"Failed:                {res['failed_tests']}")
    print("=" * 70)

    if res["all_passed"]:
        print("RESULT: SUCCESS - All rate calculator math tests PASSED.")
        print("=" * 70)
        sys.exit(0)
    else:
        print("RESULT: FAILURE - Mathematical discrepancies found.")
        print("=" * 70)
        sys.exit(1)


if __name__ == "__main__":
    main()
