/* Team-progress dashboard logic (docs/progress.html). Pure functions first, so
   `node scripts/test_progress.js` can check the merge without a browser; the DOM
   part at the bottom runs only in a page.

   Data comes from the Firebase Realtime Database that docs/javascripts/extra.js
   writes to, one document per (day, team, device):

     progress/<YYYY-MM-DD>/<team>/<dev> = {
       team, dev, zone, ts, srv, page,
       pages: { "session-1": { ts, acts: { a1: {done,total,filled,nf}, ... } }, ... },
       last:  { page, act, label, on, ts }
     }

   The dashboard streams progress/<day>.json with EventSource (Firebase REST
   streaming), keeps the raw tree, and rebuilds a per-team view on every event. */
(function (root, factory) {
  if (typeof module === "object" && module.exports) module.exports = factory();
  else root.Progress = factory();
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  var TEAM_MAX = 100;
  var STALE_MS = 10 * 60 * 1000;

  /* Firebase serialises a node whose keys are mostly small integers as an array, with null
     for the gaps -- exactly what a day of teams 1..100 looks like. Back to an object, no gaps. */
  function objectify(data) {
    if (!Array.isArray(data)) return data;
    var out = {};
    data.forEach(function (v, i) { if (v !== null && v !== undefined) out[String(i)] = v; });
    return out;
  }

  /* ---- Firebase REST streaming: apply a put/patch at a "/a/b" path ---- */
  function applyEvent(tree, kind, path, data) {
    var parts = String(path || "/").split("/").filter(Boolean);
    if (kind === "put" && parts.length === 0) return objectify(data) || {};
    tree = objectify(tree) || {};
    var node = tree;
    for (var i = 0; i < parts.length - 1; i++) {
      if (typeof node[parts[i]] !== "object" || node[parts[i]] === null) node[parts[i]] = {};
      node = node[parts[i]];
    }
    var leaf = parts[parts.length - 1];
    if (kind === "patch") {
      var target = leaf === undefined ? node : (node[leaf] = (typeof node[leaf] === "object" && node[leaf]) || {});
      Object.keys(data || {}).forEach(function (k) {
        if (data[k] === null) delete target[k]; else target[k] = data[k];
      });
    } else if (data === null || data === undefined) {
      delete node[leaf];
    } else {
      node[leaf] = data;
    }
    return tree;
  }

  /* ---- merge the devices of one team into one view of one page ---- */
  function num(x) { return typeof x === "number" && isFinite(x) ? x : 0; }

  /* activities of one reported page in worksheet order. The database sorts keys, so the
     worksheet sends `order`; documents without it (older) fall back to: lists before the
     first activity first, then a1, a2, ... numerically. */
  function pageOrder(src) {
    var acts = (src && src.acts) || {};
    var order = objectify(src && src.order);
    var out = [];
    if (order) Object.keys(order).map(function (k) { return order[k]; }).forEach(function (a) { if (acts[a] && out.indexOf(a) < 0) out.push(a); });
    var rest = Object.keys(acts).filter(function (a) { return out.indexOf(a) < 0; });
    rest.sort(function (x, y) {
      var mx = /^a(\d+)$/.exec(x), my = /^a(\d+)$/.exec(y);
      if (mx && my) return +mx[1] - +my[1];
      if (mx) return 1;
      if (my) return -1;
      return x < y ? -1 : x > y ? 1 : 0;
    });
    return out.concat(rest);
  }

  function teamView(teamNo, devices) {
    var v = { team: teamNo, zone: "", ts: 0, srv: 0, devs: 0, pages: {}, last: null };
    Object.keys(devices || {}).forEach(function (devId) {
      var d = devices[devId];
      if (!d || typeof d !== "object") return;
      v.devs++;
      var srv = num(d.srv) || num(d.ts);
      if (srv >= v.srv) { v.srv = srv; v.ts = num(d.ts); if (d.zone) v.zone = d.zone; }
      if (d.last && num(d.last.ts) > (v.last ? num(v.last.ts) : -1)) v.last = d.last;
      Object.keys(d.pages || {}).forEach(function (pg) {
        var src = d.pages[pg], dst = v.pages[pg] || (v.pages[pg] = { ts: 0, order: [], acts: {}, names: {}, steps: {} });
        dst.ts = Math.max(dst.ts, num(src && src.ts));
        var nm = (src && src.names) || {};
        Object.keys(nm).forEach(function (a) { if (typeof nm[a] === "string" && nm[a]) dst.names[a] = nm[a]; });
        var st = objectify(src && src.steps) || {};
        Object.keys(st).forEach(function (a) {                       // per task box: ticked on any device counts
          var list = objectify(st[a]) || {}, dstList = dst.steps[a] || (dst.steps[a] = []);
          Object.keys(list).forEach(function (i) {
            var s = list[i] || {}, k = +i;
            if (!dstList[k]) dstList[k] = { l: "", on: 0 };
            if (s.l && !dstList[k].l) dstList[k].l = String(s.l);
            if (num(s.on)) dstList[k].on = 1;
          });
        });
        pageOrder(src).forEach(function (a) {
          var s = src.acts[a] || {}, t = dst.acts[a];
          if (!t) { t = dst.acts[a] = { done: 0, total: 0, filled: 0, nf: 0 }; dst.order.push(a); }
          t.done = Math.max(t.done, num(s.done));
          t.total = Math.max(t.total, num(s.total));
          t.filled = Math.max(t.filled, num(s.filled));
          t.nf = Math.max(t.nf, num(s.nf));
        });
      });
    });
    return v;
  }

  /* the activities of a page, in worksheet order: from whichever team reported the most of them */
  function activityOrder(views, page) {
    var best = [];
    views.forEach(function (v) {
      var p = v.pages[page];
      if (p && p.order.length > best.length) best = p.order;
    });
    return best.slice();
  }

  function isTouched(a) { return a && (a.done > 0 || a.filled > 0); }
  function isComplete(a) { return a && a.total > 0 && a.done >= a.total; }

  /* where a team stands on a page: index of the furthest activity it has touched, and whether all are done */
  function standing(view, page, order) {
    var p = view.pages[page];
    if (!p) return { pos: -1, done: false, act: null, a: null };
    var pos = -1;
    order.forEach(function (id, i) { if (isTouched(p.acts[id])) pos = i; });
    var allDone = order.length > 0 && order.every(function (id) { return isComplete(p.acts[id]); });
    return { pos: pos, done: allDone, act: pos >= 0 ? order[pos] : null, a: pos >= 0 ? p.acts[order[pos]] : null };
  }

  /* the whole board for one page; teamMax is the dashboard's "จำนวนทีม" (default TEAM_MAX) */
  function board(tree, page, now, teamMax) {
    now = now || Date.now();
    teamMax = teamMax || TEAM_MAX;
    var views = [], unknown = [];
    tree = objectify(tree) || {};
    Object.keys(tree).forEach(function (t) {
      if (!tree[t] || typeof tree[t] !== "object") return;   // a gap, never a team
      var n = parseInt(t, 10);
      var v = teamView(t, tree[t]);
      if (!v.devs) return;                                    // every device document deleted: not a team any more
      if (/^[1-9][0-9]*$/.test(t) && n >= 1 && n <= teamMax) views.push(v); else unknown.push(v);
    });
    var order = activityOrder(views, page);
    var names = {}, steps = {};
    views.forEach(function (v) {
      var p = v.pages[page];
      if (!p) return;
      Object.keys(p.names).forEach(function (a) { names[a] = p.names[a]; });
      Object.keys(p.steps).forEach(function (a) {                     // how many teams ticked each box
        var list = steps[a] || (steps[a] = []);
        p.steps[a].forEach(function (s, i) {
          if (!s) return;
          if (!list[i]) list[i] = { l: "", n: 0 };
          if (s.l && (!list[i].l || s.l.length > list[i].l.length)) list[i].l = s.l;
          if (s.on) list[i].n++;
        });
      });
    });
    var cells = {}, counts = { none: 0, done: 0, byPos: order.map(function () { return 0; }) };
    var reported = 0, stale = 0, ticks = [];
    views.forEach(function (v) {
      var s = standing(v, page, order);
      var isStale = v.srv > 0 && now - v.srv > STALE_MS;
      cells[v.team] = { view: v, standing: s, stale: isStale };
      reported++;
      if (isStale) stale++;
      if (s.done) counts.done++; else if (s.pos < 0) counts.none++; else counts.byPos[s.pos]++;
      if (v.last && v.last.page === page) ticks.push({ team: v.team, last: v.last });
    });
    ticks.sort(function (a, b) { return num(b.last.ts) - num(a.last.ts); });
    return { page: page, order: order, names: names, steps: steps, cells: cells, counts: counts, reported: reported,
             stale: stale, unknown: unknown, ticks: ticks.slice(0, 20) };
  }

  /* ---- one team's devices, for the dashboard's reset controls: newest first, each placed on `page` ---- */
  function deviceList(team, devices, page, order, now) {
    now = now || Date.now();
    var out = [];
    devices = objectify(devices) || {};
    Object.keys(devices).forEach(function (key) {
      var d = devices[key];
      if (!d || typeof d !== "object") return;
      var one = {}; one[key] = d;
      var v = teamView(team, one), s = standing(v, page, order || []);
      var srv = num(d.srv) || num(d.ts);
      out.push({ key: key, dev: String(d.dev || key), srv: srv, stale: srv > 0 && now - srv > STALE_MS,
                 onPage: !!v.pages[page], pos: s.pos, done: s.done, act: s.act, a: s.a });
    });
    out.sort(function (x, y) { return y.srv - x.srv || (x.key < y.key ? -1 : 1); });
    return out;
  }

  /* ---- messages/<day>: newest first, each with its database id ---- */
  function messageList(tree) {
    tree = objectify(tree) || {};
    var out = [];
    Object.keys(tree).forEach(function (id) {
      var m = tree[id];
      if (!m || typeof m !== "object" || !m.text) return;
      out.push({ id: id, team: String(m.team || "?"), kind: m.kind === "help" || m.kind === "done" ? m.kind : "note",
                 text: String(m.text).slice(0, 120), zone: m.zone || "", page: m.page || "",
                 ts: num(m.srv) || num(m.ts), handled: num(m.handled), day: m._day || "" });   // handled: set by a TA, seen by every screen
    });
    out.sort(function (a, b) { return b.ts - a.ts || (a.id < b.id ? 1 : -1); });
    return out;
  }

  /* "กิจกรรม 5" for a5; otherwise the heading text the worksheet sent, since the id has lost its vowels */
  function actLabel(id, names) {
    var m = /^a(\d+)$/.exec(id);
    if (m) return "กิจกรรม " + m[1];
    if (names && names[id]) return names[id];
    if (id === "page") return "รายการอื่น";
    return id.replace(/_/g, " ");
  }

  function localDay(d) {
    d = d || new Date();
    return d.getFullYear() + "-" + ("0" + (d.getMonth() + 1)).slice(-2) + "-" + ("0" + d.getDate()).slice(-2);
  }

  return {
    TEAM_MAX: TEAM_MAX, STALE_MS: STALE_MS,
    applyEvent: applyEvent, objectify: objectify, pageOrder: pageOrder, teamView: teamView, activityOrder: activityOrder,
    standing: standing, board: board, deviceList: deviceList, messageList: messageList, actLabel: actLabel, localDay: localDay
  };
});
