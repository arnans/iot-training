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
      download (JSON), import (merge), print, and clear. Design notes: webapp/FILLABLE-WORKSHEET.md.
   4. Each sub-activity ends with a "ทำข้อนี้เสร็จแล้ว" box: a second view of its item in the
      task list at the top, so a team that has just finished need not scroll back to tick.
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
    externalLinks(root);
  }

  /* Links off the worksheet open in a new tab, so a half-filled page is never
     navigated away from -- answers live in this tab's localStorage. Links to
     other worksheet pages, and in-page anchors, stay in the same tab. */
  function externalLinks(root) {
    root.querySelectorAll(".md-typeset a[href]").forEach(function (a) {
      var href = a.getAttribute("href") || "";
      if (!/^https?:/i.test(href)) return;
      var url;
      try { url = new URL(href, location.href); } catch (e) { return; }
      if (location.protocol.indexOf("http") === 0 && url.hostname === location.hostname) return;
      a.target = "_blank";
      a.rel = "noopener noreferrer";
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
  var TEAM_MAX = 100;                // team numbers are 1..TEAM_MAX, stored as plain digits
  var TEAM_RULE = "หมายเลขกลุ่มต้องเป็นตัวเลข 1–" + TEAM_MAX;
  var store = emptyStore();
  var saveTimer;

  /* ---- team number: "๑๗", " 17 ", "กลุ่ม 17", "017" all mean team 17 ---- */
  var THAI_DIGITS = "๐๑๒๓๔๕๖๗๘๙";

  /* what the box may hold while typing: ASCII digits only, at most 3 of them */
  function teamDigits(raw) {
    return String(raw || "").replace(/[๐-๙]/g, function (c) { return THAI_DIGITS.indexOf(c); })
      .replace(/\D+/g, "").slice(0, 3);
  }

  /* the canonical value, or "" if the text is not a team number */
  function teamClean(raw) {
    var d = teamDigits(raw).replace(/^0+/, "");
    var n = parseInt(d, 10);
    return (n >= 1 && n <= TEAM_MAX) ? String(n) : "";
  }

  function teamValid() {
    var t = store.fields["team.no"];
    return !t || String(t).trim() === "" || teamClean(t) !== "";
  }

  /* red underline + tooltip on every team.no box while the value is not a team number */
  function markTeamBoxes() {
    var bad = !teamValid();
    document.querySelectorAll('.fld[data-k="team.no"]').forEach(function (el) {
      el.classList.toggle("fld--bad", bad);
      el.setAttribute("aria-invalid", bad ? "true" : "false");
      el.title = bad ? TEAM_RULE : "";
      if (typeof el.setCustomValidity === "function") el.setCustomValidity(bad ? TEAM_RULE : "");
    });
  }

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

  /* boxes inside <div class="ws-untracked" markdown> are remembered like any other but never
     reported: acknowledgement lists ("we understood these three points") are not progress */
  function tracked(cb) { return !(cb.closest && cb.closest(".ws-untracked")); }

  /* ---- "ทำข้อนี้เสร็จแล้ว": the foot of each sub-activity mirrors its box in the task list ----
     The list at the top is where a team plans; the foot of a sub-activity is where it has just
     finished, so the tick is offered there too. One state, two boxes: the mirror sets the list
     box and fires its change event, so saving and the dashboard report run as for any tick.
     A row's target is the element its bold link points at (a heading, or the paragraph of the
     end question); the section runs to the next heading, the next row's target, or the pager.
     The box joins the section's "back to the list" line where there is one (a discussion prompt
     may follow it), and closes the section on a line of its own otherwise. */
  var DONE_LABEL = "ทำข้อนี้เสร็จแล้ว";
  var mirrors = [];                                // [{ cb: list box, m: mirror box }] for the page on screen

  function isBackLine(el) {
    return el.tagName === "P" && el.children.length === 1 && el.children[0].classList.contains("ws-back");
  }

  /* { back: the section's back-link line or null, last: its last element } */
  function sectionEnd(target, targets) {
    var out = { back: null, last: target };
    for (var el = target.nextElementSibling; el; el = el.nextElementSibling) {
      if (/^(H2|H3|NAV|FOOTER)$/.test(el.tagName) || targets.indexOf(el) >= 0) break;
      if (isBackLine(el)) out.back = el;
      out.last = el;
    }
    return out;
  }

  function addMirrors() {
    mirrors = [];
    var rows = [];
    taskBoxes().forEach(function (cb) {
      var li = cb.closest("li");
      if (!li || !li.closest(".ws-tasks") || !tracked(cb)) return;
      var a = li.querySelector("strong a[href^='#']");
      var target = a && document.getElementById(decodeURIComponent(a.getAttribute("href").slice(1)));
      if (target) rows.push({ cb: cb, target: target });
    });
    var targets = rows.map(function (r) { return r.target; });
    rows.forEach(function (r) {
      if (r.target.closest(".ws-tasks")) return;    // a row pointing into the list itself
      var end = sectionEnd(r.target, targets);
      var label = document.createElement("label");
      label.className = "ws-done";
      var m = document.createElement("input");
      m.type = "checkbox";
      m.className = "ws-mirror";
      label.appendChild(m);
      label.appendChild(document.createTextNode(" " + DONE_LABEL));
      var foot = end.back;
      if (foot) {
        foot.insertBefore(label, foot.firstChild);
      } else {
        foot = document.createElement("p");
        foot.appendChild(label);
        end.last.parentNode.insertBefore(foot, end.last.nextSibling);
      }
      foot.classList.add("ws-foot");
      mirrors.push({ cb: r.cb, m: m });
    });
  }

  function syncMirrors() {
    mirrors.forEach(function (pair) { pair.m.checked = pair.cb.checked; });
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

  /* ---- progress tracker: each tick is sent to the instructor's dashboard (docs/progress.html) ----
     Only counts travel: per activity, task boxes ticked / total and answer boxes filled / total,
     plus the last tick. Answers themselves stay in this browser. The path is dated, so a
     rehearsal or a later reader at home never lands on the workshop's board. Rules that accept
     the write: webapp/database.rules.json. Nothing is sent until the team number is valid. */
  var PROGRESS_DB = "https://iot-farm-workshop-default-rtdb.asia-southeast1.firebasedatabase.app";
  var pushTimer, pushState = "", pushWhen;   // "" never tried · "ok" · "fail"

  function pad2(n) { return ("0" + n).slice(-2); }
  function today() { var d = new Date(); return d.getFullYear() + "-" + pad2(d.getMonth() + 1) + "-" + pad2(d.getDate()); }

  /* one id per browser, so a phone and a laptop of the same team are two rows the dashboard merges */
  function devId() {
    if (!store.dev) store.dev = Math.random().toString(36).slice(2, 8);
    return store.dev;
  }

  /* "activity-2" on MkDocs (/activity-2/), on a render (/renders/activity-2.html), on the combined render (visible tab) */
  function pageKey() {
    var shown = document.querySelector(".ws-page:not([hidden])");
    if (shown && shown.dataset.page) return shown.dataset.page;
    var seg = location.pathname.replace(/\/(index\.html)?$/, "").split("/").pop() || "index";
    return seg.replace(/\.html$/, "").replace(/[.#$\/\[\]]/g, "_");
  }

  /* The worksheet is one page per activity, but the dashboard (docs/progress.html) keeps one
     tab per session, so every report is filed under the session. This browser caches a summary
     of each page it has visited, and each session's record is rebuilt from those, in course
     order, on every push; activity 2's page therefore adds to session 1 instead of replacing
     activity 1's counts. Pages not listed here (record sheet, reference) report under their own name. */
  var PAGE_SESSION = {
    "session-1-start": "session-1", "activity-1": "session-1", "activity-2": "session-1", "activity-3": "session-1",
    "activity-4": "session-2", "activity-5": "session-2",
    "activity-6": "session-3", "activity-7": "session-3", "activity-8": "session-3",
    "activity-9": "session-4", "activity-10": "session-4", "activity-11": "session-4"
  };
  var PAGE_ORDER = Object.keys(PAGE_SESSION);
  function sessionKey() { return PAGE_SESSION[pageKey()] || pageKey(); }

  function sessionRecords() {
    var out = {}, slugs = Object.keys(store.progPages || {});
    function idx(s) { var i = PAGE_ORDER.indexOf(s); return i < 0 ? PAGE_ORDER.length : i; }
    slugs.sort(function (a, b) { return idx(a) - idx(b); });
    slugs.forEach(function (slug) {
      var p = store.progPages[slug], key = PAGE_SESSION[slug] || slug;
      var r = out[key] || (out[key] = { acts: {}, order: [], names: {}, steps: {}, ts: 0 });
      (p.order || []).forEach(function (id) {
        if (r.order.indexOf(id) < 0) r.order.push(id);
        r.acts[id] = p.acts[id];
        if (p.names && p.names[id]) r.names[id] = p.names[id];
        if (p.steps && p.steps[id]) r.steps[id] = p.steps[id];
      });
      if (p.ts > r.ts) r.ts = p.ts;
    });
    return out;
  }

  /* the activity an element belongs to: the nearest heading above it. id "a5" (sub-section ids
     a5-3, a2-1b fold in) and, for headings that are not numbered activities, the heading text --
     slugs drop Thai vowels ("ก่อนเริ่ม" becomes "กอนเรม"), so the dashboard needs the words */
  function actOf(el) {
    var node = el.closest(".ws-tasks") || el.closest("li") || el;
    while (node && !node.classList.contains("md-content__inner")) {
      for (var p = node.previousElementSibling; p; p = p.previousElementSibling) {
        if (/^H[234]$/.test(p.tagName) && p.id) {
          var id = p.id.replace(/^[a-z0-9-]+--/, "")   // combined render prefixes ids with the page slug
                       .replace(/^(a\d+)-.*$/, "$1")
                       .replace(/[.#$\/\[\]]/g, "_");
          var name = /^a\d+$/.test(id) ? "" : (p.textContent || "").replace(/[¶#]\s*$/, "").trim().slice(0, 40);
          return { id: id, name: name };
        }
      }
      node = node.parentElement;
    }
    return { id: "page", name: "" };
  }
  function actId(el) { return actOf(el).id; }

  /* what a task box is about: "1.1 ต่อสวิตช์ลูกลอย" from the bold link in a task list; the first words otherwise */
  function stepLabel(cb) {
    var li = cb.closest("li");
    if (!li) return "";
    var s = li.closest(".ws-tasks") ? li.querySelector("strong") : null;
    return (s || li).textContent.trim().replace(/\s+/g, " ").slice(0, 48);
  }

  /* counts per activity, the activities in page order (the database sorts keys, so order must
     travel), the heading words for the unnumbered ones, and each task box's label and state */
  function summarize() {
    var acts = {}, order = [], names = {}, steps = {}, seen = {};
    function act(el) {
      var a = actOf(el);
      if (!acts[a.id]) { acts[a.id] = { done: 0, total: 0, filled: 0, nf: 0 }; order.push(a.id); }
      if (a.name && !names[a.id]) names[a.id] = a.name;
      return a.id;
    }
    taskBoxes().filter(tracked).forEach(function (cb) {
      var id = act(cb);
      acts[id].total++;
      if (cb.checked) acts[id].done++;
      (steps[id] = steps[id] || []).push({ l: stepLabel(cb), on: cb.checked ? 1 : 0 });
    });
    document.querySelectorAll(".md-typeset .fld").forEach(function (el) {
      var k = el.dataset.k;
      if (k === "team.no" || k === "team.zone") return;
      var id = act(el);
      if (seen[id + "|" + k]) return;                 // one key counts once per activity
      seen[id + "|" + k] = 1;
      acts[id].nf++;
      if (String(store.fields[k] || "").trim() !== "") acts[id].filled++;
    });
    return { acts: acts, order: order, names: names, steps: steps };
  }

  /* Before the first report under a number, and before any change of number, make sure it is
     ours: a wrong number paints another team's cell. store.sentAs is the number this browser
     has reported as; a different valid number is verified (and confirmed) before anything is sent. */
  var verifying = null;

  function setTeamEverywhere(t) {
    if (t) store.fields["team.no"] = t; else delete store.fields["team.no"];
    fillFields(document);
    saveNow();
  }

  /* the one question to ask before reporting as `team`, or null if there is nothing to ask */
  function teamQuestion(team, old, othersExist) {
    var changing = old && old !== team;
    if (changing && othersExist) {
      return "เปลี่ยนหมายเลขกลุ่มจาก กลุ่ม " + old + " เป็น กลุ่ม " + team + " ใช่ไหม?\n\n" +
             "เบราว์เซอร์นี้เคยส่งความคืบหน้าในชื่อ กลุ่ม " + old + " และ กลุ่ม " + team +
             " มีอุปกรณ์อีกเครื่องส่งความคืบหน้าอยู่แล้ววันนี้\n\n" +
             "กด OK ถ้าเราคือกลุ่ม " + team + " จริง ๆ (อีกเครื่องเป็นโทรศัพท์หรือแล็ปท็อปของกลุ่มเรา)\n" +
             "กด Cancel เพื่อกลับไปใช้ กลุ่ม " + old;
    }
    if (changing) {
      return "เปลี่ยนหมายเลขกลุ่มจาก กลุ่ม " + old + " เป็น กลุ่ม " + team + " ใช่ไหม?\n\n" +
             "เบราว์เซอร์นี้เคยส่งความคืบหน้าในชื่อ กลุ่ม " + old + " แล้ว\n\n" +
             "กด OK ถ้าเราคือกลุ่ม " + team + " จริง ๆ (ความคืบหน้าจากเครื่องนี้จะย้ายไปอยู่กับกลุ่ม " + team + ")\n" +
             "กด Cancel เพื่อกลับไปใช้ กลุ่ม " + old;
    }
    if (othersExist) {
      return "กลุ่ม " + team + " มีอุปกรณ์อีกเครื่องส่งความคืบหน้าอยู่แล้ววันนี้\n\n" +
             "ถ้าเป็นโทรศัพท์หรือแล็ปท็อปอีกเครื่องของกลุ่มเรา กด OK\n" +
             "ถ้าไม่ใช่กลุ่มของเรา กด Cancel แล้วดูหมายเลขกลุ่มบนบัตรประจำกลุ่มอีกครั้ง";
    }
    return null;
  }

  /* look the number up first, then ask at most once */
  function verifyTeam(team) {
    if (verifying === team || document.hidden) return;        // one dialog at a time, and only in a visible tab
    verifying = team;
    var old = store.sentAs;
    var done = function (othersExist) {
      verifying = null;
      if (team !== teamClean(store.fields["team.no"])) return;    // the box changed meanwhile: that value gets its own check
      var question = teamQuestion(team, old, othersExist);
      if (question && !window.confirm(question)) {
        if (old && old !== team) { setTeamEverywhere(old); return; }
        setTeamEverywhere("");
        var box = document.querySelector('#ws-bar .fld[data-k="team.no"]');
        if (box) box.focus();
        return;
      }
      store.sentAs = team;
      saveNow();
      if (old && old !== team) {                                  // this device's row moves to the new number
        fetch(PROGRESS_DB + "/progress/" + today() + "/" + old + "/" + devId() + ".json?print=silent", { method: "DELETE", keepalive: true })
          .catch(function () {});
      }
      pushNow();
    };
    fetch(PROGRESS_DB + "/progress/" + today() + "/" + team + ".json?shallow=true")
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) {
        var others = d ? Object.keys(d).filter(function (k) { return k !== devId(); }) : [];
        done(others.length > 0);
      }, function () { done(false); });                           // offline: nothing to compare with, carry on
  }

  function pushNow(last) {
    var team = teamClean(store.fields["team.no"]);
    if (!team || !PROGRESS_DB || !hasFields(document)) return;
    if (team !== store.sentAs) { verifyTeam(team); return; }      // nothing leaves until the number is confirmed
    var now = Date.now();
    store.progPages = store.progPages || {};
    var sum = summarize();
    store.progPages[pageKey()] = { acts: sum.acts, order: sum.order, names: sum.names, steps: sum.steps, ts: now };
    if (last) store.last = last;
    saveSoon();                                   // the cache of other pages' counts rides along in the store
    var doc = {
      team: team, dev: devId(), ts: now, page: sessionKey(),
      srv: { ".sv": "timestamp" },                 // the database stamps its own clock; phones' clocks drift
      zone: ZONE_SLUG[store.fields["team.zone"]] || "",
      pages: sessionRecords(), last: store.last || null
    };
    fetch(PROGRESS_DB + "/progress/" + today() + "/" + team + "/" + devId() + ".json?print=silent",   // no echo: download quota is the free tier's limit
          { method: "PUT", body: JSON.stringify(doc), keepalive: true })
      .then(function (r) { pushState = r.ok ? "ok" : "fail-" + r.status; if (r.ok) pushWhen = new Date(); setStatus(); },
            function () { pushState = "fail"; setStatus(); });
  }

  function pushSoon() { clearTimeout(pushTimer); pushTimer = setTimeout(function () { pushNow(); }, 1500); }

  /* ---- messages to the instructor: "ขอความช่วยเหลือ", "เสร็จแล้ว", or a short line of text ---- */
  var MSG_MAX = 120, MSG_GAP = 5000, lastMsgAt = 0;
  var MSG_EMOJIS = ["👍", "🎉", "🤔", "😅", "🙏", "🔥", "🌱", "💧"];   // useful and fun, in that order

  function sendMessage(kind, text) {
    text = String(text || "").replace(/\s+/g, " ").trim().slice(0, MSG_MAX);
    if (!text || !PROGRESS_DB) return;
    var team = teamNo();
    if (!team) return;
    if (Date.now() - lastMsgAt < MSG_GAP) { composerNote("รอสักครู่แล้วส่งใหม่", true); return; }
    lastMsgAt = Date.now();
    var doc = {
      team: team, dev: devId(), kind: kind, text: text, page: sessionKey(),
      zone: ZONE_SLUG[store.fields["team.zone"]] || "", ts: Date.now(), srv: { ".sv": "timestamp" }
    };
    composerNote("กำลังส่ง…");
    fetch(PROGRESS_DB + "/messages/" + today() + ".json?print=silent",          // POST: the database picks a time-ordered id
          { method: "POST", body: JSON.stringify(doc), keepalive: true })
      .then(function (r) {
        if (r.ok) {
          var f = document.querySelector("#ws-bar .ws-msg input[type=text]");
          if (f) f.value = "";
          composerNote(kind === "help" ? "ส่งคำขอความช่วยเหลือแล้ว กรุณารอผู้สอน 🙋" : "ส่งแล้ว ✓");
        } else composerNote("ส่งไม่สำเร็จ ลองอีกครั้ง", true);
      }, function () { composerNote("ส่งไม่สำเร็จ ลองอีกครั้ง", true); });
  }

  function fillFields(root) {
    // Each visible copy needs its own radio group; data-k remains the shared answer key.
    root.querySelectorAll('.fld-radio').forEach(function (group, i) {
      group.querySelectorAll('input[type=radio]').forEach(function (el) {
        el.name = el.dataset.k + '--copy-' + i;
      });
    });
    root.querySelectorAll(".fld").forEach(function (el) {
      var v = store.fields[el.dataset.k];
      if (el.type === "radio") {
        el.checked = (v !== undefined && el.value === v);
        return;
      }
      if (el.dataset.k === "team.no") {          // phones open the number keypad
        el.inputMode = "numeric";
        el.maxLength = 3;
        el.autocomplete = "off";
      }
      el.value = (v === undefined || v === null) ? "" : v;
      grow(el);
    });
    markTeamBoxes();
    var pid = pageId();
    taskBoxes(root).forEach(function (cb, i) {
      cb.disabled = false;
      cb.checked = !!store.checks[pid + "#" + i];
    });
    syncMirrors();
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
      '<label class="ws-team">กลุ่มที่ <input class="fld" type="text" data-k="team.no" data-size="3" size="3" ' +
        'inputmode="numeric" maxlength="3" autocomplete="off" spellcheck="false"></label>' +
      '<span class="ws-status"></span>' +
      /* the file actions live in a menu: needed twice a day, not every minute */
      '<details class="ws-tools"><summary class="ws-btn ws-btn--quiet" aria-label="เครื่องมือ">⋯ เครื่องมือ</summary>' +
        '<div class="ws-menu" role="menu">' +
          '<button type="button" class="ws-btn" data-act="export" role="menuitem">⬇ ดาวน์โหลดคำตอบ (ไฟล์ JSON)</button>' +
          '<button type="button" class="ws-btn" data-act="import" role="menuitem">⬆ นำเข้าจากไฟล์</button>' +
          '<button type="button" class="ws-btn" data-act="print" role="menuitem">🖨 พิมพ์ / บันทึก PDF</button>' +
          '<button type="button" class="ws-btn ws-btn--danger" data-act="clear" role="menuitem">🗑 ล้างคำตอบทั้งหมด</button>' +
        '</div></details>' +
      '<input type="file" accept=".json,application/json" hidden>' +
      (PROGRESS_DB ?
        '<form class="ws-msg" autocomplete="off">' +
          '<button type="button" class="ws-help" data-msg="help">🙋 ขอความช่วยเหลือ</button>' +
          '<div class="ws-composer">' +
            '<button type="button" class="ws-emoji-toggle" aria-expanded="false" aria-label="อีโมจิ">😊</button>' +
            '<input type="text" maxlength="' + MSG_MAX + '" placeholder="พิมพ์ข้อความถึงผู้สอน…" aria-label="ข้อความถึงผู้สอน">' +
            '<button type="submit" class="ws-send" aria-label="ส่ง"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 11.5 21 3l-8.5 18-2.3-7.2z" fill="currentColor"/></svg></button>' +
          '</div>' +
          '<div class="ws-emojis" role="group" aria-label="ใส่อีโมจิ" hidden>' +
            MSG_EMOJIS.map(function (e) { return '<button type="button" class="ws-emo" data-emoji="' + e + '" aria-label="' + e + '">' + e + '</button>'; }).join("") +
          '</div>' +
        '</form>' : "");
    var h1 = inner.querySelector("h1");
    if (h1) h1.insertAdjacentElement("afterend", bar); else inner.insertBefore(bar, inner.firstChild);
    bar.querySelector("input[type=file]").addEventListener("change", function (e) {
      if (e.target.files && e.target.files[0]) doImport(e.target.files[0]);
      e.target.value = "";
    });
    var tools = bar.querySelector(".ws-tools");
    document.addEventListener("click", function (e) {         // the menu closes on any click outside it
      if (tools.open && !tools.contains(e.target)) tools.removeAttribute("open");
    });
    var form = bar.querySelector(".ws-msg");
    if (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        sendMessage("note", form.querySelector("input[type=text]").value);
      });
      form.addEventListener("click", function (e) {
        var box = form.querySelector("input[type=text]");
        var t = e.target.closest && e.target.closest(".ws-emoji-toggle");
        if (t) {
          var strip = form.querySelector(".ws-emojis");
          strip.hidden = !strip.hidden;
          t.setAttribute("aria-expanded", String(!strip.hidden));
          return;
        }
        var emo = e.target.closest && e.target.closest(".ws-emo");
        if (emo) {                                   // emoji go into the box; the team still presses send
          if (box.value.length < MSG_MAX - 2) box.value = (box.value + " " + emo.dataset.emoji).trim();
          box.focus();
          return;
        }
        var help = e.target.closest && e.target.closest(".ws-help");
        if (help) sendMessage("help", "ขอความช่วยเหลือ");
      });
    }
    setStatus();
  }

  /* a short note inside the composer ("ส่งแล้ว ✓"), where the eye already is */
  function composerNote(text, bad) {
    var box = document.querySelector("#ws-bar .ws-composer");
    if (!box) return;
    box.dataset.note = text;
    box.classList.toggle("is-bad", !!bad);
    clearTimeout(box._noteTimer);
    box._noteTimer = setTimeout(function () { delete box.dataset.note; box.classList.remove("is-bad"); }, 3500);
  }

  function setStatus(msg) {
    var el = document.querySelector("#ws-bar .ws-status");
    if (!el) return;
    /* one short phrase at most: the team number box beside it says who we are */
    if (msg) { el.innerHTML = '<span class="ws-note">' + msg + "</span>"; return; }
    if (!teamValid()) { el.innerHTML = '<span class="ws-bad">' + TEAM_RULE + "</span>"; return; }
    var team = teamClean(store.fields["team.no"]);
    if (!PROGRESS_DB) { el.innerHTML = ""; return; }
    if (!team) el.innerHTML = '<span class="ws-hint">← กรอกหมายเลขกลุ่ม</span>';
    else if (team !== store.sentAs) el.innerHTML = '<span class="ws-live ws-live--off">● กำลังตรวจสอบหมายเลขกลุ่ม…</span>';
    else if (pushState === "ok") el.innerHTML = '<span class="ws-live ws-live--ok" title="ความคืบหน้าของกลุ่มส่งถึงผู้สอนแล้ว">● เชื่อมต่อผู้สอนแล้ว</span>';
    else if (pushState) el.innerHTML = '<span class="ws-live ws-live--off" title="จะลองส่งใหม่เมื่อติ๊กครั้งถัดไป">● ยังส่งไม่ถึงผู้สอน</span>';
    else el.innerHTML = '<span class="ws-live ws-live--off">● กำลังเชื่อมต่อ…</span>';
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  /* the team number, asking for one (and refusing a bad one) if the box is empty or wrong */
  function teamNo() {
    var t = teamClean(store.fields["team.no"]);
    var ask = "หมายเลขกลุ่ม 1–" + TEAM_MAX + " (ใช้ตั้งชื่อไฟล์และให้ผู้สอนรู้ว่าเป็นของกลุ่มใด)";
    while (!t) {
      var raw = window.prompt(ask);
      if (raw === null) return "";                 // Cancel
      t = teamClean(raw);
      if (t) { store.fields["team.no"] = t; fillFields(document); saveNow(); }
      else ask = TEAM_RULE + " ลองอีกครั้ง";
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
    var name = "farm-team-" + t + (ZONE_SLUG[zone] ? "-" + ZONE_SLUG[zone] : "") + ".json";
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
      if (d.fields["team.no"] !== undefined) d.fields["team.no"] = teamClean(d.fields["team.no"]);  // files from before validation
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
      pushSoon();
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
    if (k === "team.no") {                        // letters and Thai digits never reach the store
      var digits = teamDigits(el.value);
      if (digits !== el.value) el.value = digits;
    }
    store.fields[k] = el.value;
    grow(el);
    document.querySelectorAll('.fld[data-k="' + k + '"]').forEach(function (o) {
      if (o !== el && o.type !== "radio") { o.value = el.value; grow(o); }
    });
    if (k === "team.no") { markTeamBoxes(); saveSoon(); return; }   // a half-typed number is not a team: checked on leaving the box
    saveSoon();
    pushSoon();
  });

  document.addEventListener("change", function (e) {
    var el = e.target;
    if (el.classList && el.classList.contains("fld") && el.type === "radio") {
      store.fields[el.dataset.k] = el.value;
      document.querySelectorAll('input.fld[type=radio]').forEach(function (other) {
        if (other.dataset.k === el.dataset.k) other.checked = other.value === el.value;
      });
      saveNow();
      pushSoon();
      return;
    }
    if (el.classList && el.classList.contains("fld") && el.dataset.k === "team.no") {
      var t = teamClean(el.value);                 // leaving the box: "017" becomes "17"
      if (t && t !== el.value) { store.fields["team.no"] = t; fillFields(document); }
      markTeamBoxes();
      saveNow();
      pushNow();                                   // verifies the number first; the dot appears once it is confirmed
      return;
    }
    if (el.classList && el.classList.contains("ws-mirror")) {
      var pair = mirrors.filter(function (p) { return p.m === el; })[0];
      if (!pair) return;
      pair.cb.checked = el.checked;                // the list box is the one that is saved and reported
      pair.cb.dispatchEvent(new Event("change", { bubbles: true }));
      return;
    }
    if (el.type === "checkbox" && el.closest && el.closest(".task-list-item")) {
      var i = taskBoxes().indexOf(el);
      if (i < 0) return;
      var key = pageId() + "#" + i;
      if (el.checked) store.checks[key] = true; else delete store.checks[key];
      saveNow();
      syncMirrors();
      if (!tracked(el)) return;                    // remembered, not reported
      pushNow({                                    // every tick reaches the dashboard at once
        page: sessionKey(), act: actId(el), on: !!el.checked, ts: Date.now(), label: stepLabel(el)
      });
    }
  });

  /* a phone that slept, or a laptop that lost WiFi, reports again as soon as it can */
  document.addEventListener("visibilitychange", function () { if (!document.hidden) pushSoon(); });
  window.addEventListener("online", pushSoon);

  document.addEventListener("click", function (e) {
    var btn = e.target.closest && e.target.closest("#ws-bar .ws-btn[data-act]");
    if (!btn) return;
    var menu = btn.closest(".ws-tools");
    if (menu) menu.removeAttribute("open");
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

  /* walkthrough videos (hooks/videos.py): play while at least half is on screen, pause when
     scrolled away, so a page with eight clips downloads only the one being watched.
     Readers who ask for reduced motion start them with the play button instead. */
  function playInView(root) {
    var vids = root.querySelectorAll("video.walkthrough");
    if (!vids.length || !("IntersectionObserver" in window)) return;
    if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { var p = e.target.play(); if (p && p.catch) p.catch(function () {}); }
        else e.target.pause();
      });
    }, { threshold: 0.5 });
    vids.forEach(function (v) { io.observe(v); });
  }

  function init() {
    decorate(document);
    playInView(document);
    bindHover(document);
    addMirrors();
    store = loadStore();
    buildBar();                                   // first, so the toolbar's team box is filled with the rest
    fillFields(document);
    pushSoon();                                   // opening a page reports where the team stands
  }

  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(init);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
