# -*- coding: utf-8 -*-
import os
import base64
from PIL import Image, ImageDraw, ImageFont

out_dir = r"C:\Users\Miguel\.gemini\antigravity\scratch\freelance-toolkit-saas\entregables"
os.makedirs(out_dir, exist_ok=True)

def get_font(size, bold=False):
    font_paths = [
        "C:\\Windows\\Fonts\\segoeuib.ttf" if bold else "C:\\Windows\\Fonts\\segoeui.ttf",
        "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf",
        "C:\\Windows\\Fonts\\calibrib.ttf" if bold else "C:\\Windows\\Fonts\\calibri.ttf"
    ]
    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def draw_gradient_rgba(draw, width, height, start_color, end_color):
    for y in range(height):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * (y / height))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * (y / height))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * (y / height))
        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))

def create_square_thumbnail(filename, bg_start, bg_end, accent_color, category_tag, title_line1, title_line2, highlight_tag, stat_label, stat_val, price_badge, format_label="Sheets & Excel"):
    W, H = 600, 600
    is_en = filename.endswith("_en")

    # 1. Base Gradient in RGBA
    base = Image.new("RGBA", (W, H))
    draw_base = ImageDraw.Draw(base)
    draw_gradient_rgba(draw_base, W, H, bg_start, bg_end)

    # 2. Subtle Grid with genuine alpha composite
    grid_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_grid = ImageDraw.Draw(grid_overlay)
    for x in range(0, W, 30):
        draw_grid.line([(x, 0), (x, H)], fill=(255, 255, 255, 14), width=1)
    for y in range(0, H, 30):
        draw_grid.line([(0, y), (W, y)], fill=(255, 255, 255, 14), width=1)

    img = Image.alpha_composite(base, grid_overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # 3. Outer Border Frame
    draw.rounded_rectangle([(16, 16), (W - 16, H - 16)], radius=20, outline=accent_color, width=2)

    # 4. Top Category & Edition Badges
    font_cat = get_font(13, bold=True)
    cat_bbox = font_cat.getbbox(category_tag)
    cat_text_w = cat_bbox[2] - cat_bbox[0]
    cat_badge_w = max(180, cat_text_w + 28)
    draw.rounded_rectangle([(36, 32), (36 + cat_badge_w, 62)], radius=8, fill=accent_color)
    draw.text((36 + 14, 38), category_tag, font=font_cat, fill=(255, 255, 255))

    font_badge = get_font(12, bold=True)
    draw.rounded_rectangle([(W - 160, 32), (W - 36, 62)], radius=8, fill=(30, 41, 59), outline=(71, 85, 105), width=1)
    draw.text((W - 145, 39), "2026 EDITION", font=font_badge, fill=(203, 213, 225))

    # 5. Main Title (High readability)
    font_title = get_font(34, bold=True)
    draw.text((36, 85), title_line1, font=font_title, fill=(255, 255, 255))
    if title_line2:
        draw.text((36, 130), title_line2, font=font_title, fill=accent_color)

    # 6. Center Mockup Card (Glassmorphism stat box)
    card_x1, card_y1 = 36, 195
    card_x2, card_y2 = W - 36, 440
    
    # Shadow
    draw.rounded_rectangle([(card_x1 + 6, card_y1 + 6), (card_x2 + 6, card_y2 + 6)], radius=16, fill=(5, 8, 16))
    # Card body
    draw.rounded_rectangle([(card_x1, card_y1), (card_x2, card_y2)], radius=16, fill=(15, 23, 42), outline=(51, 65, 85), width=2)
    
    # Card Header
    draw.rounded_rectangle([(card_x1, card_y1), (card_x2, card_y1 + 42)], radius=16, fill=(30, 41, 59))
    font_card_head = get_font(13, bold=True)
    card_header_title = "AUTOMATED SYSTEM" if is_en else "SISTEMA AUTOMATIZADO"
    draw.text((card_x1 + 18, card_y1 + 12), card_header_title, font=font_card_head, fill=(148, 163, 184))

    # Inside Card Highlights
    font_card_lbl = get_font(13, bold=False)
    font_card_val = get_font(26, bold=True)
    
    draw.text((card_x1 + 20, card_y1 + 60), stat_label, font=font_card_lbl, fill=(148, 163, 184))
    draw.text((card_x1 + 20, card_y1 + 85), stat_val, font=font_card_val, fill=(255, 255, 255))

    # Highlight Pill
    font_pill = get_font(14, bold=True)
    pill_y = card_y1 + 140
    draw.rounded_rectangle([(card_x1 + 20, pill_y), (card_x2 - 20, pill_y + 44)], radius=8, fill=(16, 185, 129))
    draw.text((card_x1 + 35, pill_y + 12), highlight_tag, font=font_pill, fill=(255, 255, 255))

    font_fmt = get_font(12, bold=False)
    compat_label = f"Compatibility: {format_label} | 100% Macro-Free" if is_en else f"Compatibilidad: {format_label} | Sin macros"
    draw.text((card_x1 + 20, pill_y + 60), compat_label, font=font_fmt, fill=(100, 116, 139))

    # 7. Bottom Action & Pricing Bar (Centered price pill)
    font_price = get_font(22, bold=True)
    badge_x1, badge_x2 = 36, 190
    badge_w = badge_x2 - badge_x1
    p_bbox = font_price.getbbox(price_badge)
    p_text_w = p_bbox[2] - p_bbox[0]
    p_x = badge_x1 + (badge_w - p_text_w) // 2
    draw.rounded_rectangle([(badge_x1, 480), (badge_x2, 535)], radius=12, fill=accent_color)
    draw.text((p_x, 492), price_badge, font=font_price, fill=(255, 255, 255))

    font_stars = get_font(14, bold=True)
    draw.text((215, 492), "⭐ ⭐ ⭐ ⭐ ⭐ 5.0", font=font_stars, fill=(251, 191, 36))
    
    font_substars = get_font(12, bold=False)
    substars_text = "Verified & Battle-Tested Template" if is_en else "Plantilla Verificada & Probada"
    draw.text((215, 514), substars_text, font=font_substars, fill=(148, 163, 184))

    # Save
    out_png = os.path.join(out_dir, filename + ".png")
    out_b64 = os.path.join(out_dir, filename + ".b64.txt")
    img.save(out_png, "PNG", quality=95)
    with open(out_png, "rb") as f:
        b64_str = base64.b64encode(f.read()).decode("utf-8")
    with open(out_b64, "w", encoding="utf-8") as f:
        f.write(b64_str)
    print(f"Generated square thumbnail: {out_png}")

def main():
    thumbnails = [
        # 1. Finance Hub
        ("thumb_finance_hub", (30, 27, 75), (15, 23, 42), (79, 70, 229),
         "FINANZAS AUTÓNOMO", "Freelance", "Finance Hub",
         "✓ Cálculo Automático IVA & IRPF", "Previsión Fiscal Anual:", "100% Sin Sorpresas", "9 €", "Google Sheets & Excel"),
        
        # 2. Client CRM
        ("thumb_client_crm", (15, 23, 42), (2, 6, 23), (37, 99, 235),
         "CRM & VENTAS B2B", "Freelance", "Client CRM",
         "✓ Pipeline Kanban & Fichas Leads", "Control de Propuestas:", "Organización Total", "9 €", "Google Sheets & Excel"),
        
        # 3. Tax Checklist
        ("thumb_tax_checklist", (6, 78, 59), (15, 23, 42), (16, 185, 129),
         "RECURSO GRATUITO", "Guía Fiscal", "Express 2026",
         "✓ 7 Requisitos Factura Legal", "RD 1619/2012 & DAC7:", "Evita Multas", "0 € GRATIS", "PDF + HTML Interactivo"),
        
        # 4. All-in-One Pack
        ("thumb_bundle_all_in_one", (17, 24, 39), (49, 46, 129), (245, 158, 11),
         "PACK 8-EN-1 DEFINITIVO", "All-in-One", "Freelance Suite",
         "✓ Los 8 Sistemas Completos", "Ahorro Directo:", "-45% Descuento", "39 €", "8 Archivos .XLSX + Web"),
        
        # 5. Quote Calculator
        ("thumb_quote_calculator", (19, 78, 74), (15, 23, 42), (13, 148, 136),
         "COTIZADOR COMERCIAL", "Cotizador de", "Presupuestos",
         "✓ Margen Contingencia (+20%)", "Tarifa Horaria Real:", "Rentabilidad Asegurada", "9 €", "Google Sheets & Excel"),
        
        # 6. Reseller Tracker
        ("thumb_reseller_tracker", (154, 52, 18), (15, 23, 42), (234, 88, 12),
         "REVENTA & E-COMMERCE", "Reseller", "Profit Tracker",
         "✓ Comisiones Wallapop, Vinted, Amazon", "Límite DAC7 Hacienda:", "Alerta 2.000 € / 30 Ventas", "9 €", "Google Sheets & Excel"),
        
        # 7. Content Planner
        ("thumb_content_planner", (88, 28, 135), (15, 23, 42), (147, 51, 234),
         "CREADORES & MARKETING", "Social Media", "Content Planner",
         "✓ 50+ Ganchos Virales (Hooks)", "Calendario Editorial:", "TikTok / IG / LinkedIn / X", "9 €", "Google Sheets & Excel"),
        
        # 8. Budget 50/30/20
        ("thumb_budget_503020", (136, 19, 55), (15, 23, 42), (225, 29, 72),
         "FINANZAS PERSONALES", "Presupuesto", "50/30/20 & Deuda",
         "✓ Calculadora Bola de Nieve", "Control Mensual de Nómina:", "Libre de Deudas", "9 €", "Google Sheets & Excel"),
        
        # 9. Email Swipe File
        ("thumb_email_swipe", (6, 78, 59), (15, 23, 42), (16, 185, 129),
         "GUIONES COMERCIALES", "Email Swipe", "File Pro",
         "✓ 40+ Guiones Listos para Copiar", "Reclamar Facturas Impagadas:", "Cobro en 48 Horas", "9 €", "Guía Interactiva HTML"),

        # --- ENGLISH THUMBNAILS ---
        # 1. Finance Hub EN
        ("thumb_finance_hub_en", (30, 27, 75), (15, 23, 42), (79, 70, 229),
         "FINANCIAL SYSTEM", "Freelance", "Finance Hub",
         "✓ Auto Revenue, Expenses & Taxes", "Annual Tax Estimation:", "100% Macro-Free", "$9", "Google Sheets & Excel"),
        
        # 2. Client CRM EN
        ("thumb_client_crm_en", (15, 23, 42), (2, 6, 23), (37, 99, 235),
         "SALES & PIPELINE", "Freelance", "Client CRM",
         "✓ Visual Kanban & Lead Directory", "Active Deals Tracker:", "No Monthly SaaS Fees", "$9", "Google Sheets & Excel"),
        
        # 3. Tax Checklist EN
        ("thumb_tax_checklist_en", (6, 78, 59), (15, 23, 42), (16, 185, 129),
         "FREE STARTER KIT", "Invoicing & Tax", "Compliance Kit",
         "✓ 7 Mandatory Invoice Rules", "Audit Prevention & Deductions:", "Zero-Fines Checklist", "$0 FREE", "PDF + Interactive HTML"),
        
        # 4. All-in-One Pack EN
        ("thumb_bundle_all_in_one_en", (17, 24, 39), (49, 46, 129), (245, 158, 11),
         "8-IN-1 SUITE BUNDLE", "All-in-One", "Freelance Suite",
         "✓ All 8 Systems Included", "Direct Bundle Savings:", "Save >45% ($72 Value)", "$39", "8 Spreadsheets + Web"),
        
        # 5. Quote Calculator EN
        ("thumb_quote_calculator_en", (19, 78, 74), (15, 23, 42), (13, 148, 136),
         "PRICING & QUOTES", "Project Quote", "Estimator Pro",
         "✓ Built-in Risk Buffers (+20%)", "Hourly & Scope Pricing:", "Never Work at a Loss", "$9", "Google Sheets & Excel"),
        
        # 6. Reseller Tracker EN
        ("thumb_reseller_tracker_en", (154, 52, 18), (15, 23, 42), (234, 88, 12),
         "E-COMMERCE & RESALE", "Reseller", "Profit Tracker",
         "✓ Auto Fee Deductions (eBay/Vinted)", "Inventory & COGS Tracking:", "Net Margin & ROI Alerts", "$9", "Google Sheets & Excel"),
        
        # 7. Content Planner EN
        ("thumb_content_planner_en", (88, 28, 135), (15, 23, 42), (147, 51, 234),
         "CREATOR TOOLS", "Social Media", "Content Planner",
         "✓ 50+ High-Retention Hook Bank", "Multi-Platform Calendar:", "TikTok / IG / LinkedIn / X", "$9", "Google Sheets & Excel"),
        
        # 8. Budget 50/30/20 EN
        ("thumb_budget_503020_en", (136, 19, 55), (15, 23, 42), (225, 29, 72),
         "PERSONAL FINANCE", "50/30/20 Budget", "& Debt Snowball",
         "✓ Rapid Debt Snowball Method", "Monthly Paycheck Manager:", "Debt-Free Roadmap", "$9", "Google Sheets & Excel"),
        
        # 9. Email Swipe File EN
        ("thumb_email_swipe_en", (6, 78, 59), (15, 23, 42), (16, 185, 129),
         "NEGOTIATION SCRIPTS", "Email Swipe", "File Pro",
         "✓ 40+ Battle-Tested Pitch Scripts", "Overdue Invoices & Rate Hikes:", "Word-for-Word Templates", "$9", "Interactive HTML Guide")
    ]

    for t in thumbnails:
        create_square_thumbnail(*t)

if __name__ == "__main__":
    main()
