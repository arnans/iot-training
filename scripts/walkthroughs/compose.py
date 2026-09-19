"""Composes a recorded walkthrough into the final MP4: title card, frames, drawn cursor and click ripples, caption strip.
   python compose.py a5-1-low-water   (the spec id)
Writes docs/images/walkthroughs/<id>.mp4 and <id>.png (the title card, used as the video poster).
Timing is edited here, not in the recording: each click gets PRE_CLICK_HOLD with the cursor already on
its target, and the idle wait recorded after a click is cut to KEEP_AFTER_CLICK before the next caption."""
import json, bisect, os, sys, shutil, subprocess
from pathlib import Path
from PIL import Image, ImageDraw
ROOT = Path(__file__).resolve().parents[2]
ID = sys.argv[1]
D = str(ROOT / '.tmp/walkthroughs' / ID)
OUT = ROOT / 'docs/images/walkthroughs'
T = json.load(open(D + '/timeline.json', encoding='utf-8'))
W, H, STRIP, SC, FPS = 1174, 869, 72, 1.2, 24
TITLE_S, END_HOLD_S = 3.0, 1.5
PRE_CLICK_HOLD = 0.6      # s held on the frame just before each click
KEEP_AFTER_CLICK = 0.7    # s of the recorded wait kept after a click before skipping to the next caption
CRF = os.environ.get('CRF', '24'); GOP = int(os.environ.get('GOP', 10 * FPS))  # quality (20-24 look the same on these screens); keyframe spacing — browsers still seek frame-accurately

frames = T['frames']; ft = [f['t'] for f in frames]
log = T['log']; lt = [e['t'] for e in log]; clicks = [e for e in log if e.get('click')]
caps = T['caps']; ct = [c['t'] for c in caps]
strips = [Image.open(f'{D}/cards/cap{i:02d}.png').convert('RGB') for i in range(len(caps))]
title = Image.open(D + '/cards/title.png').convert('RGB')
ARROW = [(0,0),(0,17),(4,13),(7,20),(10,19),(7,12),(12,12)]

def cursor(d, x, y, s=1.45):
    pts = [(x + px*s, y + py*s) for px, py in ARROW]
    d.polygon(pts, fill='black'); d.line(pts + [pts[0]], fill='white', width=2)

def pos(t):
    i = max(0, bisect.bisect_right(lt, t) - 1); return log[i]['x'], log[i]['y']

def render(t):
    fi = max(0, bisect.bisect_right(ft, t) - 1)
    ci = max(0, bisect.bisect_right(ct, t) - 1)
    x, y = pos(t); x *= SC; y *= SC
    ring = [(c, t - c['t']) for c in clicks if 0 <= t - c['t'] < 0.6]
    key = (fi, ci, round(x), round(y), tuple(round(a, 2) for _, a in ring))
    return key, lambda: draw(fi, ci, x, y, ring)

def draw(fi, ci, x, y, ring):
    im = Image.new('RGB', (W, H + STRIP))
    im.paste(Image.open(frames[fi]['file']).convert('RGB'), (0, 0)); im.paste(strips[ci], (0, H))
    d = ImageDraw.Draw(im, 'RGBA')
    for c, a in ring:   # click ripple: expanding ring plus a brief solid dot
        r = 12 + a * 55; al = int(220 * (1 - a / 0.6)); cx, cy = c['x'] * SC, c['y'] * SC
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(245, 165, 36, al), width=5)
        if a < 0.25: d.ellipse((cx - 9, cy - 9, cx + 9, cy + 9), fill=(245, 165, 36, 200))
    cursor(d, x, y)
    return im

# recorded time ranges to cut: the idle wait after each click, up to the next caption
skips = []
for c in clicks:
    nxt = [t for t in ct if t > c['t']]
    if nxt and nxt[0] - c['t'] > KEEP_AFTER_CLICK:
        skips.append((c['t'] + KEEP_AFTER_CLICK, nxt[0]))

ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H + STRIP}',
                       '-r', str(FPS), '-i', '-', '-vf', f'pad={W}:{(H + STRIP + 1) // 2 * 2}:0:0:color=0x1e2a1f',
                       '-c:v', 'libx264', '-preset', 'slow', '-crf', CRF, '-tune', 'animation', '-pix_fmt', 'yuv420p',
                       '-g', str(GOP), '-movflags', '+faststart', '-an', str(OUT / f'{ID}.mp4')], stdin=subprocess.PIPE)
n = 0
def emit(img, count):
    global n
    b = img.tobytes()
    for _ in range(count): ff.stdin.write(b)
    n += count

emit(title, round(TITLE_S * FPS))
pending = [c['t'] for c in clicks]
t, last_key, last_img = T['t0'], None, None
while t <= T['t1']:
    for a, b in skips:
        if a <= t < b: t = b
    while pending and t >= pending[0]:
        if last_img is not None: emit(last_img, round(PRE_CLICK_HOLD * FPS))
        pending.pop(0)
    key, mk = render(t)
    if key != last_key: last_img, last_key = mk(), key
    emit(last_img, 1)
    t += 1 / FPS
emit(last_img, round(END_HOLD_S * FPS))
ff.stdin.close(); ff.wait()
title.save(OUT / f'{ID}.png', optimize=True)
print(ID, n, 'frames', round(n / FPS, 1), 's', (OUT / f'{ID}.mp4').stat().st_size // 1024, 'KB')
