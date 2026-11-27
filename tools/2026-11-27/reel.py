# Reel 2026-11-27: Black Friday, screen-free Christmas gift, both Christmas books
import subprocess, random, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
W,H,FPS=1080,1920,30
NAVY=(14,27,56); GOLD=(236,196,104); CREAM=(255,246,228)
SERIF="/usr/share/fonts/truetype/google-fonts/ofl/cardo/Cardo-Bold.ttf"
SANS="/usr/share/fonts/truetype/google-fonts/ofl/montserrat/Montserrat[wght].ttf"
S="/tmp/w/"; OUT="/home/claude/mibblora-media/reels/reel4_black_friday_screen_free_gift.mp4"
def font(p,s):
    f=ImageFont.truetype(p,s)
    if p==SANS:
        try: f.set_variation_by_axes([700])
        except Exception: pass
    return f
def coloring(f):
    im=Image.open(S+f).convert("RGB"); a=np.asarray(im).min(2)
    ys,xs=np.where(a<200); pad=30
    return im.crop((max(xs.min()-pad,0),max(ys.min()-pad,0),xs.max()+pad,ys.max()+pad))
def fit(im,mw,mh):
    r=min(mw/im.width,mh/im.height); return im.resize((int(im.width*r),int(im.height*r)),Image.LANCZOS)
def framed(im,col=CREAM,b=16):
    bg=Image.new("RGB",(im.width+2*b,im.height+2*b),col); bg.paste(im,(b,b)); return bg
def front(f):
    c=Image.open(S+f).convert("RGB")
    return c.crop((int(c.width*0.508),int(c.height*0.012),int(c.width*0.99),int(c.height*0.988)))
CS=front("cov_cs-1.png"); EF=front("cov_ef-1.png"); CS.save(S+"front_cs.png"); EF.save(S+"front_ef.png")
def two_covers(h,gap=40):
    a=fit(EF,2000,h); b=fit(CS,2000,h); a=framed(a,CREAM,8); b=framed(b,CREAM,8)
    im=Image.new("RGB",(a.width+b.width+gap,max(a.height,b.height)),NAVY); im.paste(a,(0,0)); im.paste(b,(a.width+gap,0)); return im
bg=Image.new("RGB",(W,H),NAVY); glow=Image.new("L",(W,H),0)
ImageDraw.Draw(glow).ellipse((-200,300,W+200,H-200),fill=90); glow=glow.filter(ImageFilter.GaussianBlur(220))
bg=Image.composite(Image.new("RGB",(W,H),(40,62,110)),bg,glow)
random.seed(27)
flakes=[(random.uniform(0,W),random.uniform(0,H),random.uniform(2,6),random.uniform(40,120)) for _ in range(90)]
def txt(d,lines,y,size,color=GOLD,fnt=SERIF):
    f=font(fnt,size)
    for ln in lines:
        w=d.textlength(ln,font=f); d.text(((W-w)/2+3,y+3),ln,font=f,fill=(0,0,0)); d.text(((W-w)/2,y),ln,font=f,fill=color); y+=int(size*1.12)
    return y
def chip(d,label,y):
    f=font(SANS,38); w=d.textlength(label,font=f)
    d.rounded_rectangle(((W-w)/2-26,y,(W+w)/2+26,y+64),20,fill=GOLD); d.text(((W-w)/2,y+10),label,font=f,fill=NAVY)
def story_panel(f,h=None):
    im=Image.open(S+f).convert("RGB"); im=im.crop((4,4,im.width-4,im.height-4))
    r=1000/im.width; im=im.resize((1000,int(im.height*r)),Image.LANCZOS).filter(ImageFilter.UnsharpMask(2,50,2)); return framed(im)
slides=[("hook",two_covers(560),["A gift that","isn't a screen"],3.0),
        ("wide",story_panel("s_cs70-000.jpg"),["Cozy stories","to read together"],2.4),
        ("color",framed(fit(coloring("q_cs-54.png"),900,1120),(255,255,255)),["40 pages","to color"],2.2),
        ("wide",story_panel("s_ef49-000.png"),["Two books,","8 Christmas stories"],2.4),
        ("color",framed(fit(coloring("q_ef-86.png"),900,1120),(255,255,255)),["Read, color,","repeat"],2.2),
        ("end",two_covers(700,30),None,3.6)]
def render(k,img,card,t,dur):
    fr=bg.copy(); d=ImageDraw.Draw(fr); z=1.0+0.05*(t/dur)
    im=img.resize((int(img.width*z),int(img.height*z)),Image.BILINEAR)
    if k=="hook":
        chip(d,"BLACK FRIDAY GIFT IDEA",250)
        txt(d,card,360,104)
        fr.paste(im,((W-im.width)//2,1180-im.height//2))
        txt(d,["For kids ages 3-6"],1520,54,CREAM,SANS)
    elif k=="wide":
        fr.paste(im,((W-im.width)//2,1080-im.height//2)); txt(d,card,250,96)
    elif k=="color":
        fr.paste(im,((W-im.width)//2,1100-im.height//2)); txt(d,card,210,96)
    else:
        y0=300; fr.paste(im,((W-im.width)//2,y0+(img.height-im.height)//2))
        y=y0+img.height+60; y=txt(d,["Screen-free Christmas","starts here"],y,72); txt(d,["Link in bio"],y+14,58,CREAM,SANS)
    return fr
def snow(fr,gt):
    d=ImageDraw.Draw(fr)
    for x,y,r,sp in flakes:
        yy=(y+sp*gt)%H; xx=x+18*math.sin(gt*0.8+y); d.ellipse((xx-r,yy-r,xx+r,yy+r),fill=(255,255,255))
    return fr
total=sum(s[3] for s in slides)
subprocess.run(["python3","music.py",str(total)],check=True)
proc=subprocess.Popen(["ffmpeg","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-i","music.wav",
 "-c:v","libx264","-profile:v","main","-level","4.0","-preset","medium","-crf","19","-bf","0","-g","30","-pix_fmt","yuv420p",
 "-c:a","aac","-b:a","128k","-ar","48000","-ac","2","-shortest","-movflags","+faststart",OUT],stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
XF=0.3; gt=0.0; prev=None
for i,(k,img,card,dur) in enumerate(slides):
    for n in range(int(round(dur*FPS))):
        t=n/FPS; fr=render(k,img,card,t,dur)
        if prev is not None and t<XF: fr=Image.blend(prev,fr,t/XF)
        out=snow(fr,gt); proc.stdin.write(out.tobytes()); gt+=1/FPS
        if n==30: out.save(S+f"prev_{i}.jpg")
    prev=render(k,img,card,dur,dur)
proc.stdin.close(); proc.wait(); print("done",total)
