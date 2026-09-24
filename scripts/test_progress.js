#!/usr/bin/env node
/* Checks for docs/javascripts/progress.js, the dashboard's merge logic. No browser needed:
       node scripts/test_progress.js
   Feeds a small stream of Firebase events (put / patch) and asserts on the board that results. */
"use strict";
const P = require("../docs/javascripts/progress.js");

let failures = 0;
function eq(label, got, want) {
  const g = JSON.stringify(got), w = JSON.stringify(want);
  if (g !== w) { failures++; console.log("FAIL", label, "\n   got ", g, "\n   want", w); }
}

const s1 = (a1, a2) => ({ ts: 1000, acts: { "ก่อนเริ่ม": { done: 4, total: 4, filled: 2, nf: 2 }, a1, a2 } });
const A = (done, total, filled, nf) => ({ done, total, filled, nf });

// 1. initial put of a whole day: two teams, team 17 on two devices
let tree = null;
tree = P.applyEvent(tree, "put", "/", {
  "17": {
    lap1: { team: "17", dev: "lap1", zone: "red", ts: 2000, srv: 2000,
            pages: { "session-1": s1(A(3, 3, 2, 2), A(1, 5, 0, 3)) },
            last: { page: "session-1", act: "a2", label: "2.1 ทดลอง", on: true, ts: 2000 } },
    pho2: { team: "17", dev: "pho2", zone: "red", ts: 1500, srv: 1500,
            pages: { "session-1": s1(A(2, 3, 2, 2), A(2, 5, 1, 3)) } }
  },
  "3": { dev9: { team: "3", dev: "dev9", zone: "green", ts: 1800, srv: 1800,
                 pages: { "session-1": s1(A(0, 3, 0, 2), A(0, 5, 0, 3)) } } },
  "abc": { x: { team: "abc", dev: "x", ts: 1, srv: 1, pages: {} } }
});

let b = P.board(tree, "session-1", 3000);
eq("activity order follows the worksheet", b.order, ["ก่อนเริ่ม", "a1", "a2"]);
eq("devices merge by max", b.cells["17"].view.pages["session-1"].acts.a2, A(2, 5, 1, 3));
eq("team 17 stands at a2", [b.cells["17"].standing.pos, b.cells["17"].standing.act], [2, "a2"]);
eq("team 3 has only the prep list", b.cells["3"].standing.act, "ก่อนเริ่ม");
eq("counts by position", b.counts, { none: 0, done: 0, byPos: [1, 0, 1] });
eq("unknown team numbers are listed, not dropped", b.unknown.map(v => v.team), ["abc"]);
eq("last tick is the newest across devices", b.ticks[0].last.label, "2.1 ทดลอง");
eq("nothing stale yet", b.stale, 0);
eq("stale after 10 minutes (unknown teams not counted)", P.board(tree, "session-1", 2000 + P.STALE_MS + 1).stale, 2);

// 2. a patch at a device path (Firebase sends these for partial updates)
tree = P.applyEvent(tree, "patch", "/17/lap1", { ts: 4000, srv: 4000 });
eq("patch merges fields", tree["17"].lap1.ts, 4000);
eq("patch keeps siblings", tree["17"].lap1.zone, "red");

// 3. a put at a nested path replaces that node; null deletes
tree = P.applyEvent(tree, "put", "/3/dev9/pages/session-1/acts/a1", A(3, 3, 2, 2));
tree = P.applyEvent(tree, "put", "/3/dev9/pages/session-1/acts/a2", A(5, 5, 3, 3));
tree = P.applyEvent(tree, "put", "/3/dev9/pages/session-1/acts/ก่อนเริ่ม", A(4, 4, 2, 2));
b = P.board(tree, "session-1", 5000);
eq("team 3 is now done", [b.cells["3"].standing.done, b.counts.done], [true, 1]);
tree = P.applyEvent(tree, "put", "/abc", null);
eq("null put deletes", Object.keys(tree).sort(), ["17", "3"]);

// 4. a page nobody has reported yet
b = P.board(tree, "session-3", 5000);
eq("empty page: no order, all teams at none", [b.order, b.counts.none], [[], 2]);

// 4b. the database sorts keys (a1, a2, ก่อนเริ่ม): `order` restores page order; without it, a sane fallback
const sortedActs = { a1: A(2, 6, 1, 3), a2: A(0, 7, 0, 4), "ก่อนเริ่ม": A(5, 5, 2, 2) };
eq("explicit order wins", P.pageOrder({ acts: sortedActs, order: ["ก่อนเริ่ม", "a1", "a2"] }), ["ก่อนเริ่ม", "a1", "a2"]);
eq("order as Firebase array-object", P.pageOrder({ acts: sortedActs, order: { "0": "ก่อนเริ่ม", "1": "a1", "2": "a2" } }), ["ก่อนเริ่ม", "a1", "a2"]);
eq("no order: prep lists first, then a1..aN", P.pageOrder({ acts: { a10: A(0, 1, 0, 0), a2: A(0, 1, 0, 0), "ก่อนเริ่ม": A(0, 1, 0, 0) } }), ["ก่อนเริ่ม", "a2", "a10"]);
let t7 = P.applyEvent(null, "put", "/", { "7": { d: { team: "7", dev: "d", ts: 1, srv: 1, pages: { "session-1": { ts: 1, acts: sortedActs } } } } });
eq("standing uses page order, not key order", P.board(t7, "session-1", 2).cells["7"].standing.act, "a1");

// 4c. deleting a team's last device leaves an empty node; it must not count as a team
let t8 = P.applyEvent(null, "put", "/", { "8": { d: { team: "8", dev: "d", ts: 1, srv: 1, pages: { "session-1": s1(A(1, 3, 0, 2), A(0, 5, 0, 3)) } } } });
t8 = P.applyEvent(t8, "put", "/8/d", null);
eq("empty team node is not reported", P.board(t8, "session-1", 2).reported, 0);

// 5. Firebase sends integer-keyed nodes as arrays with null gaps (seen live 14 Sep 2026)
let arr = P.applyEvent(null, "put", "/", [null,
  { d: { team: "1", dev: "d", ts: 1, srv: 1, pages: { "session-1": s1(A(1, 3, 0, 2), A(0, 5, 0, 3)) } } },
  null, null,
  { d: { team: "4", dev: "d", ts: 1, srv: 1, pages: { "session-1": s1(A(3, 3, 2, 2), A(5, 5, 3, 3)) } } }]);
eq("array day becomes an object without gaps", Object.keys(arr), ["1", "4"]);
b = P.board(arr, "session-1", 2000);
eq("gaps are not teams", [b.reported, b.unknown.length, b.counts.done], [2, 0, 1]);
arr = P.applyEvent(arr, "put", "/7/d", { team: "7", dev: "d", ts: 1, srv: 1, pages: {} });
eq("later puts land on the object", Object.keys(arr), ["1", "4", "7"]);

// 4d. sub-steps: ticked on any device counts once; the board counts teams per box
let ts = P.applyEvent(null, "put", "/", {
  "11": { lap: { team: "11", dev: "lap", ts: 1, srv: 1, pages: { "session-1": { ts: 1, order: ["a1"], acts: { a1: A(1, 3, 0, 0) },
                 steps: { a1: [{ l: "1.1 ต่อสาย", on: 1 }, { l: "1.2 อ่านค่า", on: 0 }, { l: "1.3 จด", on: 0 }] } } } },
          pho: { team: "11", dev: "pho", ts: 2, srv: 2, pages: { "session-1": { ts: 2, order: ["a1"], acts: { a1: A(1, 3, 0, 0) },
                 steps: { a1: { "0": { l: "1.1 ต่อสาย", on: 0 }, "1": { l: "1.2 อ่านค่า", on: 1 }, "2": { l: "1.3 จด", on: 0 } } } } } } },
  "12": { d: { team: "12", dev: "d", ts: 1, srv: 1, pages: { "session-1": { ts: 1, order: ["a1"], acts: { a1: A(2, 3, 0, 0) },
                 steps: { a1: [{ l: "1.1 ต่อสาย", on: 1 }, { l: "1.2 อ่านค่า", on: 1 }, { l: "1.3 จด", on: 0 }] } } } } }
});
b = P.board(ts, "session-1", 3);
eq("device OR per box", b.cells["11"].view.pages["session-1"].steps.a1.map(s => s.on), [1, 1, 0]);
eq("teams per box", b.steps.a1.map(s => s.l + "=" + s.n), ["1.1 ต่อสาย=2", "1.2 อ่านค่า=2", "1.3 จด=0"]);

// 4d2. the dashboard's team count decides the grid; numbers above it are listed, not dropped
let big = P.applyEvent(null, "put", "/", { "110": { d: { team: "110", dev: "d", ts: 1, srv: 1, pages: { "session-1": s1(A(1, 3, 0, 2), A(0, 5, 0, 3)) } } } });
eq("team 110 is unknown on a 100-team board", P.board(big, "session-1", 2).unknown.map(v => v.team), ["110"]);
eq("team 110 is a cell on a 120-team board", [Object.keys(P.board(big, "session-1", 2, 120).cells), P.board(big, "session-1", 2, 120).unknown.length], [["110"], 0]);

// 4d3. one team's devices, newest first, each placed on the page, silent ones marked
const devs = P.deviceList("17", {
  "2026-09-14/old1": { team: "17", dev: "old1", ts: 1000, srv: 1000, pages: { "session-1": s1(A(3, 3, 2, 2), A(0, 5, 0, 3)) } },
  "2026-09-14/new2": { team: "17", dev: "new2", ts: 900000, srv: 900000, pages: { "session-1": s1(A(3, 3, 2, 2), A(2, 5, 1, 3)) } },
  "2026-09-14/idle": { team: "17", dev: "idle", ts: 950000, srv: 950000, pages: { "session-2": { ts: 1, acts: { a5: A(1, 7, 0, 0) } } } }
}, "session-1", ["ก่อนเริ่ม", "a1", "a2"], 1000 + P.STALE_MS + 1);
eq("devices newest first", devs.map(d => d.dev), ["idle", "new2", "old1"]);
eq("device keys keep the day", devs.map(d => d.key)[2], "2026-09-14/old1");
eq("device placed on the page", [devs[1].act, devs[1].a.done, devs[2].act], ["a2", 2, "a1"]);
eq("device not on this page", [devs[0].onPage, devs[0].pos], [false, -1]);
eq("silent device marked stale", devs.map(d => d.stale), [false, false, true]);

// 4e. messages: newest first, kinds normalised
const msgs = P.messageList({ "-Aa": { team: "3", kind: "help", text: "ปั๊มไม่ทำงาน", ts: 10, srv: 10 },
                             "-Ab": { team: "17", kind: "weird", text: "so cool", ts: 20, srv: 20 },
                             "-Ac": { team: "5", kind: "done", text: "", ts: 30 } });
eq("messages newest first, empty text dropped, unknown kind is a note", msgs.map(m => m.team + ":" + m.kind), ["17:note", "3:help"]);
eq("handled flag and day pass through", P.messageList({ "-Ad": { team: "3", kind: "help", text: "x", ts: 1, handled: 99, _day: "2026-09-20" } })[0].handled + "|" +
   P.messageList({ "-Ad": { team: "3", kind: "help", text: "x", ts: 1, handled: 99, _day: "2026-09-20" } })[0].day, "99|2026-09-20");
// a team that withdrew its own call: `cancelled` reaches the dashboard, which hides it and stops counting it
eq("cancelled flag passes through", P.messageList({ "-Ae": { team: "3", kind: "help", text: "x", ts: 1, cancelled: 77 } })[0].cancelled + "|" +
   P.messageList({ "-Ae": { team: "3", kind: "help", text: "x", ts: 1 } })[0].cancelled, "77|0");

// a multi-path PATCH (ล้างทั้งหมด) streams back as one patch whose keys are paths
let mp = P.applyEvent(null, "put", "/", { "1": { a: { team: "1" } }, "2": { b: { team: "2" }, c: { team: "2" } } });
mp = P.applyEvent(mp, "patch", "/", { "1/a": null, "2/b": null });
eq("multi-path patch deletes the named leaves only", mp, { "1": {}, "2": { c: { team: "2" } } });
let mm = P.applyEvent(null, "put", "/", { "-M1": { team: "3", kind: "help", text: "x", ts: 1 } });
mm = P.applyEvent(mm, "patch", "/", { "-M1/handled": 55 });
eq("multi-path patch sets a nested field", mm["-M1"].handled, 55);
let np = P.applyEvent({ "4": { d: { team: "4", x: 1 } } }, "patch", "/4/d", { x: 2, y: null });
eq("plain patch at a path still merges", np, { "4": { d: { team: "4", x: 2 } } });

// after ล้างทั้งหมด: messages older than the reset belong to the previous group and are dropped
const mixed = { "-Ba": { team: "3", kind: "help", text: "old", ts: 50, srv: 100 },
                "-Bb": { team: "3", kind: "note", text: "new", ts: 999, srv: 300 },
                "-Bc": { team: "4", kind: "note", text: "clock", ts: 250 } };
eq("reset drops older messages by server time", Object.keys(P.afterReset(mixed, 200)).sort(), ["-Bb", "-Bc"]);
eq("no reset keeps every message", Object.keys(P.afterReset(mixed, 0)).length, 3);
eq("reset of an empty day", P.afterReset(null, 200), {});
const prog = { "1": { a: { team: "1", ts: 50, srv: 100 } }, "2": { b: { team: "2", srv: 90 }, c: { team: "2", ts: 400 } } };
eq("reset hides devices last written before it, and teams left with none", P.progressAfter(prog, 200), { "2": { c: { team: "2", ts: 400 } } });
eq("a device that writes again comes back", Object.keys(P.progressAfter(Object.assign({}, prog, { "1": { a: { team: "1", srv: 250 } } }), 200)), ["1", "2"]);
eq("reset time is just after the newest thing received", P.resetTime(prog, mixed, 1), 401);
eq("reset time with nothing received is the clock", P.resetTime(null, null, 777), 777);

// 5. labels and the day key
eq("activity label", [P.actLabel("a5"), P.actLabel("page"), P.actLabel("ก่อนเริ่ม")], ["กิจกรรม 5", "รายการอื่น", "ก่อนเริ่ม"]);
eq("vowel-less slug is labelled by the heading text the worksheet sent", P.actLabel("กอนเรม", { "กอนเรม": "ก่อนเริ่ม" }), "ก่อนเริ่ม");
let t9 = P.applyEvent(null, "put", "/", { "9": { d: { team: "9", dev: "d", ts: 1, srv: 1,
  pages: { "session-1": { ts: 1, order: ["กอนเรม", "a1"], names: { "กอนเรม": "ก่อนเริ่ม" }, acts: { "กอนเรม": A(1, 5, 0, 0), a1: A(0, 6, 0, 0) } } } } } });
eq("board carries names", P.board(t9, "session-1", 2).names, { "กอนเรม": "ก่อนเริ่ม" });
eq("day key is zero-padded", P.localDay(new Date(2026, 8, 5)), "2026-09-05");

console.log(failures ? failures + " failure(s)" : "progress.js: all checks pass");
process.exit(failures ? 1 : 0);
