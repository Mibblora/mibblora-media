from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np, random
W,H=1080,1920; NAVY=(14,27,56); GOLD=(236,196,104); CREAM=(255,246,228)
SERIF="/usr/share/fonts/truetype/google-fonts/ofl/cardo/Cardo-Bold.ttf"
SANS="/usr/share/fonts/truetype/google-fonts/ofl/montserrat/Montserrat[wght].ttf"
S="/tmp/w/"; O="/home/claude/mibblora-media/stories/2026-11-25/"
def font(p,s):
    f=ImageFont.truetype(p,s)
    if p==SANS:
        try: f.set_variation_by_axes([700])
        except Exception: pass
    return f
def base(seed):
    bg=Image.new("RGB",(W,H),NAVY); g=Image.new("L",(W,H),0)
    ImageDraw.Draw(g).ellipse((-200,300,W+200,H-200),fill=90); g=g.filter(ImageFilter.GaussianBlur(220))
    bg=Image.composite(Image.new("RGB",(W,H),(40,62,110)),bg,g); d=ImageDraw.Draw(bg); random.seed(seed)
    for _ in range(110):
        x,y,r=random.uniform(0,W),random.uniform(0,H),random.uniform(2,5); d.ellipse((x-r,y-r,x+r,y+r),fill=(255,255,255))
    return bg
def txt(d,lines,y,size,color=GOLD,fnt=SERIF):
    f=font(fnt,size)
    for ln in lines:
        w=d.textlength(ln,font=f); d.text(((W-w)/2+3,y+3),ln,font=f,fill=(0,0,0)); d.text(((W-w)/2,y),ln,font=f,fill=color); y+=int(size*1.15)
    return y
def coloring(f):
    im=Image.open(S+f).convert("RGB"); a=np.asarray(im).min(2); ys,xs=np.where(a<200); p=30
    return im.crop((max(xs.min()-p,0),max(ys.min()-p,0),xs.max()+p,ys.max()+p))
def fit(im,mw,mh):
    r=min(mw/im.width,mh/im.height); return im.resize((int(im.width*r),int(im.height*r)),Image.LANCZOS)
def framed(im,col=(255,255,255),b=14):
    bg=Image.new("RGB",(im.width+2*b,im.height+2*b),col); bg.paste(im,(b,b)); return bg
# Story 1: before/after teaser for tonight's reel
bg=base(5); d=ImageDraw.Draw(bg)
y=txt(d,["Blank page...","to cozy story"],270,92)
c=framed(fit(coloring("q32-32.png"),470,700)); s=Image.open(S+"s-000.png").convert("RGB"); s=s.crop((4,4,s.width-4,s.height-4))
r=700/s.height; s=s.resize((int(s.width*r),700),Image.LANCZOS); s=s.crop(((s.width-470)//2,0,(s.width-470)//2+470,700)).filter(ImageFilter.UnsharpMask(2,60,2)); s=framed(s,CREAM)
bg.paste(c,(40,560)); bg.paste(s,(W-40-s.width,560))
f=font(SANS,36)
for lab,cx in (("BEFORE",40+c.width//2),("AFTER",W-40-s.width//2)):
    w=d.textlength(lab,font=f); d.rounded_rectangle((cx-w/2-22,1290,cx+w/2+22,1346),16,fill=GOLD); d.text((cx-w/2,1297),lab,font=f,fill=NAVY)
txt(d,["Meet Fina the little fox"],1400,52,CREAM,SANS)
txt(d,["New reel tonight on our profile"],1500,44,GOLD,SANS)
bg.save(O+"story_before_after.jpg",quality=92)
# Story 2: peek inside, coloring page 28
bg=base(9); d=ImageDraw.Draw(bg)
txt(d,["Peek inside"],270,104)
c=framed(fit(coloring("q28-28.png"),760,1000)); bg.paste(c,((W-c.width)//2,440))
y=440+c.height+40; y=txt(d,["Christmas in the Enchanted Forest"],y,44,CREAM,SANS); txt(d,["Link in bio"],y+14,52,GOLD,SANS)
print(y); bg.save(O+"story_peek_inside.jpg",quality=92)
