/**
 * data.js — API Client for VayuBus Backend
 * All data comes from FastAPI backend (no more hardcoded data!)
 *
 * Backend: http://localhost:8000  (dev)
 *          http://vayubus-backend-svc  (k8s)
 */

const API = (() => {

  // ── Base URL — change for production ────────────────────────
  const BASE_URL = window.VAYUBUS_API_URL || "http://localhost:8000";

  // ── Generic fetch helper ─────────────────────────────────────
  async function _fetch(endpoint, options = {}) {
    try {
      const res = await fetch(BASE_URL + endpoint, {
        headers: { "Content-Type": "application/json" },
        ...options
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: "Unknown error" }));
        throw new Error(err.detail || `HTTP ${res.status}`);
      }

      return await res.json();

    } catch (err) {
      console.error(`API Error [${endpoint}]:`, err.message);
      throw err;
    }
  }

  // ══════════════════════════════════════════════
  //  CITIES
  // ══════════════════════════════════════════════

  /** Get all cities */
  async function getCities() {
    return await _fetch("/api/cities");
  }

  /** Get major cities only */
  async function getMajorCities() {
    return await _fetch("/api/cities/major");
  }

  /** Search cities by name */
  async function searchCities(query) {
    return await _fetch(`/api/cities/search?q=${encodeURIComponent(query)}`);
  }

  // ══════════════════════════════════════════════
  //  BUSES
  // ══════════════════════════════════════════════

  /**
   * Search buses by route + date
   * @param {string} fromCity  - Origin city name
   * @param {string} toCity    - Destination city name
   * @param {string} date      - Journey date "YYYY-MM-DD"
   * @returns {Promise<Array>} - List of BusSearchResult
   */
  async function searchBuses(fromCity, toCity, date) {
    const params = new URLSearchParams({
      from_city:    fromCity,
      to_city:      toCity,
      journey_date: date
    });
    return await _fetch(`/api/buses/search?${params}`);
  }

  /**
   * Get booked seats for a bus on a date
   * @param {number} busId
   * @param {string} date  - "YYYY-MM-DD"
   */
  async function getBookedSeats(busId, date) {
    const params = new URLSearchParams({ journey_date: date });
    return await _fetch(`/api/buses/${busId}/booked?${params}`);
  }

  // ══════════════════════════════════════════════
  //  BOOKINGS
  // ══════════════════════════════════════════════

  /**
   * Create a new booking
   * @param {Object} payload - BookingIn schema
   * @returns {Promise<Object>} - BookingConfirmation
   */
  async function createBooking(payload) {
    return await _fetch("/api/bookings", {
      method: "POST",
      body:   JSON.stringify(payload)
    });
  }

  /**
   * Get booking by PNR
   * @param {string} pnr
   */
  async function getBookingByPNR(pnr) {
    return await _fetch(`/api/bookings/${pnr}`);
  }

  /**
   * Get all bookings for a phone number
   * @param {string} phone
   */
  async function getBookingsByPhone(phone) {
    return await _fetch(`/api/bookings/phone/${encodeURIComponent(phone)}`);
  }

  /**
   * Cancel a booking
   * @param {string} pnr
   */
  async function cancelBooking(pnr) {
    return await _fetch(`/api/bookings/${pnr}/cancel`, { method: "PUT" });
  }

  // ══════════════════════════════════════════════
  //  HEALTH CHECK
  // ══════════════════════════════════════════════
  async function healthCheck() {
    return await _fetch("/health");
  }

  // ── Public API ──────────────────────────────────────────────
  return {
    BASE_URL,
    getCities,
    getMajorCities,
    searchCities,
    searchBuses,
    getBookedSeats,
    createBooking,
    getBookingByPNR,
    getBookingsByPhone,
    cancelBooking,
    healthCheck
  };

})();
