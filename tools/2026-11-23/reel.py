import subprocess, random, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
W,H,FPS=1080,1920,30
NAVY=(14,27,56); GOLD=(236,196,104); CREAM=(255,246,228)
SERIF="/usr/share/fonts/truetype/google-fonts/ofl/cardo/Cardo-Bold.ttf"
SANS="/usr/share/fonts/truetype/google-fonts/ofl/montserrat/Montserrat[wght].ttf"
S="/tmp/w/"
def font(p,s):
    f=ImageFont.truetype(p,s)
    if p==SANS:
        try: f.set_variation_by_axes([700])
        except Exception: pass
    return f
def story(p):
    im=Image.open(f"{S}s{p}.png").convert("RGB"); return im.crop((12,12,im.width-12,im.height-12))
def coloring(p):
    im=Image.open(f"{S}p{p}-{p:02d}.png").convert("RGB"); a=np.asarray(im).min(2)
    ys,xs=np.where(a<200); pad=30
    return im.crop((max(xs.min()-pad,0),max(ys.min()-pad,0),xs.max()+pad,ys.max()+pad))
def fit(im,mw,mh):
    r=min(mw/im.width,mh/im.height); return im.resize((int(im.width*r),int(im.height*r)),Image.LANCZOS)
def framed(im,paper=False,b=18):
    bg=Image.new("RGB",(im.width+2*b,im.height+2*b),(255,255,255) if paper else CREAM); bg.paste(im,(b,b)); return bg
cov=Image.open(S+"cover-1.png").convert("RGB")
front=cov.crop((int(cov.width*0.535),int(cov.height*0.012),int(cov.width*0.99),int(cov.height*0.988)))
front.save("cover_front.png")
bg=Image.new("RGB",(W,H),NAVY); glow=Image.new("L",(W,H),0)
ImageDraw.Draw(glow).ellipse((-200,300,W+200,H-200),fill=90); glow=glow.filter(ImageFilter.GaussianBlur(220))
bg=Image.composite(Image.new("RGB",(W,H),(40,62,110)),bg,glow)
random.seed(11)
flakes=[(random.uniform(0,W),random.uniform(0,H),random.uniform(2,6),random.uniform(40,120)) for _ in range(90)]
def txt(d,lines,y,size,color=GOLD,fnt=SERIF):
    f=font(fnt,size)
    for ln in lines:
        w=d.textlength(ln,font=f); d.text(((W-w)/2+3,y+3),ln,font=f,fill=(0,0,0)); d.text(((W-w)/2,y),ln,font=f,fill=color); y+=int(size*1.12)
    return y
slides=[("story",5,["The Christmas star","lost its glow"],2.8),
        ("story",71,["4 friends set off","to help"],2.4),
        ("color",8,["40 pages","to color"],2.2),
        ("story",26,["4 cozy","Christmas stories"],2.2),
        ("color",56,["For kids","3 and up"],2.0),
        ("story",48,["Read, color","and dream"],2.0),
        ("end",None,None,3.6)]
prep=[]
for k,src,card,dur in slides:
    if k=="story":
        im0=story(src); r=1150/im0.height; img=im0.resize((int(im0.width*r),1150),Image.LANCZOS)
    elif k=="color": img=framed(fit(coloring(src),900,1150),paper=True)
    else: img=fit(front,820,1090)
    prep.append((k,img,card,dur))
def render(k,img,card,t,dur):
    fr=bg.copy(); d=ImageDraw.Draw(fr); z=1.0+0.05*(t/dur)
    if k=="story":
        win=1000; off=int((img.width-win)*(0.15+0.7*(t/dur))); im=framed(img.crop((off,0,off+win,img.height)))
    else: im=img.resize((int(img.width*z),int(img.height*z)),Image.BILINEAR)
    if k=="end":
        y0=230; fr.paste(im,((W-im.width)//2,y0+(img.height-im.height)//2))
        y=y0+img.height+50; y=txt(d,["Help the star shine again"],y,64); txt(d,["Link in bio"],y+10,56,CREAM,SANS)
    else:
        fr.paste(im,((W-im.width)//2,1080-im.height//2))
        if card: txt(d,card,215,96)
    return fr
def snow(fr,gt):
    d=ImageDraw.Draw(fr)
    for x,y,r,sp in flakes:
        yy=(y+sp*gt)%H; xx=x+18*math.sin(gt*0.8+y); d.ellipse((xx-r,yy-r,xx+r,yy+r),fill=(255,255,255))
    return fr
total=sum(s[3] for s in slides); print("dur",total)
subprocess.run(["python3","music.py",str(total)],check=True)
p=subprocess.Popen(["ffmpeg","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-i","music.wav",
 "-c:v","libx264","-profile:v","main","-level","4.0","-preset","medium","-crf","19","-bf","0","-g","30","-r","30","-pix_fmt","yuv420p",
 "-c:a","aac","-b:a","128k","-ar","48000","-ac","2","-shortest","-movflags","+faststart","reel.mp4"],stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
gt=0; prev=None; XF=0.3
for i,(k,img,card,dur) in enumerate(prep):
    for n in range(int(round(dur*FPS))):
        t=n/FPS; fr=render(k,img,card,t,dur)
        if prev is not None and t<XF: fr=Image.blend(prev,fr,t/XF)
        fr=snow(fr,gt); p.stdin.write(fr.tobytes()); gt+=1/FPS
        if i==0 and n==30: fr.save("frame_hook.jpg",quality=90)
        if k=="end" and n==60: fr.save("frame_end.jpg",quality=90)
        if i==2 and n==40: fr.save("frame_color.jpg",quality=90)
    prev=render(k,img,card,dur,dur)
p.stdin.close(); p.wait(); print("ok",p.returncode)
