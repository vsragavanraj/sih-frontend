/**
 * LabelGuard AI - Legal Metrology Rule Library Script
 */

document.addEventListener('DOMContentLoaded', () => {
  initRuleTabs();
});

const RULE_DATABASE = {
  mrp: {
    title: "MRP & Price Declaration Rules",
    section: "Rule 6(1)(e) & Section 36 of Legal Metrology Act, 2009",
    overview: "Every package must prominently declare the Maximum Retail Price (MRP) inclusive of all taxes in Indian Rupees (₹). Dual pricing for the same commodity in different geographical areas without statutory authorization is strictly illegal.",
    keyPoints: [
      "MRP format must be: 'MRP ₹ xx.xx (incl. of all taxes)' or 'Maximum Retail Price ₹ xx.xx (inclusive of all taxes)'.",
      "Stickers pasted over pre-printed MRP to inflate prices are an offense under Section 36(2).",
      "E-commerce platforms must display MRP on digital product listings equal to physical package MRP."
    ],
    penalties: [
      "First Offense: Fine up to ₹25,000 for non-declaration or illegal sticker alteration.",
      "Second Offense: Fine up to ₹50,000.",
      "Subsequent Offenses: Fine up to ₹1,000,000 or imprisonment up to 1 year, or both."
    ],
    fontSpecs: [
      { pkgSize: "Up to 50g / 50ml", minFont: "1.0 mm" },
      { pkgSize: "50g to 200g / 200ml", minFont: "2.0 mm" },
      { pkgSize: "200g to 1kg / 1L", minFont: "4.0 mm" },
      { pkgSize: "Above 1kg / 1L", minFont: "6.0 mm" }
    ]
  },
  netqty: {
    title: "Net Quantity & Measurement Rules",
    section: "Rule 6(1)(c) & Rule 11 of Legal Metrology Rules, 2011",
    overview: "The net weight or net volume declaration must use standard SI units (g, kg, ml, L, m, cm). Non-standard units (such as lbs, oz, or fluid ounces) without equivalent metric units are prohibited.",
    keyPoints: [
      "Net quantity must be declared on the Principal Display Panel (PDP).",
      "Allowable Maximum Permissible Errors (MPE) apply as per Schedule II.",
      "Symbol 'g' for grams, 'kg' for kilograms, 'ml' for milliliters, 'L' for liters must be strictly lowercase."
    ],
    penalties: [
      "Short delivery in net weight: Fine up to ₹50,000 under Section 30 of Act.",
      "Seizure of non-compliant packaged commodities stock."
    ],
    fontSpecs: [
      { pkgSize: "Up to 100g / 100ml", minFont: "1.5 mm" },
      { pkgSize: "100g to 500g / 500ml", minFont: "3.0 mm" },
      { pkgSize: "500g to 2kg / 2L", minFont: "4.0 mm" },
      { pkgSize: "Above 2kg / 2L", minFont: "6.0 mm" }
    ]
  },
  manufacturer: {
    title: "Manufacturer & Importer Address Rules",
    section: "Rule 6(1)(a) of Legal Metrology (Packaged Commodities) Rules",
    overview: "Every pre-packaged commodity must clearly disclose the name and complete address of the manufacturer, packer, or importer.",
    keyPoints: [
      "Address must include Street Name, City, State, and 6-digit Postal PIN Code.",
      "For imported goods: Name, address, and Country of Origin must be explicitly declared on the outer label.",
      "Generic statements like 'Packed in India' without manufacturer identity are invalid."
    ],
    penalties: [
      "Seizure of goods at customs / warehouse under Rule 32.",
      "Penalty of ₹25,000 per violation."
    ],
    fontSpecs: [
      { pkgSize: "All Package Sizes", minFont: "Minimum 1.0 mm height and clear contrast against background" }
    ]
  },
  customercare: {
    title: "Customer Care & Helpline Rules",
    section: "Rule 6(1)(h) Mandatory Consumer Grievance Declaration",
    overview: "Every pre-packaged commodity must provide consumer care details to allow buyers to contact the manufacturer or packer directly for grievances.",
    keyPoints: [
      "Must state: Name/Designation, Address, Telephone Number, and Email Address of the designated official.",
      "Toll-free numbers or 24/7 email helplines are highly recommended.",
      "Must be printed in a conspicuous place on the package."
    ],
    penalties: [
      "Compounding fine up to ₹10,000 for omission.",
      "Notice issuance by Legal Metrology Controller."
    ],
    fontSpecs: [
      { pkgSize: "All Package Sizes", minFont: "Minimum 1.5 mm height" }
    ]
  },
  packaging: {
    title: "Month/Year of Packing & PDP Ratio Rules",
    section: "Rule 6(1)(d) & Rule 7 Principal Display Panel Standards",
    overview: "Mandates clear declaration of the Month and Year in which the commodity was manufactured, packed, or imported.",
    keyPoints: [
      "Format: 'Mfg Date: MM/YYYY' or 'Packed: MM/YYYY' or 'Best Before XX Months from Packing'.",
      "Principal Display Panel (PDP) area must occupy at least 40% of the total surface area of package.",
      "Declarations must be clearly legible and contrast against background."
    ],
    penalties: [
      "Fine up to ₹25,000.",
      "Mandatory recall of expired or un-dated stock from market shelves."
    ],
    fontSpecs: [
      { pkgSize: "Standard Display Panel", minFont: "Minimum 2.0 mm height for dates" }
    ]
  }
};

function initRuleTabs() {
  const tabBtns = document.querySelectorAll('.rule-tab-btn');
  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      tabBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const ruleKey = btn.getAttribute('data-rule');
      if (RULE_DATABASE[ruleKey]) {
        renderRuleDetails(RULE_DATABASE[ruleKey]);
      }
    });
  });
}

function renderRuleDetails(rule) {
  const titleEl = document.getElementById('ruleTitle');
  const sectionEl = document.getElementById('ruleSection');
  const overviewEl = document.getElementById('ruleOverview');
  const pointsList = document.getElementById('ruleKeyPoints');
  const penaltyList = document.getElementById('rulePenalties');
  const fontBody = document.getElementById('ruleFontBody');

  if (titleEl) titleEl.textContent = rule.title;
  if (sectionEl) sectionEl.textContent = rule.section;
  if (overviewEl) overviewEl.textContent = rule.overview;

  if (pointsList) {
    pointsList.innerHTML = rule.keyPoints.map(pt => `<li><i class="ri-checkbox-circle-line"></i> ${pt}</li>`).join('');
  }

  if (penaltyList) {
    penaltyList.innerHTML = rule.penalties.map(p => `<li>${p}</li>`).join('');
  }

  if (fontBody) {
    fontBody.innerHTML = rule.fontSpecs.map(f => `
      <tr>
        <td><strong>${f.pkgSize}</strong></td>
        <td><span class="act-badge">${f.minFont}</span></td>
      </tr>
    `).join('');
  }
}
