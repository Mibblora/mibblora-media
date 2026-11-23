from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
W,H=1080,1920; NAVY=(14,27,56); GOLD=(236,196,104); CREAM=(255,246,228)
SERIF="/usr/share/fonts/truetype/google-fonts/ofl/cardo/Cardo-Bold.ttf"
SANS="/usr/share/fonts/truetype/google-fonts/ofl/montserrat/Montserrat[wght].ttf"
def font(p,s):
    f=ImageFont.truetype(p,s)
    if p==SANS:
        try: f.set_variation_by_axes([650])
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
def framed(im,b=16):
    bg=Image.new("RGB",(im.width+2*b,im.height+2*b),CREAM); bg.paste(im,(b,b)); return bg
# story 1: meet the friends (all four)
s=Image.open("/tmp/w/s71.png").convert("RGB"); s=s.crop((12,12,s.width-12,s.height-12))
fr=base(5); d=ImageDraw.Draw(fr)
y=txt(d,["Meet Bruno, Pippa,","Kimi and Lumi"],260,92)
im=s.resize((1000,int(s.height*1000/s.width)),Image.LANCZOS); im=framed(im)
fr.paste(im,((W-im.width)//2,y+50)); y=y+50+im.height+60
y=txt(d,["Four friends on a quest","to help a Christmas star"],y,50,CREAM,SANS)
c=Image.open("cover_front.png"); c.thumbnail((280,360)); fr.paste(framed(c,8),((W-c.width)//2-8,y+40))
fr.save("story_friends.jpg",quality=92)
# story 2: teaser for tonight's reel
fr=base(9); d=ImageDraw.Draw(fr)
y=txt(d,["New reel tonight"],300,96)
h=Image.open("frame_hook.jpg").convert("RGB"); h=h.resize((620,1102),Image.LANCZOS); h=framed(h,10)
fr.paste(h,((W-h.width)//2,y+40)); y=y+40+h.height+50
txt(d,["On our profile at 8 pm ET"],y,50,CREAM,SANS)
fr.save("story_teaser.jpg",quality=92)
