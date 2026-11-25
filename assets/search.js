/* PGW Feature Lab: site search.
   Index: assets/search-index.js (built by tools/build_search_index.py).
   Opens with the header button, Ctrl/Cmd+K, "/", or any element with [data-lab-search]. */
(function () {
  'use strict';
  var me = document.currentScript || document.querySelector('script[src$="assets/search.js"]');
  var BASE = me ? me.src.replace(/assets\/search\.js(\?.*)?$/, '') : '';
  var idx = null, loading = null, sel = 0, results = [];

  var css = '' +
    '.ls-btn{margin-left:auto;display:inline-flex;align-items:center;gap:8px;min-width:0;font:500 14px var(--sans,system-ui);color:var(--text-2,#475569);background:var(--bg,#F4F6F9);border:1px solid var(--border,#E2E8F0);border-radius:10px;padding:7px 10px 7px 12px;cursor:pointer;transition:border-color .2s,color .2s}' +
    '.ls-btn:hover{border-color:#BFDBFE;color:var(--accent,#1D4ED8)}' +
    '.ls-btn svg{width:16px;height:16px;flex:none}' +
    '.ls-btn kbd,.ls-hint kbd{font:11px var(--mono,monospace);background:#fff;border:1px solid var(--border,#E2E8F0);border-radius:5px;padding:1px 5px;color:var(--muted,#64748B)}' +
    '#lab-search{position:fixed;inset:0;z-index:100;display:none;background:rgba(15,23,42,.45);padding:8vh 16px 16px}' +
    '#lab-search.open{display:block}' +
    '.ls-box{max-width:760px;margin:0 auto;background:#fff;border-radius:16px;box-shadow:0 24px 60px rgba(15,23,42,.3);overflow:hidden;display:flex;flex-direction:column;max-height:84vh}' +
    '.ls-in{display:flex;align-items:center;gap:10px;padding:14px 16px;border-bottom:1px solid var(--border,#E2E8F0)}' +
    '.ls-in svg{width:20px;height:20px;color:var(--muted,#64748B);flex:none}' +
    '.ls-in input{flex:1;min-width:0;border:0;outline:0;font:500 17px var(--sans,system-ui);color:var(--ink,#0F172A);background:transparent}' +
    '.ls-in button{border:1px solid var(--border,#E2E8F0);background:#fff;border-radius:6px;font:12px var(--mono,monospace);color:var(--muted,#64748B);padding:3px 7px;cursor:pointer}' +
    '.ls-list{list-style:none;margin:0;padding:6px;overflow-y:auto}' +
    '.ls-list li a{display:block;padding:10px 12px;border-radius:10px;text-decoration:none;color:var(--ink,#0F172A)}' +
    '.ls-list li[aria-selected=true] a,.ls-list li a:hover{background:var(--accent-bg,#EFF6FF)}' +
    '.ls-h{font:600 15px var(--head,system-ui);display:block}' +
    '.ls-m{display:block;font:12px var(--mono,monospace);color:var(--muted,#64748B);margin-top:2px}' +
    '.ls-x{display:block;font-size:13.5px;color:var(--text-2,#475569);margin-top:3px;overflow-wrap:anywhere}' +
    '.ls-list mark{background:#FEF3C7;color:inherit;border-radius:3px;padding:0 1px}' +
    '.ls-k{display:inline-block;font:11px var(--mono,monospace);padding:0 6px;border-radius:999px;margin-right:6px;background:#F1F5F9;color:#334155}' +
    '.ls-k.Document{background:#EEF2FF;color:#3730A3}.ls-k.Scenario{background:#ECFDF5;color:#047857}.ls-k.Hub{background:#FFFBEB;color:#B45309}' +
    '.ls-empty,.ls-hint{padding:16px;color:var(--muted,#64748B);font-size:14px;margin:0}' +
    '.ls-hint{border-top:1px solid var(--border,#E2E8F0);display:flex;gap:14px;flex-wrap:wrap;font-size:12px}' +
    '.ls-flash{animation:lsflash 2.2s ease-out}' +
    '@keyframes lsflash{0%,30%{background:#FEF3C7;box-shadow:0 0 0 6px #FEF3C7}100%{background:transparent;box-shadow:0 0 0 6px transparent}}' +
    '@media (prefers-reduced-motion:reduce){.ls-flash{animation:none;outline:2px solid #F59E0B}}' +
    '@media (max-width:640px){.ls-btn .ls-t,.ls-btn kbd{display:none}#lab-search{padding:0}.ls-box{max-height:100vh;height:100vh;border-radius:0}}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  var ICON = '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="9" cy="9" r="6"/><path d="M13.5 13.5L17 17"/></svg>';
  var isMac = /Mac|iPhone|iPad/.test(navigator.platform || '');

  // Header button
  var hdr = document.querySelector('.lab-header .inner');
  if (hdr && !hdr.querySelector('.ls-btn')) {
    var b = document.createElement('button');
    b.type = 'button'; b.className = 'ls-btn'; b.setAttribute('aria-label', 'Search the Lab');
    b.innerHTML = ICON + '<span class="ls-t">Search</span><kbd>' + (isMac ? '⌘' : 'Ctrl') + ' K</kbd>';
    b.addEventListener('click', function () { open(''); });
    hdr.appendChild(b);
  }

  // Overlay
  var ov = document.createElement('div');
  ov.id = 'lab-search'; ov.setAttribute('role', 'dialog'); ov.setAttribute('aria-modal', 'true'); ov.setAttribute('aria-label', 'Search the Lab');
  ov.innerHTML = '<div class="ls-box"><div class="ls-in">' + ICON +
    '<input type="search" placeholder="Search pages, sections, fields, checks, scenarios" aria-label="Search" autocomplete="off" spellcheck="false" role="combobox" aria-expanded="true" aria-controls="ls-list">' +
    '<button type="button" aria-label="Close">Esc</button></div>' +
    '<ul class="ls-list" id="ls-list" role="listbox"></ul>' +
    '<p class="ls-hint"><span><kbd>↑</kbd> <kbd>↓</kbd> move</span><span><kbd>Enter</kbd> open</span><span>Search covers documents, visual pages and try-it scenarios.</span></p></div>';
  document.body.appendChild(ov);
  var inp = ov.querySelector('input'), list = ov.querySelector('.ls-list');
  ov.addEventListener('click', function (e) { if (e.target === ov) close(); });
  ov.querySelector('.ls-in button').addEventListener('click', close);

  function load() {
    if (idx) return Promise.resolve(idx);
    if (loading) return loading;
    loading = new Promise(function (res) {
      var sc = document.createElement('script');
      sc.src = BASE + 'assets/search-index.js';
      sc.onload = function () {
        var d = window.__labSearchIndex || { e: [] };
        idx = d.e.map(function (e) {
          return { f: e[0], p: e[1], k: e[2], h: e[3], u: e[4], x: e[5], lh: e[3].toLowerCase(), lp: (e[1] + ' ' + e[0]).toLowerCase(), lx: e[5].toLowerCase() };
        });
        res(idx);
      };
      sc.onerror = function () { idx = []; list.innerHTML = '<li class="ls-empty">Search is not available right now (the index could not be loaded).</li>'; res(idx); };
      document.head.appendChild(sc);
    });
    return loading;
  }

  var lastFocus = null;
  function open(q) {
    lastFocus = document.activeElement;
    ov.classList.add('open'); document.documentElement.style.overflow = 'hidden';
    inp.value = q || inp.value || ''; inp.focus(); inp.select();
    load().then(function () { run(); });
  }
  function close() {
    ov.classList.remove('open'); document.documentElement.style.overflow = '';
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }
  window.labSearch = { open: open, close: close, query: function (q) { return load().then(function () { return search(q); }); } };

  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function terms(q) { return q.toLowerCase().split(/[\s,;:()"'`]+/).map(function (t) { return t.replace(/^[^a-z0-9_#]+|[^a-z0-9_%]+$/g, ''); }).filter(function (t) { return t.length > 0; }); }

  function search(q) {
    var ts = terms(q); if (!ts.length || !idx) return [];
    var phrase = q.toLowerCase().trim(), out = [];
    for (var i = 0; i < idx.length; i++) {
      var e = idx[i], score = 0, ok = true;
      for (var j = 0; j < ts.length; j++) {
        var t = ts[j], s = 0, pos;
        if (t.indexOf('-') > -1 && e.lh.indexOf(t) < 0 && e.lx.indexOf(t) < 0) t = t.replace(/-/g, ' ');
        pos = e.lh.indexOf(t);
        if (pos > -1) s += (pos === 0 || /[^a-z0-9]/.test(e.lh[pos - 1])) ? 14 : 8;
        if (e.lp.indexOf(t) > -1) s += 4;
        pos = e.lx.indexOf(t);
        if (pos > -1) {
          var c = 0, k = pos; while (k > -1 && c < 6) { c++; k = e.lx.indexOf(t, k + t.length); }
          s += 2 + c;
          if (pos === 0 || /[^a-z0-9]/.test(e.lx[pos - 1])) s += 1;
        }
        if (!s) { ok = false; break; }
        score += s;
      }
      if (!ok) continue;
      if (ts.length > 1) { if (e.lh.indexOf(phrase) > -1) score += 20; else if (e.lx.indexOf(phrase) > -1) score += 8; }
      if (e.k === 'Scenario') score += 1;
      out.push({ e: e, s: score });
    }
    out.sort(function (a, b) { return b.s - a.s || a.e.h.length - b.e.h.length; });
    // at most 3 hits per page in the top list, so one long document does not crowd out the rest
    var per = {}, top = [], rest = [];
    out.forEach(function (r) { var k = r.e.u.split('#')[0]; per[k] = (per[k] || 0) + 1; (per[k] <= 3 ? top : rest).push(r); });
    return top.concat(rest).slice(0, 40);
  }

  function hl(text, ts) {
    var h = esc(text);
    ts.forEach(function (t) { if (t.length < 2) return; h = h.replace(new RegExp('(' + t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'ig'), '<mark>$1</mark>'); });
    return h;
  }
  function snippet(e, ts) {
    if (!e.x) return '';
    var p = -1; for (var i = 0; i < ts.length && p < 0; i++) p = e.lx.indexOf(ts[i]);
    if (p < 0) p = 0;
    var a = Math.max(0, p - 70), z = Math.min(e.x.length, p + 150);
    return (a > 0 ? '… ' : '') + e.x.slice(a, z) + (z < e.x.length ? ' …' : '');
  }

  function run() {
    var q = inp.value, ts = terms(q);
    if (!q.trim()) { list.innerHTML = '<li class="ls-empty">Type a word: a feature, field name, check, status or error, e.g. <em>deferredSplit</em>, <em>last-cent</em>, <em>rate file</em>.</li>'; results = []; return; }
    results = search(q); sel = 0;
    if (!results.length) { list.innerHTML = '<li class="ls-empty">No match for “' + esc(q) + '”. Try fewer or shorter words.</li>'; return; }
    list.innerHTML = results.map(function (r, i) {
      var e = r.e, meta = e.f + ' · ' + e.p;
      return '<li role="option" id="ls-o' + i + '" aria-selected="' + (i === 0) + '"><a href="' + esc(BASE + e.u) + '">' +
        '<span class="ls-h">' + hl(e.h, ts) + '</span>' +
        '<span class="ls-m"><span class="ls-k ' + esc(e.k.replace(/\s/g, '')) + '">' + esc(e.k) + '</span>' + esc(meta) + '</span>' +
        (e.x && e.k !== 'Scenario' ? '<span class="ls-x">' + hl(snippet(e, ts), ts) + '</span>' : '') + '</a></li>';
    }).join('');
    inp.setAttribute('aria-activedescendant', 'ls-o0');
  }
  function move(d) {
    if (!results.length) return;
    var items = list.querySelectorAll('li[role=option]');
    items[sel].setAttribute('aria-selected', 'false');
    sel = (sel + d + items.length) % items.length;
    items[sel].setAttribute('aria-selected', 'true');
    items[sel].scrollIntoView({ block: 'nearest' });
    inp.setAttribute('aria-activedescendant', 'ls-o' + sel);
  }
  var tmr; inp.addEventListener('input', function () { clearTimeout(tmr); tmr = setTimeout(function () { load().then(run); }, 60); });
  inp.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowDown') { e.preventDefault(); move(1); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); move(-1); }
    else if (e.key === 'Enter') { var a = list.querySelector('li[aria-selected=true] a'); if (a) { e.preventDefault(); go(a.getAttribute('href')); } }
  });
  list.addEventListener('click', function (e) { var a = e.target.closest('a'); if (a) { e.preventDefault(); go(a.getAttribute('href')); } });

  function go(href) {
    close();
    var u = new URL(href, location.href);
    if (u.pathname === location.pathname && u.hash) {
      if (location.hash === u.hash) flash(); else location.hash = u.hash;
    } else location.href = href;
  }

  document.addEventListener('keydown', function (e) {
    var typing = /INPUT|TEXTAREA|SELECT/.test((e.target || {}).tagName || '') || (e.target && e.target.isContentEditable);
    if ((e.ctrlKey || e.metaKey) && (e.key === 'k' || e.key === 'K')) { e.preventDefault(); ov.classList.contains('open') ? close() : open(''); }
    else if (e.key === '/' && !typing && !ov.classList.contains('open')) { e.preventDefault(); open(''); }
    else if (e.key === 'Escape' && ov.classList.contains('open')) { e.preventDefault(); close(); }
    else if (e.key === 'Tab' && ov.classList.contains('open')) {
      var f = ov.querySelectorAll('input,button,a[href]'); if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });

  // Any element with data-lab-search opens search (home page hero box)
  document.addEventListener('click', function (e) { var t = e.target.closest('[data-lab-search]'); if (t) { e.preventDefault(); open(t.value || ''); } });
  document.addEventListener('focusin', function (e) { var t = e.target.closest && e.target.closest('input[data-lab-search]'); if (t) { t.blur(); open(t.value || ''); } });

  // Highlight the section a search result pointed to
  function flash() {
    var h = decodeURIComponent(location.hash.slice(1)); if (!h || h.indexOf('=') > -1) return;
    var el = document.getElementById(h); if (!el) return;
    el.classList.remove('ls-flash'); void el.offsetWidth; el.classList.add('ls-flash');
  }
  window.addEventListener('hashchange', flash);
  if (document.readyState === 'complete') setTimeout(flash, 300); else window.addEventListener('load', function () { setTimeout(flash, 300); });
})();
