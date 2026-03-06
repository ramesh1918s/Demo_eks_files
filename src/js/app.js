/**
 * app.js — Main Application Controller
 * VayuBus Smart Bus Booking
 *
 * Orchestrates: Search → Route Map → Bus Selection → Seat Map → Passenger Form → Confirm
 */

const App = (() => {

  // ── State ────────────────────────────────────
  let state = {
    bus:      null,
    seats:    [],
    step:     1,
    maxSeats: 1,
    from:     '',
    to:       '',
    date:     ''
  };

  // ── Init ─────────────────────────────────────
  function _init() {
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('journey-date').value = today;

    document.getElementById('passengers').addEventListener('change', function(e) {
      state.maxSeats = parseInt(e.target.value) || 1;
      document.getElementById('seat-count-val').textContent = state.maxSeats;
      SeatMap.setMax(state.maxSeats);
      Summary.update(state.bus, SeatMap.getSelected());
      _updateCTA();
    });
  }

  // ── Step Manager ─────────────────────────────
  function _setStep(s) {
    state.step = s;
    const labels = ['Select Bus', 'Select Seats', 'Passenger Details'];
    document.getElementById('hdr-info').textContent = labels[s - 1];

    for (let i = 1; i <= 3; i++) {
      const item = document.getElementById('si' + i);
      const dot  = item.querySelector('.step-dot');
      const line = document.getElementById('sc' + i);

      if (i < s) {
        item.className = 'step-item done';
        dot.textContent = '\u2713';
      } else if (i === s) {
        item.className = 'step-item active';
        dot.textContent = i;
      } else {
        item.className = 'step-item';
        dot.textContent = i;
      }

      if (i < 3 && line) {
        line.className = i < s ? 'step-connector active' : 'step-connector';
      }
    }
  }

  // ── CTA Button ───────────────────────────────
  function _updateCTA() {
    const btn   = document.getElementById('cta-btn');
    const seats = SeatMap.getSelected();

    if (!state.bus) {
      btn.textContent = 'SELECT A BUS FIRST';
      btn.disabled    = true;
    } else if (seats.length === 0) {
      btn.textContent = 'SELECT SEATS';
      btn.disabled    = true;
    } else if (state.step < 3) {
      btn.textContent = 'CONTINUE WITH ' + seats.length + ' SEAT(S) \u2192';
      btn.disabled    = false;
    } else {
      btn.textContent = 'CONFIRM & PAY';
      btn.disabled    = false;
    }
  }

  // ── Public: Search Buses ──────────────────────
  function searchBuses() {
    const from = document.getElementById('from-city').value;
    const to   = document.getElementById('to-city').value;
    const date = document.getElementById('journey-date').value;

    if (from === to) { Utils.toast('Origin and destination cannot be the same!'); return; }

    state.from     = from;
    state.to       = to;
    state.date     = date;
    state.maxSeats = parseInt(document.getElementById('passengers').value) || 1;
    document.getElementById('seat-count-val').textContent = state.maxSeats;

    // Route map
    Utils.show('route-map-card');
    RouteMap.render(from, to);

    // Build bus cards
    const list = document.getElementById('bus-list');
    list.innerHTML = '';

    BusData.BUSES.forEach(function(b) {
      const avail = b.totalSeats - b.booked.length;
      const card  = document.createElement('div');
      card.className   = 'bus-card';
      card.id          = 'bcard-' + b.id;
      card.setAttribute('role', 'button');
      card.setAttribute('tabindex', '0');

      const tags = b.tags.map(function(t) {
        return '<span class="tag">' + t + '</span>';
      }).join('');

      card.innerHTML =
        '<div>' +
          '<div class="bus-name">' + b.name + '</div>' +
          '<div class="bus-meta">' + b.type + '</div>' +
          '<div class="bus-tags">' + tags + '</div>' +
        '</div>' +
        '<div class="bus-time-block">' +
          '<div class="t-time">' + b.dep + '</div>' +
          '<div class="t-label">Departs</div>' +
        '</div>' +
        '<div class="bus-dur">' + b.dur + '</div>' +
        '<div class="bus-time-block">' +
          '<div class="t-time">' + b.arr + '</div>' +
          '<div class="t-label">Arrives</div>' +
        '</div>' +
        '<div class="bus-price-block">' +
          '<div class="price">\u20B9' + b.price + '</div>' +
          '<div class="price-sub">per seat</div>' +
          '<div class="avail ' + (avail <= 8 ? 'low' : 'good') + '">' + avail + ' seats left</div>' +
        '</div>';

      card.addEventListener('click',   function() { selectBus(b); });
      card.addEventListener('keydown', function(e) { if (e.key === 'Enter') selectBus(b); });
      list.appendChild(card);
    });

    document.getElementById('bus-count').textContent = BusData.BUSES.length + ' buses found';
    Utils.show('buses-card');

    // Summary route
    document.getElementById('sum-from').textContent = from;
    document.getElementById('sum-to').textContent   = to;
    document.getElementById('sum-date').textContent = Utils.formatDate(date);
    Utils.show('sum-route-block');
    Utils.hide('sum-default-head');

    _setStep(1);
    _updateCTA();
    Utils.scrollTo('buses-card');
  }

  // ── Public: Select Bus ────────────────────────
  function selectBus(bus) {
    state.bus = bus;

    document.querySelectorAll('.bus-card').forEach(function(c) {
      c.classList.remove('selected');
    });
    document.getElementById('bcard-' + bus.id).classList.add('selected');

    Summary.update(bus, []);

    // Init seat map
    SeatMap.init(bus, state.maxSeats, function(seats) {
      state.seats = seats;
      Summary.update(bus, seats);
      _updateCTA();
    });

    Utils.show('seats-card');
    _setStep(2);
    _updateCTA();
    Utils.scrollTo('seats-card');
  }

  // ── Public: Adjust Seat Count ─────────────────
  function adjustCount(delta) {
    let v = parseInt(document.getElementById('seat-count-val').textContent) + delta;
    v = Math.max(1, Math.min(5, v));
    state.maxSeats = v;
    document.getElementById('seat-count-val').textContent  = v;
    document.getElementById('passengers').value            = v;
    SeatMap.setMax(v);
    Summary.update(state.bus, SeatMap.getSelected());
    _updateCTA();
  }

  // ── Public: CTA Click ────────────────────────
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

  // ── Private: Submit Booking ───────────────────
  function _submitBooking() {
    const seats = SeatMap.getSelected();
    const err   = Summary.validate(seats);
    if (err) { Utils.toast(err); return; }

    const pnr = Utils.generatePNR();
    let total = 0;
    seats.forEach(function(s) { total += state.bus.price * Utils.priceMultiplier(s.type); });

    document.getElementById('c-pnr').textContent   = pnr;
    document.getElementById('c-route').textContent = state.from + ' \u2192 ' + state.to;
    document.getElementById('c-bus').textContent   = state.bus.name;
    document.getElementById('c-time').textContent  = Utils.formatDate(state.date) + ', ' + state.bus.dep;
    document.getElementById('c-seats').textContent = seats.map(function(s) { return s.num; }).join(', ');
    document.getElementById('c-pax').textContent   = Summary.collectPassengerTypes(seats);
    document.getElementById('c-amt').textContent   = '\u20B9' + Math.round(total).toLocaleString('en-IN');

    Utils.show('overlay');
  }

  // ── Public: Close Modal & Reset ───────────────
  function closeModal() {
    Utils.hide('overlay');
    _reset();
  }

  function _reset() {
    state = { bus: null, seats: [], step: 1, maxSeats: 1, from: '', to: '', date: '' };

    Utils.hide('buses-card');
    Utils.hide('seats-card');
    Utils.hide('route-map-card');
    Utils.hide('sum-route-block');
    Utils.show('sum-default-head');

    Summary.reset();
    document.querySelectorAll('.bus-card').forEach(function(c) { c.classList.remove('selected'); });
    document.getElementById('seats-count-badge').textContent = '0 selected';
    document.getElementById('seat-count-val').textContent    = '1';

    _setStep(1);
    _updateCTA();
  }

  // ── Bootstrap ────────────────────────────────
  document.addEventListener('DOMContentLoaded', _init);

  return {
    searchBuses,
    selectBus,
    adjustCount,
    handleCTA,
    closeModal
  };

})();
