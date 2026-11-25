/* datalicensingstandard.org: the home page's engraved device in motion. MIT License (build/LICENSE).
   The device is the cover's own engraving. It turns toward the pointer, and the switch sets what moves:
   IN, data streaming into the dissolve at its sides; OUT, data breaking off and flying toward the viewer;
   DUST, the engraving turning to dust where the pointer passes, then reforming; MATRIX, the whole device as a
   field of dust. After 5 seconds without pointer movement the device holds still and the script stops running until
   the next movement, a touch on the device or a press; it also sleeps while the device is out of view. No request leaves this site;
   without this script the page shows the engraving still. */
(function () {
  'use strict';
  var root = document.querySelector('[data-hero]');
  if (!root || !window.requestAnimationFrame || !window.Path2D) return;
  var stage = root.querySelector('[data-stage]');
  var tilt = root.querySelector('[data-tilt]');
  var cv3 = root.querySelector('[data-dust]');
  var cv2 = root.querySelector('[data-matrix]');
  var cvs = root.querySelector('[data-stream]');
  var fallback = root.querySelector('[data-fallback]');
  var sw = root.querySelector('[data-switch]');
  if (!stage || !tilt || !cv3 || !cv2 || !cvs) return;

  var A = '/assets/device/';
  var SW = 805, VX = 425, VY = 335, CX = 425, CY = 335, F = 1400, D2R = Math.PI / 180;
  // the follow, the dust, the stream
  var TURN = 14, TILT = 8, PERS = 1600, EASE = 7;
  var REACH = 115, FORCE = 3.8, SETTLE = 0.012, REFORM = 0.7;
  var mq = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : null;
  var reduce = !!(mq && mq.matches);
  if (mq) { var onRM = function () { reduce = mq.matches; }; if (mq.addEventListener) mq.addEventListener('change', onRM); else if (mq.addListener) mq.addListener(onRM); }
  var rnd = function (a, b) { return a + Math.random() * (b - a); };
  // a critically damped spring, exact for any frame time
  var crit = function (x, v, T, w, dt) { var e0 = x - T, k = Math.exp(-w * dt), c = v + w * e0; return [T + (e0 + c * dt) * k, (v - w * c * dt) * k]; };

  var s = {
    cx: null, cy: null, last: -1e9, lx: null, ly: null, pcx: null, pcy: null, pvx: 0, pvy: 0, lastMove: -1e9, onFace: false,
    yaw: 0, yv: 0, pitch: 0, pv: 0, lt: 0, y2: 0, p2: 0, ty2: 0, tp2: 0,
    active: 0, clean: false, drawn: false, inP: [], inS: [], outP: [], acc: [0, 0, 0, 0], streamClear: true,
    mode: 'in', seen: null, modeAt: -1e9, act: performance.now(), visible: true, running: false
  };
  var HOLD = 5000;                       // the device holds still after this long without pointer movement
  function awake(now) { return now - s.act < HOLD; }
  function kick() { if (!s.running && s.visible && s.started) { s.running = true; s.lt = 0; requestAnimationFrame(tick); } }
  function wake() { s.act = performance.now(); kick(); }
  var plate = null, P3 = null, P2 = null, T = null, mcv = null, mctx = null, mimg = null;

  // the switch
  function paint() {
    var on = s.mode === 'matrix' && !!P2;
    tilt.style.opacity = on ? '0' : '1';
    cv2.style.opacity = on ? '1' : '0';
    if (!sw) return;
    var bs = sw.querySelectorAll('button[data-mode]');
    for (var i = 0; i < bs.length; i++) bs[i].setAttribute('aria-pressed', bs[i].getAttribute('data-mode') === s.mode ? 'true' : 'false');
  }
  if (sw) {
    sw.addEventListener('click', function (e) {
      var b = e.target && e.target.closest ? e.target.closest('button[data-mode]') : null;
      if (!b) return;
      s.mode = b.getAttribute('data-mode');
      if (s.mode === 'dust') need3(); if (s.mode === 'matrix') need2();
      paint(); wake();
    });
    sw.hidden = false;
  }
  paint();

  // the turned plate: a point on screen <-> the same point on the plate
  function toLocal(px, py, W, H) {
    var ox = W * 0.5, oy = H * 0.55, a = s.yaw * D2R, b = -s.pitch * D2R, tx = s.yaw * 0.7, ty = s.pitch * 0.7;
    var sx = px - ox, sy = py - oy, ca = Math.cos(a), sa = Math.sin(a), cb = Math.cos(b), sb = Math.sin(b);
    var a11 = sx * sa / PERS - ca, a12 = -sb * (sx * ca / PERS + sa), a21 = sy * sa / PERS, a22 = -(sy * sb * ca / PERS + cb);
    var det = a11 * a22 - a12 * a21;
    if (Math.abs(det) < 1e-6) return [px, py];
    return [(-sx * a22 + a12 * sy) / det - tx + ox, (-a11 * sy + a21 * sx) / det - ty + oy];
  }
  var tq = { yaw: NaN, pitch: NaN, ca: 1, sa: 0, cb: 1, sb: 0 };
  function proj(lx, ly, W, H) {
    if (tq.yaw !== s.yaw || tq.pitch !== s.pitch) {
      tq.yaw = s.yaw; tq.pitch = s.pitch;
      tq.ca = Math.cos(s.yaw * D2R); tq.sa = Math.sin(s.yaw * D2R); tq.cb = Math.cos(-s.pitch * D2R); tq.sb = Math.sin(-s.pitch * D2R);
    }
    var ox = W * 0.5, oy = H * 0.55, U = lx - ox + s.yaw * 0.7, V = ly - oy + s.pitch * 0.7;
    var X = U * tq.ca + V * tq.sb * tq.sa, Y = V * tq.cb, Z = -U * tq.sa + V * tq.sb * tq.ca, w = 1 - Z / PERS;
    return [X / w + ox, Y / w + oy];
  }
  function hit(x, y, W) {
    if (!P3) return false;
    var sc = W / SW, gx = Math.floor(x / sc / 6), gy = Math.floor(y / sc / 6);
    if (gx < 0 || gy < 0 || gx >= P3.gw || gy >= P3.gh) return false;
    return P3.occ[gy * P3.gw + gx] === 1;
  }

  // one pointer for every setting
  function onStage(e) { var r = stage.getBoundingClientRect(); return e.clientX >= r.left && e.clientX <= r.right && e.clientY >= r.top && e.clientY <= r.bottom; }
  window.addEventListener('pointermove', function (e) {
    if (e.pointerType === 'touch' && !s.touchOn) return;
    var r = stage.getBoundingClientRect(), W = stage.clientWidth, H = stage.clientHeight, k = W / (r.width || 1);
    var mx = (e.clientX - r.left) * k, my = (e.clientY - r.top) * k;
    if (s.pcx !== null) { s.pvx = (e.clientX - s.pcx) * k; s.pvy = (e.clientY - s.pcy) * k; }
    s.pcx = e.clientX; s.pcy = e.clientY;
    var now = performance.now();
    if (s.lx !== null && Math.abs(s.pvx) + Math.abs(s.pvy) > 0.5) s.lastMove = now;
    s.lx = mx; s.ly = my; s.cx = e.clientX; s.cy = e.clientY; s.last = now;
    var w = window.innerWidth || 1440;
    s.ty2 = Math.max(-1, Math.min(1, (e.clientX - (r.left + r.width / 2)) / (w * 0.45))) * 24;
    s.tp2 = Math.max(-1, Math.min(1, (e.clientY - (r.top + r.height * 0.55)) / (w * 0.32))) * 8;
    var L = toLocal(mx, my, W, H);
    s.onFace = hit(L[0], L[1], W);
    wake();
  }, { passive: true });
  window.addEventListener('pointerdown', function (e) {
    if (e.pointerType === 'touch') { s.touchOn = onStage(e); if (!s.touchOn) return; }
    wake();
  }, { passive: true });
  window.addEventListener('pointerup', function (e) { if (e.pointerType === 'touch') s.touchOn = false; }, { passive: true });
  window.addEventListener('resize', function () { s.clean = false; kick(); }, { passive: true });
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (es) {
      s.visible = es[es.length - 1].isIntersecting;
      if (s.visible) kick();
    }, { rootMargin: '200px 0px' }).observe(root);
  }
  document.documentElement.addEventListener('pointerleave', function () { s.cx = null; s.last = -1e9; s.lx = null; s.pcx = null; s.onFace = false; });

  // the device's data: the plate, its grains, the dust field, the dissolve's blocks
  var im = new Image();
  im.onload = function () { plate = im; s.clean = false; };
  im.src = A + 'plate.webp';
  function getJSON(u, f) { fetch(u).then(function (r) { return r.json(); }).then(f).catch(function () {}); }
  var asked3 = false, asked2 = false;
  function need3() { if (asked3) return; asked3 = true; getJSON(A + 'touch.json', load3); }
  function need2() { if (asked2) return; asked2 = true; getJSON(A + 'dust.json', load2); }
  function load3(d) {
    var n = d.p.length / 3, gw = d.gw, gh = d.gh, i, x, y;
    var P = { n: n, gw: gw, gh: gh, hx: new Float32Array(n), hy: new Float32Array(n), r: new Float32Array(n), ox: new Float32Array(n), oy: new Float32Array(n), vx: new Float32Array(n), vy: new Float32Array(n), dz: new Float32Array(n), lt: new Float64Array(n), rd: new Float32Array(n), cell: new Int32Array(n), occ: new Uint8Array(gw * gh) };
    var own = new Uint8Array(gw * gh);
    for (i = 0; i < n; i++) {
      P.hx[i] = d.p[i * 3]; P.hy[i] = d.p[i * 3 + 1]; P.r[i] = d.p[i * 3 + 2] / 20; P.rd[i] = Math.random() * 0.5;
      P.cell[i] = Math.floor(P.hy[i] / 6) * gw + Math.floor(P.hx[i] / 6);
      own[P.cell[i]] = 1;
    }
    for (y = 0; y < gh; y++) for (x = 0; x < gw; x++) {
      if (!own[y * gw + x]) continue;
      for (var j = -2; j <= 2; j++) for (var q = -2; q <= 2; q++) {
        var X = x + q, Y = y + j;
        if (X >= 0 && Y >= 0 && X < gw && Y < gh) P.occ[Y * gw + X] = 1;
      }
    }
    mcv = document.createElement('canvas'); mcv.width = gw; mcv.height = gh;
    mctx = mcv.getContext('2d'); mimg = mctx.createImageData(gw, gh);
    P3 = P; kick();
  }
  function load2(d) {
    var n = d.p.length / 4;
    var P = { n: n, hx: new Float32Array(n), hy: new Float32Array(n), hz: new Float32Array(n), r: new Float32Array(n), ox: new Float32Array(n), oy: new Float32Array(n), vx: new Float32Array(n), vy: new Float32Array(n) };
    for (var i = 0; i < n; i++) { P.hx[i] = d.p[i * 4]; P.hy[i] = d.p[i * 4 + 1]; P.hz[i] = d.p[i * 4 + 2]; P.r[i] = d.p[i * 4 + 3] / 20; }
    P2 = P;
    var mb = sw ? sw.querySelector('button[data-mode="matrix"]') : null;
    if (mb) mb.disabled = false;
    paint(); kick();
  }
  function later(f) { if (window.requestIdleCallback) window.requestIdleCallback(f, { timeout: 2000 }); else setTimeout(f, 1200); }
  // the first frame waits for the page to load, so the device's motion never competes with the page's first paint
  function start() { s.started = true; s.act = performance.now(); kick(); later(function () { need3(); need2(); }); }
  if (document.readyState === 'complete') later(start); else window.addEventListener('load', function () { later(start); });
  getJSON(A + 'debris.json', function (d) {
    var L = [], R = [];
    for (var i = 0; i < d.p.length; i += 4) {
      if (d.p[i + 3] < 25) continue;
      (d.p[i] < 425 ? L : R).push(d.p[i] + 1.5, d.p[i + 1] + 1.5);
    }
    T = [L, R];
  });

  // DUST: the dust field's physics, waking only where the pointer moves through the engraving
  function physics3(sc, mx, my, now, dustOn) {
    var P = P3, R2 = REACH * REACH, waking = dustOn && now - s.lastMove < 140 && s.onFace, active = 0;
    for (var n = 0; n < P.n; n++) {
      var dz = P.dz[n], bx = P.hx[n] * sc, by = P.hy[n] * sc;
      var dx = bx + P.ox[n] - mx, dy = by + P.oy[n] - my, d2 = dx * dx + dy * dy, near = d2 < R2;
      if (dz === 0 && (!waking || !near)) continue;
      if (near && dustOn && awake(now)) {
        var d = Math.sqrt(d2) + 0.01, qq = 1 - d / REACH, q2 = qq * qq;
        P.vx[n] += dx / d * q2 * FORCE + s.pvx * qq * 0.24 - dy / d * q2 * 0.9 + (Math.random() - 0.5) * qq * 2.2;
        P.vy[n] += dy / d * q2 * FORCE + s.pvy * qq * 0.24 + dx / d * q2 * 0.9 + (Math.random() - 0.5) * qq * 2.2;
        if (qq * 2.2 > dz) dz = Math.min(1, qq * 2.2);
        if (qq > 0.15) P.lt[n] = now;
      }
      P.vx[n] = (P.vx[n] - P.ox[n] * SETTLE + (Math.random() - 0.5) * 0.05) * 0.925;
      P.vy[n] = (P.vy[n] - P.oy[n] * SETTLE + (Math.random() - 0.5) * 0.05) * 0.925;
      P.ox[n] += P.vx[n]; P.oy[n] += P.vy[n];
      var disp = Math.abs(P.ox[n]) + Math.abs(P.oy[n]);
      if (disp > 3) dz = 1;
      if ((now - P.lt[n]) / 1000 > REFORM + P.rd[n] && disp < 1.5 && Math.abs(P.vx[n]) + Math.abs(P.vy[n]) < 0.2) {
        dz *= 0.95;
        if (dz < 0.01) { dz = 0; P.ox[n] = 0; P.oy[n] = 0; P.vx[n] = 0; P.vy[n] = 0; }
      }
      P.dz[n] = dz;
      if (dz > 0) active++;
    }
    s.active = active;
  }
  function drawPlate(W, H, sc, dpr) {
    var P = P3, CWp = Math.round(W * 1.2 * dpr), CHp = Math.round(H * 1.24 * dpr), n, b;
    if (cv3.width !== CWp || cv3.height !== CHp) { cv3.width = CWp; cv3.height = CHp; s.clean = false; }
    if (s.active === 0 && s.clean) return;
    var ctx = cv3.getContext('2d');
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.globalCompositeOperation = 'source-over'; ctx.globalAlpha = 1;
    ctx.clearRect(0, 0, CWp, CHp);
    ctx.setTransform(dpr, 0, 0, dpr, Math.round(W * 0.10 * dpr), Math.round(H * 0.18 * dpr));
    ctx.drawImage(plate, 0, 0, W, H);
    if (!s.drawn) { s.drawn = true; if (fallback) fallback.style.opacity = '0'; }
    if (s.active === 0 || !P) { s.clean = true; return; }
    s.clean = false;
    var md = mimg.data;
    md.fill(0);
    for (n = 0; n < P.n; n++) { if (P.dz[n] > 0) md[P.cell[n] * 4 + 3] = Math.round(P.dz[n] * 255); }
    mctx.putImageData(mimg, 0, 0);
    ctx.globalCompositeOperation = 'destination-out';
    ctx.imageSmoothingEnabled = false;
    ctx.drawImage(mcv, 0, 0, P.gw * 6 * sc, P.gh * 6 * sc);
    ctx.imageSmoothingEnabled = true;
    ctx.globalCompositeOperation = 'source-over';
    var NB = 12, paths = [];
    for (b = 0; b < NB; b++) paths.push(new Path2D());
    for (n = 0; n < P.n; n++) {
      var dz = P.dz[n];
      if (dz <= 0) continue;
      var ox = P.ox[n], oy = P.oy[n], disp = Math.abs(ox) + Math.abs(oy);
      var px = P.hx[n] * sc + ox, py = P.hy[n] * sc + oy, a, rr;
      if (disp > 3) { a = 0.55 * dz; rr = Math.max(0.5, P.r[n] * sc * Math.max(0.35, 1 - disp / 260)); }
      else { a = dz; rr = P.r[n] * sc; }
      b = Math.min(NB - 1, Math.round(a * (NB - 1)));
      if (b === 0) continue;
      paths[b].moveTo(px + rr, py); paths[b].arc(px, py, rr, 0, 6.2832);
    }
    ctx.fillStyle = '#000000';
    for (b = 1; b < NB; b++) { ctx.globalAlpha = b / (NB - 1); ctx.fill(paths[b]); }
    ctx.globalAlpha = 1;
  }

  // MATRIX: the whole device as a field of dust, turning in depth
  function drawMatrix(W, H, sc, dpr, ts, mx, my) {
    var P = P2, idle = ts - s.last > 2600;
    var ty = reduce ? 0 : (idle ? Math.sin(ts / 2600) * 9 : s.ty2);
    var tp = reduce ? 0 : (idle ? Math.sin(ts / 3400) * 3 : s.tp2);
    var k = idle ? 0.03 : 0.09;
    s.y2 += (ty - s.y2) * k; s.p2 += (tp - s.p2) * k;
    var CWp = Math.round(W * 1.2 * dpr), CHp = Math.round(H * 1.24 * dpr);
    if (cv2.width !== CWp || cv2.height !== CHp) { cv2.width = CWp; cv2.height = CHp; }
    var ctx = cv2.getContext('2d');
    ctx.setTransform(dpr, 0, 0, dpr, W * 0.10 * dpr, H * 0.18 * dpr);
    ctx.clearRect(-W * 0.10, -H * 0.18, W * 1.2, H * 1.24);
    var t = s.y2 * D2R, p = s.p2 * D2R, ct = Math.cos(t), st = Math.sin(t), cp = Math.cos(p), sp = Math.sin(p);
    var R2 = REACH * REACH, settled = new Path2D(), loose = new Path2D();
    for (var n = 0; n < P.n; n++) {
      var X = P.hx[n] - CX, Y = P.hy[n] - CY, Z = P.hz[n];
      var X1 = X * ct + Z * st, Z1 = -X * st + Z * ct, Y2 = Y * cp + Z1 * sp, Z2 = -Y * sp + Z1 * cp;
      var f = F / (F - Z2), bx = (CX + X1 * f) * sc, by = (CY + Y2 * f) * sc;
      var dx = bx + P.ox[n] - mx, dy = by + P.oy[n] - my, d2 = dx * dx + dy * dy;
      if (d2 < R2) {
        var d = Math.sqrt(d2) + 0.01, qq = 1 - d / REACH, q2 = qq * qq;
        P.vx[n] += dx / d * q2 * FORCE + s.pvx * qq * 0.24 - dy / d * q2 * 0.9 + (Math.random() - 0.5) * qq * 2.2;
        P.vy[n] += dy / d * q2 * FORCE + s.pvy * qq * 0.24 + dx / d * q2 * 0.9 + (Math.random() - 0.5) * qq * 2.2;
      }
      P.vx[n] = (P.vx[n] - P.ox[n] * SETTLE + (Math.random() - 0.5) * 0.05) * 0.925;
      P.vy[n] = (P.vy[n] - P.oy[n] * SETTLE + (Math.random() - 0.5) * 0.05) * 0.925;
      P.ox[n] += P.vx[n]; P.oy[n] += P.vy[n];
      var disp = Math.abs(P.ox[n]) + Math.abs(P.oy[n]), px = bx + P.ox[n], py = by + P.oy[n], rr;
      if (disp > 3) { rr = Math.max(0.5, P.r[n] * sc * Math.max(0.35, 1 - disp / 260)); loose.moveTo(px + rr, py); loose.arc(px, py, rr, 0, 6.2832); }
      else { rr = P.r[n] * sc * f; settled.moveTo(px + rr, py); settled.arc(px, py, rr, 0, 6.2832); }
    }
    ctx.fillStyle = '#000000'; ctx.fill(settled);
    ctx.fillStyle = 'rgba(0, 0, 0, 0.55)'; ctx.fill(loose);
  }

  // IN and OUT: data into the dissolve, or out at the viewer, in the dissolve's own blocks
  var SMALL = [4, 4, 5, 5, 5], BIG = [10, 12, 12, 13, 13];
  var POLY = [[[0, 0], [1, 0]], [[0, 0], [0, 1]], [[0, 0], [1, 0], [1, 1]], [[0, 0], [1, 0], [0, 1], [1, 1]], [[0, 0], [1, 0], [2, 0], [1, 1]], [[0, 0], [1, 0], [1, 1], [2, 1]]];
  function pick(side) { var L = T[side < 0 ? 0 : 1], i = Math.floor(Math.random() * L.length / 2) * 2; return [L[i], L[i + 1]]; }
  function spawnIn(side, g) {
    var h = pick(side), lx = h[0] * g.sc, ly = h[1] * g.sc;
    var big = Math.random() < 0.38, cluster = Math.random() < (big ? 0.25 : 0.4);
    var size = (big ? BIG : SMALL)[Math.floor(Math.random() * 5)];
    var tp = proj(lx, ly, g.W, g.H), tx = tp[0] + g.sox, ty = tp[1] + g.soy;
    var x0 = side < 0 ? -rnd(10, 90) : g.CW + rnd(10, 90);
    var y0 = Math.max(10, Math.min(g.CH - 10, ty + rnd(-0.55, 0.55) * g.H));
    var dist = Math.hypot(tx - x0, ty - y0);
    s.inP.push({ lx: lx, ly: ly, x0: x0, y0: y0, cx: (x0 + tx) / 2 - (ty - y0) * rnd(-0.28, 0.28), cy: (y0 + ty) / 2 + (tx - x0) * rnd(-0.28, 0.28), size: size * g.sc, cells: cluster ? POLY[Math.floor(Math.random() * POLY.length)] : [[0, 0]], tone: rnd(0.16, 0.62), rot0: rnd(1.2, 3.6) * (Math.random() < 0.5 ? -1 : 1), t: 0, dur: (dist / rnd(260, 430)) * (big ? 1.18 : 1), ab: -1 });
  }
  function spawnSpeck(side, g) {
    var h = pick(side), lx = h[0] * g.sc, ly = h[1] * g.sc;
    var tp = proj(lx, ly, g.W, g.H), tx = tp[0] + g.sox, ty = tp[1] + g.soy;
    var x0 = side < 0 ? -rnd(4, 40) : g.CW + rnd(4, 40);
    var y0 = Math.max(4, Math.min(g.CH - 4, ty + rnd(-0.4, 0.4) * g.H));
    s.inS.push({ lx: lx, ly: ly, x0: x0, y0: y0, size: rnd(1.1, 2.2), tone: rnd(0.25, 0.6), t: 0, dur: Math.hypot(tx - x0, ty - y0) / rnd(520, 820) });
  }
  function spawnOut(side, speck, g) {
    var h = pick(side);
    var big = !speck && Math.random() < 0.38, cluster = !speck && Math.random() < (big ? 0.25 : 0.4);
    var size = speck ? rnd(1.6, 2.6) / g.sc : (big ? BIG : SMALL)[Math.floor(Math.random() * 5)];
    var lp = proj(h[0] * g.sc, h[1] * g.sc, g.W, g.H), vp = proj(VX * g.sc, VY * g.sc, g.W, g.H);
    s.outP.push({ vpx: vp[0], vpy: vp[1], X: lp[0] - vp[0], Y: lp[1] - vp[1], Z: 0,
      vX: side * rnd(20, 120), vY: rnd(-55, 40), vZ: speck ? rnd(330, 560) : rnd(170, 360),
      size: size * g.sc, cells: cluster ? POLY[Math.floor(Math.random() * POLY.length)] : [[0, 0]],
      tone: speck ? rnd(0.3, 0.6) : rnd(0.18, 0.62), rot: rnd(0, 6.2832), wr: rnd(-2.4, 2.4), fl: rnd(0, 6.2832), wf: speck ? 0 : rnd(-3.2, 3.2), age: 0 });
  }
  function drawStream(W, H, sc, dt, now) {
    var spawning = !reduce && (s.mode === 'in' || s.mode === 'out') && awake(now), i, p;
    if (!spawning && !s.inP.length && !s.inS.length && !s.outP.length) {
      if (!s.streamClear) { var c0 = cvs.getContext('2d'); c0.setTransform(1, 0, 0, 1, 0, 0); c0.clearRect(0, 0, cvs.width, cvs.height); s.streamClear = true; }
      return;
    }
    s.streamClear = false;
    // the stream canvas is the viewport's width and starts 40% of the device's height above it (site.css)
    var CW = s.cw, CH = s.ch;
    var g = { sc: sc, sox: (CW - W) / 2, soy: H * 0.40, W: W, H: H, CW: CW, CH: CH };
    var dens = reduce ? 0 : 1;
    if (spawning) {
      var out = s.mode === 'out';
      for (var side = 0; side < 2; side++) {
        var sd = side ? 1 : -1;
        s.acc[side] += dt * (out ? 7.5 : 9) * dens;
        while (s.acc[side] >= 1) { s.acc[side] -= 1; if (out) spawnOut(sd, false, g); else spawnIn(sd, g); }
        if (!reduce) {
          s.acc[side + 2] += dt * (out ? 18 : 22) * dens;
          while (s.acc[side + 2] >= 1) { s.acc[side + 2] -= 1; if (out) spawnOut(sd, true, g); else spawnSpeck(sd, g); }
        }
      }
    }
    var dpr = Math.min(1.25, window.devicePixelRatio || 1), CWp = Math.round(CW * dpr), CHp = Math.round(CH * dpr);
    if (cvs.width !== CWp || cvs.height !== CHp) { cvs.width = CWp; cvs.height = CHp; }
    var ctx = cvs.getContext('2d');
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, CW, CH);
    ctx.fillStyle = '#000000';
    var keep = [];
    for (i = 0; i < s.inP.length; i++) {
      p = s.inP[i];
      var tp = proj(p.lx, p.ly, W, H), tx = tp[0] + g.sox, ty = tp[1] + g.soy, x, y, rot, a, sz = p.size;
      if (p.ab < 0) {
        p.t += dt / p.dur;
        var t = Math.min(1, p.t), e = 1 - Math.pow(1 - t, 2.2), m = 1 - e;
        x = m * m * p.x0 + 2 * m * e * p.cx + e * e * tx;
        y = m * m * p.y0 + 2 * m * e * p.cy + e * e * ty;
        rot = p.rot0 * Math.pow(1 - e, 1.6);
        a = p.tone * Math.min(1, p.t * 6);
        if (p.t >= 1) p.ab = 0;
      } else {
        p.ab += dt / 0.75;
        x = tx; y = ty; rot = 0;
        a = p.tone * Math.max(0, 1 - p.ab);
        sz = p.size * (1 - 0.35 * Math.min(1, p.ab));
      }
      if (p.ab >= 1) continue;
      keep.push(p);
      ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.globalAlpha = a;
      for (var c = 0; c < p.cells.length; c++) ctx.fillRect((p.cells[c][0] - 0.5) * sz, (p.cells[c][1] - 0.5) * sz, sz, sz);
      ctx.restore();
    }
    s.inP = keep;
    var keepS = [];
    for (i = 0; i < s.inS.length; i++) {
      p = s.inS[i];
      p.t += dt / p.dur;
      if (p.t >= 1) continue;
      var tq = proj(p.lx, p.ly, W, H), ex = tq[0] + g.sox, ey = tq[1] + g.soy, u = p.t * p.t * (3 - 2 * p.t);
      ctx.globalAlpha = p.tone * Math.min(1, p.t * 8) * Math.min(1, (1 - p.t) * 6);
      ctx.fillRect(p.x0 + (ex - p.x0) * u - p.size / 2, p.y0 + (ey - p.y0) * u - p.size / 2, p.size, p.size);
      keepS.push(p);
    }
    s.inS = keepS;
    var FZ = 900, keepO = [];
    for (i = 0; i < s.outP.length; i++) {
      p = s.outP[i];
      p.age += dt; p.X += p.vX * dt; p.Y += p.vY * dt; p.Z += p.vZ * dt; p.rot += p.wr * dt; p.fl += p.wf * dt;
      if (p.Z > FZ * 0.9) continue;
      var f = FZ / (FZ - p.Z), ox = p.vpx + g.sox + p.X * f, oy = p.vpy + g.soy + p.Y * f, osz = p.size * f, ext = osz * 3;
      if (ox < -ext || ox > CW + ext || oy < -ext || oy > CH + ext) continue;
      p.f = f; p.x = ox; p.y = oy; p.sz = osz;
      keepO.push(p);
    }
    keepO.sort(function (u1, u2) { return u1.Z - u2.Z; });
    for (i = 0; i < keepO.length; i++) {
      p = keepO[i];
      var al = p.tone * Math.min(1, p.age / 0.3) * (p.f > 2.6 ? Math.max(0, 1 - (p.f - 2.6) / 3.4) : 1);
      if (al <= 0.004) continue;
      ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.rot); ctx.scale(Math.max(0.14, Math.abs(Math.cos(p.fl))), 1); ctx.globalAlpha = al;
      for (var cc = 0; cc < p.cells.length; cc++) ctx.fillRect((p.cells[cc][0] - 0.5) * p.sz, (p.cells[cc][1] - 0.5) * p.sz, p.sz, p.sz);
      ctx.restore();
    }
    s.outP = keepO;
    ctx.globalAlpha = 1;
  }

  // every frame: read the layout first, write after; sleep when nothing moves
  function tick(ts) {
    if (!s.visible) { s.running = false; return; }
    var now = performance.now();
    var dt = Math.min(0.05, s.lt ? (ts - s.lt) / 1000 : 1 / 60); s.lt = ts;
    var r = stage.getBoundingClientRect(), W = stage.clientWidth, H = stage.clientHeight;
    s.cw = cvs.clientWidth; s.ch = cvs.clientHeight;
    if (s.mode !== s.seen) { if (s.mode === 'matrix') { s.y2 = s.yaw; s.p2 = s.pitch; } s.prev = s.seen; s.seen = s.mode; s.modeAt = now; s.clean = false; }
    var kk = W / (r.width || 1), sc = W / SW, dpr = Math.min(2, window.devicePixelRatio || 1), on = awake(now);
    var gy = 0, gp = 0;
    if (!reduce && s.cx !== null) {
      gy = Math.tanh((s.cx - (r.left + r.width / 2)) / (r.width * 0.55));
      gp = Math.tanh((s.cy - (r.top + r.height * 0.52)) / (r.width * 0.42));
    }
    var sy = crit(s.yaw, s.yv, gy * TURN, EASE, dt), spp = crit(s.pitch, s.pv, gp * TILT, EASE, dt);
    var turning = Math.abs(sy[0] - s.yaw) + Math.abs(spp[0] - s.pitch) > 0.0005;
    s.yaw = sy[0]; s.yv = sy[1]; s.pitch = spp[0]; s.pv = spp[1];
    if (turning) tilt.style.transform = 'perspective(' + PERS + 'px) rotateY(' + s.yaw.toFixed(3) + 'deg) rotateX(' + (-s.pitch).toFixed(3) + 'deg) translate3d(' + (s.yaw * 0.7).toFixed(2) + 'px,' + (s.pitch * 0.7).toFixed(2) + 'px,0)';
    s.pvx *= 0.82; s.pvy *= 0.82;
    var mx = -9999, my = -9999;
    if (s.cx !== null) { var L = toLocal((s.cx - r.left) * kk, (s.cy - r.top) * kk, W, H); mx = L[0]; my = L[1]; }
    if (plate) {
      var dustOn = s.mode === 'dust';
      if (P3 && (dustOn || s.active > 0)) physics3(sc, mx, my, now, dustOn);
      if (s.mode !== 'matrix' || now - s.modeAt < 700 || !s.clean) drawPlate(W, H, sc, dpr);
    }
    var matrixLive = P2 && ((s.mode === 'matrix' && on) || (now - s.modeAt < 700 && (s.mode === 'matrix' || s.prev === 'matrix')));
    if (matrixLive) drawMatrix(W, H, sc, dpr, ts, s.cx !== null ? (s.cx - r.left) * kk : -9999, s.cx !== null ? (s.cy - r.top) * kk : -9999);
    if (T) drawStream(W, H, sc, dt, now);
    var busy = (on && (!reduce || s.mode === 'dust' || s.mode === 'matrix')) || turning || s.active > 0 || (!s.clean && plate) || matrixLive || s.inP.length || s.inS.length || s.outP.length || !s.streamClear;
    if (busy) requestAnimationFrame(tick); else s.running = false;
  }
})();
