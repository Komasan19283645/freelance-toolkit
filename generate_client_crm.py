import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def create_client_crm():
    wb = openpyxl.Workbook()
    
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    title_font = Font(name="Calibri", size=16, bold=True, color="1E1B4B")
    subtitle_font = Font(name="Calibri", size=10, italic=True, color="6B7280")
    bold_font = Font(name="Calibri", size=11, bold=True)
    
    header_fill_blue = PatternFill(start_color="2563EB", end_color="2563EB", fill_type="solid") # Blue
    header_fill_purple = PatternFill(start_color="7C3AED", end_color="7C3AED", fill_type="solid") # Purple
    header_fill_teal = PatternFill(start_color="0D9488", end_color="0D9488", fill_type="solid") # Teal
    total_fill = PatternFill(start_color="F3F4F6", end_color="F3F4F6", fill_type="solid")

    thin_border = Border(
        left=Side(style='thin', color='E5E7EB'),
        right=Side(style='thin', color='E5E7EB'),
        top=Side(style='thin', color='E5E7EB'),
        bottom=Side(style='thin', color='E5E7EB')
    )
    total_border = Border(
        top=Side(style='thin', color='111827'),
        bottom=Side(style='double', color='111827')
    )

    # ----------------------------------------------------
    # HOJA 1: PIPELINE DE LEADS Y VENTAS
    # ----------------------------------------------------
    ws_leads = wb.active
    ws_leads.title = "🎯 Pipeline de Ventas"
    ws_leads.views.sheetView[0].showGridLines = True

    ws_leads["B2"] = "FREELANCE CLIENT CRM & SALES PIPELINE"
    ws_leads["B2"].font = title_font
    ws_leads["B3"] = "Control comercial y seguimiento de oportunidades de negocio"
    ws_leads["B3"].font = subtitle_font

    headers_leads = ["Fecha Contacto", "Nombre Cliente", "Empresa / Marca", "Servicio Solicitado", "Valor Estimado (€)", "Estado Lead", "Probabilidad", "Próxima Acción", "Fecha Límite"]
    for c_idx, h in enumerate(headers_leads, start=1):
        cell = ws_leads.cell(row=5, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = header_fill_blue
        cell.alignment = Alignment(horizontal="center" if "Fecha" in h or "Probabilidad" in h or "Estado" in h else "left")

    sample_leads = [
        ("2026-02-01", "Laura Gómez", "BioCosmetics S.L.", "Rediseño Tienda Shopify", 2200, "En Negociación", "80%", "Enviar contrato revisado", "2026-02-18"),
        ("2026-02-05", "Marcos Silva", "FitPro App", "Desarrollo Landing Page", 1400, "Propuesta Enviada", "60%", "Seguimiento por email", "2026-02-19"),
        ("2026-02-10", "Elena Rivas", "Consultoría Legal 360", "Auditoría SEO + Blog", 850, "Reunión Fijada", "40%", "Videollamada de descubrimiento", "2026-02-20"),
        ("2026-02-12", "Javier Soto", "Restaurante Gourmet", "Carta Digital QR + Web", 1100, "Ganado", "100%", "Facturar 50% de anticipo", "2026-02-16")
    ]

    for r_idx, row in enumerate(sample_leads, start=6):
        for c_idx, val in enumerate(row, start=1):
            cell = ws_leads.cell(row=r_idx, column=c_idx, value=val)
            cell.border = thin_border
            if c_idx == 5:
                cell.number_format = "#,##0.00 €"

    # ----------------------------------------------------
    # HOJA 2: DIRECTORIO DE CLIENTES
    # ----------------------------------------------------
    ws_clients = wb.create_sheet(title="👥 Directorio Clientes")
    ws_clients.views.sheetView[0].showGridLines = True

    headers_clients = ["Razón Social / Nombre", "Contacto Principal", "NIF / CIF", "Email", "Teléfono", "Ciudad", "Tarifa Acordada", "Total Facturado", "Notas Especiales"]
    for c_idx, h in enumerate(headers_clients, start=1):
        cell = ws_clients.cell(row=4, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = header_fill_purple
        cell.alignment = Alignment(horizontal="left")

    sample_clients = [
        ("BioCosmetics S.L.", "Laura Gómez", "B87654321", "laura@biocosmetics.es", "+34 611 222 333", "Madrid", "45 €/hora", 4200, "Prefiere reuniones los martes"),
        ("Consultoría Legal 360", "Elena Rivas", "B12345678", "contacto@legal360.com", "+34 622 333 444", "Valencia", "50 €/hora", 1850, "Puntuales en los pagos"),
        ("Restaurante Gourmet", "Javier Soto", "B99887766", "administracion@gourmet.es", "+34 633 444 555", "Sevilla", "Precio cerrado", 2500, "Comunicación vía WhatsApp")
    ]

    for r_idx, row in enumerate(sample_clients, start=5):
        for c_idx, val in enumerate(row, start=1):
            cell = ws_clients.cell(row=r_idx, column=c_idx, value=val)
            cell.border = thin_border
            if c_idx == 8:
                cell.number_format = "#,##0.00 €"

    # ----------------------------------------------------
    # HOJA 3: PROYECTOS ACTIVOS Y ENTREGAS
    # ----------------------------------------------------
    ws_projects = wb.create_sheet(title="📋 Proyectos Activos")
    ws_projects.views.sheetView[0].showGridLines = True

    headers_proj = ["ID Proyecto", "Cliente", "Nombre Proyecto", "Fecha Inicio", "Fecha Entrega", "Presupuesto (€)", "Cobrado (€)", "Pendiente (€)", "Estado", "Horas Reales"]
    for c_idx, h in enumerate(headers_proj, start=1):
        cell = ws_projects.cell(row=4, column=c_idx, value=h)
        cell.font = header_font
        cell.fill = header_fill_teal
        cell.alignment = Alignment(horizontal="center" if "Fecha" in h or "ID" in h or "Estado" in h else "left")

    sample_proj = [
        ("PRJ-01", "BioCosmetics S.L.", "Tienda Online Shopify", "2026-02-01", "2026-03-15", 2200, 1100, "=F5-G5", "En Curso", 24),
        ("PRJ-02", "Restaurante Gourmet", "Carta Digital QR", "2026-02-10", "2026-02-28", 1100, 550, "=F6-G6", "En Revisión", 12)
    ]

    for r_idx, row in enumerate(sample_proj, start=5):
        for c_idx, val in enumerate(row, start=1):
            cell = ws_projects.cell(row=r_idx, column=c_idx, value=val)
            cell.border = thin_border
            if c_idx in [6, 7, 8]:
                cell.number_format = "#,##0.00 €"

    # Autoajuste
    for sheet in [ws_leads, ws_clients, ws_projects]:
        for col in sheet.columns:
            max_len = max(len(str(cell.value or '')) for cell in col)
            col_letter = get_column_letter(col[0].column)
            sheet.column_dimensions[col_letter].width = max(max_len + 3, 14)

    output_path = r"C:\Users\Miguel\.gemini\antigravity\scratch\freelance-toolkit-saas\entregables\Freelance_Client_CRM_2026.xlsx"
    wb.save(output_path)
    print(f"Creado Client CRM en {output_path}")

create_client_crm()
