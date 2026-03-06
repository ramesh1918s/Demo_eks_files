/**
 * utils.js — Utility Functions
 * VayuBus Smart Bus Booking
 */

const Utils = (() => {

  /** Format a date string to human-readable */
  function formatDate(dateStr) {
    if (!dateStr) return '—';
    return new Date(dateStr + 'T00:00:00').toLocaleDateString('en-IN', {
      day: 'numeric', month: 'short', year: 'numeric'
    });
  }

  /** Generate random PNR code */
  function generatePNR() {
    return 'VB' + Math.random().toString(36).toUpperCase().slice(2, 8);
  }

  /** Show / hide element by id using .hidden class */
  function show(id) {
    const el = document.getElementById(id);
    if (el) el.classList.remove('hidden');
  }
  function hide(id) {
    const el = document.getElementById(id);
    if (el) el.classList.add('hidden');
  }

  /** Toast notification */
  let toastTimer = null;
  function toast(msg) {
    const t = document.getElementById('toast');
    if (!t) return;
    t.textContent = msg;
    t.classList.add('show');
    if (toastTimer) clearTimeout(toastTimer);
    toastTimer = setTimeout(() => t.classList.remove('show'), 3000);
  }

  /** Seat type helpers */
  function typeColor(type) {
    const map = { male: '#3b82f6', female: '#ec4899', child: '#f59e0b' };
    return map[type] || '#64748b';
  }
  function typeClass(type) {
    return type || 'male';
  }
  function typeIcon(type) {
    const map = { male: '\uD83D\uDC68', female: '\uD83D\uDC69', child: '\uD83E\uDDD2' };
    return map[type] || '\uD83D\uDC64';
  }
  function typeLabel(type) {
    return type ? (type.charAt(0).toUpperCase() + type.slice(1)) : 'Male';
  }

  /** Price multiplier per type */
  function priceMultiplier(type) {
    return type === 'child' ? 0.6 : 1.0;
  }

  /** Smoothly scroll element into view */
  function scrollTo(id) {
    const el = document.getElementById(id);
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  return {
    formatDate,
    generatePNR,
    show, hide,
    toast,
    typeColor, typeClass, typeIcon, typeLabel,
    priceMultiplier,
    scrollTo
  };

})();
