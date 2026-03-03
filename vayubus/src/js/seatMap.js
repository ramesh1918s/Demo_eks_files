/**
 * seatMap.js — Seat Map Builder & Interaction
 * VayuBus Smart Bus Booking
 */

const SeatMap = (() => {

  let _selectedSeats = [];   // [{ num, type }]
  let _maxSeats      = 1;
  let _onChangeCallback = null;

  /** Initialise seat map for given bus */
  function init(bus, maxSeats, onChangeCb) {
    _selectedSeats    = [];
    _maxSeats         = maxSeats;
    _onChangeCallback = onChangeCb;

    const lower = document.getElementById('chassis-lower');
    const upper = document.getElementById('chassis-upper');

    const totalSeats = bus.totalSeats;
    const half       = bus.decks === 2 ? Math.ceil(totalSeats / 2) : totalSeats;

    _buildDeck(lower, 1, half, bus.layout, bus.booked);

    if (bus.decks === 2) {
      Utils.show('upper-deck-wrap');
      _buildDeck(upper, half + 1, totalSeats, bus.layout, bus.booked);
    } else {
      Utils.hide('upper-deck-wrap');
    }

    _updatePanel();
  }

  /** Build one deck of seats */
  function _buildDeck(container, fromSeat, toSeat, layout, booked) {
    container.innerHTML =
      '<div class="driver-row"><div class="driver-seat-box">\uD83E\uDDD1\u200D\u2708\uFE0F</div></div>';

    const seatsPerRow = layout === '2+1' ? 3 : 4;
    const rows        = Math.ceil((toSeat - fromSeat + 1) / seatsPerRow);
    const cols        = layout === '2+1' ? [1, 2, 'a', 3] : [1, 2, 'a', 3, 4];

    for (let r = 0; r < rows; r++) {
      const row = document.createElement('div');
      row.className = 'seat-row';

      cols.forEach(function(col) {
        if (col === 'a') {
          const a = document.createElement('div');
          a.className = 'aisle';
          row.appendChild(a);
          return;
        }

        const sn = fromSeat + r * seatsPerRow + (col - 1);
        if (sn > toSeat) return;

        const el = document.createElement('div');
        el.className = 'seat';
        el.id        = 'seat-' + sn;
        el.textContent = sn;

        if (booked.indexOf(sn) > -1) {
          el.classList.add('booked');
        } else {
          // Visual default type pattern (decorative)
          if      (sn % 3 === 0) el.classList.add('male-seat');
          else if (sn % 5 === 0) el.classList.add('female-seat');
          else if (sn % 7 === 0) el.classList.add('child-seat');

          el.addEventListener('click', function() { _toggle(sn, el); });
        }

        row.appendChild(el);
      });

      container.appendChild(row);
    }
  }

  /** Toggle seat selection */
  function _toggle(sn, el) {
    const idx = _selectedSeats.findIndex(function(s) { return s.num === sn; });

    if (idx > -1) {
      _selectedSeats.splice(idx, 1);
      el.classList.remove('selected');
    } else {
      if (_selectedSeats.length >= _maxSeats) {
        Utils.toast('Max ' + _maxSeats + ' seat(s) allowed. Deselect one first.');
        return;
      }
      _selectedSeats.push({ num: sn, type: 'male' });
      el.classList.add('selected');
    }

    document.getElementById('seats-count-badge').textContent =
      _selectedSeats.length + ' selected';

    _updatePanel();
    if (_onChangeCallback) _onChangeCallback(_selectedSeats);
  }

  /** Re-render seat type assignment panel */
  function _updatePanel() {
    const container = document.getElementById('selected-seats-list');
    if (!container) return;

    if (_selectedSeats.length === 0) {
      container.innerHTML = '<p class="stp-empty">Select seats from the bus map</p>';
      return;
    }

    container.innerHTML = '';
    _selectedSeats.forEach(function(s, i) {
      const row = document.createElement('div');
      row.className = 'selected-seat-row';

      const mSel = s.type === 'male'   ? ' selected' : '';
      const fSel = s.type === 'female' ? ' selected' : '';
      const cSel = s.type === 'child'  ? ' selected' : '';

      row.innerHTML =
        '<span class="seat-id">Seat ' + s.num + '</span>' +
        '<select class="type-select" onchange="SeatMap.changeType(' + i + ', this.value)">' +
          '<option value="male"'   + mSel + '>\uD83D\uDC68 Male</option>'   +
          '<option value="female"' + fSel + '>\uD83D\uDC69 Female</option>' +
          '<option value="child"'  + cSel + '>\uD83E\uDDD2 Child</option>'  +
        '</select>' +
        '<div class="type-indicator" style="background:' + Utils.typeColor(s.type) + '"></div>';

      container.appendChild(row);
    });
  }

  /** Update type for a selected seat */
  function changeType(idx, type) {
    if (_selectedSeats[idx]) {
      _selectedSeats[idx].type = type;
    }
    // Update indicator colour in panel
    const rows = document.querySelectorAll('.selected-seat-row');
    if (rows[idx]) {
      const indicator = rows[idx].querySelector('.type-indicator');
      if (indicator) indicator.style.background = Utils.typeColor(type);
    }
    if (_onChangeCallback) _onChangeCallback(_selectedSeats);
  }

  /** Set new max seat count, trimming if needed */
  function setMax(max) {
    _maxSeats = max;
    while (_selectedSeats.length > _maxSeats) {
      const removed = _selectedSeats.pop();
      const el = document.getElementById('seat-' + removed.num);
      if (el) el.classList.remove('selected');
    }
    document.getElementById('seats-count-badge').textContent =
      _selectedSeats.length + ' selected';
    _updatePanel();
    if (_onChangeCallback) _onChangeCallback(_selectedSeats);
  }

  /** Get currently selected seats */
  function getSelected() {
    return _selectedSeats.slice();
  }

  return { init, changeType, setMax, getSelected };

})();
