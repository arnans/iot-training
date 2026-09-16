// Export the reviewed instructor copies to UTF-8 Aiken and a combined answer key.
// Run with --check to verify committed exports without changing files.
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '..', 'assessments');
const check = process.argv.includes('--check');
const letters = 'ABCD';
const ids = new Set();
const output = new Map();
let key = '# เฉลยและเกณฑ์ตรวจสำหรับผู้สอน\n\nเอกสารนี้มีคำตอบและคำอธิบายสำหรับแบบทดสอบทั้ง 6 ชุด รวม 45 ข้อ\n\n- ทุกข้อเป็นแบบเลือกตอบ 4 ตัวเลือก มีคำตอบที่ถูกเพียงข้อเดียว\n- ตอบถูกได้ 1 คะแนน ตอบผิดหรือไม่ตอบได้ 0 คะแนน\n- ไฟล์นี้และไฟล์ Aiken สร้างจากต้นฉบับ Markdown ด้วย `node scripts/export_assessments.cjs`\n- ไฟล์ Aiken มีเฉลยสำหรับนำเข้า LMS จึงไม่ควรแจกเป็นข้อสอบให้ผู้เรียนโดยตรง\n';
for (let session = 1; session <= 3; session++) {
  for (const phase of ['pre', 'post']) {
    const stem = `session-${session}-${phase}`;
    const source = fs.readFileSync(path.join(root, stem + '.md'), 'utf8').replace(/\r\n/g, '\n');
    const blocks = source.split(/^### ข้อ /m).slice(1);
    const expected = phase === 'pre' ? 5 : 10;
    assert.equal(blocks.length, expected, stem + ': question count');
    key += `\n## ช่วงที่ ${session} — ${phase === 'pre' ? 'ก่อนเรียน' : 'หลังเรียน'}\n`;
    const questions = blocks.map((block, index) => {
      const id = block.match(/รหัสข้อ: `([^`]+)`/)[1];
      assert.equal(id, `S${session}-${phase.toUpperCase()}-${String(index+1).padStart(2,'0')}`);
      assert(!ids.has(id), 'Duplicate ID: ' + id);
      ids.add(id);
      const question = block.match(/รหัสข้อ: `[^`]+`\r?\n\r?\n([^\r\n]+)\r?\n\r?\n- \*\*A\./)[1];
      const options = [...block.matchAll(/^- \*\*([A-D])\.\*\* (.+)$/gm)];
      assert.deepEqual(options.map(m => m[1]), [...letters], id + ': options');
      assert.equal(new Set(options.map(m => m[2].trim())).size, 4, id + ': duplicate options');
      const answer = block.match(/^- คำตอบ: \*\*([A-D])\. (.+)\*\*$/m);
      assert(answer, id + ': missing answer');
      assert.equal(answer[2], options[letters.indexOf(answer[1])][2], id + ': answer text');
      const notes = block.split('**เฉลยและเกณฑ์ตรวจ**')[1].trim();
      for (const field of ['เหตุผล', 'วัดความเข้าใจ', 'อ้างอิง', 'การให้คะแนน']) {
        assert(notes.includes(`- ${field}: `), id + ': missing ' + field);
      }
      key += `\n### ${id}\n\n- ประเภท: เลือกตอบ คำตอบเดียว\n${notes}\n`;
      return `[${id}] ${question}\n${options.map(m => `${m[1]}. ${m[2]}`).join('\n')}\nANSWER: ${answer[1]}`;
    });
    const aiken = questions.join('\n\n') + '\n';
    // Verify the actual output blocks, including Aiken's single-line question rule.
    for (const block of aiken.trim().split('\n\n')) {
      const lines = block.split('\n');
      assert.equal(lines.length, 6, stem + ': Aiken block length');
      assert(/^\[S[1-3]-(PRE|POST)-\d{2}\] .+/.test(lines[0]));
      letters.split('').forEach((letter, i) => assert(lines[i+1].startsWith(letter + '. ')));
      assert(/^ANSWER: [A-D]$/.test(lines[5]));
      assert(!block.includes('\uFFFD'), 'Invalid text encoding');
    }
    output.set(stem + '.txt', aiken);
  }
}
assert.equal(ids.size, 45);
output.set('answer-key.md', key);
for (const [name, contents] of output) {
  const target = path.join(root, name);
  if (check) assert.equal(fs.readFileSync(target, 'utf8').replace(/\r\n/g, '\n'), contents, name + ': export is out of date');
  else fs.writeFileSync(target, contents, 'utf8');
}
console.log(`${check ? 'Verified' : 'Exported'} 45 questions in 6 UTF-8 Aiken files and the answer key.`);
