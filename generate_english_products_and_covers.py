import os
import base64
import zipfile
from PIL import Image, ImageDraw, ImageFont
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

out_dir = r"C:\Users\Miguel\.gemini\antigravity\scratch\freelance-toolkit-saas\entregables"
os.makedirs(out_dir, exist_ok=True)

# ==============================================================================
# 1. GENERACIÓN DE PORTADAS EN INGLÉS
# ==============================================================================
def get_font(size, bold=False):
    font_paths = [
        "C:\\Windows\\Fonts\\segoeui.ttf",
        "C:\\Windows\\Fonts\\arial.ttf",
        "C:\\Windows\\Fonts\\calibri.ttf"
    ]
    if bold:
        font_paths = [
            "C:\\Windows\\Fonts\\segoeuib.ttf",
            "C:\\Windows\\Fonts\\arialbd.ttf",
            "C:\\Windows\\Fonts\\calibrib.ttf"
        ]
    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except:
                pass
    return ImageFont.load_default()

def draw_gradient(draw, width, height, start_color, end_color):
    for y in range(height):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * (y / height))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * (y / height))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * (y / height))
        draw.line([(0, y), (width, y)], fill=(r, g, b))

def create_cover_en(filename, bg_start, bg_end, accent_color, category_tag, title, subtitle, bullets, badge_text="2026 EDITION"):
    W, H = 1280, 720
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)

    # 1. Background gradient
    draw_gradient(draw, W, H, bg_start, bg_end)

    # 2. Subtle grid lines
    for x in range(0, W, 40):
        draw.line([(x, 0), (x, H)], fill=(255, 255, 255, 15), width=1)
    for y in range(0, H, 40):
        draw.line([(0, y), (W, y)], fill=(255, 255, 255, 15), width=1)

    # 3. Glassmorphism central card
    card_margin_x = 80
    card_margin_y = 60
    card_w = W - (card_margin_x * 2)
    card_h = H - (card_margin_y * 2)
    
    # Shadow
    draw.rounded_rectangle(
        [(card_margin_x + 8, card_margin_y + 8), (card_margin_x + card_w + 8, card_margin_y + card_h + 8)],
        radius=24, fill=(5, 5, 15)
    )
    # Body
    draw.rounded_rectangle(
        [(card_margin_x, card_margin_y), (card_margin_x + card_w, card_margin_y + card_h)],
        radius=24, fill=(17, 24, 39), outline=(55, 65, 81), width=2
    )

    # 4. Top Category Tag
    font_badge = get_font(18, bold=True)
    draw.rounded_rectangle([(card_margin_x + 50, card_margin_y + 50), (card_margin_x + 300, card_margin_y + 90)], radius=12, fill=accent_color)
    draw.text((card_margin_x + 65, card_margin_y + 58), category_tag, font=font_badge, fill=(255, 255, 255))

    # Badge Top Right
    draw.rounded_rectangle([(card_margin_x + card_w - 200, card_margin_y + 50), (card_margin_x + card_w - 50, card_margin_y + 90)], radius=12, fill=(31, 41, 55), outline=(75, 85, 99), width=1)
    draw.text((card_margin_x + card_w - 180, card_margin_y + 58), badge_text, font=font_badge, fill=(209, 213, 219))

    # 5. Main Title
    font_title = get_font(48, bold=True)
    draw.text((card_margin_x + 50, card_margin_y + 120), title, font=font_title, fill=(255, 255, 255))

    # 6. Subtitle
    font_sub = get_font(23, bold=False)
    draw.text((card_margin_x + 50, card_margin_y + 195), subtitle, font=font_sub, fill=(156, 163, 175))

    # Divider
    draw.line([(card_margin_x + 50, card_margin_y + 250), (card_margin_x + card_w - 50, card_margin_y + 250)], fill=(55, 65, 81), width=1)

    # 7. Bullets
    font_bullets = get_font(21, bold=True)
    start_bullet_y = card_margin_y + 290
    for i, bullet in enumerate(bullets):
        by = start_bullet_y + (i * 55)
        bx = card_margin_x + 50
        draw.rounded_rectangle([(bx, by - 4), (bx + 32, by + 28)], radius=8, fill=accent_color)
        draw.line([(bx + 9, by + 12), (bx + 15, by + 18)], fill=(255, 255, 255), width=3)
        draw.line([(bx + 15, by + 18), (bx + 24, by + 7)], fill=(255, 255, 255), width=3)
        draw.text((card_margin_x + 100, by), bullet, font=font_bullets, fill=(243, 244, 246))

    # 8. Floating sidebar preview
    mock_x = card_margin_x + card_w - 380
    mock_y = card_margin_y + 275
    draw.rounded_rectangle([(mock_x, mock_y), (mock_x + 330, mock_y + 230)], radius=16, fill=(31, 41, 55), outline=(75, 85, 99), width=1)
    
    font_prev_title = get_font(14, bold=True)
    font_prev_val = get_font(18, bold=True)
    font_prev_lbl = get_font(12, bold=False)

    draw.text((mock_x + 20, mock_y + 20), "ACTIVE PREVIEW", font=font_prev_title, fill=(156, 163, 175))
    draw.text((mock_x + 20, mock_y + 55), "Format:", font=font_prev_lbl, fill=(107, 114, 128))
    draw.text((mock_x + 20, mock_y + 75), ".XLSX / Google Sheets", font=font_prev_val, fill=accent_color)
    draw.text((mock_x + 20, mock_y + 115), "Compatibility:", font=font_prev_lbl, fill=(107, 114, 128))
    draw.text((mock_x + 20, mock_y + 135), "Google Sheets & Excel", font=get_font(16, bold=True), fill=(255, 255, 255))

    btn_y = mock_y + 175
    draw.rounded_rectangle([(mock_x + 20, btn_y), (mock_x + 310, btn_y + 40)], radius=10, fill=(16, 185, 129))
    draw.text((mock_x + 85, btn_y + 10), "✓ READY TO USE", font=font_prev_title, fill=(255, 255, 255))

    path = os.path.join(out_dir, filename)
    img.save(path, format="PNG", quality=95)
    with open(path.replace(".png", ".b64.txt"), "w") as f:
        f.write(base64.b64encode(open(path, "rb").read()).decode("utf-8"))
    print(f"Generated English Cover: {filename}")

# Generate all 10 English covers
covers_to_generate = [
    (
        "cover_finance_hub_en.png", (30, 27, 75), (15, 23, 42), (79, 70, 229),
        "FINANCIAL SYSTEM", "Freelance Finance Hub", "Automated revenue, expense, multi-currency & tax tracking.",
        [
            "Annual & Monthly Visual Financial Dashboards",
            "Automated Tax Reserves & Expense Deductions",
            "Invoicing Ledger & Real-Time Cash Flow",
            "Instant Cloud Access on Google Sheets & Excel"
        ]
    ),
    (
        "cover_client_crm_en.png", (23, 37, 84), (15, 23, 42), (37, 99, 235),
        "SALES & PIPELINE", "Freelance Client CRM", "Visual sales pipeline, deal stages & active project tracker.",
        [
            "Visual Deal Stages & Lead Probability Pipeline",
            "Centralized Client Directory & Contact History",
            "Project Delivery Deadlines & Payment Status",
            "Revenue Forecasting & Won/Lost Analytics"
        ]
    ),
    (
        "cover_email_swipe_en.png", (6, 78, 59), (15, 23, 42), (5, 150, 105),
        "NEGOTIATION", "Email Swipe File Pro", "40+ battle-tested scripts for high-ticket pitching & pricing.",
        [
            "Cold Outreach & High-Ticket Inbound Pitching",
            "Polite Price Increases & Handling \"You're Too High\"",
            "Stopping Scope-Creep & Free Revision Demands",
            "Firm & Professional Overdue Invoice Collection"
        ]
    ),
    (
        "cover_budget_503020_en.png", (136, 19, 55), (15, 23, 42), (225, 29, 72),
        "PERSONAL FINANCE", "50/30/20 Budget & Debt", "Master cash flow with the 50/30/20 rule and snowball plan.",
        [
            "Automated 50/30/20 Rule (Needs, Wants, Savings)",
            "Debt Snowball Rapid Payoff Calculator",
            "Monthly Expense Breakdown & Net Worth Growth",
            "Zero-Stress Financial Freedom Tracker"
        ]
    ),
    (
        "cover_habit_tracker_en.png", (120, 53, 15), (15, 23, 42), (217, 119, 6),
        "PRODUCTIVITY", "Ultimate Habit Tracker", "Gamified daily habit tracker with streaks & visual progress.",
        [
            "Daily Checkboxes with Visual Percentage Bars",
            "Consecutive Streak Counter & Gamified Scoring",
            "Weekly & Monthly Consistency Heatmaps",
            "Goal Setting for Health, Business & Mindset"
        ]
    ),
    (
        "cover_content_planner_en.png", (88, 28, 135), (15, 23, 42), (147, 51, 234),
        "CREATOR TOOLS", "Social Content Planner", "Multi-channel calendar for LinkedIn, X, TikTok & Instagram.",
        [
            "Multi-Platform Scheduling (X, LinkedIn, TikTok, IG)",
            "Proven High-Engagement Hook Bank & Ideas Vault",
            "Content Pillar Organization & Asset Manager",
            "Post-by-Post KPI Analytics & Growth Tracker"
        ]
    ),
    (
        "cover_reseller_tracker_en.png", (124, 45, 18), (15, 23, 42), (234, 88, 12),
        "E-COMMERCE & RESALE", "Reseller Profit Tracker", "Track inventory, platform fees, and net profit per item sold.",
        [
            "Automated Fee Deductions (eBay, Poshmark, Mercari)",
            "Active Inventory Value & Cost of Goods Sold (COGS)",
            "Net Margin & ROI Calculations Per Sale",
            "Annual Tax & Revenue Reporting Ledger"
        ]
    ),
    (
        "cover_quote_calculator_en.png", (19, 78, 74), (15, 23, 42), (13, 148, 136),
        "PRICING & QUOTES", "Project Quote Estimator", "Calculate profitable project scopes, risk buffers & margins.",
        [
            "Hourly & Value-Based Project Estimations",
            "Built-in Risk Buffers & Contingency Factors",
            "Automated Profit Margin Calculations",
            "Client-Ready Scope & Pricing Breakdown"
        ]
    ),
    (
        "cover_bundle_all_in_one_en.png", (49, 46, 129), (15, 23, 42), (245, 158, 11),
        "ALL-IN-ONE BUNDLE", "Freelance Productivity Suite", "The complete 8-system collection for independent pros.",
        [
            "All 8 Complete Spreadsheets & Web Systems Included",
            "Finance Hub + Client CRM + 40+ Email Swipe Files",
            "50/30/20 Budget + Habit Tracker + Content Planner",
            "Reseller Tracker + Project Estimator (Save >45%)"
        ]
    ),
    (
        "cover_tax_checklist_en.png", (6, 78, 59), (15, 23, 42), (16, 185, 129),
        "FREE STARTER TOOL", "Freelance Tax & Invoice Kit", "Essential 7-point invoice verification & tax cheat sheet.",
        [
            "7 Mandatory Legal Invoice Requirements",
            "Self-Employment Tax & Deduction Cheat Sheet",
            "Quarterly Tax Filing Deadlines Calendar",
            "Includes Exclusive 20% Discount Coupon (LANZAMIENTO20)"
        ]
    )
]

for args in covers_to_generate:
    create_cover_en(*args)

# ==============================================================================
# 2. GENERACIÓN DE HOJAS DE CÁLCULO EN INGLÉS (.xlsx)
# ==============================================================================
header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
title_font = Font(name="Calibri", size=15, bold=True, color="1E1B4B")
subtitle_font = Font(name="Calibri", size=10, italic=True, color="6B7280")
kpi_title_font = Font(name="Calibri", size=10, bold=True, color="4B5563")
bold_font = Font(name="Calibri", size=11, bold=True)
thin_border = Border(left=Side(style='thin', color='E5E7EB'), right=Side(style='thin', color='E5E7EB'), top=Side(style='thin', color='E5E7EB'), bottom=Side(style='thin', color='E5E7EB'))
total_border = Border(top=Side(style='thin', color='111827'), bottom=Side(style='double', color='111827'))

# 1. Finance Hub EN
def build_finance_hub_en():
    wb = openpyxl.Workbook()
    ws_dash = wb.active
    ws_dash.title = "📊 Annual Dashboard"
    ws_dash.views.sheetView[0].showGridLines = True
    ws_dash["B2"] = "FREELANCE FINANCE HUB 2026 (GLOBAL EDITION)"
    ws_dash["B2"].font = title_font
    ws_dash["B3"] = "Automated financial cash flow & tax tracker for independent professionals"
    ws_dash["B3"].font = subtitle_font

    kpis = [
        ("B5", "TOTAL REVENUE (GROSS)", "=SUM('💰 Revenue'!E5:E100)"),
        ("E5", "TOTAL EXPENSES", "=SUM('📉 Expenses'!E5:E100)"),
        ("H5", "NET OPERATING PROFIT", "=B6-E6"),
        ("K5", "ESTIMATED TAX RESERVE (25%)", "=H6*0.25")
    ]
    for cell_pos, label, formula in kpis:
        col = cell_pos[0]
        row = int(cell_pos[1:])
        ws_dash[f"{col}{row}"] = label
        ws_dash[f"{col}{row}"].font = kpi_title_font
        ws_dash[f"{col}{row+1}"] = formula
        ws_dash[f"{col}{row+1}"].font = Font(name="Calibri", size=18, bold=True, color="1E1B4B")
        ws_dash[f"{col}{row+1}"].number_format = "$#,##0.00"

    # Tab 2: Revenue
    ws_rev = wb.create_sheet(title="💰 Revenue")
    ws_rev.views.sheetView[0].showGridLines = True
    ws_rev["B2"] = "CLIENT INVOICING & REVENUE LOG"
    ws_rev["B2"].font = title_font
    headers_rev = ["Date", "Invoice #", "Client Name", "Project Scope", "Subtotal ($)", "Tax/VAT ($)", "Total Paid ($)", "Payment Status"]
    fill_rev = PatternFill(start_color="4F46E5", end_color="4F46E5", fill_type="solid")
    for c_idx, h in enumerate(headers_rev, start=1):
        cell = ws_rev.cell(row=4, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = fill_rev

    sample_rev = [
        ("2026-01-10", "INV-2026-001", "Acme Corp", "Website Redesign", 3500, 0, 3500, "Paid"),
        ("2026-01-18", "INV-2026-002", "Starlight Media", "Monthly Retainer", 1500, 0, 1500, "Paid"),
        ("2026-02-05", "INV-2026-003", "Apex Venture", "UX Audit & Wireframes", 2400, 0, 2400, "Pending")
    ]
    for r_idx, row in enumerate(sample_rev, start=5):
        for c_idx, val in enumerate(row, start=1):
            cell = ws_rev.cell(row=r_idx, column=c_idx, value=val)
            cell.border = thin_border
            if c_idx in [5, 6, 7]:
                cell.number_format = "$#,##0.00"

    # Tab 3: Expenses
    ws_exp = wb.create_sheet(title="📉 Expenses")
    ws_exp.views.sheetView[0].showGridLines = True
    ws_exp["B2"] = "BUSINESS OPERATING EXPENSES LOG"
    ws_exp["B2"].font = title_font
    headers_exp = ["Date", "Expense Category", "Vendor / Description", "Payment Method", "Amount ($)", "Tax Deductible?"]
    fill_exp = PatternFill(start_color="DC2626", end_color="DC2626", fill_type="solid")
    for c_idx, h in enumerate(headers_exp, start=1):
        cell = ws_exp.cell(row=4, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = fill_exp

    sample_exp = [
        ("2026-01-05", "Software & Tools", "Figma & Adobe CC Subscription", "Credit Card", 75.00, "Yes (100%)"),
        ("2026-01-12", "Hosting & Domains", "AWS & Cloudflare Services", "Credit Card", 45.00, "Yes (100%)"),
        ("2026-01-20", "Hardware", "External 4K Monitor", "Bank Transfer", 399.00, "Yes (100%)")
    ]
    for r_idx, row in enumerate(sample_exp, start=5):
        for c_idx, val in enumerate(row, start=1):
            cell = ws_exp.cell(row=r_idx, column=c_idx, value=val)
            cell.border = thin_border
            if c_idx == 5:
                cell.number_format = "$#,##0.00"

    for sheet in [ws_dash, ws_rev, ws_exp]:
        for col in sheet.columns:
            sheet.column_dimensions[get_column_letter(col[0].column)].width = 24

    path = os.path.join(out_dir, "Freelance_Finance_Hub_2026_EN.xlsx")
    wb.save(path)
    print("Generated English Excel:", path)

# 2. Client CRM EN
def build_client_crm_en():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "📊 Deal Pipeline"
    ws.views.sheetView[0].showGridLines = True
    ws["B2"] = "FREELANCE CLIENT & DEAL CRM 2026"
    ws["B2"].font = title_font
    ws["B3"] = "Sales pipeline, lead management & delivery milestone tracker"
    ws["B3"].font = subtitle_font

    headers = ["Lead / Company", "Contact Person", "Email / Phone", "Deal Stage", "Estimated Value ($)", "Win Probability (%)", "Weighted Value ($)", "Next Step"]
    fill = PatternFill(start_color="2563EB", end_color="2563EB", fill_type="solid")
    for c_idx, h in enumerate(headers, start=2):
        cell = ws.cell(row=5, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = fill

    sample = [
        ("HyperGrowth Labs", "Sarah Connor", "sarah@hypergrowth.io", "Proposal Sent", 5000, 0.70, "=F6*G6", "Follow up Thursday"),
        ("Nexus Design", "David Miller", "david@nexus.co", "Discovery Call", 2500, 0.40, "=F7*G7", "Send scope outline"),
        ("Global FinTech", "Alex Rivera", "alex@globalfin.com", "Closed / Won", 8000, 1.00, "=F8*G8", "Kickoff meeting")
    ]
    for r_idx, row in enumerate(sample, start=6):
        for c_idx, val in enumerate(row, start=2):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.border = thin_border
            if c_idx in [6, 8]:
                cell.number_format = "$#,##0.00"
            elif c_idx == 7:
                cell.number_format = "0%"

    for col in ws.columns:
        ws.column_dimensions[get_column_letter(col[0].column)].width = 22
    path = os.path.join(out_dir, "Freelance_Client_CRM_2026_EN.xlsx")
    wb.save(path)
    print("Generated English Excel:", path)

# 3. Budget 50/30/20 EN
def build_budget_en():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "📊 50-30-20 Budget"
    ws.views.sheetView[0].showGridLines = True
    ws["B2"] = "50/30/20 PERSONAL BUDGET & CASH FLOW PLANNER"
    ws["B2"].font = title_font
    ws["B3"] = "50% Essential Needs | 30% Lifestyle Wants | 20% Savings & Debt Snowball"
    ws["B3"].font = subtitle_font

    headers = ["50/30/20 Bucket", "Expense Category", "Budgeted ($)", "Actual Spent ($)", "Variance ($)", "Status"]
    fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
    for c_idx, h in enumerate(headers, start=2):
        cell = ws.cell(row=5, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = fill

    sample = [
        ("50% Needs", "Rent / Mortgage", 1400, 1400, "=D6-E6", "On Target"),
        ("50% Needs", "Groceries & Food", 450, 420, "=D7-E7", "Under Budget"),
        ("50% Needs", "Utilities & Internet", 180, 195, "=D8-E8", "Over Budget"),
        ("30% Wants", "Dining Out & Leisure", 300, 260, "=D9-E9", "On Target"),
        ("30% Wants", "Subscriptions (Gym, Netflix)", 80, 80, "=D10-E10", "On Target"),
        ("20% Savings/Debt", "Emergency Fund", 400, 400, "=D11-E11", "Funded"),
        ("20% Savings/Debt", "Debt Snowball Payoff", 250, 250, "=D12-E12", "Funded")
    ]
    for r_idx, row in enumerate(sample, start=6):
        for c_idx, val in enumerate(row, start=2):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.border = thin_border
            if c_idx in [4, 5, 6]:
                cell.number_format = "$#,##0.00"

    # Debt Snowball sheet
    ws_debt = wb.create_sheet(title="❄️ Debt Snowball")
    ws_debt.views.sheetView[0].showGridLines = True
    ws_debt["B2"] = "DEBT SNOWBALL RAPID AMORTIZATION PAYOFF PLAN"
    ws_debt["B2"].font = title_font
    debt_headers = ["Debt Name", "Balance ($)", "Interest Rate (%)", "Min Payment ($)", "Extra Snowball ($)", "Payoff Months"]
    fill_debt = PatternFill(start_color="DC2626", end_color="DC2626", fill_type="solid")
    for c_idx, h in enumerate(debt_headers, start=2):
        cell = ws_debt.cell(row=4, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = fill_debt

    sample_debts = [
        ("Credit Card 1", 1800, 19.5, 75, 150, "=ROUNDUP(C5/(E5+F5),0)"),
        ("Auto Loan", 6500, 5.8, 185, 0, "=ROUNDUP(C6/(E6+F6),0)"),
        ("Student Loan", 9200, 4.2, 120, 0, "=ROUNDUP(C7/(E7+F7),0)")
    ]
    for r_idx, row in enumerate(sample_debts, start=5):
        for c_idx, val in enumerate(row, start=2):
            cell = ws_debt.cell(row=r_idx, column=c_idx, value=val)
            cell.border = thin_border
            if c_idx in [3, 5, 6]:
                cell.number_format = "$#,##0.00"
            elif c_idx == 4:
                cell.number_format = "0.0%"

    for sheet in [ws, ws_debt]:
        for col in sheet.columns:
            sheet.column_dimensions[get_column_letter(col[0].column)].width = 22

    path = os.path.join(out_dir, "Personal_Budget_50_30_20_2026_EN.xlsx")
    wb.save(path)
    print("Generated English Excel:", path)

# 4. Ultimate Habit Tracker EN
def build_habit_tracker_en():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "🔥 Daily Habits"
    ws.views.sheetView[0].showGridLines = True
    ws["B2"] = "ULTIMATE HABIT TRACKER 2026"
    ws["B2"].font = title_font
    ws["B3"] = "Gamified daily consistency tracker with visual streak calculations"
    ws["B3"].font = subtitle_font

    headers = ["Habit / Daily Routine", "Target Category", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun", "Weekly %", "Streak Days"]
    fill = PatternFill(start_color="D97706", end_color="D97706", fill_type="solid")
    for c_idx, h in enumerate(headers, start=2):
        cell = ws.cell(row=5, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = fill
        cell.alignment = Alignment(horizontal="center" if c_idx >= 4 else "left")

    sample = [
        ("45 Min Focused Deep Work", "Career / Business", 1, 1, 1, 1, 1, 0, 0, "=SUM(D6:J6)/7", 5),
        ("Morning Workout / Cardio", "Health & Energy", 1, 1, 0, 1, 1, 1, 0, "=SUM(D7:J7)/7", 2),
        ("Read 15 Pages of Book", "Mindset & Growth", 1, 1, 1, 1, 1, 1, 1, "=SUM(D8:J8)/7", 14),
        ("Drink 2.5L Clean Water", "Health & Wellness", 1, 1, 1, 1, 0, 1, 1, "=SUM(D9:J9)/7", 3),
        ("Outreach to 3 New Leads", "Sales & Pipeline", 1, 1, 1, 1, 1, 0, 0, "=SUM(D10:J10)/7", 5)
    ]
    for r_idx, row in enumerate(sample, start=6):
        for c_idx, val in enumerate(row, start=2):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.border = thin_border
            if 4 <= c_idx <= 10:
                cell.alignment = Alignment(horizontal="center")
            if c_idx == 11:
                cell.number_format = "0.0%"
                cell.alignment = Alignment(horizontal="center")
            elif c_idx == 12:
                cell.alignment = Alignment(horizontal="center")

    for col in ws.columns:
        ws.column_dimensions[get_column_letter(col[0].column)].width = 18
    path = os.path.join(out_dir, "Ultimate_Habit_Tracker_2026_EN.xlsx")
    wb.save(path)
    print("Generated English Excel:", path)

# 5. Content Planner EN
def build_content_planner_en():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "📅 Editorial Calendar"
    ws.views.sheetView[0].showGridLines = True
    ws["B2"] = "SOCIAL MEDIA CONTENT PLANNER 2026"
    ws["B2"].font = title_font
    ws["B3"] = "Multi-channel publishing schedule, viral hook bank & KPI tracker"
    ws["B3"].font = subtitle_font

    headers = ["Scheduled Date", "Platform", "Content Pillar", "Hook / Headline", "Format", "Status", "Impressions", "Clicks / Engagements"]
    fill = PatternFill(start_color="9333EA", end_color="9333EA", fill_type="solid")
    for c_idx, h in enumerate(headers, start=2):
        cell = ws.cell(row=5, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = fill

    sample = [
        ("2026-02-01", "LinkedIn", "Authority Case Study", "How I stopped losing $1,200/mo on unpaid freelance revisions", "Text + Carousel", "Published", 4200, 310),
        ("2026-02-03", "X / Twitter", "Actionable Framework", "The 5 numbers every contractor must know before sending an invoice:", "Thread (5 tweets)", "Scheduled", 1850, 145),
        ("2026-02-05", "TikTok / Shorts", "Screen Tutorial", "Stop using manual Word docs for invoices in 2026", "Vertical Video 45s", "Drafting", 0, 0)
    ]
    for r_idx, row in enumerate(sample, start=6):
        for c_idx, val in enumerate(row, start=2):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.border = thin_border

    for col in ws.columns:
        ws.column_dimensions[get_column_letter(col[0].column)].width = 22
    path = os.path.join(out_dir, "Social_Media_Content_Planner_2026_EN.xlsx")
    wb.save(path)
    print("Generated English Excel:", path)

# 6. Reseller Profit Tracker EN
def build_reseller_en():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "📦 Sales & Inventory"
    ws.views.sheetView[0].showGridLines = True
    ws["B2"] = "RESELLER & E-COMMERCE PROFIT TRACKER"
    ws["B2"].font = title_font
    ws["B3"] = "Track purchase cost, platform fees (eBay, Poshmark, Mercari) and net margins per item"
    ws["B3"].font = subtitle_font

    headers = ["SKU / Item Name", "Purchase Date", "Buy Cost ($)", "Sale Platform", "Sale Price ($)", "Platform Fees ($)", "Shipping Cost ($)", "Net Profit ($)", "ROI %"]
    fill = PatternFill(start_color="EA580C", end_color="EA580C", fill_type="solid")
    for c_idx, h in enumerate(headers, start=2):
        cell = ws.cell(row=5, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = fill

    sample = [
        ("Vintage Leather Jacket", "2026-01-10", 25.00, "eBay", 110.00, "=F6*0.13", 8.50, "=F6-D6-G6-H6", "=I6/D6"),
        ("Noise-Canceling Headphones", "2026-01-15", 40.00, "Poshmark", 125.00, "=F7*0.20", 0.00, "=F7-D7-G7-H7", "=I7/D7"),
        ("Mechanical Keyboard", "2026-01-20", 35.00, "Mercari", 90.00, "=F8*0.10", 6.00, "=F8-D8-G8-H8", "=I8/D8")
    ]
    for r_idx, row in enumerate(sample, start=6):
        for c_idx, val in enumerate(row, start=2):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.border = thin_border
            if c_idx in [4, 6, 7, 8, 9]:
                cell.number_format = "$#,##0.00"
            elif c_idx == 10:
                cell.number_format = "0.0%"

    for col in ws.columns:
        ws.column_dimensions[get_column_letter(col[0].column)].width = 20
    path = os.path.join(out_dir, "Ecommerce_Reseller_Profit_Tracker_EN.xlsx")
    wb.save(path)
    print("Generated English Excel:", path)

# 7. Quote Calculator EN
def build_quote_calc_en():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "💼 Project Pricing"
    ws.views.sheetView[0].showGridLines = True
    ws["B2"] = "FREELANCE PROJECT QUOTE & PRICING ESTIMATOR"
    ws["B2"].font = title_font
    ws["B3"] = "Accurate hourly estimations, contingency buffers & profit margins"
    ws["B3"].font = subtitle_font

    headers = ["Deliverable / Task Phase", "Est. Hours", "Hourly Rate ($)", "Direct Costs ($)", "Contingency Buffer (20%)", "Phase Total ($)"]
    fill = PatternFill(start_color="0D9488", end_color="0D9488", fill_type="solid")
    for c_idx, h in enumerate(headers, start=2):
        cell = ws.cell(row=5, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = fill

    sample = [
        ("Phase 1: Research, Strategy & Architecture", 15, 75, 100, "=(C6*D6+E6)*0.20", "=C6*D6+E6+F6"),
        ("Phase 2: UI Design, Prototypes & Revisions", 25, 75, 50, "=(C7*D7+E7)*0.20", "=C7*D7+E7+F7"),
        ("Phase 3: Front-End Development & QA Testing", 30, 75, 150, "=(C8*D8+E8)*0.20", "=C8*D8+E8+F8")
    ]
    for r_idx, row in enumerate(sample, start=6):
        for c_idx, val in enumerate(row, start=2):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.border = thin_border
            if c_idx in [4, 5, 6, 7]:
                cell.number_format = "$#,##0.00"

    for col in ws.columns:
        ws.column_dimensions[get_column_letter(col[0].column)].width = 24
    path = os.path.join(out_dir, "Freelance_Project_Quote_Calculator_EN.xlsx")
    wb.save(path)
    print("Generated English Excel:", path)

# Build all 7 spreadsheets
build_finance_hub_en()
build_client_crm_en()
build_budget_en()
build_habit_tracker_en()
build_content_planner_en()
build_reseller_en()
build_quote_calc_en()

# ==============================================================================
# 3. GENERAR PAQUETES DUALES BILINGÜES (ZIP)
# ==============================================================================
def create_bilingual_zip(zip_name, es_file, en_file, readme_title):
    zip_path = os.path.join(out_dir, zip_name)
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # ES file
        if os.path.exists(os.path.join(out_dir, es_file)):
            zipf.write(os.path.join(out_dir, es_file), f"Spanish_Version/{es_file}")
        # EN file
        if os.path.exists(os.path.join(out_dir, en_file)):
            zipf.write(os.path.join(out_dir, en_file), f"English_Version/{en_file}")
        # Readme
        readme_content = f"""================================================================================
{readme_title}
Bilingual Edition [English + Español] • FreelanceToolkit 2026
================================================================================

THANK YOU FOR YOUR PURCHASE! / ¡GRACIAS POR TU COMPRA!

WHAT IS INCLUDED IN THIS PACKAGE:
1. English_Version/ -> Formatted in USD ($), multi-currency formulas and global P&L.
2. Spanish_Version/ -> Formatted in EUR (€), with IVA, IRPF and Spanish tax models.

HOW TO OPEN IN GOOGLE SHEETS (1-CLICK):
1. Open Google Drive (drive.google.com).
2. Click "+ New" -> "File upload".
3. Select the .xlsx file from either the English or Spanish folder.
4. Double-click the uploaded file and select "Open with Google Sheets".
5. Done! Everything is 100% cloud-synced and automated.

HOW TO OPEN IN MICROSOFT EXCEL:
1. Double-click the .xlsx file directly on Windows or Mac.
2. Click "Enable Editing" if prompted by Excel.

SUPPORT & TOOLKIT ECOSYSTEM:
Web: https://komasan19283645.github.io/freelance-toolkit/
Support / Updates: Instant digital access via Gumroad library.
"""
        zipf.writestr("INSTRUCTIONS_INSTRUCCIONES.txt", readme_content)
    print(f"Created Bilingual ZIP: {zip_path}")

create_bilingual_zip("Freelance_Finance_Hub_2026_Bilingual.zip", "Freelance_Finance_Hub_2026.xlsx", "Freelance_Finance_Hub_2026_EN.xlsx", "Freelance Finance Hub 2026")
create_bilingual_zip("Freelance_Client_CRM_2026_Bilingual.zip", "Freelance_Client_CRM_2026.xlsx", "Freelance_Client_CRM_2026_EN.xlsx", "Freelance Client CRM 2026")
create_bilingual_zip("Personal_Budget_50_30_20_Bilingual.zip", "Personal_Budget_50_30_20_2026.xlsx", "Personal_Budget_50_30_20_2026_EN.xlsx", "50/30/20 Personal Budget & Debt Snowball")
create_bilingual_zip("Ultimate_Habit_Tracker_2026_Bilingual.zip", "Ultimate_Habit_Tracker_2026.xlsx", "Ultimate_Habit_Tracker_2026_EN.xlsx", "Ultimate Habit Tracker 2026")
create_bilingual_zip("Social_Media_Content_Planner_Bilingual.zip", "Social_Media_Content_Planner_2026.xlsx", "Social_Media_Content_Planner_2026_EN.xlsx", "Social Media Content Planner 2026")
create_bilingual_zip("Ecommerce_Reseller_Profit_Tracker_Bilingual.zip", "Ecommerce_Reseller_Profit_Tracker.xlsx", "Ecommerce_Reseller_Profit_Tracker_EN.xlsx", "Reseller & E-Commerce Profit Tracker")
create_bilingual_zip("Freelance_Project_Quote_Calculator_Bilingual.zip", "Freelance_Project_Quote_Calculator.xlsx", "Freelance_Project_Quote_Calculator_EN.xlsx", "Freelance Project Quote Calculator")

# Create MASTER ALL-IN-ONE BUNDLE ZIP (containing all 8 tools in both languages)
master_bundle_path = os.path.join(out_dir, "All_in_One_Freelance_Productivity_Suite_2026.zip")
with zipfile.ZipFile(master_bundle_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    # All EN
    en_files = [
        "Freelance_Finance_Hub_2026_EN.xlsx", "Freelance_Client_CRM_2026_EN.xlsx", "Personal_Budget_50_30_20_2026_EN.xlsx",
        "Ultimate_Habit_Tracker_2026_EN.xlsx", "Social_Media_Content_Planner_2026_EN.xlsx", "Ecommerce_Reseller_Profit_Tracker_EN.xlsx",
        "Freelance_Project_Quote_Calculator_EN.xlsx", "Email_Swipe_File_Pro.html"
    ]
    for ef in en_files:
        p = os.path.join(out_dir, ef)
        if os.path.exists(p):
            zipf.write(p, f"English_Version_All_8_Systems/{ef}")
    # All ES
    es_files = [
        "Freelance_Finance_Hub_2026.xlsx", "Freelance_Client_CRM_2026.xlsx", "Personal_Budget_50_30_20_2026.xlsx",
        "Ultimate_Habit_Tracker_2026.xlsx", "Social_Media_Content_Planner_2026.xlsx", "Ecommerce_Reseller_Profit_Tracker.xlsx",
        "Freelance_Project_Quote_Calculator.xlsx", "Email_Swipe_File_Pro.html"
    ]
    for ef in es_files:
        p = os.path.join(out_dir, ef)
        if os.path.exists(p):
            zipf.write(p, f"Spanish_Version_Todos_Los_8_Sistemas/{ef}")

print(f"Master Bilingual Bundle ZIP created: {master_bundle_path}")
