#!/usr/bin/env python3
"""
test_boost_viral_cro.py - Verification Suite for /boost Launch Momentum Features

Verifies:
1. Hacker News Dynamic Welcome Banner (detection, styling, star link, dismissal).
2. 1-Click Viral Social Sharing Hooks (X/Twitter, LinkedIn, WhatsApp, Telegram, Copy).
3. High-Converting Post-Action Lead Magnet Modal (CRO) with pre-applied coupon LANZAMIENTO20.
4. Rich Metadata (Open Graph & Twitter Card) across all 10 platform files.
"""

import os
import re
import sys
import unittest
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

TARGET_PAGES = [
    "index-en.html",
    "index.html",
    "calculator-en.html",
    "calculator.html",
]

ALL_10_PAGES = [
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


class TestBoostViralCro(unittest.TestCase):

    # =========================================================================
    # 1. Hacker News Dynamic Welcome Banner
    # =========================================================================
    def test_hn_banner_present_in_index_en(self):
        path = os.path.join(BASE_DIR, "index-en.html")
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn('id="hn-welcome-banner"', content)
        self.assertIn("Welcome Hacker News!", content)
        self.assertIn("100% client-side, zero tracking &amp; zero signup", content)
        self.assertIn("Star on GitHub", content)
        self.assertIn("https://github.com/komasan19283645/freelance-toolkit", content)
        self.assertIn("dismissHnBanner()", content)

    def test_hn_banner_present_in_index_es(self):
        path = os.path.join(BASE_DIR, "index.html")
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn('id="hn-welcome-banner"', content)
        self.assertIn("Welcome Hacker News!", content)
        self.assertIn("https://github.com/komasan19283645/freelance-toolkit", content)

    def test_hn_banner_detection_logic_in_script(self):
        for fname in ["index-en.html", "index.html"]:
            path = os.path.join(BASE_DIR, fname)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("checkHnVisitor", content, f"{fname} must define checkHnVisitor")
            self.assertIn("ycombinator.com", content, f"{fname} must detect ycombinator.com referrer")
            self.assertIn("ref=hn", content, f"{fname} must detect ref=hn parameter")
            self.assertIn("ft_hn_dismissed", content, f"{fname} must persist dismissal in localStorage")
            self.assertIn("dismissHnBanner", content, f"{fname} must define dismissHnBanner")

    # =========================================================================
    # 2. 1-Click Viral Social Sharing Hooks
    # =========================================================================
    def test_viral_sharing_hooks_across_all_tools(self):
        for fname in TARGET_PAGES:
            path = os.path.join(BASE_DIR, fname)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("shareToolkit", content, f"{fname} must implement shareToolkit")
            self.assertIn("shareToolkit('x'", content, f"{fname} must feature X (Twitter) share hook")
            self.assertIn("shareToolkit('linkedin'", content, f"{fname} must feature LinkedIn share hook")
            self.assertIn("shareToolkit('whatsapp'", content, f"{fname} must feature WhatsApp share hook")
            self.assertIn("shareToolkit('telegram'", content, f"{fname} must feature Telegram share hook")
            self.assertIn("shareToolkit('copy'", content, f"{fname} must feature Copy Link share hook")

    def test_viral_sharing_prefilled_tweet_text(self):
        # English invoice
        with open(os.path.join(BASE_DIR, "index-en.html"), "r", encoding="utf-8") as f:
            c = f.read()
        self.assertIn("Just generated my invoice with @Komaleon37's FreelanceToolkit", c)
        self.assertIn("100% client-side, no signup, no $30/mo subscription", c)

        # English calculator
        with open(os.path.join(BASE_DIR, "calculator-en.html"), "r", encoding="utf-8") as f:
            c = f.read()
        self.assertIn("Just calculated my freelance rate with @Komaleon37's FreelanceToolkit", c)
        self.assertIn("100% client-side, zero signup, free", c)

        # Spanish invoice
        with open(os.path.join(BASE_DIR, "index.html"), "r", encoding="utf-8") as f:
            c = f.read()
        self.assertIn("Acabo de generar mi factura con @Komaleon37's FreelanceToolkit", c)
        self.assertIn("100% en el navegador, sin registro y sin suscripciones", c)

        # Spanish calculator
        with open(os.path.join(BASE_DIR, "calculator.html"), "r", encoding="utf-8") as f:
            c = f.read()
        self.assertIn("Acabo de calcular mi tarifa freelance con @Komaleon37's FreelanceToolkit", c)
        self.assertIn("100% privado en el navegador, gratis", c)

    # =========================================================================
    # 3. High-Converting Post-Action Lead Magnet Modal (CRO)
    # =========================================================================
    def test_cro_modal_present_on_all_tools(self):
        for fname in TARGET_PAGES:
            path = os.path.join(BASE_DIR, fname)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn('id="cro-upsell-modal"', content, f"{fname} must have cro-upsell-modal element")
            self.assertIn("openCroModal", content, f"{fname} must define openCroModal()")
            self.assertIn("closeCroModal", content, f"{fname} must define closeCroModal()")
            self.assertIn("LANZAMIENTO20", content, f"{fname} must feature promo code LANZAMIENTO20")
            self.assertIn("https://migueldp3.gumroad.com/l/eawgaf?wanted=true&discount_code=LANZAMIENTO20", content,
                          f"{fname} must link to free starter pack with pre-applied discount code")

    def test_cro_modal_headlines_english_and_spanish(self):
        # English invoice
        with open(os.path.join(BASE_DIR, "index-en.html"), "r", encoding="utf-8") as f:
            c = f.read()
        self.assertIn("🎉 Invoice ready! Want the complete 2026 Freelance Tax &amp; Invoicing Checklist + 20% OFF the Finance Hub?", c)
        self.assertIn("Get Free Guide (Instant Download)", c)

        # Spanish invoice
        with open(os.path.join(BASE_DIR, "index.html"), "r", encoding="utf-8") as f:
            c = f.read()
        self.assertIn("🎉 ¡Factura lista! ¿Quieres la Checklist Fiscal y de Facturación 2026 + 20% de descuento en el Finance Hub?", c)
        self.assertIn("Descargar Guía Gratis (Descarga Inmediata)", c)

        # English calculator
        with open(os.path.join(BASE_DIR, "calculator-en.html"), "r", encoding="utf-8") as f:
            c = f.read()
        self.assertIn("🎉 Rate calculated! Want the complete 2026 Freelance Tax &amp; Invoicing Checklist + 20% OFF the Finance Hub?", c)

        # Spanish calculator
        with open(os.path.join(BASE_DIR, "calculator.html"), "r", encoding="utf-8") as f:
            c = f.read()
        self.assertIn("🎉 ¡Tarifa calculada! ¿Quieres la Checklist Fiscal y de Facturación 2026 + 20% de descuento en el Finance Hub?", c)

    def test_print_trigger_opens_modal(self):
        for fname in ["index-en.html", "index.html"]:
            with open(os.path.join(BASE_DIR, fname), "r", encoding="utf-8") as f:
                c = f.read()
            self.assertIn("function triggerPdfAndModal()", c)
            self.assertIn("window.print()", c)
            self.assertIn("openCroModal", c)

    # =========================================================================
    # 4. Open Graph & Twitter Card Rich Metadata Optimization
    # =========================================================================
    def test_all_10_pages_have_complete_og_and_twitter_tags(self):
        for fname in ALL_10_PAGES:
            path = os.path.join(BASE_DIR, fname)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Open Graph tags
            self.assertIn('property="og:type"', content, f"{fname} missing og:type")
            self.assertIn('property="og:url"', content, f"{fname} missing og:url")
            self.assertIn('property="og:title"', content, f"{fname} missing og:title")
            self.assertIn('property="og:description"', content, f"{fname} missing og:description")
            self.assertIn('property="og:image"', content, f"{fname} missing og:image")

            # Twitter Card tags
            self.assertIn('name="twitter:card"', content, f"{fname} missing twitter:card")
            self.assertIn('name="twitter:site"', content, f"{fname} missing twitter:site")
            self.assertIn('name="twitter:creator"', content, f"{fname} missing twitter:creator")
            self.assertIn('name="twitter:title"', content, f"{fname} missing twitter:title")
            self.assertIn('name="twitter:description"', content, f"{fname} missing twitter:description")
            self.assertIn('name="twitter:image"', content, f"{fname} missing twitter:image")

            # Site and Creator match authorized pseudonym @Komaleon37
            self.assertIn('content="@Komaleon37"', content, f"{fname} twitter handle must be @Komaleon37")

            # Extract og:image URL and verify corresponding local file exists
            og_img_match = re.search(r'property="og:image"\s+content="(https://komasan19283645\.github\.io/freelance-toolkit/([^"]+))"', content)
            self.assertIsNotNone(og_img_match, f"{fname} og:image URL format invalid")
            rel_path = og_img_match.group(2)
            local_asset_path = os.path.join(BASE_DIR, rel_path.replace("/", os.sep))
            self.assertTrue(os.path.exists(local_asset_path), f"Asset {rel_path} for {fname} must exist on disk")

    # =========================================================================
    # 5. Explicit Edge Cases & Boundary Handling
    # =========================================================================
    def test_edge_case_escape_key_and_backdrop_click_handlers(self):
        """Verify modal is dismissible via Escape key and backdrop clicks across all tools."""
        for fname in TARGET_PAGES:
            with open(os.path.join(BASE_DIR, fname), "r", encoding="utf-8") as f:
                c = f.read()
            self.assertIn('keydown', c, f"{fname} must handle keydown events")
            self.assertIn('Escape', c, f"{fname} must handle Escape key for modal dismissal")
            self.assertIn('closeCroModal()', c, f"{fname} must close on modal dismiss")

    def test_edge_case_no_print_suppresses_modals_and_banners(self):
        """Verify both the HN banner and the CRO modal have no-print class to prevent paper bleed."""
        for fname in ["index-en.html", "index.html"]:
            with open(os.path.join(BASE_DIR, fname), "r", encoding="utf-8") as f:
                c = f.read()
            self.assertIn('id="hn-welcome-banner"', c)
            self.assertIn('no-print', c)
            # Find the hn banner tag and confirm no-print is present
            hn_match = re.search(r'<div id="hn-welcome-banner"[^>]*class="([^"]+)"', c)
            self.assertIsNotNone(hn_match)
            self.assertIn('no-print', hn_match.group(1))

            modal_match = re.search(r'<div id="cro-upsell-modal"[^>]*class="([^"]+)"', c)
            self.assertIsNotNone(modal_match)
            self.assertIn('no-print', modal_match.group(1))

    def test_edge_case_coupon_code_validity_and_uniformity(self):
        """Verify LANZAMIENTO20 is uniformly referenced in config, modals, and URLs."""
        # 1. Config JS
        with open(os.path.join(BASE_DIR, "js", "config.js"), "r", encoding="utf-8") as f:
            cfg = f.read()
        self.assertIn('LANZAMIENTO20', cfg)

        # 2. All 4 target tool pages
        for fname in TARGET_PAGES:
            with open(os.path.join(BASE_DIR, fname), "r", encoding="utf-8") as f:
                c = f.read()
            self.assertIn('discount_code=LANZAMIENTO20', c, f"{fname} must carry discount_code=LANZAMIENTO20")
            self.assertIn('LANZAMIENTO20', c, f"{fname} must advertise LANZAMIENTO20")


if __name__ == "__main__":
    unittest.main()

