# Reel 2026-11-25: enchanted-forest before/after, Fina the fox
import subprocess, random, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
W,H,FPS=1080,1920,30
NAVY=(14,27,56); GOLD=(236,196,104); CREAM=(255,246,228)
SERIF="/usr/share/fonts/truetype/google-fonts/ofl/cardo/Cardo-Bold.ttf"
SANS="/usr/share/fonts/truetype/google-fonts/ofl/montserrat/Montserrat[wght].ttf"
S="/tmp/w/"; OUT="/home/claude/mibblora-media/reels/reel3_enchanted_forest_fina_before_after.mp4"
def font(p,s):
    f=ImageFont.truetype(p,s)
    if p==SANS:
        try: f.set_variation_by_axes([700])
        except Exception: pass
    return f
def story(name):
    im=Image.open(S+name).convert("RGB"); im=im.crop((4,4,im.width-4,im.height-4))
    return im
def coloring(p):
    im=Image.open(f"{S}p{p}-{p}.png").convert("RGB"); a=np.asarray(im).min(2)
    ys,xs=np.where(a<200); pad=30
    return im.crop((max(xs.min()-pad,0),max(ys.min()-pad,0),xs.max()+pad,ys.max()+pad))
def fit(im,mw,mh):
    r=min(mw/im.width,mh/im.height); return im.resize((int(im.width*r),int(im.height*r)),Image.LANCZOS)
def cover_fit(im,w,h):
    r=max(w/im.width,h/im.height); im=im.resize((int(im.width*r)+1,int(im.height*r)+1),Image.LANCZOS)
    x=(im.width-w)//2; y=(im.height-h)//2; return im.crop((x,y,x+w,y+h))
def framed(im,paper=False,b=16):
    bg=Image.new("RGB",(im.width+2*b,im.height+2*b),(255,255,255) if paper else CREAM); bg.paste(im,(b,b)); return bg
cov=Image.open(S+"coverhi-1.png").convert("RGB")
front=cov.crop((int(cov.width*0.508),int(cov.height*0.012),int(cov.width*0.99),int(cov.height*0.988)))
front.save(S+"cover_front.png")
bg=Image.new("RGB",(W,H),NAVY); glow=Image.new("L",(W,H),0)
ImageDraw.Draw(glow).ellipse((-200,300,W+200,H-200),fill=90); glow=glow.filter(ImageFilter.GaussianBlur(220))
bg=Image.composite(Image.new("RGB",(W,H),(40,62,110)),bg,glow)
random.seed(25)
flakes=[(random.uniform(0,W),random.uniform(0,H),random.uniform(2,6),random.uniform(40,120)) for _ in range(90)]
def txt(d,lines,y,size,color=GOLD,fnt=SERIF):
    f=font(fnt,size)
    for ln in lines:
        w=d.textlength(ln,font=f); d.text(((W-w)/2+3,y+3),ln,font=f,fill=(0,0,0)); d.text(((W-w)/2,y),ln,font=f,fill=color); y+=int(size*1.12)
    return y
# before/after panel: same size box, coloring page vs story picture
BW,BH=940,1150
before=Image.new("RGB",(BW,BH),(255,255,255)); c=fit(coloring(32),BW-40,BH-40); before.paste(c,((BW-c.width)//2,(BH-c.height)//2))
after=cover_fit(story("s-000.png").filter(ImageFilter.UnsharpMask(1.2,60,2)),BW,BH)
def story_panel(name):
    im=story(name); r=1000/im.width; im=im.resize((1000,int(im.height*r)),Image.LANCZOS).filter(ImageFilter.UnsharpMask(2,50,2)); return im
slides=[("ba",None,["Blank page...","to cozy story"],4.8),
        ("color",36,["40 pages","to color"],2.2),
        ("wide","s-001.png",["Fina's lantern","lights the way"],2.3),
        ("color",64,["Made for","ages 3-6"],2.1),
        ("wide","s48-000.png",["4 cozy","Christmas stories"],2.1),
        ("end",None,None,3.4)]
prep=[]
for k,src,card,dur in slides:
    if k=="color": img=framed(fit(coloring(src),900,1150),paper=True)
    elif k=="wide": img=framed(story_panel(src))
    elif k=="end": img=fit(front,820,1040)
    else: img=None
    prep.append((k,img,card,dur))
def ease(x): x=min(max(x,0),1); return x*x*(3-2*x)
def render(k,img,card,t,dur):
    fr=bg.copy(); d=ImageDraw.Draw(fr); z=1.0+0.05*(t/dur)
    if k=="ba":
        p=ease((t-1.6)/1.4); cut=int(BW*p)
        im=before.copy()
        if cut>0: im.paste(after.crop((0,0,cut,BH)),(0,0))
        im=framed(im,paper=True)
        x0=(W-im.width)//2; y0=1080-im.height//2; fr.paste(im,(x0,y0))
        if 0<cut<BW:
            d.rectangle((x0+16+cut-3,y0+16,x0+16+cut+3,y0+16+BH),fill=GOLD)
        lab="BEFORE" if p<0.5 else "AFTER"
        f=font(SANS,40); w=d.textlength(lab,font=f)
        d.rounded_rectangle(((W-w)/2-24,y0+BH-60,(W+w)/2+24,y0+BH+4),18,fill=NAVY); d.text(((W-w)/2,y0+BH-54),lab,font=f,fill=CREAM)
        txt(d,card[:1] if t<1.6 else card,200,100)
    elif k=="wide":
        im=img.resize((int(img.width*z),int(img.height*z)),Image.BILINEAR); fr.paste(im,((W-im.width)//2,1060-im.height//2))
        txt(d,card,240,100)
    elif k=="color":
        im=img.resize((int(img.width*z),int(img.height*z)),Image.BILINEAR); fr.paste(im,((W-im.width)//2,1080-im.height//2))
        txt(d,card,200,100)
    else:
        im=img.resize((int(img.width*z),int(img.height*z)),Image.BILINEAR)
        y0=250; fr.paste(im,((W-im.width)//2,y0+(img.height-im.height)//2))
        y=y0+img.height+50; y=txt(d,["Color Fina's Christmas"],y,66); txt(d,["Link in bio"],y+10,56,CREAM,SANS)
    return fr
def snow(fr,gt):
    d=ImageDraw.Draw(fr)
    for x,y,r,sp in flakes:
        yy=(y+sp*gt)%H; xx=x+18*math.sin(gt*0.8+y); d.ellipse((xx-r,yy-r,xx+r,yy+r),fill=(255,255,255))
    return fr
total=sum(s[3] for s in prep)
subprocess.run(["python3","music.py",str(total)],check=True)
proc=subprocess.Popen(["ffmpeg","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-i","music.wav",
 "-c:v","libx264","-profile:v","main","-level","4.0","-preset","medium","-crf","19","-bf","0","-g","30","-pix_fmt","yuv420p",
 "-c:a","aac","-b:a","128k","-ar","48000","-ac","2","-shortest","-movflags","+faststart",OUT],stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
XF=0.3; gt=0.0; prev=None
for i,(k,img,card,dur) in enumerate(prep):
    for n in range(int(round(dur*FPS))):
        t=n/FPS; fr=render(k,img,card,t,dur)
        if prev is not None and t<XF: fr=Image.blend(prev,fr,t/XF)
        proc.stdin.write(snow(fr,gt).tobytes()); gt+=1/FPS
        if i==0 and n==45: snow(fr.copy(),gt).save(S+"prev_0.jpg")
        if i==0 and n==120: snow(fr.copy(),gt).save(S+"prev_1.jpg")
        if n==30 and i>0: snow(fr.copy(),gt).save(S+f"prev_{i+1}.jpg")
    prev=render(k,img,card,dur,dur)
proc.stdin.close(); proc.wait(); print("done",total)
