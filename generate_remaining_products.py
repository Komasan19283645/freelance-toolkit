import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import base64
import os

out_dir = r"C:\Users\Miguel\.gemini\antigravity\scratch\freelance-toolkit-saas\entregables"
os.makedirs(out_dir, exist_ok=True)

header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
title_font = Font(name="Calibri", size=15, bold=True, color="1E1B4B")
subtitle_font = Font(name="Calibri", size=10, italic=True, color="6B7280")
bold_font = Font(name="Calibri", size=11, bold=True)
thin_border = Border(left=Side(style='thin', color='E5E7EB'), right=Side(style='thin', color='E5E7EB'), top=Side(style='thin', color='E5E7EB'), bottom=Side(style='thin', color='E5E7EB'))
total_border = Border(top=Side(style='thin', color='111827'), bottom=Side(style='double', color='111827'))

# ==============================================================================
# PRODUCTO 4: 50/30/20 PERSONAL BUDGET & DEBT SNOWBALL TRACKER
# ==============================================================================
def create_budget_503020():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "📊 Presupuesto 50-30-20"
    ws.views.sheetView[0].showGridLines = True
    
    ws["B2"] = "PLANIFICADOR FINANCIERO 50/30/20 & CONTROL DE GASTOS"
    ws["B2"].font = title_font
    ws["B3"] = "Regla 50% Necesidades | 30% Deseos | 20% Ahorro e Inversión"
    ws["B3"].font = subtitle_font

    headers = ["Categoría 50/30/20", "Concepto de Gasto", "Presupuestado (€)", "Gasto Real (€)", "Diferencia (€)", "Estado"]
    fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
    for c_idx, h in enumerate(headers, start=2):
        cell = ws.cell(row=5, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = fill
        cell.alignment = Alignment(horizontal="center" if "Estado" in h else "left")

    sample_data = [
        ("50% Necesidad", "Alquiler / Hipoteca", 850, 850, "=C6-D6", "OK"),
        ("50% Necesidad", "Supermercado y comida", 350, 320, "=C7-D7", "Bajo presupuesto"),
        ("50% Necesidad", "Luz, Agua, Internet", 140, 155, "=C8-D8", "Excedido"),
        ("30% Deseos", "Restaurantes y ocio", 200, 180, "=C9-D9", "OK"),
        ("30% Deseos", "Suscripciones (Netflix/Gym)", 60, 60, "=C10-D10", "OK"),
        ("20% Ahorro/Deuda", "Fondo de Emergencia", 300, 300, "=C11-D11", "Completado"),
        ("20% Ahorro/Deuda", "Plan Amortización Deuda", 150, 150, "=C12-D12", "Completado")
    ]
    for r_idx, row in enumerate(sample_data, start=6):
        for c_idx, val in enumerate(row, start=2):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.border = thin_border
            if c_idx in [4, 5, 6]:
                cell.number_format = "#,##0.00 €"

    # Hoja de deudas
    ws_debt = wb.create_sheet(title="❄️ Calculadora Bola de Nieve")
    ws_debt.views.sheetView[0].showGridLines = True
    ws_debt["B2"] = "MÉTODO BOLA DE NIEVE: PLAN DE LIQUIDACIÓN DE DEUDAS"
    ws_debt["B2"].font = title_font
    debt_headers = ["Nombre Deuda", "Saldo Pendiente (€)", "Tipo Interés (%)", "Cuota Mínima (€)", "Pago Extra (€)", "Meses Estimados"]
    fill_debt = PatternFill(start_color="DC2626", end_color="DC2626", fill_type="solid")
    for c_idx, h in enumerate(debt_headers, start=2):
        cell = ws_debt.cell(row=4, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = fill_debt

    sample_debts = [
        ("Tarjeta de Crédito", 1200, 18.5, 60, 100, "=ROUNDUP(C5/(E5+F5),0)"),
        ("Préstamo Coche", 4500, 6.5, 140, 0, "=ROUNDUP(C6/(E6+F6),0)"),
        ("Financiación Portátil", 650, 0.0, 65, 0, "=ROUNDUP(C7/(E7+F7),0)")
    ]
    for r_idx, row in enumerate(sample_debts, start=5):
        for c_idx, val in enumerate(row, start=2):
            cell = ws_debt.cell(row=r_idx, column=c_idx, value=val)
            cell.border = thin_border
            if c_idx in [3, 5, 6]:
                cell.number_format = "#,##0.00 €"
            elif c_idx == 4:
                cell.number_format = "0.0\"%\""

    for sheet in [ws, ws_debt]:
        for col in sheet.columns:
            sheet.column_dimensions[get_column_letter(col[0].column)].width = 22

    path = os.path.join(out_dir, "Personal_Budget_50_30_20_2026.xlsx")
    wb.save(path)
    with open(path.replace(".xlsx", ".b64.txt"), "w") as f:
        f.write(base64.b64encode(open(path, "rb").read()).decode("utf-8"))
    print("Creado Producto 4:", path)

# ==============================================================================
# PRODUCTO 5: ULTIMATE HABIT TRACKER GAMIFICADO
# ==============================================================================
def create_habit_tracker():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "🔥 Hábitos Diarios"
    ws.views.sheetView[0].showGridLines = True
    ws["B2"] = "ULTIMATE HABIT TRACKER 2026"
    ws["B2"].font = title_font
    ws["B3"] = "Construye hábitos atómicos con seguimiento de racha y porcentaje de éxito"
    ws["B3"].font = subtitle_font

    headers = ["Hábito / Rutina", "Categoría", "Objetivo", "L", "M", "X", "J", "V", "S", "D", "% Cumplido", "Racha Actual"]
    fill = PatternFill(start_color="047857", end_color="047857", fill_type="solid")
    for c_idx, h in enumerate(headers, start=2):
        cell = ws.cell(row=5, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = fill
        cell.alignment = Alignment(horizontal="center")

    sample_habits = [
        ("Leer 20 minutos", "Mente", "Diario", 1, 1, 1, 1, 1, 0, 1, "=SUM(E6:K6)/7", "6 días"),
        ("Entrenamiento / Gym", "Salud", "4x / semana", 1, 0, 1, 0, 1, 1, 0, "=SUM(E7:K7)/4", "4 días"),
        ("Beber 2.5L de agua", "Salud", "Diario", 1, 1, 1, 1, 1, 1, 1, "=SUM(E8:K8)/7", "18 días"),
        ("Bloque de Deep Work 2h", "Productividad", "Lun-Vie", 1, 1, 1, 1, 1, 0, 0, "=SUM(E9:K9)/5", "5 días"),
        ("Planificar día siguiente", "Organización", "Diario", 1, 1, 1, 1, 0, 0, 1, "=SUM(E10:K10)/7", "1 día")
    ]
    for r_idx, row in enumerate(sample_habits, start=6):
        for c_idx, val in enumerate(row, start=2):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.border = thin_border
            cell.alignment = Alignment(horizontal="center" if c_idx >= 5 else "left")
            if c_idx == 12:
                cell.number_format = "0.0%"

    for col in ws.columns:
        ws.column_dimensions[get_column_letter(col[0].column)].width = 16
    ws.column_dimensions["B"].width = 28

    path = os.path.join(out_dir, "Ultimate_Habit_Tracker_2026.xlsx")
    wb.save(path)
    with open(path.replace(".xlsx", ".b64.txt"), "w") as f:
        f.write(base64.b64encode(open(path, "rb").read()).decode("utf-8"))
    print("Creado Producto 5:", path)

# ==============================================================================
# PRODUCTO 6: SOCIAL MEDIA CONTENT PLANNER 2026
# ==============================================================================
def create_content_planner():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "📅 Calendario Editorial"
    ws.views.sheetView[0].showGridLines = True
    ws["B2"] = "SOCIAL MEDIA & CONTENT PLANNER 2026"
    ws["B2"].font = title_font
    ws["B3"] = "Planificador estratégico de publicaciones, guiones, formatos y métricas"
    ws["B3"].font = subtitle_font

    headers = ["Fecha Pub.", "Canal", "Pilar de Contenido", "Título / Gancho Principal", "Formato", "Estado", "Enlace / Borrador", "Visualizaciones", "Interacciones"]
    fill = PatternFill(start_color="7C3AED", end_color="7C3AED", fill_type="solid")
    for c_idx, h in enumerate(headers, start=2):
        cell = ws.cell(row=5, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = fill

    sample_content = [
        ("2026-03-01", "LinkedIn", "Consejo Profesional", "El error que comete el 90% de autónomos al fijar precios", "Post Texto", "Publicado", "https://linkedin.com/...", 4200, 185),
        ("2026-03-03", "TikTok", "Tutorial Rápido", "Cómo calculo mi IRPF en 15 segundos con esta plantilla", "Vídeo Vertical", "Programado", "Borrador guardado", 0, 0),
        ("2026-03-05", "Twitter/X", "Caso de Estudio", "Cómo pase de facturar 1.200€ a 3.500€/mes cambiando mi propuesta", "Hilo", "Borrador", "Notas Notion", 0, 0),
        ("2026-03-08", "Instagram", "Educativo", "Infografía: 5 gastos deducibles que tu gestor no te cuenta", "Carrusel", "En Diseño", "Figma", 0, 0)
    ]
    for r_idx, row in enumerate(sample_content, start=6):
        for c_idx, val in enumerate(row, start=2):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.border = thin_border
            if c_idx in [9, 10]:
                cell.number_format = "#,##0"

    for col in ws.columns:
        ws.column_dimensions[get_column_letter(col[0].column)].width = 20
    ws.column_dimensions["E"].width = 36

    path = os.path.join(out_dir, "Social_Media_Content_Planner_2026.xlsx")
    wb.save(path)
    with open(path.replace(".xlsx", ".b64.txt"), "w") as f:
        f.write(base64.b64encode(open(path, "rb").read()).decode("utf-8"))
    print("Creado Producto 6:", path)

# ==============================================================================
# PRODUCTO 7: E-COMMERCE & RESELLING PROFIT TRACKER
# ==============================================================================
def create_reseller_tracker():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "📦 Control de Ventas & P&L"
    ws.views.sheetView[0].showGridLines = True
    ws["B2"] = "E-COMMERCE & RESELLING PROFIT TRACKER"
    ws["B2"].font = title_font
    ws["B3"] = "Calculadora neta de beneficios para Wallapop, Vinted, eBay, Amazon y Shopify"
    ws["B3"].font = subtitle_font

    headers = ["Fecha", "Artículo / Producto", "Plataforma", "Precio Compra (€)", "Precio Venta (€)", "Comisión Plataforma (€)", "Envío/Costes (€)", "Beneficio Neto (€)", "% Margen"]
    fill = PatternFill(start_color="D97706", end_color="D97706", fill_type="solid")
    for c_idx, h in enumerate(headers, start=2):
        cell = ws.cell(row=5, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = fill

    sample_items = [
        ("2026-02-15", "Cámara Vintage 35mm", "Wallapop", 25.00, 75.00, 3.75, 4.50, "=F6-E6-G6-H6", "=I6/F6"),
        ("2026-02-18", "Chaqueta Cuero Retro", "Vinted", 15.00, 48.00, 0.00, 2.50, "=F7-E7-G7-H7", "=I7/F7"),
        ("2026-02-22", "Auriculares Inalámbricos", "Amazon", 32.00, 79.90, 11.98, 5.00, "=F8-E8-G8-H8", "=I8/F8")
    ]
    for r_idx, row in enumerate(sample_items, start=6):
        for c_idx, val in enumerate(row, start=2):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.border = thin_border
            if c_idx in [5, 6, 7, 8, 9]:
                cell.number_format = "#,##0.00 €"
            elif c_idx == 10:
                cell.number_format = "0.0%"

    for col in ws.columns:
        ws.column_dimensions[get_column_letter(col[0].column)].width = 20
    ws.column_dimensions["C"].width = 28

    path = os.path.join(out_dir, "Ecommerce_Reseller_Profit_Tracker.xlsx")
    wb.save(path)
    with open(path.replace(".xlsx", ".b64.txt"), "w") as f:
        f.write(base64.b64encode(open(path, "rb").read()).decode("utf-8"))
    print("Creado Producto 7:", path)

# ==============================================================================
# PRODUCTO 8: FREELANCE PROJECT PRICING & QUOTE CALCULATOR
# ==============================================================================
def create_quote_calculator():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "💼 Cotizador de Presupuestos"
    ws.views.sheetView[0].showGridLines = True
    ws["B2"] = "CALCULADORA AVANZADA DE PRESUPUESTOS Y MARGEN"
    ws["B2"].font = title_font
    ws["B3"] = "Estima costes reales, horas, margen de imprevistos y beneficio comercial"
    ws["B3"].font = subtitle_font

    headers = ["Fase del Proyecto", "Horas Estimadas", "Tarifa/Hora (€)", "Coste Mano Obra (€)", "Costes Externos (€)", "Margen Imprevistos (15%)", "Precio Final Recomendado (€)"]
    fill = PatternFill(start_color="0F766E", end_color="0F766E", fill_type="solid")
    for c_idx, h in enumerate(headers, start=2):
        cell = ws.cell(row=5, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = fill

    sample_quote = [
        ("Fase 1: Análisis y Wireframes", 12, 45, "=C6*D6", 0, "=E6*0.15", "=E6+F6+G6"),
        ("Fase 2: Diseño UI en Figma", 20, 45, "=C7*D7", 50, "=(E7+F7)*0.15", "=E7+F7+G7"),
        ("Fase 3: Desarrollo Web Frontend", 35, 45, "=C8*D8", 120, "=(E8+F8)*0.15", "=E8+F8+G8"),
        ("Fase 4: Pruebas y Despliegue", 8, 45, "=C9*D9", 30, "=(E9+F9)*0.15", "=E9+F9+G9")
    ]
    for r_idx, row in enumerate(sample_quote, start=6):
        for c_idx, val in enumerate(row, start=2):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.border = thin_border
            if c_idx in [4, 5, 6, 7, 8]:
                cell.number_format = "#,##0.00 €"

    for col in ws.columns:
        ws.column_dimensions[get_column_letter(col[0].column)].width = 22
    ws.column_dimensions["B"].width = 30

    path = os.path.join(out_dir, "Freelance_Project_Quote_Calculator.xlsx")
    wb.save(path)
    with open(path.replace(".xlsx", ".b64.txt"), "w") as f:
        f.write(base64.b64encode(open(path, "rb").read()).decode("utf-8"))
    print("Creado Producto 8:", path)

if __name__ == "__main__":
    create_budget_503020()
    create_habit_tracker()
    create_content_planner()
    create_reseller_tracker()
    create_quote_calculator()
