#!/usr/bin/env python3
"""
distribute_organic_campaign.py - Multi-Channel Organic Distribution Engine & Simulator

Automates and simulates organic, educational acquisition distribution across verified
pseudonym channels with human-like pacing (45–90 seconds delay) and strict pre-flight
guardrail enforcement (zero commercial Gumroad links on Reddit, total LinkedIn prohibition,
and strict pseudonym attribution).

Supported Channels:
- Reddit: u/Komaleon (STRICT: Zero direct Gumroad links; educational GitHub Pages only)
- X / Twitter: @Komaleon37 (Value threads, preview cards, Gumroad with LANZAMIENTO20)
- Pinterest: @migueldpsp (2:3 vertical pins, high-intent SEO queries)
- Gumroad Store: migueldp3 (Digital product engine)

Zero external dependencies - pure Python 3 standard library.
"""

import os
import sys
import re
import time
import random
import argparse
from typing import Dict, List, Any, Optional

# Ensure UTF-8 output on Windows
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARKETING_DIR = os.path.join(BASE_DIR, "marketing")

AUTHORIZED_ACCOUNTS = {
    "reddit": "u/Komaleon",
    "twitter": "@Komaleon37",
    "pinterest": "@migueldpsp",
    "gumroad": "migueldp3",
    "github": "komasan19283645",
}

FORBIDDEN_PLATFORMS = {"linkedin"}

KNOWN_GITHUB_PAGES_ENDPOINTS = {
    "",
    "index.html",
    "index-en.html",
    "calculator.html",
    "calculator-en.html",
    "store.html",
    "store-en.html",
    "contracts.html",
    "como-hacer-factura-autonomo-irpf-iva.html",
    "ventas-vinted-wallapop-hacienda-dac7.html",
    "metodo-50-30-20-presupuesto-espanol.html",
}


class PreflightValidationError(Exception):
    """Raised when marketing copy or payload violates distribution policies."""
    pass


def extract_urls(text: str) -> List[str]:
    """Extracts all HTTP/HTTPS URLs from given text."""
    url_pattern = re.compile(r'https?://[^\s\)\>\]\"\'\`]+')
    return url_pattern.findall(text)


def validate_reddit_payload(title: str, body: str, file_origin: str) -> List[str]:
    """
    Validates Reddit distribution payload according to Requirement R3:
    1. Zero direct commercial Gumroad links.
    2. Links must point only to verified educational GitHub Pages guides or tools.
    3. Account must strictly be u/Komaleon.
    """
    errors = []
    combined = f"{title}\n{body}"

    # Rule 1: Zero direct Gumroad links on Reddit
    if "gumroad.com" in combined.lower():
        errors.append(
            f"[{file_origin}] VIOLATION R3: Direct commercial Gumroad link detected in Reddit payload! "
            f"Reddit strategy strictly forbids commercial checkout links."
        )

    # Rule 2: All external links must be official GitHub Pages
    urls = extract_urls(combined)
    for url in urls:
        if "komasan19283645.github.io" not in url:
            errors.append(
                f"[{file_origin}] VIOLATION R3: Non-compliant external link on Reddit: '{url}'. "
                f"Only educational GitHub Pages URLs (komasan19283645.github.io) are allowed."
            )

    return errors


def validate_twitter_payload(tweet_text: str, file_origin: str) -> List[str]:
    """Validates X/Twitter payload for authorized branding and valid destinations."""
    errors = []
    # Check for unauthorized platforms
    for forbidden in FORBIDDEN_PLATFORMS:
        if f"{forbidden}.com" in tweet_text.lower():
            errors.append(
                f"[{file_origin}] VIOLATION R4: Prohibited platform link '{forbidden}' found in Twitter payload."
            )
    return errors


def validate_pinterest_payload(pin_title: str, pin_desc: str, pin_url: str, file_origin: str) -> List[str]:
    """Validates Pinterest payload for 2:3 vertical spec and valid destination URLs."""
    errors = []
    urls = extract_urls(f"{pin_desc} {pin_url}")
    for url in urls:
        if "komasan19283645.github.io" not in url and "migueldp3.gumroad.com" not in url:
            errors.append(
                f"[{file_origin}] VIOLATION: Invalid Pinterest target destination URL '{url}'."
            )
    return errors


def parse_and_validate_campaigns(marketing_dir: str = MARKETING_DIR) -> Dict[str, Any]:
    """
    Reads and runs pre-flight validation on all campaign documents.
    Returns parsed campaign items structured by channel.
    """
    campaign_data = {
        "reddit": [],
        "twitter": [],
        "pinterest": [],
        "posts_legacy": [],
        "errors": [],
    }

    # 1. Parse Reddit Campaign (marketing/reddit_campaign_distribution.md)
    reddit_path = os.path.join(marketing_dir, "reddit_campaign_distribution.md")
    if os.path.exists(reddit_path):
        with open(reddit_path, "r", encoding="utf-8") as f:
            reddit_content = f.read()

        # Check persona
        if AUTHORIZED_ACCOUNTS["reddit"] not in reddit_content:
            campaign_data["errors"].append(
                f"[reddit_campaign_distribution.md] Missing authorized Reddit persona '{AUTHORIZED_ACCOUNTS['reddit']}'."
            )

        # Check for any Gumroad link
        if "gumroad.com" in reddit_content.lower():
            campaign_data["errors"].append(
                "[reddit_campaign_distribution.md] VIOLATION R3: 'gumroad.com' found in Reddit campaign file!"
            )

        # Extract blueprints
        blueprints = re.split(r'###\s+Blueprint\s+\d+:\s+', reddit_content)[1:]
        for idx, bp in enumerate(blueprints, 1):
            title_match = re.search(r'\*\*Title:\*\*\s*(.+)', bp)
            title = title_match.group(1).strip() if title_match else f"Blueprint {idx}"
            sub_match = re.search(r'`(r/\w+)`', bp)
            sub = sub_match.group(1) if sub_match else "r/freelance"

            errs = validate_reddit_payload(title, bp, f"reddit_campaign_distribution.md:Blueprint {idx}")
            campaign_data["errors"].extend(errs)

            campaign_data["reddit"].append({
                "id": f"reddit_bp_{idx}",
                "channel": "reddit",
                "account": AUTHORIZED_ACCOUNTS["reddit"],
                "target_community": sub,
                "title": title,
                "content_preview": bp[:140].replace("\n", " "),
                "raw": bp,
            })
    else:
        campaign_data["errors"].append("Missing required campaign file: marketing/reddit_campaign_distribution.md")

    # 2. Parse X/Twitter Campaign (marketing/x_twitter_campaign_threads.md)
    twitter_path = os.path.join(marketing_dir, "x_twitter_campaign_threads.md")
    if os.path.exists(twitter_path):
        with open(twitter_path, "r", encoding="utf-8") as f:
            tw_content = f.read()

        if AUTHORIZED_ACCOUNTS["twitter"] not in tw_content:
            campaign_data["errors"].append(
                f"[x_twitter_campaign_threads.md] Missing authorized Twitter persona '{AUTHORIZED_ACCOUNTS['twitter']}'."
            )

        # Extract threads
        threads = re.split(r'###\s+Thread\s+\d+:\s+', tw_content)[1:]
        for idx, th in enumerate(threads, 1):
            hook_match = re.search(r'\*\*Tweet 1 \(Hook\):\*\*\s*```text\s*(.*?)\s*```', th, re.DOTALL)
            hook = hook_match.group(1).strip() if hook_match else f"Thread {idx}"
            errs = validate_twitter_payload(th, f"x_twitter_campaign_threads.md:Thread {idx}")
            campaign_data["errors"].extend(errs)

            campaign_data["twitter"].append({
                "id": f"twitter_thread_{idx}",
                "channel": "twitter",
                "account": AUTHORIZED_ACCOUNTS["twitter"],
                "type": "thread",
                "title": hook[:80].replace("\n", " "),
                "content_preview": hook[:140].replace("\n", " "),
                "raw": th,
            })

        # Extract single cards
        cards = re.split(r'###\s+Card\s+\d+:\s+', tw_content)[1:]
        for idx, card in enumerate(cards, 1):
            campaign_data["twitter"].append({
                "id": f"twitter_card_{idx}",
                "channel": "twitter",
                "account": AUTHORIZED_ACCOUNTS["twitter"],
                "type": "product_card",
                "title": f"Product Drop Card {idx}",
                "content_preview": card[:140].replace("\n", " "),
                "raw": card,
            })
    else:
        campaign_data["errors"].append("Missing required campaign file: marketing/x_twitter_campaign_threads.md")

    # 3. Parse Pinterest Campaign (marketing/pinterest_campaign_pins_international.md)
    pin_path = os.path.join(marketing_dir, "pinterest_campaign_pins_international.md")
    if os.path.exists(pin_path):
        with open(pin_path, "r", encoding="utf-8") as f:
            pin_content = f.read()

        if AUTHORIZED_ACCOUNTS["pinterest"] not in pin_content:
            campaign_data["errors"].append(
                f"[pinterest_campaign_pins_international.md] Missing authorized Pinterest handle '{AUTHORIZED_ACCOUNTS['pinterest']}'."
            )

        # Must specify 2:3 vertical aspect ratio
        if "2:3" not in pin_content and "1000x1500" not in pin_content:
            campaign_data["errors"].append(
                "[pinterest_campaign_pins_international.md] Missing mandatory 2:3 vertical (1000x1500px) aspect ratio."
            )

        pins = re.split(r'###\s+Pin\s+\d+:\s+', pin_content)[1:]
        for idx, pin_block in enumerate(pins, 1):
            title_m = re.search(r'\*\*Title \(SEO\):\*\*\s*(.+)', pin_block)
            url_m = re.search(r'\*\*Destination URL:\*\*\s*(.+)', pin_block)
            p_title = title_m.group(1).strip() if title_m else f"Pin {idx}"
            p_url = url_m.group(1).strip() if url_m else ""

            errs = validate_pinterest_payload(p_title, pin_block, p_url, f"pinterest_campaign_pins_international.md:Pin {idx}")
            campaign_data["errors"].extend(errs)

            campaign_data["pinterest"].append({
                "id": f"pinterest_pin_{idx}",
                "channel": "pinterest",
                "account": AUTHORIZED_ACCOUNTS["pinterest"],
                "title": p_title,
                "destination_url": p_url,
                "content_preview": pin_block[:140].replace("\n", " "),
                "raw": pin_block,
            })
    else:
        campaign_data["errors"].append("Missing required campaign file: marketing/pinterest_campaign_pins_international.md")

    # 4. Parse & check legacy posts_redes_sociales.md (quarantine and Gumroad removal)
    legacy_path = os.path.join(marketing_dir, "posts_redes_sociales.md")
    if os.path.exists(legacy_path):
        with open(legacy_path, "r", encoding="utf-8") as f:
            leg_content = f.read()

        # Check that LinkedIn section has the mandatory quarantine notice
        if "## 1. LinkedIn" in leg_content:
            if "QUARANTIN" not in leg_content and "PROHIB" not in leg_content:
                campaign_data["errors"].append(
                    "[posts_redes_sociales.md] VIOLATION R4: LinkedIn section must be quarantined with an explicit prohibition banner!"
                )

        # Check section 3 (Reddit) has 0 Gumroad links
        reddit_section_match = re.search(r'## 3\. Reddit.*?(?=## 4|\Z)', leg_content, re.DOTALL)
        if reddit_section_match:
            sec_text = reddit_section_match.group(0)
            if "gumroad.com" in sec_text.lower():
                campaign_data["errors"].append(
                    "[posts_redes_sociales.md] VIOLATION R3: Commercial Gumroad link still present in Reddit section!"
                )

    return campaign_data


def simulate_distribution(
    campaign_data: Dict[str, Any],
    channel_filter: str = "all",
    dry_run: bool = True,
    min_pacing: float = 45.0,
    max_pacing: float = 90.0,
) -> Dict[str, Any]:
    """
    Executes distribution simulation across channels with randomized human pacing (45-90 seconds).
    In dry-run mode, validates payloads and logs simulated delays without pausing execution.
    """
    results = {
        "total_dispatched": 0,
        "items": [],
        "total_simulated_wait_seconds": 0.0,
        "success": True,
    }

    if campaign_data["errors"]:
        print("[!] Pre-flight validation failed with errors:")
        for err in campaign_data["errors"]:
            print(f"    - {err}")
        results["success"] = False
        return results

    channels_to_run = []
    if channel_filter in ("all", "reddit"):
        channels_to_run.append(("Reddit", campaign_data["reddit"]))
    if channel_filter in ("all", "twitter"):
        channels_to_run.append(("X/Twitter", campaign_data["twitter"]))
    if channel_filter in ("all", "pinterest"):
        channels_to_run.append(("Pinterest", campaign_data["pinterest"]))

    print("\n" + "=" * 76)
    print(f"  STARTING ORGANIC CAMPAIGN DISTRIBUTION ENGINE {'[DRY RUN]' if dry_run else '[LIVE SIMULATION]'}")
    print(f"  Pacing Constraints: {min_pacing:.0f}s - {max_pacing:.0f}s human delay between actions")
    print("=" * 76)

    for ch_name, items in channels_to_run:
        print(f"\n[*] Processing Channel: {ch_name} ({len(items)} items queued)")
        for idx, item in enumerate(items, 1):
            # Calculate human randomized delay between 45 and 90 seconds
            delay = random.uniform(min_pacing, max_pacing)
            results["total_simulated_wait_seconds"] += delay
            results["total_dispatched"] += 1

            print(f"  ├─ [{item['id']}] Account: {item['account']} | Title: \"{item['title']}\"")
            print(f"  │  Preview: {item['content_preview']}...")

            if dry_run:
                print(f"  │  [PACING] Simulated human delay: {delay:.1f}s (bypassed in --dry-run)")
            else:
                print(f"  │  [PACING] Enforcing human-like delay: {delay:.1f}s...")
                time.sleep(delay)

            results["items"].append({
                "id": item["id"],
                "channel": item["channel"],
                "account": item["account"],
                "title": item["title"],
                "delay_seconds": delay,
                "status": "SIMULATED_DISPATCH",
            })

    print("-" * 76)
    print(f"  Distribution Completed: {results['total_dispatched']} items successfully processed.")
    print(f"  Total Simulated Pacing: {results['total_simulated_wait_seconds']:.1f} seconds "
          f"({results['total_simulated_wait_seconds']/60:.1f} minutes).")
    print("=" * 76 + "\n")

    return results


def main():
    parser = argparse.ArgumentParser(description="FreelanceToolkit Multi-Channel Organic Distribution Engine")
    parser.add_argument("--dry-run", action="store_true", default=False, help="Run validation and simulation without sleep delays")
    parser.add_argument("--channel", choices=["all", "reddit", "twitter", "pinterest"], default="all", help="Filter target channel")
    parser.add_argument("--min-pacing", type=float, default=45.0, help="Minimum human pacing in seconds (default: 45)")
    parser.add_argument("--max-pacing", type=float, default=90.0, help="Maximum human pacing in seconds (default: 90)")
    args = parser.parse_args()

    print("=" * 76)
    print("  FreelanceToolkit - Multi-Channel Organic Distribution Engine (R3)")
    print(f"  Authorized Accounts: Reddit: {AUTHORIZED_ACCOUNTS['reddit']} | Twitter: {AUTHORIZED_ACCOUNTS['twitter']} | Pinterest: {AUTHORIZED_ACCOUNTS['pinterest']}")
    print(f"  Mode: {'DRY RUN (Rapid Verification)' if args.dry_run else 'LIVE PACED SIMULATION'}")
    print("=" * 76)

    # 1. Pre-flight Validation
    campaign_data = parse_and_validate_campaigns()

    if campaign_data["errors"]:
        print("\n[!] PRE-FLIGHT VALIDATION FAILED! The following violations were detected:")
        for err in campaign_data["errors"]:
            print(f"  [X] {err}")
        print("\nDistribution aborted to prevent policy violations.")
        sys.exit(1)

    print("\n[PASS] Pre-flight validation passed successfully:")
    print(f"  - Reddit Blueprints:    {len(campaign_data['reddit'])} (0 commercial links, u/Komaleon confirmed)")
    print(f"  - Twitter Threads/Cards: {len(campaign_data['twitter'])} (@Komaleon37 confirmed)")
    print(f"  - Pinterest Visual Pins: {len(campaign_data['pinterest'])} (2:3 vertical specs, @migueldpsp confirmed)")

    # 2. Simulate Distribution
    sim_res = simulate_distribution(
        campaign_data,
        channel_filter=args.channel,
        dry_run=args.dry_run,
        min_pacing=args.min_pacing,
        max_pacing=args.max_pacing,
    )

    if sim_res["success"]:
        print("[SUCCESS] Multi-channel organic distribution campaign verified and ready.")
        sys.exit(0)
    else:
        print("[FAILURE] Distribution execution encountered errors.")
        sys.exit(1)


if __name__ == "__main__":
    main()
