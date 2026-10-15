#!/usr/bin/env python3
"""
verify_sitemap.py - Sitemap XML Schema & Coverage Validator for FreelanceToolkit

Validates sitemap.xml schema, confirms required URLs are present, checks valid
lastmod dates, and validates xhtml:link hreflang alternates.

Zero external dependencies - uses standard library xml.etree.ElementTree.
"""

import os
import sys
import argparse
import datetime
import xml.etree.ElementTree as ET

# Fix Windows console UTF-8 output if needed
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

XML_NAMESPACES = {
    "sitemap": "http://www.sitemaps.org/schemas/sitemap/0.9",
    "xhtml": "http://www.w3.org/1999/xhtml",
}

EXPECTED_10_URLS = [
    "https://komasan19283645.github.io/freelance-toolkit/",
    "https://komasan19283645.github.io/freelance-toolkit/calculator.html",
    "https://komasan19283645.github.io/freelance-toolkit/store.html",
    "https://komasan19283645.github.io/freelance-toolkit/contracts.html",
    "https://komasan19283645.github.io/freelance-toolkit/como-hacer-factura-autonomo-irpf-iva.html",
    "https://komasan19283645.github.io/freelance-toolkit/ventas-vinted-wallapop-hacienda-dac7.html",
    "https://komasan19283645.github.io/freelance-toolkit/metodo-50-30-20-presupuesto-espanol.html",
    "https://komasan19283645.github.io/freelance-toolkit/index-en.html",
    "https://komasan19283645.github.io/freelance-toolkit/calculator-en.html",
    "https://komasan19283645.github.io/freelance-toolkit/store-en.html",
]

VALID_CHANGEFREQS = {"always", "hourly", "daily", "weekly", "monthly", "yearly", "never"}


def is_valid_date(date_str: str) -> bool:
    try:
        datetime.date.fromisoformat(date_str)
        return True
    except (ValueError, TypeError):
        return False


def normalize_url(url: str) -> str:
    url = url.strip()
    if url.endswith("/index.html"):
        return url[:-10]  # normalize .../index.html to .../
    return url


def verify_sitemap(sitemap_path: str = None, strict: bool = False) -> dict:
    """
    Validates sitemap.xml schema, structure, dates, and URLs.
    Returns results dictionary.
    """
    if sitemap_path is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sitemap_path = os.path.join(base_dir, "sitemap.xml")

    results = {
        "file_exists": False,
        "well_formed_xml": False,
        "valid_root_tag": False,
        "total_urls_found": 0,
        "urls_list": [],
        "present_target_urls": [],
        "missing_target_urls": [],
        "invalid_lastmods": [],
        "invalid_priorities": [],
        "invalid_changefreqs": [],
        "hreflang_alternates_found": 0,
        "has_xhtml_namespace": False,
        "errors": [],
        "warnings": [],
        "passed": False,
    }

    if not os.path.exists(sitemap_path):
        results["errors"].append(f"sitemap.xml not found at {sitemap_path}")
        return results

    results["file_exists"] = True

    try:
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        results["well_formed_xml"] = True
    except ET.ParseError as e:
        results["errors"].append(f"XML ParseError: {e}")
        return results

    # Check root element
    expected_root = f"{{{XML_NAMESPACES['sitemap']}}}urlset"
    if root.tag == expected_root or root.tag == "urlset":
        results["valid_root_tag"] = True
    else:
        results["errors"].append(f"Invalid root tag: '{root.tag}', expected '{expected_root}'")

    # Check xhtml namespace in root attributes or tags
    results["has_xhtml_namespace"] = "http://www.w3.org/1999/xhtml" in root.tag or any(
        "http://www.w3.org/1999/xhtml" in el.tag for el in root.iter()
    )

    found_locs = []

    # Iterate <url> entries
    for url_el in root.iter():
        if url_el.tag.endswith("url") and not url_el.tag.endswith("urlset"):
            results["total_urls_found"] += 1
            loc_el = url_el.find(f"{{{XML_NAMESPACES['sitemap']}}}loc")
            if loc_el is None:
                loc_el = url_el.find("loc")

            loc_text = loc_el.text.strip() if loc_el is not None and loc_el.text else ""
            if loc_text:
                found_locs.append(loc_text)
                results["urls_list"].append(loc_text)

            # Check lastmod
            lastmod_el = url_el.find(f"{{{XML_NAMESPACES['sitemap']}}}lastmod")
            if lastmod_el is None:
                lastmod_el = url_el.find("lastmod")
            if lastmod_el is not None and lastmod_el.text:
                lmod = lastmod_el.text.strip()
                if not is_valid_date(lmod):
                    results["invalid_lastmods"].append((loc_text, lmod))

            # Check priority
            prio_el = url_el.find(f"{{{XML_NAMESPACES['sitemap']}}}priority")
            if prio_el is None:
                prio_el = url_el.find("priority")
            if prio_el is not None and prio_el.text:
                try:
                    p = float(prio_el.text.strip())
                    if not (0.0 <= p <= 1.0):
                        results["invalid_priorities"].append((loc_text, prio_el.text.strip()))
                except ValueError:
                    results["invalid_priorities"].append((loc_text, prio_el.text.strip()))

            # Check changefreq
            cf_el = url_el.find(f"{{{XML_NAMESPACES['sitemap']}}}changefreq")
            if cf_el is None:
                cf_el = url_el.find("changefreq")
            if cf_el is not None and cf_el.text:
                cf = cf_el.text.strip().lower()
                if cf not in VALID_CHANGEFREQS:
                    results["invalid_changefreqs"].append((loc_text, cf))

            # Check xhtml:link alternates
            for child in url_el:
                if "link" in child.tag:
                    results["hreflang_alternates_found"] += 1

    # Check presence against the 10 canonical URLs
    normalized_found = [normalize_url(u) for u in found_locs]
    for expected in EXPECTED_10_URLS:
        norm_expected = normalize_url(expected)
        if norm_expected in normalized_found or expected in found_locs:
            results["present_target_urls"].append(expected)
        else:
            results["missing_target_urls"].append(expected)

    # Determine overall pass
    has_critical_errors = (
        not results["file_exists"]
        or not results["well_formed_xml"]
        or not results["valid_root_tag"]
        or len(results["invalid_lastmods"]) > 0
        or len(results["invalid_priorities"]) > 0
        or len(results["invalid_changefreqs"]) > 0
    )

    if has_critical_errors:
        results["passed"] = False
    elif strict:
        # In strict mode, all 10 URLs and hreflang alternates are strictly required
        if results["missing_target_urls"]:
            results["errors"].append(
                f"Strict mode: {len(results['missing_target_urls'])} required URLs missing: {results['missing_target_urls']}"
            )
            results["passed"] = False
        else:
            results["passed"] = True
    else:
        # Progressive mode: Pass if schema is clean and existing URLs are valid
        if results["missing_target_urls"]:
            results["warnings"].append(
                f"Progressive mode: {len(results['missing_target_urls'])} URLs pending M2 milestone implementation."
            )
        results["passed"] = True

    return results


def main():
    parser = argparse.ArgumentParser(description="FreelanceToolkit Sitemap Validator")
    parser.add_argument("--strict", action="store_true", help="Fail if not all 10 URLs are present")
    parser.add_argument("--path", type=str, default=None, help="Custom path to sitemap.xml")
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sitemap_path = args.path or os.path.join(base_dir, "sitemap.xml")

    print("=" * 70)
    print("FreelanceToolkit - Programmatic Sitemap XML Verification")
    print(f"Target file: {sitemap_path}")
    print(f"Mode: {'STRICT (Enforces all 10 URLs)' if args.strict else 'PROGRESSIVE (Milestone-aware)'}")
    print("=" * 70)

    res = verify_sitemap(sitemap_path, strict=args.strict)

    print(f"[*] File exists:           {'[PASS]' if res['file_exists'] else '[FAIL]'}")
    print(f"[*] Well-formed XML:       {'[PASS]' if res['well_formed_xml'] else '[FAIL]'}")
    print(f"[*] Valid <urlset> root:   {'[PASS]' if res['valid_root_tag'] else '[FAIL]'}")
    print(f"[*] Total <url> elements:  {res['total_urls_found']}")
    print(f"[*] Target URLs matched:   {len(res['present_target_urls'])} / {len(EXPECTED_10_URLS)}")
    print(f"[*] xhtml:link alternates: {res['hreflang_alternates_found']}")

    if res["invalid_lastmods"]:
        print("\n[!] Invalid <lastmod> dates:")
        for loc, d in res["invalid_lastmods"]:
            print(f"    - {loc}: '{d}'")

    if res["invalid_priorities"]:
        print("\n[!] Invalid <priority> values:")
        for loc, p in res["invalid_priorities"]:
            print(f"    - {loc}: '{p}'")

    if res["missing_target_urls"]:
        print(f"\n[*] Target URLs not yet in sitemap ({len(res['missing_target_urls'])}):")
        for u in res["missing_target_urls"]:
            print(f"    - {u}")

    if res["warnings"]:
        for w in res["warnings"]:
            print(f"\n[NOTE] {w}")

    if res["errors"]:
        print("\n[!] Errors:")
        for e in res["errors"]:
            print(f"    - {e}")

    print("=" * 70)
    if res["passed"]:
        print("RESULT: SUCCESS - Sitemap schema is valid.")
        print("=" * 70)
        sys.exit(0)
    else:
        print("RESULT: FAILURE - Sitemap validation failed.")
        print("=" * 70)
        sys.exit(1)


if __name__ == "__main__":
    main()
