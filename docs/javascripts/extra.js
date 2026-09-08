/* Worksheet page behaviour, loaded after Material's bundle via mkdocs.yml extra_javascript.
   1. Tag recurring elements so extra.css can style them:
        <strong>Hardware</strong> / Driver / Recorder / Tester   -> role chips
        blockquotes that start with "บันทึกผล" or "จดลงใบบันทึก"  -> record note panel
   2. Hover preview for step screenshots: resting the pointer on a "ดูภาพ" chip (a.glightbox)
      shows the screenshot in a floating panel beside it; leaving hides it. Click still opens
      the glightbox lightbox, which is also the only path on touch screens (no hover there).
   3. Fillable worksheet: every <input class="fld"> / <textarea class="fld"> / radio group that
      hooks/fields.py generated, plus the task-list checkboxes, is saved to localStorage as the
      team types and restored on every page load. A toolbar under the page title offers
      download (JSON), import (merge), print, and clear. Design notes: FILLABLE-WORKSHEET.md.
   Runs on every page load, including Material's instant navigation. */
(function () {
  var ROLES = { Hardware: "hardware", Driver: "driver", Recorder: "recorder", Tester: "tester" };

  function decorate(root) {
    root.querySelectorAll(".md-typeset strong").forEach(function (el) {
      var key = el.textContent.trim();
      if (ROLES[key]) {
        el.classList.add("role", "role-" + ROLES[key]);
      }
    });
    root.querySelectorAll(".md-typeset blockquote").forEach(function (el) {
      var t = el.textContent.trim();
      if (t.indexOf("บันทึกผล") === 0 || t.indexOf("จดลงใบบันทึก") === 0) {
        el.classList.add("note-record");
      }
    });
  }

  /* ---- hover preview ---- */
  var canHover = window.matchMedia && window.matchMedia("(hover: hover)").matches;
  var panel, img, cap, timer, current;

  function ensurePanel() {
    if (panel) return;
    panel = document.createElement("div");
    panel.id = "shot-hover";
    panel.hidden = true;
    img = document.createElement("img");
    img.alt = "";
    cap = document.createElement("div");
    cap.className = "shot-hover__cap";
    panel.appendChild(img);
    panel.appendChild(cap);
    document.body.appendChild(panel);
    img.addEventListener("load", function () { if (current) place(current); });
  }

  function place(a) {
    var r = a.getBoundingClientRect();
    var vw = window.innerWidth, vh = window.innerHeight, pad = 16;
    var w = Math.min(760, Math.floor(vw * 0.6));
    panel.style.width = w + "px";
    var ph = panel.offsetHeight;
    var x = r.right + pad;                       // prefer to the right of the chip
    if (x + w > vw - pad) x = r.left - w - pad;  // else to the left
    if (x < pad) x = pad;                        // else clamp
    var y = r.top - 24;
    if (y + ph > vh - pad) y = vh - pad - ph;
    if (y < pad) y = pad;
    panel.style.left = x + "px";
    panel.style.top = y + "px";
  }

  function show(a) {
    ensurePanel();
    current = a;
    img.src = a.getAttribute("href");
    cap.textContent = a.getAttribute("data-title") || "";
    panel.hidden = false;
    place(a);
  }

  function hide() {
    current = null;
    if (panel) panel.hidden = true;
  }

  function bindHover(root) {
    if (!canHover) return;
    root.querySelectorAll("a.glightbox").forEach(function (a) {
      if (a.dataset.hoverBound) return;
      a.dataset.hoverBound = "1";
      a.addEventListener("mouseenter", function () {
        clearTimeout(timer);
        timer = setTimeout(function () { show(a); }, 120);
      });
      a.addEventListener("mouseleave", function () { clearTimeout(timer); hide(); });
      a.addEventListener("focus", function () { show(a); });
      a.addEventListener("blur", hide);
      a.addEventListener("click", hide);
    });
  }

  /* ---- fillable worksheet ---- */
  var STORE = "farm-worksheet.v1";   // bump the suffix if the stored shape ever changes
  var ZONE_SLUG = { "แดง": "red", "เขียว": "green", "น้ำเงิน": "blue" };
  var store = emptyStore();
  var saveTimer;

  function emptyStore() { return { v: 1, fields: {}, checks: {} }; }

  function loadStore() {
    try {
      var d = JSON.parse(localStorage.getItem(STORE));
      if (d && typeof d.fields === "object") {
        d.checks = d.checks || {};
        return d;
      }
    } catch (e) { /* no storage, or corrupt: start clean */ }
    return emptyStore();
  }

  function writeStore() {
    store.v = 1;
    store.updated = new Date().toISOString();
    try {
      localStorage.setItem(STORE, JSON.stringify(store));
      setStatus();
    } catch (e) {
      setStatus("เบราว์เซอร์นี้ไม่อนุญาตให้เก็บข้อมูล คำตอบจะหายเมื่อปิดหน้า ให้ดาวน์โหลดคำตอบไว้ก่อน");
    }
  }

  function saveSoon() { clearTimeout(saveTimer); saveTimer = setTimeout(writeStore, 300); }
  function saveNow() { clearTimeout(saveTimer); writeStore(); }

  function pageId() { return location.pathname.replace(/index\.html$/, ""); }

  function taskBoxes(root) {
    return Array.prototype.slice.call(
      (root || document).querySelectorAll(".md-typeset .task-list-item input[type=checkbox]")
    );
  }

  /* a box grows to fit what is typed, so nothing is clipped on screen or in print */
  function grow(el) {
    if (el.tagName === "TEXTAREA") {
      el.style.height = "auto";
      el.style.height = (el.scrollHeight + 2) + "px";
    } else if (el.type === "text") {
      var base = parseInt(el.dataset.size, 10) || 10;
      el.size = Math.max(base, el.value.length + 1);
    }
  }

  function fillFields(root) {
    root.querySelectorAll(".fld").forEach(function (el) {
      var v = store.fields[el.dataset.k];
      if (el.type === "radio") {
        el.checked = (v !== undefined && el.value === v);
        return;
      }
      el.value = (v === undefined || v === null) ? "" : v;
      grow(el);
    });
    var pid = pageId();
    taskBoxes(root).forEach(function (cb, i) {
      cb.disabled = false;
      cb.checked = !!store.checks[pid + "#" + i];
    });
  }

  function hasFields(root) {
    return !!(root.querySelector(".fld") || root.querySelector(".task-list-item input[type=checkbox]"));
  }

  /* ---- toolbar ---- */
  function buildBar() {
    var inner = document.querySelector(".md-content__inner");
    if (!inner || inner.querySelector("#ws-bar") || !hasFields(inner)) return;
    var bar = document.createElement("div");
    bar.id = "ws-bar";
    bar.innerHTML =
      '<span class="ws-status"></span>' +
      '<button type="button" class="ws-btn" data-act="export">ดาวน์โหลดคำตอบ</button>' +
      '<button type="button" class="ws-btn" data-act="import">นำเข้าจากไฟล์</button>' +
      '<button type="button" class="ws-btn" data-act="print">พิมพ์ / บันทึก PDF</button>' +
      '<button type="button" class="ws-btn ws-btn--quiet" data-act="clear">ล้างคำตอบทั้งหมด</button>' +
      '<input type="file" accept=".json,application/json" hidden>';
    var h1 = inner.querySelector("h1");
    if (h1) h1.insertAdjacentElement("afterend", bar); else inner.insertBefore(bar, inner.firstChild);
    bar.querySelector("input[type=file]").addEventListener("change", function (e) {
      if (e.target.files && e.target.files[0]) doImport(e.target.files[0]);
      e.target.value = "";
    });
    setStatus();
  }

  function setStatus(msg) {
    var el = document.querySelector("#ws-bar .ws-status");
    if (!el) return;
    if (msg) { el.innerHTML = "<strong>" + msg + "</strong>"; return; }
    var team = (store.fields["team.no"] || "").trim();
    var n = Object.keys(store.fields).filter(function (k) { return String(store.fields[k]).trim() !== ""; }).length;
    var when = "";
    if (store.updated) {
      var d = new Date(store.updated);
      when = " · บันทึกล่าสุด " + d.getHours() + ":" + ("0" + d.getMinutes()).slice(-2);
    }
    el.innerHTML = (team ? "<strong>ทีม " + escapeHtml(team) + "</strong> · " : "") +
      (n ? "กรอกแล้ว " + n + " ช่อง" : "ยังไม่มีคำตอบ") +
      " · คำตอบเก็บอยู่ในเบราว์เซอร์นี้เท่านั้น" + when;
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  function teamNo() {
    var t = (store.fields["team.no"] || "").trim();
    if (!t) {
      t = (window.prompt("หมายเลขทีม (ใช้ตั้งชื่อไฟล์และให้ผู้สอนรู้ว่าเป็นของทีมใด)") || "").trim();
      if (t) { store.fields["team.no"] = t; fillFields(document); saveNow(); }
    }
    return t;
  }

  function doExport() {
    var t = teamNo();
    if (!t) return;
    var zone = store.fields["team.zone"] || "";
    var out = {
      kind: "iot-farm-worksheet",
      v: 1,
      team: t,
      zone: zone,
      exported: new Date().toISOString(),
      fields: store.fields,
      checks: store.checks
    };
    var name = "farm-team-" + t.replace(/[^\w฀-๿-]+/g, "") +
      (ZONE_SLUG[zone] ? "-" + ZONE_SLUG[zone] : "") + ".json";
    var blob = new Blob([JSON.stringify(out, null, 2)], { type: "application/json" });
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = name;
    document.body.appendChild(a);
    a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 1500);
  }

  /* merge rule: fill empty boxes; ask once before overwriting boxes that already differ */
  function doImport(file) {
    var reader = new FileReader();
    reader.onload = function () {
      var d;
      try { d = JSON.parse(reader.result); } catch (e) { d = null; }
      if (!d || typeof d.fields !== "object") {
        window.alert("ไฟล์นี้ไม่ใช่ไฟล์คำตอบของใบงาน");
        return;
      }
      var added = 0, conflicts = [];
      Object.keys(d.fields).forEach(function (k) {
        var nv = d.fields[k], cur = store.fields[k];
        if (nv === undefined || nv === null || String(nv).trim() === "") return;
        if (cur === undefined || cur === null || String(cur).trim() === "") { store.fields[k] = nv; added++; }
        else if (String(cur) !== String(nv)) conflicts.push(k);
      });
      var overwritten = 0;
      if (conflicts.length &&
          window.confirm("มี " + conflicts.length + " ช่องที่กรอกไว้แล้วในเครื่องนี้และต่างจากในไฟล์\n" +
                         "กด OK เพื่อใช้ค่าจากไฟล์แทน หรือ Cancel เพื่อคงค่าในเครื่องนี้")) {
        conflicts.forEach(function (k) { store.fields[k] = d.fields[k]; });
        overwritten = conflicts.length;
      }
      Object.keys(d.checks || {}).forEach(function (k) { if (d.checks[k]) store.checks[k] = true; });
      saveNow();
      fillFields(document);
      window.alert("นำเข้าแล้ว เติมช่องว่าง " + added + " ช่อง" +
        (overwritten ? " เขียนทับ " + overwritten + " ช่อง" : "") +
        (conflicts.length && !overwritten ? " คงค่าเดิม " + conflicts.length + " ช่อง" : ""));
    };
    reader.readAsText(file);
  }

  function doClear() {
    if (!window.confirm("ลบคำตอบทั้งหมดที่เก็บในเบราว์เซอร์นี้?\nถ้ายังไม่ได้ดาวน์โหลดคำตอบไว้ ให้กด Cancel แล้วดาวน์โหลดก่อน")) return;
    store = emptyStore();
    saveNow();
    fillFields(document);
  }

  /* one set of listeners for the whole document: survives instant navigation */
  document.addEventListener("input", function (e) {
    var el = e.target;
    if (!el.classList || !el.classList.contains("fld") || el.type === "radio") return;
    var k = el.dataset.k;
    store.fields[k] = el.value;
    grow(el);
    document.querySelectorAll('.fld[data-k="' + k + '"]').forEach(function (o) {
      if (o !== el && o.type !== "radio") { o.value = el.value; grow(o); }
    });
    saveSoon();
  });

  document.addEventListener("change", function (e) {
    var el = e.target;
    if (el.classList && el.classList.contains("fld") && el.type === "radio") {
      store.fields[el.dataset.k] = el.value;
      saveNow();
      return;
    }
    if (el.type === "checkbox" && el.closest && el.closest(".task-list-item")) {
      var i = taskBoxes().indexOf(el);
      if (i < 0) return;
      var key = pageId() + "#" + i;
      if (el.checked) store.checks[key] = true; else delete store.checks[key];
      saveNow();
    }
  });

  document.addEventListener("click", function (e) {
    var btn = e.target.closest && e.target.closest("#ws-bar .ws-btn");
    if (!btn) return;
    var act = btn.dataset.act;
    if (act === "export") doExport();
    else if (act === "import") document.querySelector("#ws-bar input[type=file]").click();
    else if (act === "print") window.print();
    else if (act === "clear") doClear();
  });

  /* another tab (record sheet open beside a session page) saved: show its values here */
  window.addEventListener("storage", function (e) {
    if (e.key !== STORE) return;
    store = loadStore();
    fillFields(document);
    setStatus();
  });

  function init() {
    decorate(document);
    bindHover(document);
    store = loadStore();
    fillFields(document);
    buildBar();
  }

  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(init);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
