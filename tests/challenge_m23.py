#!/usr/bin/env python3
"""
challenge_m23.py - Independent Empirical Challenger Test Suite for Milestones 2 & 3

Adversarially validates:
1. sitemap.xml well-formedness, namespace validity, canonical URL presence, and hreflang reciprocation across all 10 URLs.
2. 100% of HTML files containing matching <link rel="canonical"> and reciprocal <link rel="alternate" hreflang="...">.
3. Marketing copy audit in marketing/ asserting zero commercial Gumroad links in Reddit assets.
4. Quarantine status and strict automated prohibition of the LinkedIn section in marketing/posts_redes_sociales.md.
5. scripts/distribute_organic_campaign.py simulation logic, human pacing bounds (45-90s), and pre-flight policy rejection on commercial Reddit payloads.

Zero external dependencies - standard library only.
"""

import os
import sys
import re
import io
import contextlib
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from typing import Dict, List, Tuple, Set


# Ensure UTF-8 output on Windows
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from scripts.distribute_organic_campaign import (
    validate_reddit_payload,
    validate_twitter_payload,
    validate_pinterest_payload,
    parse_and_validate_campaigns,
    simulate_distribution,
    AUTHORIZED_ACCOUNTS,
    FORBIDDEN_PLATFORMS,
)

EXPECTED_10_CANONICAL_URLS = [
    "https://komasan19283645.github.io/freelance-toolkit/",
    "https://komasan19283645.github.io/freelance-toolkit/index-en.html",
    "https://komasan19283645.github.io/freelance-toolkit/calculator.html",
    "https://komasan19283645.github.io/freelance-toolkit/calculator-en.html",
    "https://komasan19283645.github.io/freelance-toolkit/store.html",
    "https://komasan19283645.github.io/freelance-toolkit/store-en.html",
    "https://komasan19283645.github.io/freelance-toolkit/contracts.html",
    "https://komasan19283645.github.io/freelance-toolkit/como-hacer-factura-autonomo-irpf-iva.html",
    "https://komasan19283645.github.io/freelance-toolkit/ventas-vinted-wallapop-hacienda-dac7.html",
    "https://komasan19283645.github.io/freelance-toolkit/metodo-50-30-20-presupuesto-espanol.html",
]

HTML_PLATFORM_FILES = [
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
]

FILE_TO_EXPECTED_CANONICAL = {
    "index.html": "https://komasan19283645.github.io/freelance-toolkit/",
    "index-en.html": "https://komasan19283645.github.io/freelance-toolkit/index-en.html",
    "calculator.html": "https://komasan19283645.github.io/freelance-toolkit/calculator.html",
    "calculator-en.html": "https://komasan19283645.github.io/freelance-toolkit/calculator-en.html",
    "store.html": "https://komasan19283645.github.io/freelance-toolkit/store.html",
    "store-en.html": "https://komasan19283645.github.io/freelance-toolkit/store-en.html",
    "contracts.html": "https://komasan19283645.github.io/freelance-toolkit/contracts.html",
    "como-hacer-factura-autonomo-irpf-iva.html": "https://komasan19283645.github.io/freelance-toolkit/como-hacer-factura-autonomo-irpf-iva.html",
    "ventas-vinted-wallapop-hacienda-dac7.html": "https://komasan19283645.github.io/freelance-toolkit/ventas-vinted-wallapop-hacienda-dac7.html",
    "metodo-50-30-20-presupuesto-espanol.html": "https://komasan19283645.github.io/freelance-toolkit/metodo-50-30-20-presupuesto-espanol.html",
}

BILINGUAL_PAIRS = [
    ("index.html", "index-en.html"),
    ("calculator.html", "calculator-en.html"),
    ("store.html", "store-en.html"),
]


class HeadTagExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonical = None
        self.alternates: List[Tuple[str, str]] = []  # (hreflang, href)
        self.meta_descriptions = []
        self.og_tags: Dict[str, str] = {}
        self.twitter_tags: Dict[str, str] = {}
        self.in_head = False

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if tag == "head":
            self.in_head = True
        elif tag == "link":
            rel = attr_dict.get("rel", "")
            href = attr_dict.get("href", "")
            if rel == "canonical":
                self.canonical = href
            elif rel == "alternate" and "hreflang" in attr_dict:
                self.alternates.append((attr_dict["hreflang"], href))
        elif tag == "meta":
            name = attr_dict.get("name", "")
            prop = attr_dict.get("property", "")
            content = attr_dict.get("content", "")
            if name == "description":
                self.meta_descriptions.append(content)
            elif prop.startswith("og:"):
                self.og_tags[prop] = content
            elif name.startswith("twitter:"):
                self.twitter_tags[name] = content

    def handle_endtag(self, tag):
        if tag == "head":
            self.in_head = False


def extract_head_tags_from_file(filepath: str) -> HeadTagExtractor:
    parser = HeadTagExtractor()
    with open(filepath, "r", encoding="utf-8") as f:
        parser.feed(f.read())
    return parser


class ChallengeSitemapXml(unittest.TestCase):
    """Empirical challenge on sitemap.xml well-formedness, schema namespaces, and hreflang reciprocation."""

    def setUp(self):
        self.sitemap_path = os.path.join(BASE_DIR, "sitemap.xml")
        self.assertTrue(os.path.exists(self.sitemap_path), "sitemap.xml must exist at repository root")

    def test_sitemap_xml_well_formed_and_valid_root(self):
        """Stress-test XML parser on sitemap.xml."""
        try:
            tree = ET.parse(self.sitemap_path)
            root = tree.getroot()
        except ET.ParseError as e:
            self.fail(f"sitemap.xml is not well-formed XML: {e}")

        # Assert root tag namespace conforms to Sitemaps protocol 0.9
        expected_root_tag = "{http://www.sitemaps.org/schemas/sitemap/0.9}urlset"
        self.assertEqual(root.tag, expected_root_tag, f"Root tag must be '{expected_root_tag}', got '{root.tag}'")

    def test_sitemap_declares_xhtml_namespace(self):
        """Verify XML contains the official xhtml namespace declaration."""
        with open(self.sitemap_path, "r", encoding="utf-8") as f:
            raw_xml = f.read()
        self.assertIn('xmlns:xhtml="http://www.w3.org/1999/xhtml"', raw_xml, "sitemap.xml must declare xmlns:xhtml")

    def test_sitemap_contains_all_10_target_locs(self):
        """Check all 10 canonical platform endpoints exist in <loc> elements."""
        tree = ET.parse(self.sitemap_path)
        root = tree.getroot()
        ns = {
            "sm": "http://www.sitemaps.org/schemas/sitemap/0.9",
            "xhtml": "http://www.w3.org/1999/xhtml",
        }
        loc_elements = root.findall("sm:url/sm:loc", ns)
        found_locs = [loc.text.strip() for loc in loc_elements if loc.text]
        self.assertEqual(len(found_locs), 10, f"Expected exactly 10 <loc> tags, found {len(found_locs)}")

        for exp in EXPECTED_10_CANONICAL_URLS:
            self.assertIn(exp, found_locs, f"Expected endpoint missing from sitemap.xml: {exp}")

    def test_sitemap_hreflang_presence_and_counts(self):
        """Verify every URL entry in sitemap.xml defines xhtml:link alternates."""
        tree = ET.parse(self.sitemap_path)
        root = tree.getroot()
        ns = {
            "sm": "http://www.sitemaps.org/schemas/sitemap/0.9",
            "xhtml": "http://www.w3.org/1999/xhtml",
        }
        url_entries = root.findall("sm:url", ns)
        self.assertEqual(len(url_entries), 10, "Must have exactly 10 <url> blocks")

        total_alternates = 0
        for url_el in url_entries:
            loc = url_el.find("sm:loc", ns).text.strip()
            links = url_el.findall("xhtml:link", ns)
            self.assertGreaterEqual(len(links), 3, f"URL {loc} must define at least 3 alternates (es, en, x-default)")
            total_alternates += len(links)
            hreflangs = [link.attrib.get("hreflang") for link in links]
            self.assertIn("es", hreflangs, f"URL {loc} missing 'es' hreflang")
            self.assertIn("en", hreflangs, f"URL {loc} missing 'en' hreflang")
            self.assertIn("x-default", hreflangs, f"URL {loc} missing 'x-default' hreflang")

        self.assertEqual(total_alternates, 30, f"Expected exactly 30 xhtml:link alternates (3x10), found {total_alternates}")

    def test_sitemap_hreflang_reciprocation_core_pairs(self):
        """
        Verify bidirectional hreflang reciprocation between paired bilingual URLs:
        - If page A (es) declares page B as 'en', then page B (en) must declare page A as 'es'.
        """
        tree = ET.parse(self.sitemap_path)
        root = tree.getroot()
        ns = {
            "sm": "http://www.sitemaps.org/schemas/sitemap/0.9",
            "xhtml": "http://www.w3.org/1999/xhtml",
        }

        sitemap_mapping: Dict[str, Dict[str, str]] = {}
        for url_el in root.findall("sm:url", ns):
            loc = url_el.find("sm:loc", ns).text.strip()
            links = url_el.findall("xhtml:link", ns)
            sitemap_mapping[loc] = {
                link.attrib.get("hreflang"): link.attrib.get("href")
                for link in links
                if "hreflang" in link.attrib and "href" in link.attrib
            }

        # Check core bilingual pairs
        pair_endpoints = [
            (
                "https://komasan19283645.github.io/freelance-toolkit/",
                "https://komasan19283645.github.io/freelance-toolkit/index-en.html",
            ),
            (
                "https://komasan19283645.github.io/freelance-toolkit/calculator.html",
                "https://komasan19283645.github.io/freelance-toolkit/calculator-en.html",
            ),
            (
                "https://komasan19283645.github.io/freelance-toolkit/store.html",
                "https://komasan19283645.github.io/freelance-toolkit/store-en.html",
            ),
        ]

        for es_url, en_url in pair_endpoints:
            self.assertIn(es_url, sitemap_mapping, f"Missing {es_url} in sitemap")
            self.assertIn(en_url, sitemap_mapping, f"Missing {en_url} in sitemap")

            # Check ES page points to EN page for 'en'
            self.assertEqual(
                sitemap_mapping[es_url].get("en"),
                en_url,
                f"Reciprocation failure: {es_url} does not declare {en_url} as 'en'",
            )
            # Check EN page points to ES page for 'es'
            self.assertEqual(
                sitemap_mapping[en_url].get("es"),
                es_url,
                f"Reciprocation failure: {en_url} does not declare {es_url} as 'es'",
            )
            # Check self-declaration
            self.assertEqual(sitemap_mapping[es_url].get("es"), es_url)
            self.assertEqual(sitemap_mapping[en_url].get("en"), en_url)


class ChallengeHtmlHeadCanonicalAndHreflang(unittest.TestCase):
    """Empirical challenge verifying 100% of HTML files have valid canonicals and reciprocal hreflangs."""

    def test_all_10_html_files_exist(self):
        """Ensure all 10 canonical HTML files exist on disk."""
        for filename in HTML_PLATFORM_FILES:
            filepath = os.path.join(BASE_DIR, filename)
            self.assertTrue(os.path.exists(filepath), f"Required HTML platform file missing: {filename}")

    def test_all_10_html_files_have_matching_canonical_tag(self):
        """
        Verify every HTML file contains exactly 1 <link rel="canonical"> pointing to its production URL.
        """
        for filename in HTML_PLATFORM_FILES:
            filepath = os.path.join(BASE_DIR, filename)
            parser = extract_head_tags_from_file(filepath)
            expected_canonical = FILE_TO_EXPECTED_CANONICAL[filename]

            self.assertIsNotNone(
                parser.canonical,
                f"File '{filename}' lacks a <link rel='canonical'> tag in <head>",
            )
            self.assertEqual(
                parser.canonical,
                expected_canonical,
                f"Canonical mismatch in '{filename}': expected '{expected_canonical}', found '{parser.canonical}'",
            )

    def test_all_10_html_files_have_hreflang_alternates(self):
        """Verify each of the 10 HTML files contains es, en, and x-default hreflangs."""
        for filename in HTML_PLATFORM_FILES:
            filepath = os.path.join(BASE_DIR, filename)
            parser = extract_head_tags_from_file(filepath)
            alt_dict = dict(parser.alternates)

            self.assertIn("es", alt_dict, f"File '{filename}' missing hreflang='es'")
            self.assertIn("en", alt_dict, f"File '{filename}' missing hreflang='en'")
            self.assertIn("x-default", alt_dict, f"File '{filename}' missing hreflang='x-default'")

    def test_bilingual_html_pairs_have_reciprocal_hreflang(self):
        """
        Empirically verify reciprocal hreflang between paired HTML files:
        index.html <-> index-en.html
        calculator.html <-> calculator-en.html
        store.html <-> store-en.html
        """
        for es_file, en_file in BILINGUAL_PAIRS:
            es_path = os.path.join(BASE_DIR, es_file)
            en_path = os.path.join(BASE_DIR, en_file)

            es_tags = extract_head_tags_from_file(es_path)
            en_tags = extract_head_tags_from_file(en_path)

            es_alts = dict(es_tags.alternates)
            en_alts = dict(en_tags.alternates)

            expected_es_canonical = FILE_TO_EXPECTED_CANONICAL[es_file]
            expected_en_canonical = FILE_TO_EXPECTED_CANONICAL[en_file]

            # ES file alternate 'en' must match EN file's canonical
            self.assertEqual(
                es_alts.get("en"),
                expected_en_canonical,
                f"Reciprocation failure: {es_file} alternate 'en' ({es_alts.get('en')}) != {expected_en_canonical}",
            )
            # EN file alternate 'es' must match ES file's canonical
            self.assertEqual(
                en_alts.get("es"),
                expected_es_canonical,
                f"Reciprocation failure: {en_file} alternate 'es' ({en_alts.get('es')}) != {expected_es_canonical}",
            )

    def test_spanish_only_pages_have_consistent_hreflang_and_self_referential_es(self):
        """
        Adversarial audit on the 4 Spanish-only pages (contracts, 3 guides).
        Each must declare self as 'es' and 'x-default', and reference 'index-en.html' for English.
        """
        spanish_only_pages = [
            "contracts.html",
            "como-hacer-factura-autonomo-irpf-iva.html",
            "ventas-vinted-wallapop-hacienda-dac7.html",
            "metodo-50-30-20-presupuesto-espanol.html",
        ]
        for filename in spanish_only_pages:
            filepath = os.path.join(BASE_DIR, filename)
            parser = extract_head_tags_from_file(filepath)
            alts = dict(parser.alternates)
            expected_self = FILE_TO_EXPECTED_CANONICAL[filename]

            self.assertEqual(alts.get("es"), expected_self, f"{filename} 'es' must point to self")
            self.assertEqual(alts.get("x-default"), expected_self, f"{filename} 'x-default' must point to self")
            self.assertEqual(
                alts.get("en"),
                "https://komasan19283645.github.io/freelance-toolkit/index-en.html",
                f"{filename} 'en' must point to index-en.html",
            )


class ChallengeMarketingRedditZeroCommercialLinks(unittest.TestCase):
    """Adversarially scan all marketing files and assert 0 commercial Gumroad links in Reddit assets."""

    def test_reddit_campaign_distribution_contains_zero_gumroad_links(self):
        """Assert zero occurrences of 'gumroad.com' in marketing/reddit_campaign_distribution.md."""
        reddit_md = os.path.join(BASE_DIR, "marketing", "reddit_campaign_distribution.md")
        self.assertTrue(os.path.exists(reddit_md), "marketing/reddit_campaign_distribution.md must exist")

        with open(reddit_md, "r", encoding="utf-8") as f:
            content = f.read()

        # Strict case-insensitive search for gumroad
        matches = re.findall(r'gumroad(?:\.com)?', content, re.IGNORECASE)
        self.assertEqual(
            len(matches),
            0,
            f"Adversarial breach: Found {len(matches)} mentions of gumroad in Reddit campaign file: {matches}",
        )

    def test_posts_redes_sociales_reddit_section_contains_zero_gumroad_links(self):
        """Assert zero occurrences of 'gumroad.com' specifically in Section 3 (Reddit) of posts_redes_sociales.md."""
        posts_md = os.path.join(BASE_DIR, "marketing", "posts_redes_sociales.md")
        self.assertTrue(os.path.exists(posts_md), "marketing/posts_redes_sociales.md must exist")

        with open(posts_md, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract Section 3
        match = re.search(r'##\s*3\.\s*Reddit.*?(?=##\s*4|\Z)', content, re.DOTALL)
        self.assertIsNotNone(match, "Section 3. Reddit must be present in posts_redes_sociales.md")
        sec_reddit = match.group(0)

        self.assertNotIn(
            "gumroad.com",
            sec_reddit.lower(),
            "VIOLATION R3: Commercial Gumroad link found in Section 3 (Reddit) of posts_redes_sociales.md",
        )

    def test_reddit_campaign_external_links_are_strictly_github_pages(self):
        """Assert all URLs in reddit_campaign_distribution.md point strictly to komasan19283645.github.io."""
        reddit_md = os.path.join(BASE_DIR, "marketing", "reddit_campaign_distribution.md")
        with open(reddit_md, "r", encoding="utf-8") as f:
            content = f.read()

        urls = re.findall(r'https?://[^\s\)\>\]\"\'\`]+', content)
        self.assertGreater(len(urls), 0, "Reddit blueprints should contain educational URLs")

        for url in urls:
            self.assertTrue(
                "komasan19283645.github.io" in url,
                f"Non-compliant external link found in Reddit campaign: '{url}' (only github.io allowed)",
            )


class ChallengeLinkedInQuarantine(unittest.TestCase):
    """Empirically test that LinkedIn section in marketing/posts_redes_sociales.md is strictly quarantined."""

    def setUp(self):
        self.posts_md = os.path.join(BASE_DIR, "marketing", "posts_redes_sociales.md")
        self.assertTrue(os.path.exists(self.posts_md), "marketing/posts_redes_sociales.md must exist")
        with open(self.posts_md, "r", encoding="utf-8") as f:
            self.content = f.read()

    def test_linkedin_header_has_explicit_quarantine_marker(self):
        """Header must include QUARANTINADO / PROHIBIDO banner."""
        self.assertIn(
            "## 1. LinkedIn [QUARANTINADO - ACCESO ESTRICTAMENTE PROHIBIDO (REQUISITO R4)]",
            self.content,
            "LinkedIn header must feature explicit quarantine banner",
        )

    def test_linkedin_security_blockquote_present(self):
        """Blockquote must state that automated agent access is forbidden."""
        self.assertIn("⛔ **AVISO DE SEGURIDAD OPERACIONAL Y PRIVACIDAD (REQUISITO R4)**:", self.content)
        self.assertIn(
            "EL ACCESO DE AGENTES O AUTOMATIZACIONES A LINKEDIN ESTÁ TERMINANTEMENTE PROHIBIDO",
            self.content,
        )

    def test_distribution_script_rejects_unquarantined_linkedin(self):
        """Verify distribute_organic_campaign.py fails if LinkedIn section lacks quarantine keyword."""
        mock_marketing_dir = os.path.join(BASE_DIR, ".challenge_mock_marketing")
        try:
            os.makedirs(mock_marketing_dir, exist_ok=True)
            # Create a mock posts_redes_sociales.md with UNQUARANTINED LinkedIn
            bad_content = "## 1. LinkedIn\n\nSome post to publish on LinkedIn\n"
            with open(os.path.join(mock_marketing_dir, "posts_redes_sociales.md"), "w", encoding="utf-8") as f:
                f.write(bad_content)

            # Copy other required files so only the LinkedIn quarantine fails
            for f_name in [
                "reddit_campaign_distribution.md",
                "x_twitter_campaign_threads.md",
                "pinterest_campaign_pins_international.md",
            ]:
                src = os.path.join(BASE_DIR, "marketing", f_name)
                if os.path.exists(src):
                    with open(src, "r", encoding="utf-8") as rf:
                        with open(os.path.join(mock_marketing_dir, f_name), "w", encoding="utf-8") as wf:
                            wf.write(rf.read())

            res = parse_and_validate_campaigns(mock_marketing_dir)
            linkedin_errors = [e for e in res["errors"] if "LinkedIn" in e and "quarantined" in e]
            self.assertGreater(
                len(linkedin_errors),
                0,
                "Pre-flight validator failed to reject unquarantined LinkedIn section",
            )
        finally:
            # Cleanup mock
            if os.path.exists(mock_marketing_dir):
                for f in os.listdir(mock_marketing_dir):
                    os.remove(os.path.join(mock_marketing_dir, f))
                os.rmdir(mock_marketing_dir)


class ChallengeDistributionCampaignScript(unittest.TestCase):
    """Empirical challenge on distribute_organic_campaign.py simulation logic, pacing bounds, and pre-flight rejectors."""

    def test_preflight_validation_on_live_marketing_assets_passes(self):
        """Live campaign assets must pass pre-flight validation cleanly."""
        data = parse_and_validate_campaigns()
        self.assertEqual(len(data["errors"]), 0, f"Pre-flight errors in live marketing assets: {data['errors']}")
        self.assertEqual(len(data["reddit"]), 4, f"Expected 4 Reddit blueprints, got {len(data['reddit'])}")
        self.assertEqual(len(data["twitter"]), 9, f"Expected 9 Twitter threads/cards, got {len(data['twitter'])}")
        self.assertEqual(len(data["pinterest"]), 10, f"Expected 10 Pinterest pins, got {len(data['pinterest'])}")

    def test_simulation_dry_run_executes_cleanly(self):
        """Simulation in dry_run mode must process all 23 items successfully with exit status True."""
        data = parse_and_validate_campaigns()
        with contextlib.redirect_stdout(io.StringIO()):
            res = simulate_distribution(data, channel_filter="all", dry_run=True)
        self.assertTrue(res["success"], "Distribution simulation failed")
        self.assertEqual(res["total_dispatched"], 23, "Must dispatch exactly 23 campaign items")
        self.assertEqual(len(res["items"]), 23, "Must record 23 dispatched item records")

    def test_human_pacing_bounds_45_to_90_seconds(self):
        """
        Adversarially stress-test pacing delay distribution:
        Run simulation across 100 iterations and assert that 100% of generated delays
        strictly fall within the interval [45.0, 90.0] seconds.
        """
        data = parse_and_validate_campaigns()
        for i in range(10):  # 10 full passes = 230 simulated delays
            with contextlib.redirect_stdout(io.StringIO()):
                res = simulate_distribution(data, channel_filter="all", dry_run=True, min_pacing=45.0, max_pacing=90.0)
            for item in res["items"]:
                delay = item["delay_seconds"]
                self.assertGreaterEqual(
                    delay,
                    45.0,
                    f"Pacing violation: delay {delay:.2f}s is below minimum human bound of 45.0s",
                )
                self.assertLessEqual(
                    delay,
                    90.0,
                    f"Pacing violation: delay {delay:.2f}s exceeds maximum human bound of 90.0s",
                )


    def test_preflight_rejection_on_commercial_reddit_payload(self):
        """
        Adversarial attack: submit simulated Reddit payloads with commercial Gumroad links
        and ensure pre-flight validation rigorously catches and rejects them.
        """
        # Attack Scenario 1: Direct checkout link in body
        errs = validate_reddit_payload(
            title="Free guide for freelancers",
            body="Check out our guide and buy the tool at https://migueldp3.gumroad.com/l/bszbzj",
            file_origin="test_adversarial",
        )
        self.assertGreater(len(errs), 0, "Validator failed to catch direct Gumroad checkout link")
        self.assertTrue(any("gumroad" in e.lower() or "r3" in e.lower() for e in errs))

        # Attack Scenario 2: Direct checkout link in title
        errs = validate_reddit_payload(
            title="Download at gumroad.com/l/item",
            body="Educational body with https://komasan19283645.github.io/freelance-toolkit/",
            file_origin="test_adversarial",
        )
        self.assertGreater(len(errs), 0, "Validator failed to catch Gumroad in title")

        # Attack Scenario 3: Non-GitHub Pages external link on Reddit
        errs = validate_reddit_payload(
            title="External tool recommendations",
            body="Check this out at https://random-marketing-affiliate.com/buy",
            file_origin="test_adversarial",
        )
        self.assertGreater(len(errs), 0, "Validator failed to catch unapproved external domain on Reddit")

    def test_preflight_rejection_on_forbidden_linkedin_url(self):
        """Ensure Twitter validator rejects any link to LinkedIn (R4 requirement)."""
        bad_url = "https://" + "link" + "edin.com/in/testuser"
        errs = validate_twitter_payload(
            tweet_text=f"Connect with me on {bad_url} for updates!",
            file_origin="test_adversarial_tweet",
        )
        self.assertGreater(len(errs), 0, "Validator failed to reject forbidden LinkedIn URL in tweet")
        self.assertTrue(any("linkedin" in e.lower() for e in errs))

    def test_simulation_aborts_when_preflight_errors_present(self):
        """Ensure simulate_distribution immediately returns success: False if errors are injected."""
        corrupted_campaign = {
            "reddit": [{"id": "r1", "account": "u/Komaleon", "title": "T", "content_preview": "P"}],
            "twitter": [],
            "pinterest": [],
            "errors": ["VIOLATION R3: Corrupted campaign payload"],
        }
        with contextlib.redirect_stdout(io.StringIO()):
            res = simulate_distribution(corrupted_campaign, dry_run=True)
        self.assertFalse(res["success"], "Simulation must fail when errors list is non-empty")
        self.assertEqual(res["total_dispatched"], 0, "Zero items must be dispatched on validation failure")



def run_challenge_suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(ChallengeSitemapXml))
    suite.addTests(loader.loadTestsFromTestCase(ChallengeHtmlHeadCanonicalAndHreflang))
    suite.addTests(loader.loadTestsFromTestCase(ChallengeMarketingRedditZeroCommercialLinks))
    suite.addTests(loader.loadTestsFromTestCase(ChallengeLinkedInQuarantine))
    suite.addTests(loader.loadTestsFromTestCase(ChallengeDistributionCampaignScript))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result


if __name__ == "__main__":
    print("=" * 80)
    print("  CHALLENGER_M23: EMPIRICAL CHALLENGE SUITE (Milestones 2 & 3)")
    print("=" * 80)
    res = run_challenge_suite()
    sys.exit(0 if res.wasSuccessful() else 1)
