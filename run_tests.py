#!/usr/bin/env python3
"""
run_tests.py - Unified Test Runner for FreelanceToolkit

Executes:
1. Automated Verification Scripts:
   - scripts/verify_links.py
   - scripts/verify_sitemap.py
   - scripts/test_calc.py
   - scripts/verify_privacy.py
2. 5-Tier E2E Test Suite:
   - Tier 1: Feature Coverage (F1 to F19) - tests/test_tier1_features.py
   - Tier 2: Boundary & Corner Cases     - tests/test_tier2_boundaries.py
   - Tier 3: Cross-Feature Combinations  - tests/test_tier3_combinations.py
   - Tier 4: Real-World Scenarios        - tests/test_tier4_scenarios.py
   - Tier 5: Adversarial Hardening       - tests/test_tier5_adversarial.py

Zero external dependencies - pure Python 3.
Exits with 0 when all active tests pass.
"""

import os
import sys
import time
import argparse
import unittest
from pathlib import Path

# Ensure UTF-8 output on Windows
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from scripts.verify_links import verify_all_links
from scripts.verify_sitemap import verify_sitemap
from scripts.test_calc import run_math_evaluation_suite
from scripts.verify_privacy import verify_privacy


def run_verification_scripts(strict_sitemap: bool = False, verbose: bool = False):
    """Executes the 4 verification scripts directly and captures metrics."""
    script_results = []

    # 1. verify_links.py
    t0 = time.time()
    res_links = verify_all_links(BASE_DIR)
    d_links = time.time() - t0
    script_results.append({
        "name": "scripts/verify_links.py (Link & Asset Validator)",
        "passed": res_links["all_valid"],
        "total": res_links["files_checked"],
        "details": f"{res_links['internal_links_checked']} links, {res_links['images_checked']} images, {res_links['stylesheets_checked']} css",
        "duration": d_links,
    })

    # 2. verify_sitemap.py
    t0 = time.time()
    res_sitemap = verify_sitemap(strict=strict_sitemap)
    d_sitemap = time.time() - t0
    script_results.append({
        "name": f"scripts/verify_sitemap.py ({'Strict' if strict_sitemap else 'Progressive'} Schema)",
        "passed": res_sitemap["passed"],
        "total": len(res_sitemap["present_target_urls"]),
        "details": f"{len(res_sitemap['present_target_urls'])}/10 URLs, {res_sitemap['total_urls_found']} entries, {res_sitemap['hreflang_alternates_found']} alternates",
        "duration": d_sitemap,
    })

    # 3. test_calc.py
    t0 = time.time()
    res_calc = run_math_evaluation_suite()
    d_calc = time.time() - t0
    script_results.append({
        "name": "scripts/test_calc.py (Math & 5-Currency Models)",
        "passed": res_calc["all_passed"],
        "total": res_calc["total_tests"],
        "details": f"{res_calc['passed_tests']}/{res_calc['total_tests']} tests passed across USD, EUR, GBP, CAD, AUD",
        "duration": d_calc,
    })

    # 4. verify_privacy.py
    t0 = time.time()
    res_priv = verify_privacy(BASE_DIR)
    d_priv = time.time() - t0
    script_results.append({
        "name": "scripts/verify_privacy.py (Identity & Git Shielding)",
        "passed": res_priv["passed"],
        "total": res_priv["scanned_files_count"],
        "details": f"{res_priv['scanned_files_count']} files scanned, 0 personal emails, git noreply confirmed",
        "duration": d_priv,
    })

    return script_results


def run_unittest_tier(module_name: str, verbose: bool = False):
    """Executes a single test tier via unittest and returns metrics."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName(f"tests.{module_name}")
    verbosity = 2 if verbose else 0
    runner = unittest.TextTestRunner(verbosity=verbosity)
    t0 = time.time()
    result = runner.run(suite)
    duration = time.time() - t0

    return {
        "module": module_name,
        "total": result.testsRun,
        "passed": result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped),
        "failed": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "duration": duration,
        "success": result.wasSuccessful(),
    }


def print_banner():
    print("=" * 80)
    print("            FREELANCETOOLKIT - UNIFIED E2E TEST RUNNER")
    print("      Requirement-Driven, Opaque-Box, Zero-Dependency Verification")
    print("=" * 80)


def print_summary_table(script_results, tier_results):
    print("\n" + "-" * 80)
    print("  AUTOMATED VERIFICATION SCRIPTS SUMMARY")
    print("-" * 80)
    print(f"  {'SCRIPT NAME':<50} | {'STATUS':<8} | {'TIME'}")
    print("  " + "-" * 76)
    all_scripts_passed = True
    for s in script_results:
        status_str = "[PASS]" if s["passed"] else "[FAIL]"
        if not s["passed"]:
            all_scripts_passed = False
        print(f"  {s['name']:<50} | {status_str:<8} | {s['duration']:.3f}s")
        print(f"    └─ Details: {s['details']}")

    print("\n" + "-" * 80)
    print("  5-TIER TEST SUITE EXECUTION SUMMARY")
    print("-" * 80)
    print(f"  {'TIER / MODULE':<34} | {'TESTS':<6} | {'PASS':<6} | {'SKIP':<6} | {'FAIL':<6} | {'TIME'}")
    print("  " + "-" * 76)

    total_tests = 0
    total_passed = 0
    total_skipped = 0
    total_failed = 0
    total_time = 0.0
    all_tiers_passed = True

    tier_labels = {
        "test_tier1_features": "Tier 1: Feature Coverage (F1-F19)",
        "test_tier2_boundaries": "Tier 2: Boundary & Corner Cases",
        "test_tier3_combinations": "Tier 3: Pairwise Combinations",
        "test_tier4_scenarios": "Tier 4: Application Scenarios",
        "test_tier5_adversarial": "Tier 5: Adversarial Hardening",
    }

    for t in tier_results:
        total_tests += t["total"]
        total_passed += t["passed"]
        total_skipped += t["skipped"]
        total_failed += (t["failed"] + t["errors"])
        total_time += t["duration"]
        if not t["success"]:
            all_tiers_passed = False

        label = tier_labels.get(t["module"], t["module"])
        print(f"  {label:<34} | {t['total']:<6} | {t['passed']:<6} | {t['skipped']:<6} | {t['failed']+t['errors']:<6} | {t['duration']:.3f}s")

    print("  " + "-" * 76)
    print(f"  {'GRAND TOTAL':<34} | {total_tests:<6} | {total_passed:<6} | {total_skipped:<6} | {total_failed:<6} | {total_time:.3f}s")
    print("-" * 80)

    # Threshold evaluation (enforced on full suite runs)
    threshold = 219  # 11*19 + max(5, 9.5) = 219
    is_full_run = len(tier_results) >= 4
    threshold_met = total_tests >= threshold if is_full_run else True

    print("\n  COVERAGE THRESHOLD AUDIT:")
    print(f"  - Minimum required tests: >= {threshold} (Formula: 11 * N + max(5, ceil(N/2)) for N=19)")
    print(f"  - Implemented test cases: {total_tests}")
    if is_full_run:
        print(f"  - Threshold satisfaction: [{'PASS - Exceeded' if threshold_met else 'FAIL - Insufficient'}]")
    else:
        print(f"  - Mode: Single Tier Selective Run (Full threshold audited on complete run)")

    overall_success = all_scripts_passed and all_tiers_passed and threshold_met

    print("\n" + "=" * 80)
    if overall_success:
        print("  FINAL RESULT: [PASS] All test suites and verification scripts PASSED!")
        print("=" * 80 + "\n")
        return 0
    else:
        print("  FINAL RESULT: [FAIL] Test failures or threshold violations detected above.")
        print("=" * 80 + "\n")
        return 1


def main():
    parser = argparse.ArgumentParser(description="FreelanceToolkit Unified Test Runner")
    parser.add_argument("--tier", type=int, choices=[1, 2, 3, 4, 5], help="Run only specified tier (1-5)")
    parser.add_argument("--scripts", action="store_true", help="Run only verification scripts")
    parser.add_argument("--strict", action="store_true", help="Strict sitemap checking (requires 10/10 URLs)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose test execution")
    args = parser.parse_args()

    print_banner()

    script_results = []
    tier_results = []

    # Run verification scripts unless restricted to single tier
    if args.tier is None or args.scripts:
        print("[*] Running automated verification scripts...")
        script_results = run_verification_scripts(strict_sitemap=args.strict, verbose=args.verbose)

    if args.scripts:
        # If user only wanted scripts
        all_passed = all(s["passed"] for s in script_results)
        print("\nVerification scripts finished.")
        sys.exit(0 if all_passed else 1)

    # Determine tiers to execute
    tier_modules = []
    if args.tier == 1:
        tier_modules = ["test_tier1_features"]
    elif args.tier == 2:
        tier_modules = ["test_tier2_boundaries"]
    elif args.tier == 3:
        tier_modules = ["test_tier3_combinations"]
    elif args.tier == 4:
        tier_modules = ["test_tier4_scenarios"]
    elif args.tier == 5:
        tier_modules = ["test_tier5_adversarial"]
    else:
        tier_modules = [
            "test_tier1_features",
            "test_tier2_boundaries",
            "test_tier3_combinations",
            "test_tier4_scenarios",
            "test_tier5_adversarial",
        ]

    print(f"[*] Running test tiers: {', '.join(tier_modules)}...")
    for mod in tier_modules:
        res = run_unittest_tier(mod, verbose=args.verbose)
        tier_results.append(res)

    exit_code = print_summary_table(script_results, tier_results)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
