/**
 * LabelGuard AI - Compliance Certificate Generator Module
 */

function generateCertificateModal(
  productName = "Organic Whole Wheat Flour 5kg",
  certId = null,
) {
  const finalCertId =
    certId || `LM-CERT-2026-${Math.floor(10000 + Math.random() * 90000)}`;
  const currentDate = new Date().toLocaleDateString("en-GB", {
    day: "2-digit",
    month: "long",
    year: "numeric",
  });

  // Remove existing modal if any
  const existingModal = document.getElementById("certModalOverlay");
  if (existingModal) existingModal.remove();

  // Create Modal Markup
  const modalHTML = `
    <div class="modal-overlay active" id="certModalOverlay">
      <div class="modal-card" style="max-width: 680px; padding: 2.5rem; background: #fbfcf8d1; border: 4px double #1E3A8A; position: static; box-shadow: 0 8px 24px rgba(240, 198, 48, 0.15);">
        <button class="modal-close-btn" onclick="closeCertModal()"><i class="ri-close-line"></i></button>
        
        <!-- Official Watermark Crest -->
        <div style="text-align: center; margin-bottom: 1.5rem;">
          <img src="assets/logo-emblem.svg" alt="Emblem" style="width: 64px; height: 64px; margin: 0 auto 0.5rem;" />
          <h4 style="font-family: 'Merriweather', serif; color: #0A192F; font-size: 0.95rem; text-transform: uppercase; letter-spacing: 1px;">
            Government of India • Ministry of Consumer Affairs
          </h4>
          <h5 style="font-size: 0.8rem; color: #D97706; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px;">
            Department of Legal Metrology Enforcement
          </h5>
        </div>

        <div style="text-align: center; padding: 1rem 0; border-top: 1px solid #CBD5E1; border-bottom: 1px solid #CBD5E1; margin-bottom: 1.5rem;">
          <h2 style="font-size: 1.6rem; font-weight: 800; color: #0F2C59; text-transform: uppercase; letter-spacing: 0.5px;">
            Certificate of Legal Metrology Compliance
          </h2>
          <p style="font-size: 0.8125rem; color: #64748B; margin-top: 4px;">
            Issued under Rule 27 of Legal Metrology (Packaged Commodities) Rules, 2011
          </p>
        </div>

        <!-- Certificate Metadata Grid -->
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.25rem; background: white; padding: 1.25rem; border-radius: 8px; border: 1px solid #E2E8F0; margin-bottom: 1.5rem;">
          <div>
            <span style="font-size: 0.75rem; color: #64748B; font-weight: 700; text-transform: uppercase;">Certificate ID</span>
            <p style="font-size: 1.05rem; font-weight: 800; color: #0F172A; font-family: monospace;">${finalCertId}</p>
          </div>
          <div>
            <span style="font-size: 0.75rem; color: #64748B; font-weight: 700; text-transform: uppercase;">Date of Verification</span>
            <p style="font-size: 1rem; font-weight: 700; color: #0F172A;">${currentDate}</p>
          </div>
          <div style="grid-column: span 2;">
            <span style="font-size: 0.75rem; color: #64748B; font-weight: 700; text-transform: uppercase;">Product Name</span>
            <p style="font-size: 1.1rem; font-weight: 700; color: #1E3A8A;">${productName}</p>
          </div>
          <div style="grid-column: span 2;">
            <span style="font-size: 0.75rem; color: #64748B; font-weight: 700; text-transform: uppercase;">Compliance Status</span>
            <div style="display: inline-flex; align-items: center; gap: 0.5rem; background: #D1FAE5; color: #065F46; font-weight: 800; font-size: 0.875rem; padding: 0.4rem 1rem; border-radius: 50px; margin-top: 4px;">
              <i class="ri-checkbox-circle-fill"></i> VERIFIED COMPLIANT (100% DECLARATION MATCH)
            </div>
          </div>
        </div>

        <!-- Verification Signature & QR Box -->
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
          <div style="display: flex; align-items: center; gap: 1rem;">
            <div style="width: 70px; height: 70px; background: #0F172A; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-size: 2rem;">
              <i class="ri-qr-code-line"></i>
            </div>
            <div>
              <span style="font-size: 0.75rem; color: #64748B; display: block;">Scan QR to verify authentic badge on Ministry Portal</span>
              <span style="font-size: 0.75rem; font-weight: 700; color: #2563EB;">Hash: 8f92a10b4c8932e...</span>
            </div>
          </div>
          <div style="text-align: right;">
            <img src="https://api.iconify.design/lucide:signature.svg?color=%231e3a8a" alt="Signature" style="height: 36px; margin-left: auto;" />
            <span style="font-size: 0.8125rem; font-weight: 700; color: #0F172A; display: block;">Authorized AI Verification Officer</span>
            <span style="font-size: 0.7rem; color: #64748B;">Legal Metrology Department</span>
          </div>
        </div>

        <!-- Action Download Button -->
        <div style="display: flex; justify-content: flex-end; gap: 1rem; border-top: 1px solid #CBD5E1; padding-top: 1.25rem;">
          <button class="btn btn-secondary" onclick="closeCertModal()">Close</button>
          <button class="btn btn-primary" onclick="downloadCertificatePDF()"><i class="ri-download-2-line"></i> Download Certificate</button>
        </div>
      </div>
    </div>
  `;

  document.body.insertAdjacentHTML("beforeend", modalHTML);
}

function closeCertModal() {
  const modal = document.getElementById("certModalOverlay");
  if (modal) modal.remove();
}

function downloadCertificatePDF() {
  window.print();
}
