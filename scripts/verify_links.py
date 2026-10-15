#!/usr/bin/env python3
"""
verify_links.py - Programmatic Link & Asset Validator for FreelanceToolkit

Validates all internal links, image paths, stylesheets, and bidirectional
language switchers across all 10 platform HTML files.

Zero external dependencies - uses standard library html.parser.
"""

import os
import sys
from html.parser import HTMLParser
from pathlib import Path

# Fix Windows console UTF-8 output if needed
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# The 10 canonical HTML platform files
TARGET_HTML_FILES = [
    "index.html",
    "calculator.html",
    "store.html",
    "contracts.html",
    "como-hacer-factura-autonomo-irpf-iva.html",
    "ventas-vinted-wallapop-hacienda-dac7.html",
    "metodo-50-30-20-presupuesto-espanol.html",
    "index-en.html",
    "calculator-en.html",
    "store-en.html",
]

# Language switch expectations
LANGUAGE_SWITCH_PAIRS = {
    "index.html": ["index-en.html"],
    "calculator.html": ["calculator-en.html"],
    "store.html": ["store-en.html"],
    "index-en.html": ["index.html"],
    "calculator-en.html": ["calculator.html"],
    "store-en.html": ["store.html"],
    "contracts.html": ["index-en.html", "store-en.html"],
}


class ResourceExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []          # <a href="...">
        self.stylesheets = []    # <link rel="stylesheet" href="...">
        self.images = []         # <img src="...">
        self.scripts = []        # <script src="...">
        self.favicons = []       # <link rel="icon" href="...">
        self.og_images = []      # <meta property="og:image" content="...">

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if tag == "a" and "href" in attr_dict:
            self.links.append(attr_dict["href"])
        elif tag == "link":
            rel = attr_dict.get("rel", "")
            href = attr_dict.get("href", "")
            if "stylesheet" in rel:
                self.stylesheets.append(href)
            elif "icon" in rel:
                self.favicons.append(href)
        elif tag == "img" and "src" in attr_dict:
            self.images.append(attr_dict["src"])
        elif tag == "script" and "src" in attr_dict:
            self.scripts.append(attr_dict["src"])
        elif tag == "meta":
            prop = attr_dict.get("property", "")
            content = attr_dict.get("content", "")
            if prop == "og:image" and content:
                self.og_images.append(content)


def clean_target_path(url: str) -> str:
    """Strip query parameters and hash anchors from relative URLs."""
    if not url:
        return ""
    clean = url.split("#")[0].split("?")[0].strip()
    return clean


def verify_all_links(base_dir: str = None) -> dict:
    """
    Validates all internal links, assets, and language switchers.
    Returns a structured dictionary of results.
    """
    if base_dir is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    results = {
        "files_checked": 0,
        "missing_html_files": [],
        "total_links_found": 0,
        "internal_links_checked": 0,
        "broken_internal_links": [],
        "stylesheets_checked": 0,
        "broken_stylesheets": [],
        "images_checked": 0,
        "broken_images": [],
        "scripts_checked": 0,
        "broken_scripts": [],
        "language_switcher_status": {},
        "all_valid": True,
    }

    for html_name in TARGET_HTML_FILES:
        html_path = os.path.join(base_dir, html_name)
        if not os.path.exists(html_path):
            results["missing_html_files"].append(html_name)
            results["all_valid"] = False
            continue

        results["files_checked"] += 1

        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()

        extractor = ResourceExtractor()
        extractor.feed(content)

        results["total_links_found"] += len(extractor.links)

        # 1. Verify internal <a> links
        for link in extractor.links:
            if link.startswith(("http://", "https://", "mailto:", "tel:", "#", "javascript:")):
                continue

            results["internal_links_checked"] += 1
            clean_link = clean_target_path(link)
            if not clean_link:
                continue

            target_path = os.path.join(base_dir, clean_link)
            if not os.path.exists(target_path):
                results["broken_internal_links"].append({
                    "source": html_name,
                    "target": link,
                    "resolved": target_path
                })
                results["all_valid"] = False

        # 2. Verify stylesheets
        for ss in extractor.stylesheets:
            if ss.startswith(("http://", "https://")):
                continue
            results["stylesheets_checked"] += 1
            clean_ss = clean_target_path(ss)
            target_path = os.path.join(base_dir, clean_ss)
            if not os.path.exists(target_path):
                results["broken_stylesheets"].append({
                    "source": html_name,
                    "target": ss,
                    "resolved": target_path
                })
                results["all_valid"] = False

        # 3. Verify images
        for img in extractor.images:
            if img.startswith(("http://", "https://", "data:")):
                continue
            results["images_checked"] += 1
            clean_img = clean_target_path(img)
            target_path = os.path.join(base_dir, clean_img)
            if not os.path.exists(target_path):
                results["broken_images"].append({
                    "source": html_name,
                    "target": img,
                    "resolved": target_path
                })
                results["all_valid"] = False

        # 4. Verify scripts
        for sc in extractor.scripts:
            if sc.startswith(("http://", "https://")):
                continue
            results["scripts_checked"] += 1
            clean_sc = clean_target_path(sc)
            target_path = os.path.join(base_dir, clean_sc)
            if not os.path.exists(target_path):
                results["broken_scripts"].append({
                    "source": html_name,
                    "target": sc,
                    "resolved": target_path
                })
                results["all_valid"] = False

        # 5. Verify Language Switcher
        if html_name in LANGUAGE_SWITCH_PAIRS:
            expected_targets = LANGUAGE_SWITCH_PAIRS[html_name]
            clean_links = [clean_target_path(l) for l in extractor.links]
            found = any(tgt in clean_links for tgt in expected_targets)
            results["language_switcher_status"][html_name] = {
                "expected": expected_targets,
                "found": found,
            }
            if not found:
                results["all_valid"] = False

    return results


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print("=" * 70)
    print("FreelanceToolkit - Programmatic Link & Asset Verification")
    print(f"Scanning directory: {base_dir}")
    print("=" * 70)

    res = verify_all_links(base_dir)

    print(f"[*] Platform HTML files checked: {res['files_checked']} / {len(TARGET_HTML_FILES)}")
    if res["missing_html_files"]:
        print(f"[!] MISSING HTML files: {res['missing_html_files']}")

    print(f"[*] Internal <a> links verified: {res['internal_links_checked']}")
    print(f"[*] Stylesheet links verified:  {res['stylesheets_checked']}")
    print(f"[*] Image assets verified:      {res['images_checked']}")
    print(f"[*] Script assets verified:     {res['scripts_checked']}")

    if res["broken_internal_links"]:
        print("\n[!] BROKEN INTERNAL LINKS:")
        for b in res["broken_internal_links"]:
            print(f"    - In {b['source']}: '{b['target']}' (not found at {b['resolved']})")

    if res["broken_stylesheets"]:
        print("\n[!] BROKEN STYLESHEETS:")
        for b in res["broken_stylesheets"]:
            print(f"    - In {b['source']}: '{b['target']}'")

    if res["broken_images"]:
        print("\n[!] BROKEN IMAGES:")
        for b in res["broken_images"]:
            print(f"    - In {b['source']}: '{b['target']}'")

    if res["broken_scripts"]:
        print("\n[!] BROKEN SCRIPTS:")
        for b in res["broken_scripts"]:
            print(f"    - In {b['source']}: '{b['target']}'")

    print("\n[*] Bidirectional Language Switcher Check:")
    for src, status in res["language_switcher_status"].items():
        mark = "[PASS]" if status["found"] else "[FAIL]"
        print(f"    {mark} {src} -> {status['expected']}")

    print("=" * 70)
    if res["all_valid"]:
        print("RESULT: SUCCESS - Zero broken links, zero broken assets, switchers intact.")
        print("=" * 70)
        sys.exit(0)
    else:
        print("RESULT: FAILURE - Discrepancies detected above.")
        print("=" * 70)
        sys.exit(1)


if __name__ == "__main__":
    main()
