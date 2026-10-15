import os
import re

base_dir = r"C:\Users\Miguel\.gemini\antigravity\scratch\freelance-toolkit-saas"

pages_meta = {
    "index.html": {
        "title": "FreelanceToolkit - Generador de Facturas y Presupuestos Gratis en PDF",
        "desc": "Crea facturas y presupuestos profesionales en PDF gratis. Cálculo automático de IVA e IRPF, descarga inmediata y privacidad total sin registros.",
        "image": "https://komasan19283645.github.io/freelance-toolkit/entregables/cover_bundle_all_in_one.png",
        "url": "https://komasan19283645.github.io/freelance-toolkit/index.html"
    },
    "calculator.html": {
        "title": "Calculadora de Tarifa por Hora Freelance - FreelanceToolkit",
        "desc": "Calcula cuánto cobrar por hora según tus gastos, vacaciones e impuestos para no perder dinero como freelance o autónomo.",
        "image": "https://komasan19283645.github.io/freelance-toolkit/entregables/cover_quote_calculator.png",
        "url": "https://komasan19283645.github.io/freelance-toolkit/calculator.html"
    },
    "store.html": {
        "title": "Catálogo de Plantillas Profesionales Google Sheets & Excel - FreelanceToolkit",
        "desc": "Sistemas listos para usar: Control de Finanzas, CRM de Clientes, Presupuesto 50/30/20, Tracker de Hábitos y Reventa DAC7.",
        "image": "https://komasan19283645.github.io/freelance-toolkit/entregables/cover_bundle_all_in_one.png",
        "url": "https://komasan19283645.github.io/freelance-toolkit/store.html"
    },
    "contracts.html": {
        "title": "Modelos de Contratos y Cláusulas Freelance Gratuitas - FreelanceToolkit",
        "desc": "Cláusulas esenciales y modelos de contratos para autónomos: confidencialidad (NDA), cesión de derechos de autor e intereses de demora.",
        "image": "https://komasan19283645.github.io/freelance-toolkit/entregables/cover_client_crm.png",
        "url": "https://komasan19283645.github.io/freelance-toolkit/contracts.html"
    },
    "ventas-vinted-wallapop-hacienda-dac7.html": {
        "title": "Ventas en Vinted y Wallapop: Cuándo Obliga Hacienda a Declarar (DAC7)",
        "desc": "Guía práctica 2026: Límite de 30 ventas o 2.000€, cómo justificar ventas a pérdida y cálculo de márgenes con plantilla Excel.",
        "image": "https://komasan19283645.github.io/freelance-toolkit/entregables/cover_reseller_tracker.png",
        "url": "https://komasan19283645.github.io/freelance-toolkit/ventas-vinted-wallapop-hacienda-dac7.html"
    },
    "como-hacer-factura-autonomo-irpf-iva.html": {
        "title": "Cómo Hacer una Factura de Autónomo: Guía IRPF (7% vs 15%) e IVA 2026",
        "desc": "Aprende los requisitos legales para emitir facturas en España, cómo aplicar retenciones según tu antigüedad y descarga modelos gratis.",
        "image": "https://komasan19283645.github.io/freelance-toolkit/entregables/cover_finance_hub.png",
        "url": "https://komasan19283645.github.io/freelance-toolkit/como-hacer-factura-autonomo-irpf-iva.html"
    },
    "metodo-50-30-20-presupuesto-espanol.html": {
        "title": "El Método de Ahorro 50/30/20 y Plan Bola de Nieve en España",
        "desc": "Organiza tu sueldo mensual paso a paso: 50% necesidades, 30% ocio y 20% ahorro con plantilla interactiva para Google Sheets.",
        "image": "https://komasan19283645.github.io/freelance-toolkit/entregables/cover_budget_503020.png",
        "url": "https://komasan19283645.github.io/freelance-toolkit/metodo-50-30-20-presupuesto-espanol.html"
    }
}

mobile_nav_snippet = """
    <!-- Menú móvil desplegable -->
    <div id="mobile-menu" class="hidden md:hidden border-t border-slate-200 bg-white/95 px-4 pt-2 pb-4 space-y-1.5 shadow-lg">
      <a href="index.html" class="block px-3 py-2 text-sm font-semibold rounded-lg text-slate-700 hover:bg-slate-100">Facturación Gratis</a>
      <a href="calculator.html" class="block px-3 py-2 text-sm font-medium rounded-lg text-slate-700 hover:bg-slate-100">Calculadora de Tarifa</a>
      <a href="store.html" class="block px-3 py-2 text-sm font-medium rounded-lg text-indigo-700 bg-indigo-50 hover:bg-indigo-100 flex items-center justify-between">
        <span>⭐ Plantillas Pro (Excel & Sheets)</span>
        <span class="text-xs bg-indigo-200 text-indigo-800 px-2 py-0.5 rounded font-bold">9 €</span>
      </a>
      <a href="contracts.html" class="block px-3 py-2 text-sm font-medium rounded-lg text-slate-700 hover:bg-slate-100">Contratos & NDAs</a>
      <div class="pt-2 border-t border-slate-100 space-y-1">
        <span class="block px-3 text-xs font-bold text-slate-400 uppercase tracking-wider">Guías Gratuitas</span>
        <a href="ventas-vinted-wallapop-hacienda-dac7.html" class="block px-3 py-1.5 text-xs text-slate-600 hover:text-slate-900">Ventas Vinted/Wallapop & DAC7</a>
        <a href="como-hacer-factura-autonomo-irpf-iva.html" class="block px-3 py-1.5 text-xs text-slate-600 hover:text-slate-900">Cómo Facturar (IRPF 7%/15%)</a>
        <a href="metodo-50-30-20-presupuesto-espanol.html" class="block px-3 py-1.5 text-xs text-slate-600 hover:text-slate-900">Método 50/30/20 Ahorro</a>
        <a href="entregables/Guia_Fiscal_Express_Autonomo_2026.html" class="block px-3 py-1.5 text-xs font-semibold text-emerald-600 hover:text-emerald-700">🎁 Checklist Fiscal Express (Gratis)</a>
      </div>
    </div>
"""

hamburger_button_snippet = """
        <!-- Botón menú móvil -->
        <button type="button" onclick="document.getElementById('mobile-menu').classList.toggle('hidden')" class="md:hidden p-2 rounded-lg text-slate-600 hover:text-slate-900 hover:bg-slate-100 focus:outline-none" aria-label="Abrir menú">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
        </button>
"""

for filename, meta in pages_meta.items():
    filepath = os.path.join(base_dir, filename)
    if not os.path.exists(filepath):
        print(f"Skipping {filename}, not found.")
        continue
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 1. Update/Inject Head metadata
    og_block = f"""
  <link rel="icon" type="image/svg+xml" href="favicon.svg">
  
  <!-- Open Graph / Redes Sociales -->
  <meta property="og:type" content="website">
  <meta property="og:url" content="{meta['url']}">
  <meta property="og:title" content="{meta['title']}">
  <meta property="og:description" content="{meta['desc']}">
  <meta property="og:image" content="{meta['image']}">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@Komaleon37">
  <meta name="twitter:creator" content="@Komaleon37">
  <meta name="twitter:title" content="{meta['title']}">
  <meta name="twitter:description" content="{meta['desc']}">
  <meta name="twitter:image" content="{meta['image']}">
"""
    if '<meta property="og:title"' not in content:
        content = content.replace("</head>", f"{og_block}</head>")
    
    # 2. Add hamburger button and mobile menu if header exists
    if "</header>" in content and 'id="mobile-menu"' not in content:
        # Insert hamburger button right before the closing div of navbar right actions or in right container
        # Let's find </header> and insert mobile_nav_snippet right before </header>
        content = content.replace("</header>", f"{mobile_nav_snippet}\n  </header>")
        
        # Add hamburger button inside the header bar
        # Find the last button/action container inside header before the closing of header container
        # In all pages, there is a container like <div class="flex items-center space-x-3"> or <a href="store.html" class="text-xs font-semibold
        if 'aria-label="Abrir menú"' not in content:
            # Insert hamburger button before the closing of the header container div
            content = re.sub(r'(</div>\s*</div>\s*</div>\s*<!-- Menú móvil desplegable -->)', 
                             hamburger_button_snippet + r'\1', content, count=1)
            # If not replaced, find <div class="flex items-center space-x-3">
            if 'aria-label="Abrir menú"' not in content:
                content = content.replace('class="flex items-center space-x-3">', 'class="flex items-center space-x-2 sm:space-x-3">' + hamburger_button_snippet)

    # 3. Add link to Guia_Fiscal_Express_Autonomo_2026.html in the footer if not present
    if "Guia_Fiscal_Express_Autonomo_2026.html" not in content and "<footer" in content:
        footer_link = ' | <a href="entregables/Guia_Fiscal_Express_Autonomo_2026.html" class="text-emerald-400 hover:text-emerald-300 font-semibold">Checklist Fiscal Gratis</a>'
        content = content.replace('© 2026 FreelanceToolkit. Todas las herramientas funcionan 100% en tu navegador y no almacenan datos.', 
                                  '© 2026 FreelanceToolkit. Todas las herramientas funcionan 100% en tu navegador y no almacenan datos.' + footer_link)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Successfully upgraded {filename} with Open Graph, Favicon and Mobile Nav.")

print("All HTML files processed successfully.")
