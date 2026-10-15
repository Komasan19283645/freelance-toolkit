import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule
import base64
import os

out_dir = r"C:\Users\Miguel\.gemini\antigravity\scratch\freelance-toolkit-saas\entregables"
os.makedirs(out_dir, exist_ok=True)

# Tipografías y paletas de nivel corporativo
title_font = Font(name="Segoe UI", size=15, bold=True, color="0F172A")
subtitle_font = Font(name="Segoe UI", size=9, italic=True, color="64748B")
header_font = Font(name="Segoe UI", size=10, bold=True, color="FFFFFF")
bold_font = Font(name="Segoe UI", size=10, bold=True, color="0F172A")
regular_font = Font(name="Segoe UI", size=10, color="1E293B")
kpi_label_font = Font(name="Segoe UI", size=9, bold=True, color="475569")
kpi_val_font = Font(name="Segoe UI", size=18, bold=True, color="0F172A")

thin_border = Border(
    left=Side(style='thin', color='E2E8F0'),
    right=Side(style='thin', color='E2E8F0'),
    top=Side(style='thin', color='E2E8F0'),
    bottom=Side(style='thin', color='E2E8F0')
)
total_border = Border(
    top=Side(style='thin', color='0F172A'),
    bottom=Side(style='double', color='0F172A')
)

# Colores de formato condicional (Pasteles limpios)
green_fill = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
green_font = Font(name="Segoe UI", size=10, color="166534", bold=True)

red_fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
red_font = Font(name="Segoe UI", size=10, color="991B1B", bold=True)

blue_fill = PatternFill(start_color="DBEAFE", end_color="DBEAFE", fill_type="solid")
blue_font = Font(name="Segoe UI", size=10, color="1E40AF", bold=True)

amber_fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")
amber_font = Font(name="Segoe UI", size=10, color="92400E", bold=True)

purple_fill = PatternFill(start_color="F3E8FF", end_color="F3E8FF", fill_type="solid")
purple_font = Font(name="Segoe UI", size=10, color="6B21A8", bold=True)


# ==============================================================================
# 1. UPGRADE FINANCE HUB
# ==============================================================================
def upgrade_finance_hub():
    wb = openpyxl.Workbook()
    
    # Hoja 1: Dashboard
    ws_dash = wb.active
    ws_dash.title = "📊 Dashboard Anual"
    ws_dash.views.sheetView[0].showGridLines = True
    ws_dash["B2"] = "FREELANCE FINANCE HUB 2026"
    ws_dash["B2"].font = title_font
    ws_dash["B3"] = "Control fiscal y financiero para autónomos y freelancers en España"
    ws_dash["B3"].font = subtitle_font

    kpis = [
        ("B5", "INGRESOS TOTALES (BASE)", "=SUM('💰 Ingresos'!E5:E100)"),
        ("E5", "GASTOS TOTALES (BASE)", "=SUM('📉 Gastos'!E5:E100)"),
        ("H5", "BENEFICIO NETO ANTES IMPUESTOS", "=B6-E6"),
        ("K5", "PREVISIÓN IVA A PAGAR (HACIENDA)", "=SUM('💰 Ingresos'!G5:G100)-SUM('📉 Gastos'!F5:F100)")
    ]
    for col_start, label, formula in kpis:
        c_label = ws_dash[col_start]
        row_num = int(col_start[1:])
        col_letter = col_start[0]
        c_val = ws_dash[f"{col_letter}{row_num+1}"]
        
        c_label.value = label
        c_label.font = kpi_label_font
        c_val.value = formula
        c_val.font = kpi_val_font
        c_val.number_format = "#,##0.00 €"
        
        c2_letter = chr(ord(col_letter)+1)
        ws_dash.merge_cells(f"{col_start}:{c2_letter}{row_num}")
        ws_dash.merge_cells(f"{col_letter}{row_num+1}:{c2_letter}{row_num+1}")
        
        # Fondo sutil de tarjeta
        fill_card = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
        for r in range(row_num, row_num+2):
            for c in [col_letter, c2_letter]:
                ws_dash[f"{c}{r}"].fill = fill_card
                ws_dash[f"{c}{r}"].border = thin_border

    # Tabla resumen mensual
    headers_dash = ["Mes", "Ingresos Brutos", "Gastos Totales", "Beneficio Neto", "IVA Repercutido", "IVA Soportado"]
    for idx, h in enumerate(headers_dash, start=2):
        c = ws_dash.cell(row=9, column=idx, value=h)
        c.font = header_font
        c.fill = PatternFill(start_color="312E81", end_color="312E81", fill_type="solid") # Indigo profundo
        c.alignment = Alignment(horizontal="center" if idx==2 else "right")

    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    for i, m in enumerate(meses, start=10):
        ws_dash[f"B{i}"] = m
        ws_dash[f"B{i}"].font = regular_font
        ws_dash[f"B{i}"].border = thin_border
        
        ws_dash[f"C{i}"] = f"=SUMIFS('💰 Ingresos'!E:E, '💰 Ingresos'!A:A, \">=\"&DATE(2026,{i-9},1), '💰 Ingresos'!A:A, \"<=\"&EOMONTH(DATE(2026,{i-9},1),0))"
        ws_dash[f"D{i}"] = f"=SUMIFS('📉 Gastos'!E:E, '📉 Gastos'!A:A, \">=\"&DATE(2026,{i-9},1), '📉 Gastos'!A:A, \"<=\"&EOMONTH(DATE(2026,{i-9},1),0))"
        ws_dash[f"E{i}"] = f"=C{i}-D{i}"
        ws_dash[f"F{i}"] = f"=SUMIFS('💰 Ingresos'!G:G, '💰 Ingresos'!A:A, \">=\"&DATE(2026,{i-9},1), '💰 Ingresos'!A:A, \"<=\"&EOMONTH(DATE(2026,{i-9},1),0))"
        ws_dash[f"G{i}"] = f"=SUMIFS('📉 Gastos'!F:F, '📉 Gastos'!A:A, \">=\"&DATE(2026,{i-9},1), '📉 Gastos'!A:A, \"<=\"&EOMONTH(DATE(2026,{i-9},1),0))"
        
        for col in ["C", "D", "E", "F", "G"]:
            cell = ws_dash[f"{col}{i}"]
            cell.font = regular_font
            cell.number_format = "#,##0.00 €"
            cell.border = thin_border

    # Fila de Totales
    ws_dash["B22"] = "TOTAL ANUAL"
    ws_dash["B22"].font = bold_font
    ws_dash["B22"].border = total_border
    for col in ["C", "D", "E", "F", "G"]:
        c = ws_dash[f"{col}22"]
        c.value = f"=SUM({col}10:{col}21)"
        c.font = bold_font
        c.number_format = "#,##0.00 €"
        c.border = total_border

    # Formato condicional en Beneficio Neto: Verde si > 0, Rojo si < 0
    ws_dash.conditional_formatting.add("E10:E21", CellIsRule(operator='greaterThan', formula=['0'], stopIfTrue=True, fill=green_fill, font=green_font))
    ws_dash.conditional_formatting.add("E10:E21", CellIsRule(operator='lessThan', formula=['0'], stopIfTrue=True, fill=red_fill, font=red_font))

    # Hoja 2: Ingresos
    ws_ing = wb.create_sheet(title="💰 Ingresos")
    ws_ing.views.sheetView[0].showGridLines = True
    ws_ing["B2"] = "REGISTRO DE FACTURAS EMITIDAS"
    ws_ing["B2"].font = title_font
    
    headers_ing = ["Fecha", "Nº Factura", "Cliente", "Concepto", "Base Imponible (€)", "% IVA", "Cuota IVA (€)", "% IRPF", "Retención IRPF (€)", "Total Factura (€)"]
    for idx, h in enumerate(headers_ing, start=1):
        c = ws_ing.cell(row=4, column=idx, value=h)
        c.font = header_font
        c.fill = PatternFill(start_color="059669", end_color="059669", fill_type="solid") # Emerald
        c.alignment = Alignment(horizontal="center" if "Fecha" in h or "%" in h else "left")

    sample_ing = [
        ("2026-01-15", "FAC-2026-001", "Acme Corp S.L.", "Consultoría Estratégica Enero", 1500.00, 0.21, "=E5*F5", 0.15, "=E5*H5", "=E5+G5-I5"),
        ("2026-01-28", "FAC-2026-002", "Studio Design S.L.", "Desarrollo Web Frontend", 2200.00, 0.21, "=E6*F6", 0.15, "=E6*H6", "=E6+G6-I6"),
        ("2026-02-10", "FAC-2026-003", "Innovatech Europa", "Mantenimiento Mensual", 800.00, 0.21, "=E7*F7", 0.07, "=E7*H7", "=E7+G7-I7")
    ]
    for r_idx, row in enumerate(sample_ing, start=5):
        for c_idx, val in enumerate(row, start=1):
            cell = ws_ing.cell(row=r_idx, column=c_idx, value=val)
            cell.font = regular_font
            cell.border = thin_border
            if c_idx in [5, 7, 9, 10]:
                cell.number_format = "#,##0.00 €"
            elif c_idx in [6, 8]:
                cell.number_format = "0%"

    # Validación de datos desplegable para % IVA y % IRPF
    dv_iva = DataValidation(type="list", formula1='"21%,10%,4%,0%"', allow_blank=True)
    ws_ing.add_data_validation(dv_iva)
    dv_iva.add("F5:F100")

    dv_irpf = DataValidation(type="list", formula1='"15%,7%,0%"', allow_blank=True)
    ws_ing.add_data_validation(dv_irpf)
    dv_irpf.add("H5:H100")

    # Hoja 3: Gastos
    ws_gas = wb.create_sheet(title="📉 Gastos")
    ws_gas.views.sheetView[0].showGridLines = True
    ws_gas["B2"] = "REGISTRO DE GASTOS Y DEDUCCIONES"
    ws_gas["B2"].font = title_font

    headers_gas = ["Fecha", "Nº Factura / Ticket", "Proveedor", "Categoría Deducible", "Base Imponible (€)", "IVA Deducible (€)", "Total Pagado (€)"]
    for idx, h in enumerate(headers_gas, start=1):
        c = ws_gas.cell(row=4, column=idx, value=h)
        c.font = header_font
        c.fill = PatternFill(start_color="DC2626", end_color="DC2626", fill_type="solid") # Red
        c.alignment = Alignment(horizontal="center" if "Fecha" in h else "left")

    sample_gas = [
        ("2026-01-05", "EXP-01", "Seguridad Social", "Cuota Autónomos", 294.00, 0.00, 294.00),
        ("2026-01-10", "EXP-02", "Adobe Creative Cloud", "Software / SaaS", 62.99, 13.23, 76.22),
        ("2026-01-20", "EXP-03", "Asesoría Fiscal Online", "Gestoría / Legal", 75.00, 15.75, 90.75),
        ("2026-01-25", "EXP-04", "Vodafone Fibra", "Suministros (Luz/Internet)", 45.00, 9.45, 54.45)
    ]
    for r_idx, row in enumerate(sample_gas, start=5):
        for c_idx, val in enumerate(row, start=1):
            cell = ws_gas.cell(row=r_idx, column=c_idx, value=val)
            cell.font = regular_font
            cell.border = thin_border
            if c_idx in [5, 6, 7]:
                cell.number_format = "#,##0.00 €"

    # Desplegable de Categorías
    dv_cat = DataValidation(type="list", formula1='"Cuota Autónomos,Software / SaaS,Gestoría / Legal,Suministros (Luz/Internet),Material / Hardware,Marketing / Publicidad,Viajes / Dietas,Otros"', allow_blank=True)
    ws_gas.add_data_validation(dv_cat)
    dv_cat.add("D5:D100")

    # Ajuste automático de anchos
    for ws in [ws_dash, ws_ing, ws_gas]:
        for col in ws.columns:
            ws.column_dimensions[get_column_letter(col[0].column)].width = 20
    ws_dash.column_dimensions["B"].width = 18
    ws_ing.column_dimensions["D"].width = 30
    ws_gas.column_dimensions["C"].width = 25

    path = os.path.join(out_dir, "Freelance_Finance_Hub_2026.xlsx")
    wb.save(path)
    with open(path.replace(".xlsx", ".b64.txt"), "w") as f:
        f.write(base64.b64encode(open(path, "rb").read()).decode("utf-8"))
    print("Upgraded Finance Hub:", path)


# ==============================================================================
# 2. UPGRADE CLIENT CRM
# ==============================================================================
def upgrade_client_crm():
    wb = openpyxl.Workbook()
    ws_leads = wb.active
    ws_leads.title = "🎯 Pipeline de Ventas"
    ws_leads.views.sheetView[0].showGridLines = True

    ws_leads["B2"] = "FREELANCE CLIENT CRM & PIPELINE 2026"
    ws_leads["B2"].font = title_font
    ws_leads["B3"] = "Control comercial, seguimiento de oportunidades y directorio activo"
    ws_leads["B3"].font = subtitle_font

    headers_leads = ["Fecha Contacto", "Nombre Cliente", "Empresa / Marca", "Servicio Solicitado", "Valor Estimado (€)", "Estado Lead", "Probabilidad", "Próxima Acción", "Fecha Límite"]
    for c_idx, h in enumerate(headers_leads, start=1):
        cell = ws_leads.cell(row=5, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = PatternFill(start_color="1D4ED8", end_color="1D4ED8", fill_type="solid")
        cell.alignment = Alignment(horizontal="center" if "Fecha" in h or "Probabilidad" in h or "Estado" in h else "left")

    sample_leads = [
        ("2026-02-01", "Laura Gómez", "BioCosmetics S.L.", "Rediseño Tienda Shopify", 2200, "En Negociación", "80%", "Enviar contrato revisado", "2026-02-18"),
        ("2026-02-05", "Marcos Silva", "FitPro App", "Desarrollo Landing Page", 1400, "Propuesta Enviada", "60%", "Seguimiento por email", "2026-02-19"),
        ("2026-02-10", "Elena Rivas", "Consultoría Legal 360", "Auditoría SEO + Blog", 850, "Reunión Fijada", "40%", "Videollamada de descubrimiento", "2026-02-20"),
        ("2026-02-12", "Javier Soto", "Restaurante Gourmet", "Carta Digital QR + Web", 1100, "Ganado", "100%", "Facturar 50% de anticipo", "2026-02-16"),
        ("2026-02-14", "Carlos Peña", "Inmobiliaria Centro", "Campaña Publicitaria Ads", 600, "Perdido", "0%", "Sin presupuesto disponible", "2026-02-15")
    ]
    for r_idx, row in enumerate(sample_leads, start=6):
        for c_idx, val in enumerate(row, start=1):
            cell = ws_leads.cell(row=r_idx, column=c_idx, value=val)
            cell.font = regular_font
            cell.border = thin_border
            if c_idx == 5:
                cell.number_format = "#,##0.00 €"

    # Validación desplegable para Estado y Probabilidad
    dv_estado = DataValidation(type="list", formula1='"Ganado,En Negociación,Propuesta Enviada,Reunión Fijada,Nuevo Lead,Perdido"', allow_blank=True)
    ws_leads.add_data_validation(dv_estado)
    dv_estado.add("F6:F100")

    dv_prob = DataValidation(type="list", formula1='"100%,80%,60%,40%,20%,0%"', allow_blank=True)
    ws_leads.add_data_validation(dv_prob)
    dv_prob.add("G6:G100")

    # Formato condicional inteligente para Estados del Pipeline
    ws_leads.conditional_formatting.add("F6:F100", CellIsRule(operator='equal', formula=['"Ganado"'], stopIfTrue=True, fill=green_fill, font=green_font))
    ws_leads.conditional_formatting.add("F6:F100", CellIsRule(operator='equal', formula=['"En Negociación"'], stopIfTrue=True, fill=blue_fill, font=blue_font))
    ws_leads.conditional_formatting.add("F6:F100", CellIsRule(operator='equal', formula=['"Propuesta Enviada"'], stopIfTrue=True, fill=purple_fill, font=purple_font))
    ws_leads.conditional_formatting.add("F6:F100", CellIsRule(operator='equal', formula=['"Perdido"'], stopIfTrue=True, fill=red_fill, font=red_font))

    # Hoja 2: Directorio Clientes
    ws_clients = wb.create_sheet(title="👥 Directorio Clientes")
    ws_clients.views.sheetView[0].showGridLines = True
    headers_clients = ["Razón Social / Nombre", "Contacto Principal", "NIF / CIF", "Email", "Teléfono", "Ciudad", "Tarifa Acordada", "Total Facturado", "Estado Cliente", "Notas"]
    for c_idx, h in enumerate(headers_clients, start=1):
        cell = ws_clients.cell(row=4, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = PatternFill(start_color="6D28D9", end_color="6D28D9", fill_type="solid")

    sample_clients = [
        ("BioCosmetics S.L.", "Laura Gómez", "B87654321", "laura@biocosmetics.es", "+34 611 222 333", "Madrid", "45 €/hora", 4200, "Activo", "Reuniones martes"),
        ("Consultoría Legal 360", "Elena Rivas", "B12345678", "contacto@legal360.com", "+34 622 333 444", "Valencia", "50 €/hora", 1850, "Activo", "Puntuales en pago"),
        ("Restaurante Gourmet", "Javier Soto", "B99887766", "admin@gourmet.es", "+34 633 444 555", "Sevilla", "Precio cerrado", 2500, "Inactivo", "Proyecto entregado")
    ]
    for r_idx, row in enumerate(sample_clients, start=5):
        for c_idx, val in enumerate(row, start=1):
            cell = ws_clients.cell(row=r_idx, column=c_idx, value=val)
            cell.font = regular_font
            cell.border = thin_border
            if c_idx == 8:
                cell.number_format = "#,##0.00 €"

    dv_client_status = DataValidation(type="list", formula1='"Activo,En Pausa,Inactivo,Lead Potencial"', allow_blank=True)
    ws_clients.add_data_validation(dv_client_status)
    dv_client_status.add("I5:I100")
    ws_clients.conditional_formatting.add("I5:I100", CellIsRule(operator='equal', formula=['"Activo"'], stopIfTrue=True, fill=green_fill, font=green_font))

    for ws in [ws_leads, ws_clients]:
        for col in ws.columns:
            ws.column_dimensions[get_column_letter(col[0].column)].width = 22
    ws_leads.column_dimensions["D"].width = 28

    path = os.path.join(out_dir, "Freelance_Client_CRM_2026.xlsx")
    wb.save(path)
    with open(path.replace(".xlsx", ".b64.txt"), "w") as f:
        f.write(base64.b64encode(open(path, "rb").read()).decode("utf-8"))
    print("Upgraded Client CRM:", path)


# ==============================================================================
# 3. UPGRADE PERSONAL BUDGET 50/30/20 & DEBT
# ==============================================================================
def upgrade_budget():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "📊 Presupuesto 50-30-20"
    ws.views.sheetView[0].showGridLines = True
    ws["B2"] = "PLANIFICADOR FINANCIERO 50/30/20 & CONTROL DE GASTOS"
    ws["B2"].font = title_font
    ws["B3"] = "Regla de oro: 50% Necesidades | 30% Deseos | 20% Ahorro e Inversión"
    ws["B3"].font = subtitle_font

    headers = ["Categoría 50/30/20", "Concepto de Gasto", "Presupuestado (€)", "Gasto Real (€)", "Diferencia (€)", "Estado Presupuesto"]
    for c_idx, h in enumerate(headers, start=2):
        cell = ws.cell(row=5, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
        cell.alignment = Alignment(horizontal="center" if "Estado" in h else "left")

    sample_data = [
        ("50% Necesidades", "Alquiler / Hipoteca", 850, 850, "=D6-E6", "OK"),
        ("50% Necesidades", "Supermercado y alimentación", 350, 320, "=D7-E7", "Bajo Presupuesto"),
        ("50% Necesidades", "Suministros (Luz, Agua, Fibra)", 140, 165, "=D8-E8", "Excedido"),
        ("30% Deseos", "Restaurantes, ocio y salidas", 200, 180, "=D9-E9", "OK"),
        ("30% Deseos", "Suscripciones (Netflix, Gym)", 60, 60, "=D10-E10", "OK"),
        ("30% Deseos", "Viajes y escapadas", 150, 190, "=D11-E11", "Excedido"),
        ("20% Ahorro/Deuda", "Aportación Fondo Emergencia", 300, 300, "=D12-E12", "Completado"),
        ("20% Ahorro/Deuda", "Amortización Extra Préstamos", 150, 150, "=D13-E13", "Completado")
    ]
    for r_idx, row in enumerate(sample_data, start=6):
        for c_idx, val in enumerate(row, start=2):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.font = regular_font
            cell.border = thin_border
            if c_idx in [4, 5, 6]:
                cell.number_format = "#,##0.00 €"

    # Fila de Totales
    ws["B14"] = "TOTAL GENERAL"
    ws["B14"].font = bold_font
    ws["B14"].border = total_border
    for col in ["D", "E", "F"]:
        c = ws[f"{col}14"]
        c.value = f"=SUM({col}6:{col}13)"
        c.font = bold_font
        c.number_format = "#,##0.00 €"
        c.border = total_border

    # Validación desplegable para Categoría 50/30/20 y Estado
    dv_503020 = DataValidation(type="list", formula1='"50% Necesidades,30% Deseos,20% Ahorro/Deuda"', allow_blank=True)
    ws.add_data_validation(dv_503020)
    dv_503020.add("B6:B100")

    dv_status_budget = DataValidation(type="list", formula1='"OK,Bajo Presupuesto,Excedido,Completado"', allow_blank=True)
    ws.add_data_validation(dv_status_budget)
    dv_status_budget.add("G6:G100")

    # Formato condicional de Alertas
    ws.conditional_formatting.add("G6:G100", CellIsRule(operator='equal', formula=['"Excedido"'], stopIfTrue=True, fill=red_fill, font=red_font))
    ws.conditional_formatting.add("G6:G100", CellIsRule(operator='equal', formula=['"OK"'], stopIfTrue=True, fill=green_fill, font=green_font))
    ws.conditional_formatting.add("G6:G100", CellIsRule(operator='equal', formula=['"Completado"'], stopIfTrue=True, fill=blue_fill, font=blue_font))

    # Hoja 2: Bola de Nieve (Deudas)
    ws_debt = wb.create_sheet(title="❄️ Calculadora Bola de Nieve")
    ws_debt.views.sheetView[0].showGridLines = True
    ws_debt["B2"] = "MÉTODO BOLA DE NIEVE: PLAN DE AMORTIZACIÓN ACELERADA"
    ws_debt["B2"].font = title_font
    ws_debt["B3"] = "Estrategia matemática: liquida la deuda más pequeña primero para ganar tracción psicológica"
    ws_debt["B3"].font = subtitle_font

    debt_headers = ["Nombre Deuda", "Saldo Pendiente (€)", "Tipo Interés (%)", "Cuota Mínima (€)", "Pago Extra Bola (€)", "Meses Estimados Para Pagar", "Estado"]
    for c_idx, h in enumerate(debt_headers, start=2):
        cell = ws_debt.cell(row=5, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = PatternFill(start_color="B91C1C", end_color="B91C1C", fill_type="solid")

    sample_debts = [
        ("Financiación Portátil", 650, 0.0, 65, 100, "=ROUNDUP(C6/(E6+F6),0)", "Prioridad 1"),
        ("Tarjeta de Crédito", 1200, 19.5, 60, 0, "=ROUNDUP(C7/(E7+F7),0)", "Prioridad 2"),
        ("Préstamo Coche", 4500, 6.5, 140, 0, "=ROUNDUP(C8/(E8+F8),0)", "Prioridad 3")
    ]
    for r_idx, row in enumerate(sample_debts, start=6):
        for c_idx, val in enumerate(row, start=2):
            cell = ws_debt.cell(row=r_idx, column=c_idx, value=val)
            cell.font = regular_font
            cell.border = thin_border
            if c_idx in [3, 5, 6]:
                cell.number_format = "#,##0.00 €"
            elif c_idx == 4:
                cell.number_format = "0.0%"

    dv_priority = DataValidation(type="list", formula1='"Prioridad 1,Prioridad 2,Prioridad 3,Pagada"', allow_blank=True)
    ws_debt.add_data_validation(dv_priority)
    dv_priority.add("H6:H50")
    ws_debt.conditional_formatting.add("H6:H50", CellIsRule(operator='equal', formula=['"Prioridad 1"'], stopIfTrue=True, fill=amber_fill, font=amber_font))
    ws_debt.conditional_formatting.add("H6:H50", CellIsRule(operator='equal', formula=['"Pagada"'], stopIfTrue=True, fill=green_fill, font=green_font))

    for s in [ws, ws_debt]:
        for col in s.columns:
            s.column_dimensions[get_column_letter(col[0].column)].width = 24

    path = os.path.join(out_dir, "Personal_Budget_50_30_20_2026.xlsx")
    wb.save(path)
    with open(path.replace(".xlsx", ".b64.txt"), "w") as f:
        f.write(base64.b64encode(open(path, "rb").read()).decode("utf-8"))
    print("Upgraded Budget 50/30/20:", path)


# ==============================================================================
# 4. UPGRADE HABIT TRACKER
# ==============================================================================
def upgrade_habit_tracker():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "🔥 Hábitos Diarios"
    ws.views.sheetView[0].showGridLines = True
    ws["B2"] = "ULTIMATE HABIT TRACKER 2026: RUTINAS & RACHAS"
    ws["B2"].font = title_font
    ws["B3"] = "Introduce 1 para completado, 0 para no realizado. El sistema calcula rachas y % de éxito automático."
    ws["B3"].font = subtitle_font

    headers = ["Hábito / Rutina Diaria", "Área de Vida", "Frecuencia Meta", "L", "M", "X", "J", "V", "S", "D", "% Cumplimiento", "Racha Activa"]
    for c_idx, h in enumerate(headers, start=2):
        cell = ws.cell(row=5, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = PatternFill(start_color="047857", end_color="047857", fill_type="solid")
        cell.alignment = Alignment(horizontal="center")

    sample_habits = [
        ("Lectura 20 minutos", "Mente & Foco", "Diario", 1, 1, 1, 1, 1, 0, 1, "=SUM(E6:K6)/7", "6 días"),
        ("Entrenamiento / Gym", "Salud Física", "4x / semana", 1, 0, 1, 0, 1, 1, 0, "=SUM(E7:K7)/4", "4 días"),
        ("Beber 2.5L de agua", "Salud Física", "Diario", 1, 1, 1, 1, 1, 1, 1, "=SUM(E8:K8)/7", "18 días"),
        ("Bloque Deep Work 2h", "Productividad", "Lun-Vie", 1, 1, 1, 1, 1, 0, 0, "=SUM(E9:K9)/5", "5 días"),
        ("Planificar siguiente día", "Organización", "Diario", 1, 1, 1, 1, 0, 0, 1, "=SUM(E10:K10)/7", "1 día")
    ]
    for r_idx, row in enumerate(sample_habits, start=6):
        for c_idx, val in enumerate(row, start=2):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.font = regular_font
            cell.border = thin_border
            cell.alignment = Alignment(horizontal="center" if c_idx >= 5 else "left")
            if c_idx == 12:
                cell.number_format = "0.0%"

    # Validación 1 / 0 para los días
    dv_binary = DataValidation(type="list", formula1='"1,0"', allow_blank=True)
    ws.add_data_validation(dv_binary)
    dv_binary.add("E6:K50")

    # Formato condicional: 1 en verde esmeralda con número blanco, 0 en gris suave
    ws.conditional_formatting.add("E6:K50", CellIsRule(operator='equal', formula=['1'], stopIfTrue=True, fill=green_fill, font=green_font))
    ws.conditional_formatting.add("E6:K50", CellIsRule(operator='equal', formula=['0'], stopIfTrue=True, fill=PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid"), font=Font(color="94A3B8")))

    # Desplegables de Categoría y Frecuencia
    dv_habit_cat = DataValidation(type="list", formula1='"Salud Física,Productividad,Mente & Foco,Finanzas,Organización,Relaciones"', allow_blank=True)
    ws.add_data_validation(dv_habit_cat)
    dv_habit_cat.add("C6:C50")

    dv_habit_freq = DataValidation(type="list", formula1='"Diario,Lun-Vie,Fines de semana,4x / semana,3x / semana"', allow_blank=True)
    ws.add_data_validation(dv_habit_freq)
    dv_habit_freq.add("D6:D50")

    for col in ws.columns:
        ws.column_dimensions[get_column_letter(col[0].column)].width = 16
    ws.column_dimensions["B"].width = 28
    ws.column_dimensions["C"].width = 20

    path = os.path.join(out_dir, "Ultimate_Habit_Tracker_2026.xlsx")
    wb.save(path)
    with open(path.replace(".xlsx", ".b64.txt"), "w") as f:
        f.write(base64.b64encode(open(path, "rb").read()).decode("utf-8"))
    print("Upgraded Habit Tracker:", path)


# ==============================================================================
# 5. UPGRADE SOCIAL MEDIA CONTENT PLANNER
# ==============================================================================
def upgrade_content_planner():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "📅 Calendario Editorial"
    ws.views.sheetView[0].showGridLines = True
    ws["B2"] = "SOCIAL MEDIA CONTENT PLANNER & METRICS 2026"
    ws["B2"].font = title_font
    ws["B3"] = "Planificador estratégico de publicaciones, guiones, estados de producción y conversión"
    ws["B3"].font = subtitle_font

    headers = ["Fecha Pub.", "Canal / Red Social", "Pilar Temático", "Título / Gancho (Hook)", "Formato", "Estado Producción", "Borrador / Link", "Impresiones", "Clics / Ventas"]
    for c_idx, h in enumerate(headers, start=2):
        cell = ws.cell(row=5, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = PatternFill(start_color="6D28D9", end_color="6D28D9", fill_type="solid")
        cell.alignment = Alignment(horizontal="center" if "Fecha" in h or "Estado" in h or "Canal" in h else "left")

    sample_content = [
        ("2026-03-01", "LinkedIn", "Consejo Experto", "El error que comete el 90% de autónomos al fijar precios", "Post Texto", "Publicado", "https://linkedin.com/...", 4200, 18),
        ("2026-03-03", "TikTok", "Tutorial Práctico", "Cómo calcular tu IRPF en 15 segundos con esta plantilla", "Vídeo Corto (Reel/TikTok)", "Programado", "Borrador CapCut", 0, 0),
        ("2026-03-05", "Twitter / X", "Caso de Estudio", "Cómo pasé de 1.200€ a 3.500€/mes cambiando 3 cláusulas en mi propuesta", "Hilo", "Guion Listo", "Notion", 0, 0),
        ("2026-03-08", "Instagram", "Educativo", "Infografía: 5 gastos que tu gestor no te cuenta que son deducibles", "Carrusel", "Grabando", "Figma", 0, 0),
        ("2026-03-12", "YouTube", "Masterclass", "Finanzas Freelance 2026: Guía completa paso a paso", "Vídeo Largo", "Idea", "Documento Drive", 0, 0)
    ]
    for r_idx, row in enumerate(sample_content, start=6):
        for c_idx, val in enumerate(row, start=2):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.font = regular_font
            cell.border = thin_border
            if c_idx in [9, 10]:
                cell.number_format = "#,##0"

    # Desplegables de Canal, Formato y Estado
    dv_channel = DataValidation(type="list", formula1='"TikTok,Instagram,LinkedIn,Twitter / X,YouTube,Newsletter"', allow_blank=True)
    ws.add_data_validation(dv_channel)
    dv_channel.add("C6:C100")

    dv_format = DataValidation(type="list", formula1='"Vídeo Corto (Reel/TikTok),Post Texto,Carrusel,Infografía,Hilo,Vídeo Largo"', allow_blank=True)
    ws.add_data_validation(dv_format)
    dv_format.add("F6:F100")

    dv_prod_status = DataValidation(type="list", formula1='"Publicado,Programado,Editado,Grabando,Guion Listo,Idea"', allow_blank=True)
    ws.add_data_validation(dv_prod_status)
    dv_prod_status.add("G6:G100")

    # Formato condicional de estados de contenido
    ws.conditional_formatting.add("G6:G100", CellIsRule(operator='equal', formula=['"Publicado"'], stopIfTrue=True, fill=green_fill, font=green_font))
    ws.conditional_formatting.add("G6:G100", CellIsRule(operator='equal', formula=['"Programado"'], stopIfTrue=True, fill=purple_fill, font=purple_font))
    ws.conditional_formatting.add("G6:G100", CellIsRule(operator='equal', formula=['"Grabando"'], stopIfTrue=True, fill=amber_fill, font=amber_font))
    ws.conditional_formatting.add("G6:G100", CellIsRule(operator='equal', formula=['"Idea"'], stopIfTrue=True, fill=blue_fill, font=blue_font))

    for col in ws.columns:
        ws.column_dimensions[get_column_letter(col[0].column)].width = 20
    ws.column_dimensions["E"].width = 38

    path = os.path.join(out_dir, "Social_Media_Content_Planner_2026.xlsx")
    wb.save(path)
    with open(path.replace(".xlsx", ".b64.txt"), "w") as f:
        f.write(base64.b64encode(open(path, "rb").read()).decode("utf-8"))
    print("Upgraded Content Planner:", path)


# ==============================================================================
# 6. UPGRADE RESELLER & E-COMMERCE PROFIT TRACKER
# ==============================================================================
def upgrade_reseller_tracker():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "📦 Control de Ventas & P&L"
    ws.views.sheetView[0].showGridLines = True
    ws["B2"] = "E-COMMERCE & RESELLING PROFIT TRACKER"
    ws["B2"].font = title_font
    ws["B3"] = "Calculadora neta de margen real para Wallapop, Vinted, Amazon, eBay y Shopify"
    ws["B3"].font = subtitle_font

    headers = ["Fecha Compra", "Artículo / Producto", "Plataforma Venta", "Estado Artículo", "Precio Compra (€)", "Precio Venta (€)", "Comisión Plataforma (€)", "Envío/Portes (€)", "Beneficio Neto (€)", "% Margen"]
    for c_idx, h in enumerate(headers, start=2):
        cell = ws.cell(row=5, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = PatternFill(start_color="D97706", end_color="D97706", fill_type="solid")
        cell.alignment = Alignment(horizontal="center" if "Fecha" in h or "Estado" in h or "Plataforma" in h else "left")

    sample_items = [
        ("2026-02-15", "Cámara Vintage 35mm Olympus", "Wallapop", "Vendido", 25.00, 75.00, 3.75, 4.50, "=G6-F6-H6-I6", "=J6/G6"),
        ("2026-02-18", "Chaqueta Cuero Retro", "Vinted", "Vendido", 15.00, 48.00, 0.00, 2.50, "=G7-F7-H7-I7", "=J7/G7"),
        ("2026-02-22", "Auriculares Inalámbricos Pro", "Amazon", "Vendido", 32.00, 79.90, 11.98, 5.00, "=G8-F8-H8-I8", "=J8/G8"),
        ("2026-02-25", "Juego Retro Game Boy", "eBay", "En Stock / Almacén", 12.00, 45.00, 0.00, 0.00, 0.00, 0.00)
    ]
    for r_idx, row in enumerate(sample_items, start=6):
        for c_idx, val in enumerate(row, start=2):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.font = regular_font
            cell.border = thin_border
            if c_idx in [6, 7, 8, 9, 10]:
                cell.number_format = "#,##0.00 €"
            elif c_idx == 11:
                cell.number_format = "0.0%"

    dv_platform = DataValidation(type="list", formula1='"Wallapop,Vinted,Amazon,eBay,Milanuncios,Etsy,Shopify"', allow_blank=True)
    ws.add_data_validation(dv_platform)
    dv_platform.add("D6:D100")

    dv_item_status = DataValidation(type="list", formula1='"Vendido,En Stock / Almacén,Reservado,Enviado,Devuelto"', allow_blank=True)
    ws.add_data_validation(dv_item_status)
    dv_item_status.add("E6:E100")

    ws.conditional_formatting.add("E6:E100", CellIsRule(operator='equal', formula=['"Vendido"'], stopIfTrue=True, fill=green_fill, font=green_font))
    ws.conditional_formatting.add("E6:E100", CellIsRule(operator='equal', formula=['"En Stock / Almacén"'], stopIfTrue=True, fill=amber_fill, font=amber_font))
    ws.conditional_formatting.add("E6:E100", CellIsRule(operator='equal', formula=['"Devuelto"'], stopIfTrue=True, fill=red_fill, font=red_font))

    for col in ws.columns:
        ws.column_dimensions[get_column_letter(col[0].column)].width = 20
    ws.column_dimensions["C"].width = 30

    path = os.path.join(out_dir, "Ecommerce_Reseller_Profit_Tracker.xlsx")
    wb.save(path)
    with open(path.replace(".xlsx", ".b64.txt"), "w") as f:
        f.write(base64.b64encode(open(path, "rb").read()).decode("utf-8"))
    print("Upgraded Reseller Tracker:", path)


# ==============================================================================
# 7. UPGRADE PROJECT QUOTE CALCULATOR
# ==============================================================================
def upgrade_quote_calculator():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "💼 Cotizador de Presupuestos"
    ws.views.sheetView[0].showGridLines = True
    ws["B2"] = "CALCULADORA AVANZADA DE PRESUPUESTOS & MARGEN COMERCIAL"
    ws["B2"].font = title_font
    ws["B3"] = "Desglose por fases, cálculo de tarifa/hora base, margen de contingencia y precio final formal"
    ws["B3"].font = subtitle_font

    headers = ["Fase del Proyecto", "Horas Estimadas", "Tarifa Base (€/h)", "Coste Mano de Obra (€)", "Costes Externos/Licencias (€)", "% Margen Imprevistos", "Colchón Contingencia (€)", "Precio Final Recomendado (€)"]
    for c_idx, h in enumerate(headers, start=2):
        cell = ws.cell(row=5, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = PatternFill(start_color="0F766E", end_color="0F766E", fill_type="solid")

    sample_quote = [
        ("Fase 1: Auditoría y Estrategia", 10, 45, "=C6*D6", 0, 0.15, "=E6*G6", "=E6+F6+H6"),
        ("Fase 2: Prototipado y Wireframes", 18, 45, "=C7*D7", 50, 0.15, "=(E7+F7)*G7", "=E7+F7+H7"),
        ("Fase 3: Desarrollo Web y Backend", 35, 45, "=C8*D8", 120, 0.20, "=(E8+F8)*G8", "=E8+F8+H8"),
        ("Fase 4: Testing, Despliegue y Formación", 10, 45, "=C9*D9", 30, 0.15, "=(E9+F9)*G9", "=E9+F9+H9")
    ]
    for r_idx, row in enumerate(sample_quote, start=6):
        for c_idx, val in enumerate(row, start=2):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.font = regular_font
            cell.border = thin_border
            if c_idx in [4, 5, 6, 8, 9]:
                cell.number_format = "#,##0.00 €"
            elif c_idx == 7:
                cell.number_format = "0%"

    # Fila de Totales del Presupuesto
    ws["B10"] = "TOTAL PRESUPUESTO PROYECTO"
    ws["B10"].font = bold_font
    ws["B10"].border = total_border
    
    ws["C10"] = "=SUM(C6:C9)" # Total Horas
    ws["C10"].font = bold_font
    ws["C10"].border = total_border
    
    ws["D10"] = "-"
    ws["D10"].alignment = Alignment(horizontal="center")
    ws["D10"].border = total_border
    
    for col in ["E", "F", "H", "I"]:
        c = ws[f"{col}10"]
        c.value = f"=SUM({col}6:{col}9)"
        c.font = bold_font
        c.number_format = "#,##0.00 €"
        c.border = total_border
    ws["G10"].border = total_border

    # Desplegable para Margen de Contingencia
    dv_contingency = DataValidation(type="list", formula1='"10%,15%,20%,25%,30%"', allow_blank=True)
    ws.add_data_validation(dv_contingency)
    dv_contingency.add("G6:G50")

    for col in ws.columns:
        ws.column_dimensions[get_column_letter(col[0].column)].width = 24
    ws.column_dimensions["B"].width = 36

    path = os.path.join(out_dir, "Freelance_Project_Quote_Calculator.xlsx")
    wb.save(path)
    with open(path.replace(".xlsx", ".b64.txt"), "w") as f:
        f.write(base64.b64encode(open(path, "rb").read()).decode("utf-8"))
    print("Upgraded Quote Calculator:", path)


def main():
    upgrade_finance_hub()
    upgrade_client_crm()
    upgrade_budget()
    upgrade_habit_tracker()
    upgrade_content_planner()
    upgrade_reseller_tracker()
    upgrade_quote_calculator()
    print("Todas las plantillas han sido actualizadas con éxito.")

if __name__ == "__main__":
    main()
