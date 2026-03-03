/**
 * routeMap.js — Route Map Canvas Renderer & Timeline Builder
 * VayuBus Smart Bus Booking
 */

const RouteMap = (() => {

  /** Build and render route map for a given from/to pair */
  function render(from, to) {
    const key   = from + '-' + to;
    const keyRev = to + '-' + from;
    const data  = BusData.ROUTES[key] || BusData.ROUTES[keyRev] || BusData.ROUTES['default'];

    document.getElementById('route-distance').textContent = data.dist;
    _drawCanvas(data);
    _buildTimeline(data);
  }

  /** Draw the route on HTML canvas */
  function _drawCanvas(data) {
    const canvas = document.getElementById('mapCanvas');
    if (!canvas) return;

    const dpr  = window.devicePixelRatio || 1;
    const W    = canvas.offsetWidth  || 700;
    const H    = 140;

    canvas.width  = W * dpr;
    canvas.height = H * dpr;

    const ctx = canvas.getContext('2d');
    ctx.scale(dpr, dpr);

    // Background
    ctx.fillStyle = '#1a2234';
    ctx.fillRect(0, 0, W, H);

    // Grid
    ctx.strokeStyle = 'rgba(31,45,69,.5)';
    ctx.lineWidth = 0.5;
    for (let x = 0; x < W; x += 40) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke(); }
    for (let y = 0; y < H; y += 30) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke(); }

    const stops = data.stops;
    const n     = stops.length;

    // Generate control points with gentle wave
    const pts = stops.map((_, i) => ({
      x: 40 + (i / (n - 1)) * (W - 80),
      y: H / 2 + (i % 2 === 0 ? -16 : 16)
    }));

    // Glow path
    ctx.beginPath();
    ctx.moveTo(pts[0].x, pts[0].y);
    for (let i = 1; i < n; i++) {
      const mx = (pts[i-1].x + pts[i].x) / 2;
      const my = (pts[i-1].y + pts[i].y) / 2;
      ctx.quadraticCurveTo(pts[i-1].x, pts[i-1].y, mx, my);
    }
    ctx.lineTo(pts[n-1].x, pts[n-1].y);

    ctx.strokeStyle = 'rgba(0,212,170,.15)';
    ctx.lineWidth   = 8;
    ctx.stroke();

    ctx.strokeStyle = '#00d4aa';
    ctx.lineWidth   = 2;
    ctx.stroke();

    // Stop dots
    pts.forEach((p, i) => {
      const isOrigin = i === 0;
      const isDest   = i === n - 1;
      const r        = isOrigin || isDest ? 7 : 5;

      ctx.beginPath();
      ctx.arc(p.x, p.y, r, 0, Math.PI * 2);
      ctx.fillStyle = isOrigin ? '#00d4aa' : isDest ? '#3b82f6' : '#f59e0b';
      ctx.fill();
      ctx.strokeStyle = '#0d1117';
      ctx.lineWidth   = 2;
      ctx.stroke();

      // Label
      const lbl  = stops[i].split('(')[0].trim().slice(0, 10);
      const above = i % 2 === 0;
      ctx.font      = 'bold ' + (isOrigin || isDest ? 11 : 9) + 'px JetBrains Mono, monospace';
      ctx.fillStyle = isOrigin ? '#00d4aa' : isDest ? '#93c5fd' : '#fcd34d';
      ctx.textAlign = 'center';
      ctx.fillText(lbl, p.x, above ? p.y - 12 : p.y + 18);
    });

    // Bus icon mid-route
    const mid = pts[Math.floor(n / 2)];
    ctx.font      = '15px serif';
    ctx.textAlign = 'center';
    ctx.fillText('\uD83D\uDE8C', mid.x, mid.y - 4);
  }

  /** Build the stop timeline below the canvas */
  function _buildTimeline(data) {
    const container = document.getElementById('route-timeline');
    if (!container) return;

    container.innerHTML = '';
    data.stops.forEach(function(stop, i) {
      const isOrigin = i === 0;
      const isDest   = i === data.stops.length - 1;
      const dotClass = isOrigin ? 'origin' : isDest ? 'dest' : 'via';
      const badgeClass = isOrigin ? 'badge-origin' : isDest ? 'badge-dest' : 'badge-via';
      const badgeText  = isOrigin ? 'Origin' : isDest ? 'Dest' : 'Via';
      const subText    = isOrigin ? 'Boarding Point' : isDest ? 'Drop Point' : 'Via Stop';

      const row = document.createElement('div');
      row.className = 'route-stop';
      row.innerHTML =
        '<div class="stop-dot ' + dotClass + '"></div>' +
        '<div class="stop-info">' +
          '<div class="stop-name">' + stop + '</div>' +
          '<div class="stop-sub">'  + subText + '</div>' +
        '</div>' +
        '<div class="stop-time">' + (data.times[i] || '') + '</div>' +
        '<div style="margin-left:8px">' +
          '<span class="stop-badge ' + badgeClass + '">' + badgeText + '</span>' +
        '</div>';
      container.appendChild(row);
    });
  }

  return { render };

})();
