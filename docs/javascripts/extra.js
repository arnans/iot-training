/* Worksheet page behaviour, loaded after Material's bundle via mkdocs.yml extra_javascript.
   1. Tag recurring elements so extra.css can style them:
        <strong>Hardware</strong> / Driver / Recorder / Tester   -> role chips
        blockquotes that start with "จดลงใบบันทึก"               -> record-sheet note panel
   2. Hover preview for step screenshots: resting the pointer on a "ดูภาพ" chip (a.glightbox)
      shows the screenshot in a floating panel beside it; leaving hides it. Click still opens
      the glightbox lightbox, which is also the only path on touch screens (no hover there).
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
      if (el.textContent.trim().indexOf("จดลงใบบันทึก") === 0) {
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

  function init() {
    decorate(document);
    bindHover(document);
  }

  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(init);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
