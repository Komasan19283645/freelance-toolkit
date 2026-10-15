import base64
import os
from PIL import Image, ImageDraw, ImageFont

def get_font(size, bold=False):
    # Intentar cargar fuentes del sistema Windows
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

def create_cover(filename, bg_start, bg_end, accent_color, category_tag, title, subtitle, bullets, badge_text):
    W, H = 1280, 720
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)

    # 1. Fondo degradado profesional
    draw_gradient(draw, W, H, bg_start, bg_end)

    # 2. Rejilla sutil de fondo
    grid_color = (255, 255, 255, 12)
    for x in range(0, W, 40):
        draw.line([(x, 0), (x, H)], fill=(255, 255, 255, 15), width=1)
    for y in range(0, H, 40):
        draw.line([(0, y), (W, y)], fill=(255, 255, 255, 15), width=1)

    # 3. Tarjeta central de contenido (Estilo Glassmorphism)
    card_margin_x = 80
    card_margin_y = 60
    card_w = W - (card_margin_x * 2)
    card_h = H - (card_margin_y * 2)
    
    # Sombra de la tarjeta
    draw.rounded_rectangle(
        [(card_margin_x + 8, card_margin_y + 8), (card_margin_x + card_w + 8, card_margin_y + card_h + 8)],
        radius=24, fill=(5, 5, 15)
    )
    # Cuerpo de la tarjeta
    draw.rounded_rectangle(
        [(card_margin_x, card_margin_y), (card_margin_x + card_w, card_margin_y + card_h)],
        radius=24, fill=(17, 24, 39), outline=(55, 65, 81), width=2
    )

    # 4. Badge superior izquierdo (Categoría)
    font_badge = get_font(18, bold=True)
    draw.rounded_rectangle([(card_margin_x + 50, card_margin_y + 50), (card_margin_x + 280, card_margin_y + 90)], radius=12, fill=accent_color)
    draw.text((card_margin_x + 65, card_margin_y + 58), category_tag, font=font_badge, fill=(255, 255, 255))

    # Badge superior derecho (Edición 2026)
    draw.rounded_rectangle([(card_margin_x + card_w - 200, card_margin_y + 50), (card_margin_x + card_w - 50, card_margin_y + 90)], radius=12, fill=(31, 41, 55), outline=(75, 85, 99), width=1)
    draw.text((card_margin_x + card_w - 180, card_margin_y + 58), "EDICIÓN 2026", font=font_badge, fill=(209, 213, 219))

    # 5. Título Principal
    font_title = get_font(52, bold=True)
    draw.text((card_margin_x + 50, card_margin_y + 120), title, font=font_title, fill=(255, 255, 255))

    # 6. Subtítulo
    font_sub = get_font(24, bold=False)
    draw.text((card_margin_x + 50, card_margin_y + 195), subtitle, font=font_sub, fill=(156, 163, 175))

    # Línea divisoria
    draw.line([(card_margin_x + 50, card_margin_y + 250), (card_margin_x + card_w - 50, card_margin_y + 250)], fill=(55, 65, 81), width=1)

    # 7. Viñetas de características (Bullets)
    font_bullets = get_font(22, bold=True)
    start_bullet_y = card_margin_y + 290
    for i, bullet in enumerate(bullets):
        by = start_bullet_y + (i * 55)
        # Checkmark icon box
        draw.rounded_rectangle([(card_margin_x + 50, by - 4), (card_margin_x + 82, by + 28)], radius=8, fill=accent_color)
        draw.text((card_margin_x + 58, by), "✓", font=get_font(20, bold=True), fill=(255, 255, 255))
        draw.text((card_margin_x + 100, by), bullet, font=font_bullets, fill=(243, 244, 246))

    # 8. Elemento visual mockup a la derecha (Tarjeta flotante de métrica)
    mock_x = card_margin_x + card_w - 380
    mock_y = card_margin_y + 280
    draw.rounded_rectangle([(mock_x, mock_y), (mock_x + 330, mock_y + 260)], radius=16, fill=(31, 41, 55), outline=(75, 85, 99), width=2)
    
    # Cabecera de la mini tarjeta
    draw.rounded_rectangle([(mock_x, mock_y), (mock_x + 330, mock_y + 50)], radius=16, fill=(55, 65, 81))
    draw.text((mock_x + 20, mock_y + 15), "VISTA PREVIA ACTIVA", font=get_font(16, bold=True), fill=(229, 231, 235))
    
    # Contenido mini tarjeta
    draw.text((mock_x + 25, mock_y + 75), "Formato:", font=get_font(15, bold=False), fill=(156, 163, 175))
    draw.text((mock_x + 25, mock_y + 100), badge_text, font=get_font(20, bold=True), fill=accent_color)
    
    draw.text((mock_x + 25, mock_y + 145), "Compatibilidad:", font=get_font(15, bold=False), fill=(156, 163, 175))
    draw.text((mock_x + 25, mock_y + 170), "Google Sheets & Excel", font=get_font(18, bold=True), fill=(255, 255, 255))
    
    draw.rounded_rectangle([(mock_x + 20, mock_y + 210), (mock_x + 310, mock_y + 245)], radius=8, fill=(16, 185, 129))
    draw.text((mock_x + 75, mock_y + 218), "✓ LISTO PARA USAR", font=get_font(14, bold=True), fill=(255, 255, 255))

    # Guardar imagen PNG
    out_dir = r"C:\Users\Miguel\.gemini\antigravity\scratch\freelance-toolkit-saas\entregables"
    out_png = os.path.join(out_dir, filename + ".png")
    out_b64 = os.path.join(out_dir, filename + ".b64.txt")
    
    img.save(out_png, "PNG", quality=95)
    
    # Guardar base64
    with open(out_png, "rb") as f:
        b64_str = base64.b64encode(f.read()).decode("utf-8")
    with open(out_b64, "w") as f:
        f.write(b64_str)

    print(f"Generado {out_png} y {out_b64}")

def main():
    # 1. Cover Finance Hub
    create_cover(
        filename="cover_finance_hub",
        bg_start=(30, 27, 75),      # Indigo oscuro
        bg_end=(15, 23, 42),        # Slate profundo
        accent_color=(79, 70, 229), # Indigo eléctrico
        category_tag="PLANTILLA FINANCIERA",
        title="Freelance Finance Hub",
        subtitle="Control automático de ingresos, gastos, IVA e IRPF trimestral.",
        bullets=[
            "Dashboard Anual con métricas y gráficos visuales",
            "Cálculo automático de retenciones de IRPF e IVA",
            "Previsión de impuestos (Hacienda sin sorpresas)",
            "Acceso en la nube desde PC, tablet o móvil"
        ],
        badge_text="Hoja de Cálculo .XLSX"
    )

    # 2. Cover Client CRM
    create_cover(
        filename="cover_client_crm",
        bg_start=(15, 23, 42),       # Dark Slate
        bg_end=(2, 6, 23),          # Casi negro
        accent_color=(37, 99, 235),  # Azul Real
        category_tag="SISTEMA COMERCIAL CRM",
        title="Freelance Client CRM",
        subtitle="Gestiona tus clientes, presupuestos y proyectos sin pagar cuotas.",
        bullets=[
            "Pipeline de ventas y estado de propuestas",
            "Ficha unificada de clientes y datos fiscales",
            "Gestor de proyectos en curso y entregas",
            "Control de facturación histórica y notas"
        ],
        badge_text="Sistema CRM en Sheets"
    )

    # 3. Cover Email Swipe File
    create_cover(
        filename="cover_email_swipe",
        bg_start=(6, 78, 59),        # Esmeralda profundo
        bg_end=(15, 23, 42),        # Slate
        accent_color=(16, 185, 129),# Esmeralda brillante
        category_tag="GUIONES COMERCIALES",
        title="Email Swipe File Pro",
        subtitle="40+ guiones probados de negociación, captación y cobro de facturas.",
        bullets=[
            "Emails de contacto en frío con alta tasa de respuesta",
            "Cadencia de 4 pasos para cobrar facturas atrasadas",
            "Fórmula para subir tarifas sin perder clientes",
            "Guía interactiva lista para copiar y personalizar"
        ],
        badge_text="Biblioteca Digital HTML"
    )

    # 4. Cover Personal Budget 50/30/20
    create_cover(
        filename="cover_budget_503020",
        bg_start=(136, 19, 55),      # Rose / Borgoña
        bg_end=(15, 23, 42),         # Slate profundo
        accent_color=(225, 29, 72),  # Rose brillante
        category_tag="FINANZAS PERSONALES",
        title="Presupuesto 50/30/20 & Deuda",
        subtitle="Control de gastos mensuales y plan de amortización Bola de Nieve.",
        bullets=[
            "Distribución automática: 50% Necesidades, 30% Deseos, 20% Ahorro",
            "Calculadora de amortización acelerada de deudas",
            "Alertas visuales de desviación presupuestaria",
            "Planificador de fondo de emergencia integrado"
        ],
        badge_text="Hoja de Cálculo .XLSX"
    )

    # 5. Cover Habit Tracker
    create_cover(
        filename="cover_habit_tracker",
        bg_start=(120, 53, 15),      # Amber / Marrón cálido
        bg_end=(15, 23, 42),         # Slate profundo
        accent_color=(217, 119, 6),  # Ámbar dorado
        category_tag="PRODUCTIVIDAD Y RUTINAS",
        title="Ultimate Habit Tracker",
        subtitle="Seguimiento de hábitos diarios gamificado con barras de progreso y rachas.",
        bullets=[
            "Matriz visual de seguimiento mensual y diario",
            "Cálculo automático de % de cumplimiento y rachas",
            "Cuadrícula de evaluación semanal de rendimiento",
            "Compatible con Google Sheets y Excel sin macros"
        ],
        badge_text="Hoja de Cálculo .XLSX"
    )

    # 6. Cover Social Media Content Planner
    create_cover(
        filename="cover_content_planner",
        bg_start=(88, 28, 135),      # Púrpura intenso
        bg_end=(15, 23, 42),         # Slate profundo
        accent_color=(147, 51, 234), # Púrpura neón
        category_tag="CREADORES Y MARKETING",
        title="Social Media Content Planner",
        subtitle="Planifica tus contenidos en TikTok, LinkedIn e Instagram con métricas.",
        bullets=[
            "Calendario editorial con estados de publicación",
            "Banco de ganchos (Hooks) y llamadas a la acción (CTA)",
            "Control de alcance, impresiones y tasa de conversión",
            "Organizador de assets, copys y enlaces listos"
        ],
        badge_text="Hoja de Cálculo .XLSX"
    )

    # 7. Cover Reseller Profit Tracker
    create_cover(
        filename="cover_reseller_tracker",
        bg_start=(154, 52, 18),      # Naranja quemado
        bg_end=(15, 23, 42),         # Slate profundo
        accent_color=(234, 88, 12),  # Naranja brillante
        category_tag="E-COMMERCE Y REVENTA",
        title="Reseller Profit Tracker",
        subtitle="Control de ventas y comisiones para Wallapop, Vinted y Amazon.",
        bullets=[
            "Cálculo automático de comisiones de plataforma y envíos",
            "Margen neto y ROI por cada artículo vendido",
            "Control de inventario en almacén y compras pendientes",
            "Resumen mensual de beneficio neto y facturación"
        ],
        badge_text="Hoja de Cálculo .XLSX"
    )

    # 8. Cover Quote Calculator
    create_cover(
        filename="cover_quote_calculator",
        bg_start=(19, 78, 74),       # Verde azulado oscuro
        bg_end=(15, 23, 42),         # Slate profundo
        accent_color=(13, 148, 136), # Teal brillante
        category_tag="COTIZADOR COMERCIAL",
        title="Calculadora de Presupuestos",
        subtitle="Calcula precios por hora, márgenes de contingencia y precio final infalible.",
        bullets=[
            "Desglose por fases, horas estimadas y coste/hora base",
            "Margen de seguridad por imprevistos (+15% a +30%)",
            "Generador automático de resumen para propuesta formal",
            "Evita presupuestos a la baja y proyectos a pérdidas"
        ],
        badge_text="Hoja de Cálculo .XLSX"
    )

    # 9. Cover All-in-One Pack (Bundle Completo 8 Sistemas)
    create_cover(
        filename="cover_bundle_all_in_one",
        bg_start=(17, 24, 39),        # Slate casi negro
        bg_end=(49, 46, 129),         # Indigo noche
        accent_color=(245, 158, 11),  # Oro / Ámbar brillante
        category_tag="SUITE COMPLETA (8 EN 1)",
        title="All-in-One Freelance Pack",
        subtitle="Colección completa de 8 sistemas profesionales con un 40% de descuento.",
        bullets=[
            "Incluye Finance Hub, Client CRM y Email Swipe File",
            "Presupuesto 50/30/20, Habit Tracker y Content Planner",
            "Calculadoras de E-Commerce y Cotizador de Proyectos",
            "Acceso inmediato a los 8 archivos y actualizaciones"
        ],
        badge_text="Pack Completo (8 Sistemas)"
    )

if __name__ == "__main__":
    main()


