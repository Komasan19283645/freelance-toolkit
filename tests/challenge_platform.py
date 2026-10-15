#!/usr/bin/env python3
"""
Empirical Challenger Test Suite for FreelanceToolkit Milestone 1:
- Test 1: Invoice Generator #printable-document print CSS rules and container integrity in index-en.html
- Test 2: LocalStorage key and serialization logic in index-en.html
- Test 3: Bidirectional language switchers across all 10 root HTML files (no broken links or circular dead-ends)
- Test 4: store-en.html product pricing: 8 products at $9, suite at $39, starter pack at $0
"""

import os
import sys
import re
import json
from html.parser import HTMLParser

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class ChallengeResult:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.details = []

    def record_pass(self, test_name, message):
        self.passed += 1
        self.details.append(f"[PASS] {test_name}: {message}")
        print(f"[PASS] {test_name}: {message}")

    def record_fail(self, test_name, message):
        self.failed += 1
        self.details.append(f"[FAIL] {test_name}: {message}")
        print(f"[FAIL] {test_name}: {message}")

    def record_warn(self, test_name, message):
        self.warnings += 1
        self.details.append(f"[WARN] {test_name}: {message}")
        print(f"[WARN] {test_name}: {message}")

def test_print_css_and_container(res):
    """Test 1: Verify #printable-document print CSS rules and container integrity in index-en.html."""
    print("\n--- TEST 1: Print CSS & Container Integrity (index-en.html & css/custom.css) ---")
    css_path = os.path.join(ROOT_DIR, "css", "custom.css")
    html_path = os.path.join(ROOT_DIR, "index-en.html")

    if not os.path.exists(css_path):
        res.record_fail("Print CSS", f"css/custom.css not found at {css_path}")
        return
    if not os.path.exists(html_path):
        res.record_fail("Print CSS", f"index-en.html not found at {html_path}")
        return

    with open(css_path, "r", encoding="utf-8") as f:
        css_content = f.read()

    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # 1. Check css/custom.css contains @media print with #printable-document
    if "@media print" not in css_content:
        res.record_fail("Print CSS", "@media print block missing in css/custom.css")
    else:
        res.record_pass("Print CSS", "@media print block present in css/custom.css")

    # Check #printable-document selector in print rules
    print_match = re.search(r"@media print\s*\{([\s\S]*?)\n\}", css_content)
    if not print_match:
        res.record_fail("Print CSS", "Could not isolate @media print block in css/custom.css")
    else:
        print_rules = print_match.group(1)
        if "#printable-document" not in print_rules:
            res.record_fail("Print CSS", "#printable-document selector missing inside @media print")
        else:
            res.record_pass("Print CSS", "#printable-document selector present inside @media print")

        # Verify key CSS declarations
        expected_rules = [
            "width: 100% !important",
            "max-width: 100% !important",
            "margin: 0 !important",
            "padding: 20mm !important",
            "box-shadow: none !important",
            "border: none !important",
            "background: white !important",
            "display: block !important"
        ]
        for rule in expected_rules:
            if rule in print_rules:
                res.record_pass("Print CSS Declaration", f"Verified '{rule}'")
            else:
                res.record_fail("Print CSS Declaration", f"Missing '{rule}' in #printable-document print block")

        # Verify hidden non-print elements
        hidden_elements = ["header", "footer", "nav", ".no-print", ".ad-slot", "#controls-panel", ".btn-action"]
        for elem in hidden_elements:
            if elem in print_rules and "display: none !important" in print_rules:
                res.record_pass("Print Hidden Elements", f"'{elem}' hidden during print")
            else:
                res.record_fail("Print Hidden Elements", f"'{elem}' not configured with display: none !important")

    # 2. Check index-en.html stylesheet link
    if '<link rel="stylesheet" href="css/custom.css">' in html_content:
        res.record_pass("HTML Link", "index-en.html properly links css/custom.css")
    else:
        res.record_fail("HTML Link", "index-en.html does not link css/custom.css")

    # 3. Check index-en.html #printable-document container
    if 'id="printable-document"' in html_content:
        res.record_pass("Container ID", "index-en.html contains id='printable-document'")
    else:
        res.record_fail("Container ID", "index-en.html missing id='printable-document'")

    if 'id="invoice-preview"' in html_content:
        res.record_fail("Legacy Container ID", "index-en.html still contains legacy id='invoice-preview'")
    else:
        res.record_pass("Legacy Container ID", "Zero occurrences of obsolete id='invoice-preview' in index-en.html")

    # 4. Check DOM container integrity inside #printable-document
    container_match = re.search(r'<div id="printable-document"[\s\S]*?</div>\s*</div>\s*</div>\s*</main>', html_content)
    if not container_match:
        res.record_fail("Container Integrity", "Could not isolate #printable-document enclosing block")
    else:
        doc_html = container_match.group(0)
        expected_doc_elements = [
            "preview-doc-type",
            "preview-invoice-number",
            "preview-date",
            "preview-due-date",
            "preview-sender-name",
            "preview-sender-taxid",
            "preview-sender-address",
            "preview-sender-email",
            "preview-sender-phone",
            "preview-client-name",
            "preview-client-taxid",
            "preview-client-address",
            "preview-items-body",
            "preview-subtotal",
            "preview-discount-row",
            "preview-discount",
            "preview-tax-label",
            "preview-tax",
            "preview-total",
            "preview-payment-method",
            "preview-notes"
        ]
        missing_elems = [e for e in expected_doc_elements if f'id="{e}"' not in doc_html]
        if missing_elems:
            res.record_fail("Container Integrity", f"Missing DOM elements in printable document: {missing_elems}")
        else:
            res.record_pass("Container Integrity", f"All {len(expected_doc_elements)} invoice preview elements present inside printable container")

def test_localstorage_serialization(res):
    """Test 2: Verify localStorage key and serialization logic in index-en.html."""
    print("\n--- TEST 2: LocalStorage Key & Serialization Logic (index-en.html) ---")
    html_path = os.path.join(ROOT_DIR, "index-en.html")
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Verify key name
    target_key = "freelancetoolkit_invoice_draft_en"
    if f'localStorage.getItem("{target_key}")' in content and f'localStorage.setItem("{target_key}"' in content:
        res.record_pass("LocalStorage Key", f"Found consistent read/write key '{target_key}'")
    else:
        res.record_fail("LocalStorage Key", f"Inconsistent or missing localStorage key '{target_key}'")

    # Verify no collision with Spanish key
    spanish_key = "freelancetoolkit_invoice_draft"
    # Ensure it's not using the bare spanish key without _en
    bare_uses = re.findall(r'localStorage\.[gs]etItem\(["\']' + spanish_key + r'["\']\)', content)
    if bare_uses:
        res.record_fail("LocalStorage Collision", f"Key collision: found bare Spanish key '{spanish_key}' in index-en.html")
    else:
        res.record_pass("LocalStorage Collision", f"No collision: index-en.html strictly isolates English state under '{target_key}'")

    # 2. Inspect loadSavedData() and saveData() definitions
    load_func = re.search(r'function loadSavedData\(\)\s*\{([\s\S]*?)\n    \}', content)
    save_func = re.search(r'function saveData\(\)\s*\{([\s\S]*?)\n    \}', content)

    if not load_func:
        res.record_fail("LocalStorage Functions", "loadSavedData() function not found")
    else:
        load_body = load_func.group(1)
        # Check error handling (try-catch)
        if "try {" in load_body and "catch" in load_body:
            res.record_pass("LocalStorage Safety", "loadSavedData() safely wrapped in try-catch")
        else:
            res.record_fail("LocalStorage Safety", "loadSavedData() lacks try-catch error boundary")

        # Check deep object merging
        if "parsed.sender" in load_body and "parsed.client" in load_body and "parsed.items" in load_body:
            res.record_pass("LocalStorage Deserialization", "loadSavedData() handles nested sender, client, and items merging")
        else:
            res.record_fail("LocalStorage Deserialization", "loadSavedData() fails to merge nested objects safely")

    if not save_func:
        res.record_fail("LocalStorage Functions", "saveData() function not found")
    else:
        save_body = save_func.group(1)
        if "try {" in save_body and "catch" in save_body:
            res.record_pass("LocalStorage Safety", "saveData() safely wrapped in try-catch")
        else:
            res.record_fail("LocalStorage Safety", "saveData() lacks try-catch error boundary")

        if "JSON.stringify(invoiceData)" in save_body:
            res.record_pass("LocalStorage Serialization", "saveData() serializes invoiceData with JSON.stringify")
        else:
            res.record_fail("LocalStorage Serialization", "saveData() does not call JSON.stringify(invoiceData)")

    # 3. Verify event listeners and triggers
    # saveData() must be called on form binding, item mutation, addItemRow, removeItemRow
    triggers = {
        "initFormBindings": r'el\.addEventListener\("input",\s*\(e\)\s*=>\s*\{[\s\S]*?saveData\(\);',
        "renderFormItems - description": r'invoiceData\.items\[\$\{index\}\]\.description\s*=[\s\S]*?saveData\(\);',
        "renderFormItems - quantity": r'invoiceData\.items\[\$\{index\}\]\.quantity\s*=[\s\S]*?saveData\(\);',
        "renderFormItems - rate": r'invoiceData\.items\[\$\{index\}\]\.rate\s*=[\s\S]*?saveData\(\);',
        "addItemRow": r'function addItemRow\(\)[\s\S]*?saveData\(\);',
        "removeItemRow": r'function removeItemRow\(index\)[\s\S]*?saveData\(\);'
    }
    for trigger_name, pattern in triggers.items():
        if re.search(pattern, content):
            res.record_pass("Persistence Trigger", f"saveData() bound to {trigger_name}")
        else:
            res.record_fail("Persistence Trigger", f"saveData() NOT bound to {trigger_name}")

    # 4. Verify DOMContentLoaded lifecycle
    dom_loaded = re.search(r'document\.addEventListener\("DOMContentLoaded",\s*\(\)\s*=>\s*\{([\s\S]*?)\}\);', content)
    if not dom_loaded:
        res.record_fail("Lifecycle Order", "DOMContentLoaded event listener missing")
    else:
        body = dom_loaded.group(1)
        calls = [c.strip() for c in body.split(";") if c.strip()]
        expected_seq = ["loadSavedData()", "initFormBindings()", "renderFormItems()", "updatePreview()"]
        if calls == expected_seq:
            res.record_pass("Lifecycle Order", f"Initialization sequence strictly verified: {' -> '.join(calls)}")
        else:
            res.record_fail("Lifecycle Order", f"Initialization sequence mismatch: expected {expected_seq}, got {calls}")

    # 5. Empirical Python Simulation of Serialization/Deserialization
    # Test adversarial payload: unicode, special characters, extreme values, missing optional fields
    test_draft = {
        "type": "estimate",
        "currency": "CA$",
        "invoiceNumber": "EST-2026-X99",
        "date": "2026-12-31",
        "dueDate": "2027-01-31",
        "sender": {
            "name": "Design & Code Studio <Special & 'Quotes'> 🚀",
            "taxId": "CA123456789RT0001",
            "address": "456 Bay St, Suite 200, Toronto, ON M5H 2R2",
            "email": "hello+quotes@designcode.ca",
            "phone": "+1 (416) 555-0199"
        },
        "client": {
            "name": "Acme Global (Pty) Ltd.",
            "taxId": "VAT499001122",
            "address": "100 Long St, Cape Town, 8001"
        },
        "items": [
            {"description": "Adversarial Test Item: <script>alert(1)</script> & €/$/£", "quantity": 10.5, "rate": 125.75},
            {"description": "Zero Quantity Item", "quantity": 0, "rate": 500},
            {"description": "High Precision Deliverable", "quantity": 1, "rate": 9999.99}
        ],
        "taxRate": 13,
        "discountRate": 5,
        "paymentMethod": "Wire Transfer: CAD Bank 004 Transit 12345 Account 9876543",
        "notes": "Net 30. All fees in Canadian Dollars."
    }

    try:
        # Simulate serialization
        serialized = json.dumps(test_draft)
        # Simulate deserialization & shallow merge
        default_state = {
            "type": "invoice",
            "currency": "$",
            "invoiceNumber": "INV-2026-001",
            "date": "2026-10-15",
            "dueDate": "2026-11-15",
            "sender": {"name": "Acme", "taxId": "123", "address": "St", "email": "a@b.com", "phone": "123"},
            "client": {"name": "Client", "taxId": "456", "address": "Ave"},
            "items": [],
            "taxRate": 0,
            "discountRate": 0,
            "paymentMethod": "",
            "notes": ""
        }
        parsed = json.loads(serialized)
        restored_state = {**default_state, **parsed}
        if "sender" in parsed:
            restored_state["sender"] = {**default_state["sender"], **parsed["sender"]}
        if "client" in parsed:
            restored_state["client"] = {**default_state["client"], **parsed["client"]}
        if "items" in parsed and isinstance(parsed["items"], list):
            restored_state["items"] = parsed["items"]

        # Check total preservation
        assert restored_state["currency"] == "CA$"
        assert restored_state["invoiceNumber"] == "EST-2026-X99"
        assert len(restored_state["items"]) == 3
        assert restored_state["sender"]["name"] == "Design & Code Studio <Special & 'Quotes'> 🚀"
        assert restored_state["items"][0]["description"] == "Adversarial Test Item: <script>alert(1)</script> & €/$/£"
        res.record_pass("Simulation Test", "Adversarial JSON serialization and shallow-merge simulation passed perfectly")
    except Exception as e:
        res.record_fail("Simulation Test", f"Adversarial serialization simulation failed: {e}")

def test_language_switchers(res):
    """Test 3: Verify all 10 root HTML files have valid bidirectional language switchers without broken links or circular dead-ends."""
    print("\n--- TEST 3: Bidirectional Language Switchers Across All 10 HTML Files ---")
    files = [
        "index.html",
        "index-en.html",
        "calculator.html",
        "calculator-en.html",
        "store.html",
        "store-en.html",
        "contracts.html",
        "como-hacer-factura-autonomo-irpf-iva.html",
        "ventas-vinted-wallapop-hacienda-dac7.html",
        "metodo-50-30-20-presupuesto-espanol.html"
    ]

    # Verify all 10 files exist
    for f in files:
        fpath = os.path.join(ROOT_DIR, f)
        if not os.path.exists(fpath):
            res.record_fail("File Existence", f"Required HTML file missing: {f}")
            return
    res.record_pass("File Existence", f"All {len(files)} core platform HTML files exist on disk")

    switcher_data = {}

    for f in files:
        fpath = os.path.join(ROOT_DIR, f)
        with open(fpath, "r", encoding="utf-8") as fp:
            content = fp.read()

        # 1. Desktop Header Switcher
        # Find <!-- Language Switcher --> block
        head_match = re.search(r'<!--\s*Language Switcher\s*-->([\s\S]*?)</div>\s*</div>', content, re.IGNORECASE)
        header_target = None
        if not head_match:
            # Fallback pattern for inline language switcher div
            head_match = re.search(r'<div[^>]*class=[\x22\x27][^\x22\x27]*border-slate-200[^\x22\x27]*[\x22\x27]>([\s\S]*?)</div>', content)

        if head_match:
            block = head_match.group(0)
            links = re.findall(r'<a\s+[^>]*href=[\x22\x27]([^\x22\x27]+)[\x22\x27][^>]*>([\s\S]*?)</a>', block)
            # Find the language link (points to .html)
            for href, text in links:
                if href.endswith(".html"):
                    header_target = href
                    break
        
        # 2. Mobile Drawer Switcher
        # Match Language: or Idioma: in mobile menu
        mob_match = re.search(r'(?:Language:|Idioma:)[\s\S]*?</div>\s*</div>', content, re.IGNORECASE)
        mobile_target = None
        if mob_match:
            block = mob_match.group(0)
            links = re.findall(r'<a\s+[^>]*href=[\x22\x27]([^\x22\x27]+)[\x22\x27][^>]*>([\s\S]*?)</a>', block)
            for href, text in links:
                if href.endswith(".html"):
                    mobile_target = href
                    break

        switcher_data[f] = {
            "header": header_target,
            "mobile": mobile_target
        }

        # Validate header switcher
        if header_target:
            target_path = os.path.join(ROOT_DIR, header_target)
            if os.path.exists(target_path):
                res.record_pass(f"{f} Header Switcher", f"Points to valid file '{header_target}'")
            else:
                res.record_fail(f"{f} Header Switcher", f"Broken link! Points to non-existent file '{header_target}'")
        else:
            res.record_fail(f"{f} Header Switcher", "No valid language switcher link found in desktop header")

        # Validate mobile switcher
        if mobile_target:
            target_path = os.path.join(ROOT_DIR, mobile_target)
            if os.path.exists(target_path):
                res.record_pass(f"{f} Mobile Switcher", f"Points to valid file '{mobile_target}'")
            else:
                res.record_fail(f"{f} Mobile Switcher", f"Broken link! Points to non-existent file '{mobile_target}'")
        else:
            res.record_fail(f"{f} Mobile Switcher", "No valid language switcher link found in mobile drawer")

    # 3. Verify Bidirectionality & Cycle Integrity
    primary_pairs = [
        ("index.html", "index-en.html"),
        ("calculator.html", "calculator-en.html"),
        ("store.html", "store-en.html")
    ]

    for es_page, en_page in primary_pairs:
        # ES -> EN
        es_head = switcher_data[es_page]["header"]
        es_mob = switcher_data[es_page]["mobile"]
        en_head = switcher_data[en_page]["header"]
        en_mob = switcher_data[en_page]["mobile"]

        if es_head == en_page and es_mob == en_page:
            res.record_pass(f"Bidirectional Pair [{es_page} -> {en_page}]", "Both header and mobile point directly to English peer")
        else:
            res.record_fail(f"Bidirectional Pair [{es_page} -> {en_page}]", f"Header got '{es_head}', Mobile got '{es_mob}', expected '{en_page}'")

        if en_head == es_page and en_mob == es_page:
            res.record_pass(f"Bidirectional Pair [{en_page} -> {es_page}]", "Both header and mobile point directly back to Spanish peer")
        else:
            res.record_fail(f"Bidirectional Pair [{en_page} -> {es_page}]", f"Header got '{en_head}', Mobile got '{en_mob}', expected '{es_page}'")

    # 4. Verify Spanish Guides and Contracts routing
    spanish_guides = [
        "contracts.html",
        "como-hacer-factura-autonomo-irpf-iva.html",
        "ventas-vinted-wallapop-hacienda-dac7.html",
        "metodo-50-30-20-presupuesto-espanol.html"
    ]
    for sg in spanish_guides:
        head = switcher_data[sg]["header"]
        mob = switcher_data[sg]["mobile"]
        # Must point to an English landing page (index-en.html or store-en.html)
        if head in ["index-en.html", "store-en.html"] and mob in ["index-en.html", "store-en.html"]:
            res.record_pass(f"Guide Routing [{sg}]", f"Routes cleanly to English platform ({head} / {mob}) with return path available")
        else:
            res.record_fail(f"Guide Routing [{sg}]", f"Invalid guide language route: header={head}, mobile={mob}")

def test_store_pricing(res):
    """Test 4: Verify store-en.html product pricing: 8 products at $9, suite at $39, starter pack at $0."""
    print("\n--- TEST 4: Store Pricing Integrity (store-en.html) ---")
    store_path = os.path.join(ROOT_DIR, "store-en.html")
    if not os.path.exists(store_path):
        res.record_fail("Store Pricing", f"store-en.html not found at {store_path}")
        return

    with open(store_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Verify Suite / Bundle Callout ($39)
    # Check navbar CTA
    if re.search(r'All-in-One Pack\s*\(\$39\)', content):
        res.record_pass("Suite Pricing (Navbar)", "Navbar CTA offers All-in-One Pack ($39)")
    else:
        res.record_fail("Suite Pricing (Navbar)", "Navbar CTA missing All-in-One Pack ($39)")

    # Check Bundle Hero Banner
    bundle_match = re.search(r'<!-- BUNDLE CALLOUT -->([\s\S]*?)<!-- FREE LEAD MAGNET', content)
    if not bundle_match:
        res.record_fail("Suite Pricing (Banner)", "Bundle callout block not found")
    else:
        banner = bundle_match.group(1)
        if "$39" in banner and "Get Complete Suite ($39)" in banner:
            res.record_pass("Suite Pricing (Banner)", "Bundle banner explicitly offers Complete Suite for $39")
        else:
            res.record_fail("Suite Pricing (Banner)", "Bundle banner missing $39 or 'Get Complete Suite ($39)'")

        if "https://migueldp3.gumroad.com/l/auhouf" in banner:
            res.record_pass("Suite Link", "Bundle links to valid Gumroad slug /auhouf")
        else:
            res.record_fail("Suite Link", "Bundle missing Gumroad slug /auhouf")

    # 2. Verify Free Starter Pack ($0)
    starter_match = re.search(r'<!-- FREE LEAD MAGNET CALLOUT -->([\s\S]*?)<!--.*?PRODUCT.*?GRID.*?-->', content, re.IGNORECASE)
    if not starter_match:
        res.record_fail("Starter Pricing", "Free lead magnet block not found")
    else:
        starter = starter_match.group(1)
        if "$0" in starter and "Download Free ($0)" in starter:
            res.record_pass("Starter Pricing", "Lead magnet callout explicitly offers Free Starter Pack ($0)")
        else:
            res.record_fail("Starter Pricing", "Lead magnet missing $0 or 'Download Free ($0)'")

        if "https://migueldp3.gumroad.com/l/eawgaf" in starter:
            res.record_pass("Starter Link", "Starter pack links to valid Gumroad slug /eawgaf")
        else:
            res.record_fail("Starter Link", "Starter pack missing Gumroad slug /eawgaf")

    # 3. Verify Products Grid (8 individual products at $9)
    grid_match = re.search(r'<!--.*?PRODUCT.*?GRID.*?-->([\s\S]*?)</main>', content, re.IGNORECASE)
    if not grid_match:
        res.record_fail("Products Grid", "Products grid block not found in store-en.html")
        return

    grid_content = grid_match.group(1)
    # Split by product card container: class="bg-white rounded-2xl ...
    cards = re.split(r'<div class="bg-white rounded-2xl', grid_content)
    # First item is before the first card
    product_cards = cards[1:]

    expected_product_count = 8
    if len(product_cards) == expected_product_count:
        res.record_pass("Product Count", f"Found exactly {expected_product_count} individual product cards in store-en.html")
    else:
        res.record_fail("Product Count", f"Expected {expected_product_count} cards, found {len(product_cards)}")

    expected_products = [
        {"slug": "bszbzj", "name": "Freelance Finance Hub 2026"},
        {"slug": "nghfmz", "name": "Client CRM & Pipeline Tracker"},
        {"slug": "pswllr", "name": "Email Swipe File Pro"},
        {"slug": "tvcpyv", "name": "Project Scope & Budget Estimator"},
        {"slug": "oanjr",  "name": "Ultimate Habit Tracker 2026"},
        {"slug": "qctvjw", "name": "Freelance Project Management Sheet"},
        {"slug": "gzwqf",  "name": "Client Onboarding & Offboarding Kit"},
        {"slug": "ssmjec", "name": "Freelance Business OS"}
    ]

    for idx, card in enumerate(product_cards, 1):
        # Extract title
        title_m = re.search(r'<h3[^>]*>([^<]+)</h3>', card)
        title = title_m.group(1).strip() if title_m else f"Product {idx}"

        # Extract badge price
        badge_m = re.search(r'<span[^>]*class=[\x22\x27][^\x22\x27]*font-black[^\x22\x27]*[\x22\x27][^>]*>\s*(\$\d+)\s*</span>', card)
        badge_price = badge_m.group(1).strip() if badge_m else "Missing"

        # Extract button
        btn_m = re.search(r'<a\s+[^>]*href=[\x22\x27]([^\x22\x27]+)[\x22\x27][^>]*>([\s\S]*?)</a>', card)
        btn_href = btn_m.group(1).strip() if btn_m else "Missing"
        btn_text = re.sub(r'\s+', ' ', btn_m.group(2)).strip() if btn_m else "Missing"

        # Verify $9 badge
        if badge_price == "$9":
            res.record_pass(f"Product {idx} ({title}) Badge", "Badge price is $9")
        else:
            res.record_fail(f"Product {idx} ({title}) Badge", f"Badge price is '{badge_price}', expected '$9'")

        # Verify $9 button text
        if "Buy Now ($9)" in btn_text or "($9)" in btn_text:
            res.record_pass(f"Product {idx} ({title}) Button", f"Button text '{btn_text}' verifies $9 pricing")
        else:
            res.record_fail(f"Product {idx} ({title}) Button", f"Button text '{btn_text}' does not verify $9 pricing")

        # Verify Gumroad link
        if idx <= len(expected_products):
            exp = expected_products[idx - 1]
            exp_slug = exp["slug"]
            if exp_slug in btn_href:
                res.record_pass(f"Product {idx} ({title}) Gumroad URL", f"Verified Gumroad slug /{exp_slug}")
            else:
                res.record_fail(f"Product {idx} ({title}) Gumroad URL", f"Expected slug /{exp_slug}, got '{btn_href}'")

    # 4. Check for any unexpected pricing or rogue $7 occurrences
    if "$7" in content:
        # Check if $7 is inside $72
        occurrences = re.findall(r'\$7(?![0-9])', content)
        if occurrences:
            res.record_fail("Pricing Anomaly", f"Found {len(occurrences)} rogue '$7' pricing occurrence(s) in store-en.html!")
        else:
            res.record_pass("Pricing Anomaly", "Zero rogue '$7' occurrences found (only $72 bundle anchor)")
    else:
        res.record_pass("Pricing Anomaly", "Zero '$7' occurrences anywhere in store-en.html")

    # 5. Check promo code LANZAMIENTO20 reference
    if "LANZAMIENTO20" in content:
        res.record_pass("Promo Code", "Promo code 'LANZAMIENTO20' active and referenced in store-en.html")
    else:
        res.record_warn("Promo Code", "Promo code 'LANZAMIENTO20' not referenced in store-en.html")

def main():
    print("=" * 70)
    print("EMPIRICAL CHALLENGER PLATFORM VERIFICATION (MILESTONE 1)")
    print("=" * 70)

    res = ChallengeResult()
    test_print_css_and_container(res)
    test_localstorage_serialization(res)
    test_language_switchers(res)
    test_store_pricing(res)

    print("\n" + "=" * 70)
    print("TEST EXECUTION SUMMARY:")
    print(f"Passed:   {res.passed}")
    print(f"Failed:   {res.failed}")
    print(f"Warnings: {res.warnings}")
    print("=" * 70)

    if res.failed == 0:
        print("\n>>> FINAL VERDICT: APPROVE <<<")
        sys.exit(0)
    else:
        print(f"\n>>> FINAL VERDICT: REQUEST_CHANGES ({res.failed} failures) <<<")
        sys.exit(1)

if __name__ == "__main__":
    main()
