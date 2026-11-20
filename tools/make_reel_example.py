import subprocess, random, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

W, H, FPS = 1080, 1920, 30
NAVY = (14, 27, 56)
GOLD = (236, 196, 104)
CREAM = (255, 246, 228)
SERIF = "/usr/share/fonts/truetype/google-fonts/ofl/cardo/Cardo-Bold.ttf"
SANS = "/usr/share/fonts/truetype/google-fonts/ofl/montserrat/Montserrat[wght].ttf"

def font(path, size, weight=None):
    f = ImageFont.truetype(path, size)
    if path == SANS:
        try: f.set_variation_by_axes([weight or 750])
        except Exception: pass
    return f

def story(name):
    return Image.open(f"src/{name}_img.png").convert("RGB")

def coloring(name):
    im = Image.open(f"src/{name}.png").convert("RGB")
    a = np.asarray(im).min(2)
    ys, xs = np.where(a < 200)
    pad = 30
    return im.crop((max(xs.min()-pad,0), max(ys.min()-pad,0), xs.max()+pad, ys.max()+pad))

def fit(im, maxw, maxh):
    r = min(maxw/im.width, maxh/im.height)
    return im.resize((int(im.width*r), int(im.height*r)), Image.LANCZOS)

def framed(im, paper=False):
    border = 18
    bg = Image.new("RGB", (im.width+2*border, im.height+2*border), CREAM if not paper else (255,255,255))
    bg.paste(im, (border, border))
    return bg

# background with soft vignette
bg = Image.new("RGB", (W, H), NAVY)
glow = Image.new("L", (W, H), 0)
ImageDraw.Draw(glow).ellipse((-200, 300, W+200, H-200), fill=90)
glow = glow.filter(ImageFilter.GaussianBlur(220))
bg = Image.composite(Image.new("RGB", (W, H), (40, 62, 110)), bg, glow)

random.seed(3)
flakes = [(random.uniform(0, W), random.uniform(0, H), random.uniform(2, 6), random.uniform(40, 120)) for _ in range(90)]

def draw_text_block(d, lines, y, size, color=GOLD, fnt=SERIF):
    f = font(fnt, size)
    for ln in lines:
        w = d.textlength(ln, font=f)
        d.text(((W-w)/2+3, y+3), ln, font=f, fill=(0,0,0))
        d.text(((W-w)/2, y), ln, font=f, fill=color)
        y += int(size*1.12)
    return y

# slides: (kind, source, card lines, duration)
slides = [
    ("story", "p5-05",  ["LOOK INSIDE THIS", "CHRISTMAS BOOK"], 2.4),
    ("story", "p4-04",  ["4 cozy", "Christmas stories"], 2.2),
    ("color", "p56-56",  ["40 pages", "to color"], 2.2),
    ("story", "p26-26", ["Meet Fina", "the little fox"], 2.0),
    ("color", "p32-32", ["Made for", "ages 3-6"], 2.0),
    ("story", "p71-71", ["No screens", "needed"], 2.0),
    ("end",   "cover", None, 3.2),
]

prepared = []
for kind, src, card, dur in slides:
    if kind == "story":
        im0 = story(src); r = 1150/im0.height
        img = im0.resize((int(im0.width*r), 1150), Image.LANCZOS)
    elif kind == "color":
        img = framed(fit(coloring(src), 940, 1180), paper=True)
    else:
        img = fit(Image.open("src/cover_front.png").convert("RGB"), 820, 1090)
    prepared.append((kind, img, card, dur))

def render_slide(kind, img, card, t, dur):
    fr = bg.copy()
    d = ImageDraw.Draw(fr)
    z = 1.0 + 0.05 * (t / dur)
    if kind == "story":
        win = 1000; maxoff = img.width - win
        off = int(maxoff*(0.15 + 0.7*(t/dur)))
        im = framed(img.crop((off, 0, off+win, img.height)))
    else:
        im = img.resize((int(img.width*z), int(img.height*z)), Image.BILINEAR)
    if kind == "end":
        y0 = 190
        fr.paste(im, ((W-im.width)//2, y0 + (img.height-im.height)//2))
        y = y0 + img.height + 50
        y = draw_text_block(d, ["The perfect Christmas gift"], y, 64, GOLD)
        draw_text_block(d, ["Link in bio"], y+10, 56, CREAM, SANS)
    else:
        cy = 1060
        fr.paste(im, ((W-im.width)//2, cy - im.height//2))
        if card:
            draw_text_block(d, card, 200, 100)
    # snow
    sd = ImageDraw.Draw(fr)
    return fr

def add_snow(fr, gt):
    d = ImageDraw.Draw(fr)
    for x, y, r, sp in flakes:
        yy = (y + sp*gt) % H
        xx = x + 18*math.sin(gt*0.8 + y)
        d.ellipse((xx-r, yy-r, xx+r, yy+r), fill=(255,255,255))
    return fr

proc = subprocess.Popen(["ffmpeg","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
    "-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p","-movflags","+faststart","reel1_fabelnori_look_inside.mp4"],
    stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

XF = 0.3
gt = 0.0
prev_last = None
for i, (kind, img, card, dur) in enumerate(prepared):
    n = int(dur*FPS)
    for k in range(n):
        t = k/FPS
        fr = render_slide(kind, img, card, t, dur)
        if prev_last is not None and t < XF:
            fr = Image.blend(prev_last, fr, t/XF)
        fr = add_snow(fr, gt)
        proc.stdin.write(fr.tobytes())
        gt += 1/FPS
    prev_last = render_slide(kind, img, card, dur, dur)
proc.stdin.close(); proc.wait()
# cover image
render_slide(*prepared[0][:3], 0.5, 2.4).convert("RGB").save("reel1_cover.jpg", quality=92)
print("done")
