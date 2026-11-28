# Carousel 2026-11-28: 5 screen-free gifts for ages 3-6 (gift guide, both Christmas books)
# Inputs rendered to /tmp/w with pdftoppm (covers 150 dpi, pages 300 dpi)
import random, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
W,H=1080,1350; NAVY=(14,27,56); GOLD=(236,196,104); CREAM=(255,246,228)
SERIF="/usr/share/fonts/truetype/google-fonts/ofl/cardo/Cardo-Bold.ttf"
SANS="/usr/share/fonts/truetype/google-fonts/ofl/montserrat/Montserrat[wght].ttf"
S="/tmp/w/"; O="/home/claude/mibblora-media/posts/2026-11-28/"
import os; os.makedirs(O,exist_ok=True)
N=7
def font(p,s,wt=700):
    f=ImageFont.truetype(p,s)
    if p==SANS:
        try: f.set_variation_by_axes([wt])
        except Exception: pass
    return f
def base(seed):
    bg=Image.new("RGB",(W,H),NAVY); g=Image.new("L",(W,H),0)
    ImageDraw.Draw(g).ellipse((-200,200,W+200,H-100),fill=90); g=g.filter(ImageFilter.GaussianBlur(200))
    bg=Image.composite(Image.new("RGB",(W,H),(40,62,110)),bg,g); d=ImageDraw.Draw(bg); random.seed(seed)
    for _ in range(80):
        x,y,r=random.uniform(0,W),random.uniform(0,H),random.uniform(2,5); d.ellipse((x-r,y-r,x+r,y+r),fill=(255,255,255))
    return bg
def txt(d,lines,y,size,color=GOLD,fnt=SERIF,wt=700):
    f=font(fnt,size,wt)
    for ln in lines:
        w=d.textlength(ln,font=f); d.text(((W-w)/2+3,y+3),ln,font=f,fill=(0,0,0)); d.text(((W-w)/2,y),ln,font=f,fill=color); y+=int(size*1.2)
    return y
def chrome(bg,i):
    d=ImageDraw.Draw(bg); f=font(SANS,30,600)
    d.text((130,H-110),"@mibblora",font=f,fill=CREAM)
    s=f"{i}/{N}"; d.text((W-130-d.textlength(s,font=f),H-110),s,font=f,fill=CREAM)
def coloring(fn):
    im=Image.open(S+fn).convert("RGB"); a=np.asarray(im).min(2); ys,xs=np.where(a<200); p=30
    return im.crop((max(xs.min()-p,0),max(ys.min()-p,0),xs.max()+p,ys.max()+p))
def fit(im,mw,mh):
    r=min(mw/im.width,mh/im.height); return im.resize((int(im.width*r),int(im.height*r)),Image.LANCZOS)
def framed(im,col=CREAM,b=12):
    bg=Image.new("RGB",(im.width+2*b,im.height+2*b),col); bg.paste(im,(b,b)); return bg
def front(fn):
    c=Image.open(S+fn).convert("RGB")
    return c.crop((int(c.width*0.508),int(c.height*0.012),int(c.width*0.99),int(c.height*0.988)))
EF=front("cov_ef-1.png"); CS=front("cov_cs-1.png")
def badge(d,num,y):
    r=46; d.ellipse((W/2-r,y,W/2+r,y+2*r),fill=GOLD); f=font(SERIF,64)
    s=str(num); w=d.textlength(s,font=f); d.text((W/2-w/2,y+6),s,font=f,fill=NAVY)
def save(bg,i,name):
    chrome(bg,i); bg.save(O+f"{i:02d}_{name}.jpg",quality=90); print(i,name)

# 1 Cover
bg=base(128); d=ImageDraw.Draw(bg)
f=font(SANS,32); lab="GIFT GUIDE"; w=d.textlength(lab,font=f)
d.rounded_rectangle(((W-w)/2-26,150,(W+w)/2+26,206),18,fill=GOLD); d.text(((W-w)/2,158),lab,font=f,fill=NAVY)
txt(d,["5 screen-free gifts","for ages 3-6"],240,92)
a=framed(fit(coloring("q_ef-44.png"),360,520),(255,255,255)); b=framed(fit(coloring("q_cs-22.png"),360,520),(255,255,255))
a=a.rotate(5,expand=True,fillcolor=NAVY,resample=Image.BICUBIC); b=b.rotate(-5,expand=True,fillcolor=NAVY,resample=Image.BICUBIC)
x0=(W-a.width-b.width+40)//2; bg.paste(a,(x0,500)); bg.paste(b,(x0+a.width-40,520))
txt(d,["Cozy ideas for little hands"],1110,40,CREAM,SANS,600)
save(bg,1,"cover")

# 2 Christmas in the Enchanted Forest
bg=base(2); d=ImageDraw.Draw(bg); badge(d,1,120)
txt(d,["A Christmas story book"],230,64)
c=framed(fit(EF,340,500)); p=framed(fit(Image.open(S+"pic_ef-70.png"),500,500))
x0=(W-c.width-p.width-30)//2; bg.paste(c,(x0,400)); bg.paste(p,(x0+c.width+30,400+(c.height-p.height)//2))
y=txt(d,["Christmas in the Enchanted Forest"],1000,40,GOLD,SANS)
txt(d,["4 cozy stories to read together,","plus 40 coloring pages."],y+20,36,CREAM,SANS,500)
save(bg,2,"enchanted_forest")

# 3 The Secret of the Christmas Stars
bg=base(3); d=ImageDraw.Draw(bg); badge(d,2,120)
txt(d,["A bedtime star story"],230,64)
c=framed(fit(CS,340,500)); p=framed(fit(Image.open(S+"pic_cs-26.png"),500,500))
x0=(W-c.width-p.width-30)//2; bg.paste(c,(x0,400)); bg.paste(p,(x0+c.width+30,400+(c.height-p.height)//2))
y=txt(d,["The Secret of the Christmas Stars"],1000,40,GOLD,SANS)
txt(d,["4 Christmas stories with little friends,","plus 40 coloring pages."],y+20,36,CREAM,SANS,500)
save(bg,3,"christmas_stars")

# 4 Chunky crayons (drawn)
bg=base(4); d=ImageDraw.Draw(bg); badge(d,3,120)
txt(d,["Chunky crayons"],230,72)
cols=[(229,75,75),(245,166,35),(248,214,72),(92,184,92),(66,139,202),(155,89,182)]
cx=W/2-3*110+55
for k,cl in enumerate(cols):
    x=cx+k*110-35; top=420+abs(k-2.5)*30
    d.polygon([(x,top+80),(x+35,top),(x+70,top+80)],fill=cl)
    d.rounded_rectangle((x,top+80,x+70,top+500),10,fill=cl)
    d.rectangle((x,top+170,x+70,top+215),fill=CREAM); d.rectangle((x,top+380,x+70,top+425),fill=CREAM)
txt(d,["Thick and easy to grip for small hands.","Pairs well with a coloring book."],1010,36,CREAM,SANS,500)
save(bg,4,"crayons")

# 5 Play dough (drawn)
bg=base(5); d=ImageDraw.Draw(bg); badge(d,4,120)
txt(d,["A play dough set"],230,72)
for k,(cl,x,y,r) in enumerate([((229,75,75),330,600,130),((92,184,92),600,560,150),((66,139,202),780,760,120),((248,214,72),420,820,110)]):
    d.ellipse((x-r,y-r*0.8,x+r,y+r*0.8),fill=cl)
    d.ellipse((x-r*0.5,y-r*0.6,x-r*0.1,y-r*0.35),fill=tuple(min(255,c+60) for c in cl))
txt(d,["Squish, roll and shape.","Great for a quiet afternoon at the table."],1010,36,CREAM,SANS,500)
save(bg,5,"play_dough")

# 6 Flashlight for bedtime stories (drawn + star coloring page)
bg=base(6); d=ImageDraw.Draw(bg); badge(d,5,120)
txt(d,["A story-time flashlight"],230,64)
pg=framed(fit(coloring("q_cs-30.png"),420,560),(255,255,255)); bg.paste(pg,(560,380))
beam=Image.new("L",(W,H),0); ImageDraw.Draw(beam).polygon([(380,700),(600,420),(980,940),(400,760)],fill=70)
beam=beam.filter(ImageFilter.GaussianBlur(30)); bg=Image.composite(Image.new("RGB",(W,H),(255,240,190)),bg,beam); d=ImageDraw.Draw(bg)
fl=Image.new("RGBA",(420,140),(0,0,0,0)); fd=ImageDraw.Draw(fl)
fd.rounded_rectangle((0,30,300,110),24,fill=(66,139,202)); fd.polygon([(290,20),(400,0),(400,140),(290,120)],fill=(236,196,104)); fd.rectangle((120,45,160,95),fill=CREAM)
fl=fl.rotate(25,expand=True,resample=Image.BICUBIC); bg.paste(fl,(90,640),fl)
txt(d,["Lights off, one more story under the covers.","Makes bedtime feel like an adventure."],1010,36,CREAM,SANS,500)
save(bg,6,"flashlight")

# 7 Recap + CTA
bg=base(7); d=ImageDraw.Draw(bg)
txt(d,["Save this gift list"],150,76)
items=["1  Christmas in the Enchanted Forest","2  The Secret of the Christmas Stars","3  Chunky crayons","4  A play dough set","5  A story-time flashlight"]
f=font(SANS,38,600); y=290
for it in items:
    d.text((150,y),it,font=f,fill=CREAM); y+=62
a=framed(fit(EF,300,430)); b=framed(fit(CS,300,430)); x0=(W-a.width-b.width-40)//2
bg.paste(a,(x0,650)); bg.paste(b,(x0+a.width+40,650))
txt(d,["Both books: Link in bio"],1110,48,GOLD,SANS)
save(bg,7,"save_link_in_bio")
