# Stories 2026-11-28: gift guide teaser + peek inside Enchanted Forest (page 60)
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np, random
W,H=1080,1920; NAVY=(14,27,56); GOLD=(236,196,104); CREAM=(255,246,228)
SERIF="/usr/share/fonts/truetype/google-fonts/ofl/cardo/Cardo-Bold.ttf"
SANS="/usr/share/fonts/truetype/google-fonts/ofl/montserrat/Montserrat[wght].ttf"
S="/tmp/w/"; O="/home/claude/mibblora-media/stories/2026-11-28/"; P="/home/claude/mibblora-media/posts/2026-11-28/"
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
def framed(im,col=(255,255,255),b=12):
    bg=Image.new("RGB",(im.width+2*b,im.height+2*b),col); bg.paste(im,(b,b)); return bg
# 1 teaser
bg=base(281); d=ImageDraw.Draw(bg)
f=font(SANS,38); lab="NEW GIFT GUIDE"; w=d.textlength(lab,font=f)
d.rounded_rectangle(((W-w)/2-26,270,(W+w)/2+26,334),20,fill=GOLD); d.text(((W-w)/2,280),lab,font=f,fill=NAVY)
c=framed(fit(Image.open(P+"01_cover.jpg"),760,950),CREAM,10); bg.paste(c,((W-c.width)//2,400))
y=400+c.height+50; txt(d,["New post tonight on our profile"],y,46,CREAM,SANS)
bg.save(O+"story_gift_guide_teaser.jpg",quality=92); print("s1",y)
# 2 peek inside EF p60
bg=base(282); d=ImageDraw.Draw(bg)
txt(d,["Peek inside"],270,104)
c=framed(fit(coloring("q_ef-60.png"),740,980)); bg.paste(c,((W-c.width)//2,440))
y=440+c.height+40; y=txt(d,["Christmas in the Enchanted Forest"],y,44,CREAM,SANS); y=txt(d,["Link in bio"],y+14,52,GOLD,SANS)
bg.save(O+"story_peek_inside.jpg",quality=92); print("s2",y)
