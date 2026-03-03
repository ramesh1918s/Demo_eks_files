/**
 * summary.js — Summary Panel & Passenger Form Builder
 * VayuBus Smart Bus Booking
 */

const Summary = (() => {

  /** Update the summary panel based on current bus + seats */
  function update(bus, seats) {
    if (!bus) return;

    document.getElementById('s-bus').textContent = bus.name;
    document.getElementById('s-dep').textContent = bus.dep + ' \u2192 ' + bus.arr;
    document.getElementById('s-dur').textContent = bus.dur;

    if (!seats || seats.length === 0) {
      Utils.hide('s-seats-row');
      document.getElementById('s-total').textContent = '0';
      return;
    }

    Utils.show('s-seats-row');

    let total = 0;
    const chips = seats.map(function(s) {
      const mult = Utils.priceMultiplier(s.type);
      total += bus.price * mult;
      const cls = Utils.typeClass(s.type);
      return '<span class="chip ' + cls + '">' + s.num + '\xB7' + s.type[0].toUpperCase() + '</span>';
    });

    document.getElementById('s-chips').innerHTML = chips.join('');
    document.getElementById('s-total').textContent = Math.round(total).toLocaleString('en-IN');
  }

  /** Render the passenger form for each selected seat */
  function buildPassengerForm(seats) {
    const pf     = document.getElementById('pax-form');
    const fields = document.getElementById('pax-fields');

    fields.innerHTML = '';

    seats.forEach(function(s, i) {
      const icon    = Utils.typeIcon(s.type);
      const label   = Utils.typeLabel(s.type);
      const ageHint = s.type === 'child' ? '5\u201312' : '25';
      const cls     = Utils.typeClass(s.type);

      const div = document.createElement('div');
      div.className = 'pax-block';
      div.innerHTML =
        '<div class="pax-block-title ' + cls + '">' +
          icon + ' ' + label + ' Passenger \u2014 Seat ' + s.num +
        '</div>' +
        '<div class="pax-row">' +
          '<div class="pf"><label for="p' + i + '-fn">First Name</label>' +
            '<input type="text" id="p' + i + '-fn" placeholder="First name"></div>' +
          '<div class="pf"><label for="p' + i + '-ln">Last Name</label>' +
            '<input type="text" id="p' + i + '-ln" placeholder="Last name"></div>' +
        '</div>' +
        '<div class="pax-row">' +
          '<div class="pf"><label for="p' + i + '-age">Age</label>' +
            '<input type="number" id="p' + i + '-age" placeholder="' + ageHint + '" min="1" max="120"></div>' +
          '<div class="pf"><label for="p' + i + '-id">ID Proof</label>' +
            '<select id="p' + i + '-id">' +
              '<option>Aadhaar</option>' +
              '<option>PAN</option>' +
              '<option>Passport</option>' +
              '<option>Driving Licence</option>' +
            '</select></div>' +
        '</div>';

      fields.appendChild(div);
    });

    pf.classList.remove('hidden');
    pf.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  /** Validate all passenger form fields. Returns error string or null */
  function validate(seats) {
    for (let i = 0; i < seats.length; i++) {
      const fn  = document.getElementById('p' + i + '-fn');
      const ln  = document.getElementById('p' + i + '-ln');
      const age = document.getElementById('p' + i + '-age');
      if (!fn || !fn.value.trim())  return 'Enter first name for Passenger ' + (i+1);
      if (!ln || !ln.value.trim())  return 'Enter last name for Passenger '  + (i+1);
      if (!age || !age.value.trim()) return 'Enter age for Passenger '        + (i+1);
    }
    const phone = document.getElementById('c-phone');
    const email = document.getElementById('c-email');
    if (!phone || !phone.value.trim()) return 'Enter contact phone number';
    if (!email || !email.value.trim()) return 'Enter contact email address';
    return null;
  }

  /** Collect passenger names for confirmation */
  function collectPassengerTypes(seats) {
    return seats.map(function(s) {
      return Utils.typeLabel(s.type);
    }).join(', ');
  }

  /** Reset the form */
  function reset() {
    const pf = document.getElementById('pax-form');
    pf.classList.add('hidden');
    document.getElementById('pax-fields').innerHTML = '';
    const phone = document.getElementById('c-phone');
    const email = document.getElementById('c-email');
    if (phone) phone.value = '';
    if (email) email.value = '';
    Utils.hide('s-seats-row');
    document.getElementById('s-total').textContent = '0';
    document.getElementById('s-chips').innerHTML   = '';
    document.getElementById('s-bus').textContent   = '\u2014';
    document.getElementById('s-dep').textContent   = '\u2014';
    document.getElementById('s-dur').textContent   = '\u2014';
  }

  return { update, buildPassengerForm, validate, collectPassengerTypes, reset };

})();
