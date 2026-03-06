/**
 * app.js — Main Application Controller
 * VayuBus — Now powered by FastAPI backend!
 *
 * Flow: Search → API → Route Map → Seat Map → Passenger Form → Confirm
 */

const App = (() => {

  // ── State ─────────────────────────────────────────────────
  let state = {
    bus:      null,   // selected BusSearchResult
    seats:    [],     // [{ num, type }]
    step:     1,
    maxSeats: 1,
    from:     "",
    to:       "",
    date:     ""
  };

  // ── Init ──────────────────────────────────────────────────
  async function _init() {
    // Set today's date
    const today = new Date().toISOString().split("T")[0];
    document.getElementById("journey-date").value = today;

    // Load cities into dropdowns from API
    await _loadCities();

    // Passengers dropdown change
    document.getElementById("passengers").addEventListener("change", function (e) {
      state.maxSeats = parseInt(e.target.value) || 1;
      document.getElementById("seat-count-val").textContent = state.maxSeats;
      SeatMap.setMax(state.maxSeats);
      Summary.update(state.bus, SeatMap.getSelected());
      _updateCTA();
    });
  }

  // ── Load cities from API into dropdowns ───────────────────
  async function _loadCities() {
    try {
      const cities = await API.getCities();
      const fromSel = document.getElementById("from-city");
      const toSel   = document.getElementById("to-city");

      fromSel.innerHTML = "";
      toSel.innerHTML   = "";

      cities.forEach(function (city) {
        const opt1 = new Option(city.name, city.name);
        const opt2 = new Option(city.name, city.name);
        fromSel.appendChild(opt1);
        toSel.appendChild(opt2);
      });

      // Set defaults
      if (cities.length > 0) fromSel.value = "Hyderabad";
      if (cities.length > 1) toSel.value   = "Chennai";

    } catch (err) {
      Utils.toast("⚠️ Could not load cities. Using defaults.");
      _loadFallbackCities();
    }
  }

  // ── Fallback cities if API is down ────────────────────────
  function _loadFallbackCities() {
    const defaults = [
      "Hyderabad","Chennai","Bengaluru","Mumbai","Delhi",
      "Pune","Kolkata","Ahmedabad","Jaipur","Kochi"
    ];
    const fromSel = document.getElementById("from-city");
    const toSel   = document.getElementById("to-city");
    fromSel.innerHTML = "";
    toSel.innerHTML   = "";
    defaults.forEach(function (c) {
      fromSel.appendChild(new Option(c, c));
      toSel.appendChild(new Option(c, c));
    });
    fromSel.value = "Hyderabad";
    toSel.value   = "Chennai";
  }

  // ── Step Manager ──────────────────────────────────────────
  function _setStep(s) {
    state.step = s;
    const labels = ["Select Bus", "Select Seats", "Passenger Details"];
    document.getElementById("hdr-info").textContent = labels[s - 1];

    for (let i = 1; i <= 3; i++) {
      const item = document.getElementById("si" + i);
      const dot  = item.querySelector(".step-dot");
      const line = document.getElementById("sc" + i);

      if (i < s) {
        item.className    = "step-item done";
        dot.textContent   = "✓";
      } else if (i === s) {
        item.className    = "step-item active";
        dot.textContent   = i;
      } else {
        item.className    = "step-item";
        dot.textContent   = i;
      }

      if (i < 3 && line) {
        line.className = i < s ? "step-connector active" : "step-connector";
      }
    }
  }

  // ── CTA Button ────────────────────────────────────────────
  function _updateCTA() {
    const btn   = document.getElementById("cta-btn");
    const seats = SeatMap.getSelected();

    if (!state.bus) {
      btn.textContent = "SELECT A BUS FIRST";
      btn.disabled    = true;
    } else if (seats.length === 0) {
      btn.textContent = "SELECT SEATS";
      btn.disabled    = true;
    } else if (state.step < 3) {
      btn.textContent = "CONTINUE WITH " + seats.length + " SEAT(S) →";
      btn.disabled    = false;
    } else {
      btn.textContent = "CONFIRM & PAY";
      btn.disabled    = false;
    }
  }

  // ── Loading indicator ─────────────────────────────────────
  function _setLoading(id, loading) {
    const el = document.getElementById(id);
    if (!el) return;
    if (loading) {
      el.innerHTML = '<div class="loading-row"><span class="spinner"></span> Loading...</div>';
    }
  }

  // ══════════════════════════════════════════════════════════
  //  PUBLIC: Search Buses — calls API
  // ══════════════════════════════════════════════════════════
  async function searchBuses() {
    const from = document.getElementById("from-city").value;
    const to   = document.getElementById("to-city").value;
    const date = document.getElementById("journey-date").value;

    if (from === to) {
      Utils.toast("Origin and destination cannot be the same!");
      return;
    }

    state.from     = from;
    state.to       = to;
    state.date     = date;
    state.maxSeats = parseInt(document.getElementById("passengers").value) || 1;
    document.getElementById("seat-count-val").textContent = state.maxSeats;

    // Show route map
    Utils.show("route-map-card");
    RouteMap.renderFromSearch(from, to);

    // Show loading state
    Utils.show("buses-card");
    _setLoading("bus-list", true);
    document.getElementById("bus-count").textContent = "Searching...";

    // Summary route block
    document.getElementById("sum-from").textContent = from;
    document.getElementById("sum-to").textContent   = to;
    document.getElementById("sum-date").textContent = Utils.formatDate(date);
    Utils.show("sum-route-block");
    Utils.hide("sum-default-head");

    _setStep(1);
    _updateCTA();

    try {
      // ── Call API ──────────────────────────────
      const buses = await API.searchBuses(from, to, date);

      const list = document.getElementById("bus-list");
      list.innerHTML = "";

      if (buses.length === 0) {
        list.innerHTML =
          '<div class="no-results">' +
          '🚌 No buses found for this route. Try a different date or route!</div>';
        document.getElementById("bus-count").textContent = "0 buses found";
        return;
      }

      buses.forEach(function (b) {
        const avail = b.available;
        const card  = document.createElement("div");
        card.className   = "bus-card";
        card.id          = "bcard-" + b.bus_id;
        card.setAttribute("role", "button");
        card.setAttribute("tabindex", "0");

        const tags = (b.amenities || []).map(function (t) {
          return '<span class="tag">' + t + "</span>";
        }).join("");

        const stars = "★".repeat(Math.round(b.rating)) +
                      "☆".repeat(5 - Math.round(b.rating));

        card.innerHTML =
          "<div>" +
            '<div class="bus-name">' + b.bus_name + "</div>" +
            '<div class="bus-meta">' + b.bus_type + " · " + b.operator + "</div>" +
            '<div class="bus-rating" style="color:var(--amber);font-size:.75rem;margin-top:3px">' +
              stars + " " + b.rating +
            "</div>" +
            '<div class="bus-tags">' + tags + "</div>" +
          "</div>" +
          '<div class="bus-time-block">' +
            '<div class="t-time">' + b.departure + "</div>" +
            '<div class="t-label">Departs</div>' +
          "</div>" +
          '<div class="bus-dur">' + b.duration + "</div>" +
          '<div class="bus-time-block">' +
            '<div class="t-time">' + b.arrival + "</div>" +
            '<div class="t-label">Arrives</div>' +
          "</div>" +
          '<div class="bus-price-block">' +
            '<div class="price">₹' + b.price + "</div>" +
            '<div class="price-sub">per seat</div>' +
            '<div class="avail ' + (avail <= 8 ? "low" : "good") + '">' +
              avail + " seats left" +
            "</div>" +
          "</div>";

        card.addEventListener("click",   function () { selectBus(b); });
        card.addEventListener("keydown", function (e) {
          if (e.key === "Enter") selectBus(b);
        });
        list.appendChild(card);
      });

      document.getElementById("bus-count").textContent = buses.length + " buses found";
      Utils.scrollTo("buses-card");

    } catch (err) {
      document.getElementById("bus-list").innerHTML =
        '<div class="no-results">❌ Error loading buses: ' + err.message + "</div>";
      document.getElementById("bus-count").textContent = "Error";
      Utils.toast("Failed to load buses. Check backend connection.");
    }
  }

  // ══════════════════════════════════════════════════════════
  //  PUBLIC: Select Bus — load real booked seats from API
  // ══════════════════════════════════════════════════════════
  async function selectBus(bus) {
    state.bus = bus;

    document.querySelectorAll(".bus-card").forEach(function (c) {
      c.classList.remove("selected");
    });
    const card = document.getElementById("bcard-" + bus.bus_id);
    if (card) card.classList.add("selected");

    Summary.update(bus, []);

    // Use booked seats from search result (already from API)
    const bookedSeats = bus.booked_seats || [];

    // Build bus object compatible with SeatMap
    const busObj = {
      totalSeats: bus.total_seats,
      layout:     bus.layout,
      decks:      bus.decks,
      booked:     bookedSeats,
      price:      bus.price
    };

    SeatMap.init(busObj, state.maxSeats, function (seats) {
      state.seats = seats;
      Summary.update(bus, seats);
      _updateCTA();
    });

    Utils.show("seats-card");
    _setStep(2);
    _updateCTA();
    Utils.scrollTo("seats-card");
  }

  // ── Public: Adjust Seat Count ──────────────────────────────
  function adjustCount(delta) {
    let v = parseInt(document.getElementById("seat-count-val").textContent) + delta;
    v = Math.max(1, Math.min(5, v));
    state.maxSeats = v;
    document.getElementById("seat-count-val").textContent = v;
    document.getElementById("passengers").value           = v;
    SeatMap.setMax(v);
    Summary.update(state.bus, SeatMap.getSelected());
    _updateCTA();
  }

  // ── Public: CTA Click ──────────────────────────────────────
  function handleCTA() {
    const seats = SeatMap.getSelected();
    if (state.step === 2 && seats.length > 0) {
      Summary.buildPassengerForm(seats);
      _setStep(3);
      _updateCTA();
    } else if (state.step === 3) {
      _submitBooking();
    }
  }

  // ══════════════════════════════════════════════════════════
  //  PRIVATE: Submit Booking — POST to API, save to DB!
  // ══════════════════════════════════════════════════════════
  async function _submitBooking() {
    const seats = SeatMap.getSelected();
    const err   = Summary.validate(seats);
    if (err) { Utils.toast(err); return; }

    // Build passengers array
    const passengers = seats.map(function (s, i) {
      return {
        seat_number: s.num,
        seat_type:   s.type,
        first_name:  document.getElementById("p" + i + "-fn").value.trim(),
        last_name:   document.getElementById("p" + i + "-ln").value.trim(),
        age:         parseInt(document.getElementById("p" + i + "-age").value),
        id_proof:    document.getElementById("p" + i + "-id").value
      };
    });

    // Build booking payload
    const payload = {
      bus_id:        state.bus.bus_id,
      from_city:     state.from,
      to_city:       state.to,
      journey_date:  state.date,
      contact_phone: document.getElementById("c-phone").value.trim(),
      contact_email: document.getElementById("c-email").value.trim(),
      passengers:    passengers
    };

    // Disable CTA while submitting
    const btn = document.getElementById("cta-btn");
    btn.textContent = "BOOKING... ⏳";
    btn.disabled    = true;

    try {
      // ── POST to API — saves to DB! ──────────
      const confirmation = await API.createBooking(payload);

      // ── Show confirmation modal ──────────────
      document.getElementById("c-pnr").textContent   = confirmation.pnr;
      document.getElementById("c-route").textContent = state.from + " → " + state.to;
      document.getElementById("c-bus").textContent   = confirmation.bus_name;
      document.getElementById("c-time").textContent  =
        Utils.formatDate(state.date) + ", " + confirmation.departure;
      document.getElementById("c-seats").textContent =
        confirmation.seats.join(", ");
      document.getElementById("c-pax").textContent   =
        confirmation.passengers.map(function (p) {
          return Utils.typeLabel(p.seat_type);
        }).join(", ");
      document.getElementById("c-amt").textContent   =
        "₹" + confirmation.total_amount.toLocaleString("en-IN");

      Utils.show("overlay");

    } catch (err) {
      Utils.toast("Booking failed: " + err.message);
      btn.textContent = "CONFIRM & PAY";
      btn.disabled    = false;
    }
  }

  // ── Public: Close Modal & Reset ───────────────────────────
  function closeModal() {
    Utils.hide("overlay");
    _reset();
  }

  function _reset() {
    state = { bus: null, seats: [], step: 1, maxSeats: 1, from: "", to: "", date: "" };

    Utils.hide("buses-card");
    Utils.hide("seats-card");
    Utils.hide("route-map-card");
    Utils.hide("sum-route-block");
    Utils.show("sum-default-head");

    Summary.reset();
    document.querySelectorAll(".bus-card").forEach(function (c) {
      c.classList.remove("selected");
    });
    document.getElementById("seats-count-badge").textContent = "0 selected";
    document.getElementById("seat-count-val").textContent    = "1";

    _setStep(1);
    _updateCTA();
  }

  // ── Bootstrap ────────────────────────────────────────────
  document.addEventListener("DOMContentLoaded", _init);

  return {
    searchBuses,
    selectBus,
    adjustCount,
    handleCTA,
    closeModal
  };

})();
