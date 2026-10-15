/**
 * LÓGICA DE FACTURACIÓN Y PRESUPUESTOS
 */

let invoiceData = {
  type: "factura",
  currency: "€",
  invoiceNumber: "FAC-2026-001",
  date: new Date().toISOString().split("T")[0],
  dueDate: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split("T")[0],
  
  sender: {
    name: "Mi Nombre / Empresa",
    taxId: "12345678Z",
    address: "Calle Principal 123, 28001 Madrid",
    email: "hola@minegocio.com",
    phone: "+34 600 000 000"
  },

  client: {
    name: "Cliente Ejemplo S.L.",
    taxId: "B87654321",
    address: "Avenida de la Innovación 45, 08001 Barcelona",
    email: "facturas@clienteejemplo.com"
  },

  items: [
    { description: "Diseño y desarrollo de sitio web corporativo", quantity: 1, rate: 1200 },
    { description: "Mantenimiento mensual y hosting (Primer mes)", quantity: 1, rate: 150 }
  ],

  taxRate: 21,
  withholdingRate: 15,
  discountRate: 0,
  paymentMethod: "Transferencia bancaria a ES12 3456 7890 1234 5678 9012",
  notes: "Gracias por confiar en nuestros servicios. Plazo de abono: 30 días naturales.",
  logoUrl: ""
};

function loadSavedData() {
  try {
    const saved = localStorage.getItem("freelancetoolkit_invoice_draft");
    if (saved) invoiceData = { ...invoiceData, ...JSON.parse(saved) };
  } catch (e) {}
}

function saveData() {
  try {
    localStorage.setItem("freelancetoolkit_invoice_draft", JSON.stringify(invoiceData));
  } catch (e) {}
}

function renderFormItems() {
  const container = document.getElementById("items-container");
  if (!container) return;

  container.innerHTML = "";
  invoiceData.items.forEach((item, index) => {
    const row = document.createElement("div");
    row.className = "grid grid-cols-12 gap-2 items-center bg-slate-50 p-2.5 rounded-lg border border-slate-200";
    
    row.innerHTML = `
      <div class="col-span-12 sm:col-span-6">
        <input type="text" value="${escapeHtml(item.description)}" data-index="${index}" data-field="description" 
          placeholder="Descripción del servicio..." 
          class="w-full text-xs rounded border-slate-300 p-1.5">
      </div>
      <div class="col-span-4 sm:col-span-2">
        <input type="number" min="0.01" step="any" value="${item.quantity}" data-index="${index}" data-field="quantity" 
          placeholder="Cant." 
          class="w-full text-xs rounded border-slate-300 p-1.5 text-right">
      </div>
      <div class="col-span-4 sm:col-span-3">
        <div class="relative">
          <input type="number" min="0" step="any" value="${item.rate}" data-index="${index}" data-field="rate" 
            placeholder="Precio" 
            class="w-full text-xs rounded border-slate-300 p-1.5 pr-6 text-right">
          <span class="absolute right-2 top-1.5 text-xs text-slate-400">${invoiceData.currency}</span>
        </div>
      </div>
      <div class="col-span-4 sm:col-span-1 flex justify-end">
        <button type="button" onclick="removeItem(${index})" class="text-red-500 hover:text-red-700 p-1" title="Eliminar">
          ✕
        </button>
      </div>
    `;
    container.appendChild(row);
  });

  container.querySelectorAll("input").forEach(input => {
    input.addEventListener("input", (e) => {
      const idx = parseInt(e.target.dataset.index, 10);
      const field = e.target.dataset.field;
      let val = e.target.value;
      if (field === "quantity" || field === "rate") val = parseFloat(val) || 0;
      invoiceData.items[idx][field] = val;
      updateCalculations();
      updatePreview();
      saveData();
    });
  });
}

function addItem() {
  invoiceData.items.push({ description: "", quantity: 1, rate: 0 });
  renderFormItems();
  updateCalculations();
  updatePreview();
  saveData();
}

function removeItem(index) {
  if (invoiceData.items.length <= 1) return;
  invoiceData.items.splice(index, 1);
  renderFormItems();
  updateCalculations();
  updatePreview();
  saveData();
}

function calculateTotals() {
  const subtotal = invoiceData.items.reduce((sum, item) => sum + ((item.quantity || 0) * (item.rate || 0)), 0);
  const discountAmount = subtotal * ((invoiceData.discountRate || 0) / 100);
  const taxableBase = Math.max(0, subtotal - discountAmount);
  const taxAmount = taxableBase * ((invoiceData.taxRate || 0) / 100);
  const withholdingAmount = taxableBase * ((invoiceData.withholdingRate || 0) / 100);
  const total = taxableBase + taxAmount - withholdingAmount;

  return { subtotal, discountAmount, taxableBase, taxAmount, withholdingAmount, total };
}

function formatMoney(amount) {
  return new Intl.NumberFormat("es-ES", { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(amount) + " " + invoiceData.currency;
}

function updateCalculations() {
  const totals = calculateTotals();
  const subtotalEl = document.getElementById("calc-subtotal");
  const taxEl = document.getElementById("calc-tax");
  const withholdingEl = document.getElementById("calc-withholding");
  const totalEl = document.getElementById("calc-total");

  if (subtotalEl) subtotalEl.textContent = formatMoney(totals.subtotal);
  if (taxEl) taxEl.textContent = formatMoney(totals.taxAmount);
  if (withholdingEl) withholdingEl.textContent = "- " + formatMoney(totals.withholdingAmount);
  if (totalEl) totalEl.textContent = formatMoney(totals.total);
}

function updatePreview() {
  const preview = document.getElementById("printable-document");
  if (!preview) return;

  const totals = calculateTotals();
  const isQuote = invoiceData.type === "presupuesto";
  const docTitle = isQuote ? "PRESUPUESTO" : "FACTURA";

  preview.innerHTML = `
    <div class="space-y-6">
      <div class="flex justify-between items-start pb-6 border-b border-slate-200">
        <div>
          ${invoiceData.logoUrl ? `<img src="${invoiceData.logoUrl}" alt="Logo" class="max-h-14 mb-2 object-contain">` : ""}
          <h1 class="text-xl font-bold text-slate-900">${escapeHtml(invoiceData.sender.name || "Tu Nombre")}</h1>
          <p class="text-xs text-slate-500 font-mono">NIF/CIF: ${escapeHtml(invoiceData.sender.taxId || "-")}</p>
          <p class="text-xs text-slate-600 mt-1 whitespace-pre-line">${escapeHtml(invoiceData.sender.address || "")}</p>
          <p class="text-xs text-slate-600">${escapeHtml(invoiceData.sender.email || "")} | ${escapeHtml(invoiceData.sender.phone || "")}</p>
        </div>
        
        <div class="text-right">
          <span class="inline-block px-3 py-1 text-xs font-semibold uppercase tracking-wider rounded-md ${isQuote ? 'bg-amber-100 text-amber-800' : 'bg-indigo-100 text-indigo-800'}">
            ${docTitle}
          </span>
          <p class="text-lg font-bold text-slate-900 mt-2">${escapeHtml(invoiceData.invoiceNumber)}</p>
          <div class="text-xs text-slate-500 mt-1 space-y-0.5">
            <p><span class="font-medium text-slate-700">Emisión:</span> ${invoiceData.date}</p>
            <p><span class="font-medium text-slate-700">Vencimiento:</span> ${invoiceData.dueDate}</p>
          </div>
        </div>
      </div>

      <div class="bg-slate-50 p-4 rounded-lg border border-slate-200">
        <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1">Cliente</p>
        <h2 class="text-sm font-bold text-slate-900">${escapeHtml(invoiceData.client.name || "Nombre del Cliente")}</h2>
        <p class="text-xs text-slate-600 font-mono">NIF/CIF: ${escapeHtml(invoiceData.client.taxId || "-")}</p>
        <p class="text-xs text-slate-600 mt-1 whitespace-pre-line">${escapeHtml(invoiceData.client.address || "")}</p>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-left text-xs">
          <thead>
            <tr class="border-b-2 border-slate-200 text-xs font-semibold text-slate-500 uppercase">
              <th class="py-2.5">Descripción</th>
              <th class="py-2.5 text-right w-16">Cant.</th>
              <th class="py-2.5 text-right w-24">Precio</th>
              <th class="py-2.5 text-right w-24">Total</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 text-slate-700">
            ${invoiceData.items.map(item => `
              <tr>
                <td class="py-2 pr-2 font-medium">${escapeHtml(item.description || "Concepto")}</td>
                <td class="py-2 text-right">${item.quantity}</td>
                <td class="py-2 text-right">${formatMoney(item.rate)}</td>
                <td class="py-2 text-right font-semibold text-slate-900">${formatMoney((item.quantity || 0) * (item.rate || 0))}</td>
              </tr>
            `).join("")}
          </tbody>
        </table>
      </div>

      <div class="flex justify-end pt-4 border-t border-slate-200">
        <div class="w-64 space-y-1.5 text-xs">
          <div class="flex justify-between text-slate-600">
            <span>Subtotal:</span>
            <span class="font-medium">${formatMoney(totals.subtotal)}</span>
          </div>
          <div class="flex justify-between text-slate-600">
            <span>IVA (${invoiceData.taxRate}%):</span>
            <span class="font-medium">${formatMoney(totals.taxAmount)}</span>
          </div>
          ${invoiceData.withholdingRate > 0 ? `
            <div class="flex justify-between text-amber-700">
              <span>IRPF (-${invoiceData.withholdingRate}%):</span>
              <span>-${formatMoney(totals.withholdingAmount)}</span>
            </div>
          ` : ""}
          <div class="flex justify-between text-sm font-bold text-slate-900 pt-2 border-t border-slate-900">
            <span>TOTAL:</span>
            <span>${formatMoney(totals.total)}</span>
          </div>
        </div>
      </div>

      <div class="pt-4 border-t border-slate-200 text-xs text-slate-600 space-y-2">
        ${invoiceData.paymentMethod ? `<p><span class="font-semibold text-slate-800">Forma de pago:</span> ${escapeHtml(invoiceData.paymentMethod)}</p>` : ""}
        ${invoiceData.notes ? `<p class="whitespace-pre-line text-slate-500">${escapeHtml(invoiceData.notes)}</p>` : ""}
      </div>
    </div>
  `;
}

function bindFormEvents() {
  const sync = (id, obj, prop, isNumber = false) => {
    const el = document.getElementById(id);
    if (!el) return;
    el.value = obj[prop] || "";
    el.addEventListener("input", (e) => {
      obj[prop] = isNumber ? (parseFloat(e.target.value) || 0) : e.target.value;
      updateCalculations();
      updatePreview();
      saveData();
    });
  };

  sync("doc-type", invoiceData, "type");
  sync("currency-select", invoiceData, "currency");
  sync("invoice-number", invoiceData, "invoiceNumber");
  sync("invoice-date", invoiceData, "date");
  sync("invoice-due-date", invoiceData, "dueDate");

  sync("sender-name", invoiceData.sender, "name");
  sync("sender-taxid", invoiceData.sender, "taxId");
  sync("sender-address", invoiceData.sender, "address");
  sync("sender-email", invoiceData.sender, "email");
  sync("sender-phone", invoiceData.sender, "phone");

  sync("client-name", invoiceData.client, "name");
  sync("client-taxid", invoiceData.client, "taxId");
  sync("client-address", invoiceData.client, "address");

  sync("tax-rate", invoiceData, "taxRate", true);
  sync("withholding-rate", invoiceData, "withholdingRate", true);
  sync("payment-method", invoiceData, "paymentMethod");
  sync("invoice-notes", invoiceData, "notes");

  const addBtn = document.getElementById("btn-add-item");
  if (addBtn) addBtn.addEventListener("click", addItem);

  const printBtn = document.getElementById("btn-print-pdf");
  if (printBtn) printBtn.addEventListener("click", () => window.print());
}

function escapeHtml(str) {
  if (!str) return "";
  return String(str).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
}

document.addEventListener("DOMContentLoaded", () => {
  loadSavedData();
  bindFormEvents();
  renderFormItems();
  updateCalculations();
  updatePreview();
});
