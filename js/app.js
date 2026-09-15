/**
 * LabelGuard AI - Shared Application Scripts & Accessibility Controllers
 * Connected with Python FastAPI Backend (http://localhost:8000)
 */

window.LABELGUARD_API_URL = "http://localhost:8000";

document.addEventListener('DOMContentLoaded', () => {
  initNavbar();
  initAccessibilityToolbar();
});

/* Sticky Navbar Scroll Effect & Mobile Drawer */
function initNavbar() {
  const navbar = document.querySelector('.navbar');
  const mobileToggle = document.querySelector('.mobile-toggle');
  
  if (navbar) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 20) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
    });
  }

  if (mobileToggle) {
    mobileToggle.addEventListener('click', () => {
      document.body.classList.toggle('mobile-menu-active');
      const icon = mobileToggle.querySelector('i');
      if (icon) {
        if (document.body.classList.contains('mobile-menu-active')) {
          icon.className = 'ri-close-line';
        } else {
          icon.className = 'ri-menu-line';
        }
      }
    });
  }
}

/* Accessibility Toolbar Controls (High Contrast, Font Resize) */
function initAccessibilityToolbar() {
  const btnHighContrast = document.getElementById('btnHighContrast');
  const btnFontIncrease = document.getElementById('btnFontIncrease');
  const btnFontReset = document.getElementById('btnFontReset');
  const btnFontDecrease = document.getElementById('btnFontDecrease');

  if (btnHighContrast) {
    btnHighContrast.addEventListener('click', () => {
      document.body.classList.toggle('high-contrast');
    });
  }

  if (btnFontIncrease) {
    btnFontIncrease.addEventListener('click', () => {
      document.body.classList.remove('font-sm');
      document.body.classList.add('font-lg');
    });
  }

  if (btnFontReset) {
    btnFontReset.addEventListener('click', () => {
      document.body.classList.remove('font-lg', 'font-sm');
    });
  }

  if (btnFontDecrease) {
    btnFontDecrease.addEventListener('click', () => {
      document.body.classList.remove('font-lg');
      document.body.classList.add('font-sm');
    });
  }
}
