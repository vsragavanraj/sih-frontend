/**
 * LabelGuard AI - Admin Analytics Dashboard Scripts (Linked with FastAPI Backend)
 */

const API_BASE_URL = "http://localhost:8000";

document.addEventListener('DOMContentLoaded', () => {
  fetchLiveBackendStats();
  initAnalyticsCharts();
  initViolationsTable();
});

/**
 * Fetches real-time dashboard analytics from FastAPI GET /stats
 */
async function fetchLiveBackendStats() {
  try {
    const response = await fetch(`${API_BASE_URL}/stats`);
    if (response.ok) {
      const stats = await response.json();
      updateKPICards(stats);
      console.log("[LabelGuard AI] Successfully loaded live backend stats:", stats);
    }
  } catch (err) {
    console.warn("[LabelGuard AI] Backend /stats offline, using baseline stats.", err);
  }
}

/**
 * Updates KPI cards with live backend stats
 */
function updateKPICards(stats) {
  const kpiTotal = document.getElementById('kpiTotalScans');
  const kpiCompliant = document.getElementById('kpiCompliantScans');
  const kpiNonCompliant = document.getElementById('kpiNonCompliantScans');
  const kpiAccuracy = document.getElementById('kpiAccuracyRate');

  if (kpiTotal && stats.total_scans !== undefined) {
    kpiTotal.textContent = stats.total_scans.toLocaleString();
  }
  if (kpiCompliant && stats.compliant !== undefined) {
    kpiCompliant.textContent = stats.compliant.toLocaleString();
  }
  if (kpiNonCompliant && stats.non_compliant !== undefined) {
    kpiNonCompliant.textContent = stats.non_compliant.toLocaleString();
  }
  if (kpiAccuracy && stats.accuracy !== undefined) {
    kpiAccuracy.textContent = `${stats.accuracy}%`;
  }
}

function initAnalyticsCharts() {
  // 1. Line Chart - Monthly Scanning Trend
  const lineCtx = document.getElementById('scansLineChart');
  if (lineCtx) {
    new Chart(lineCtx.getContext('2d'), {
      type: 'line',
      data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug'],
        datasets: [
          {
            label: 'Total Scanned',
            data: [1240, 1420, 1580, 1710, 1850, 2100, 2340, 2458],
            borderColor: '#2563EB',
            backgroundColor: 'rgba(37, 99, 235, 0.1)',
            fill: true,
            tension: 0.4,
            borderWidth: 3
          },
          {
            label: 'Compliant Packages',
            data: [1110, 1260, 1400, 1520, 1640, 1860, 2080, 2183],
            borderColor: '#059669',
            backgroundColor: 'transparent',
            tension: 0.4,
            borderWidth: 2,
            borderDash: [5, 5]
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top' }
        },
        scales: {
          y: { grid: { color: '#E2E8F0' } },
          x: { grid: { display: false } }
        }
      }
    });
  }

  // 2. Bar Chart - Top Violations by Category
  const barCtx = document.getElementById('violationsBarChart');
  if (barCtx) {
    new Chart(barCtx.getContext('2d'), {
      type: 'bar',
      data: {
        labels: ['Missing Address', 'MRP Sticker', 'Font Size', 'Expired Date', 'Missing Origin', 'Dual Pricing'],
        datasets: [{
          label: 'Violations Count',
          data: [42, 31, 28, 19, 14, 8],
          backgroundColor: [
            '#EF4444',
            '#F59E0B',
            '#3B82F6',
            '#8B5CF6',
            '#EC4899',
            '#64748B'
          ],
          borderRadius: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        },
        scales: {
          y: { grid: { color: '#E2E8F0' } },
          x: { grid: { display: false } }
        }
      }
    });
  }

  // 3. Pie Chart - Package Category Distribution
  const pieCtx = document.getElementById('categoryPieChart');
  if (pieCtx) {
    new Chart(pieCtx.getContext('2d'), {
      type: 'doughnut',
      data: {
        labels: ['Food & Beverages', 'Cosmetics', 'Electronics', 'Pharma', 'Imported Goods'],
        datasets: [{
          data: [42, 24, 16, 12, 6],
          backgroundColor: [
            '#1D4ED8',
            '#2563EB',
            '#60A5FA',
            '#93C5FD',
            '#F59E0B'
          ],
          borderWidth: 2,
          borderColor: '#FFFFFF'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'bottom' }
        }
      }
    });
  }
}

/* Violations Data Table Search & Filter */
function initViolationsTable() {
  const searchInput = document.getElementById('tableSearchInput');
  const tableRows = document.querySelectorAll('.gov-data-table tbody tr');

  if (!searchInput) return;

  searchInput.addEventListener('keyup', (e) => {
    const term = e.target.value.toLowerCase();
    tableRows.forEach(row => {
      const text = row.textContent.toLowerCase();
      if (text.includes(term)) {
        row.style.display = '';
      } else {
        row.style.display = 'none';
      }
    });
  });
}
