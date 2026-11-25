# "We Wish You a Merry Christmas" (traditional, public domain), newly synthesized: celesta/music box + soft bells
import numpy as np, wave, sys
SR=48000; bpm=92; q=60/bpm; DUR=float(sys.argv[1]) if len(sys.argv)>1 else 16.6
N={'G4':392.0,'A4':440.0,'B4':493.88,'C5':523.25,'D5':587.33,'E5':659.25,'F5':698.46,'C3':130.81,'F3':174.61,'G3':196.0,'A3':220.0,'D3':146.83,'E3':164.81}
mel=[('G4',1),('C5',1),('C5',.5),('D5',.5),('C5',.5),('B4',.5),('A4',1),('A4',1),('A4',1),
     ('D5',1),('D5',.5),('E5',.5),('D5',.5),('C5',.5),('B4',1),('G4',1),('G4',1),
     ('E5',1),('E5',.5),('F5',.5),('E5',.5),('D5',.5),('C5',1),('A4',1),('G4',.5),('G4',.5),
     ('A4',1),('D5',1),('B4',1),('C5',3)]
bass=['C3','F3','D3','G3','E3','A3','F3','G3','C3']  # one per bar after pickup
out=np.zeros(int(SR*(DUR+3)))
def tone(f,dur,amp,partials=((1,1),(2,.4),(3,.15),(4.1,.07)),decay=2.0):
    t=np.arange(int(SR*dur))/SR
    s=sum(a*np.sin(2*np.pi*f*m*t)*np.exp(-t*decay*(1+m*.5)) for m,a in partials)
    return amp*s*np.minimum(1,t/0.004)
def add(sig,st):
    i=int(st*SR); j=min(len(out),i+len(sig)); 
    if i<len(out): out[i:j]+=sig[:j-i]
t=0.3
for n,b in mel:
    add(tone(N[n],b*q+1.2,0.3),t); add(tone(N[n]*2,b*q+0.8,0.06,decay=3),t); t+=b*q
t=0.3+q
for n in bass:
    add(tone(N[n],3*q+1,0.16,partials=((1,1),(2,.25)),decay=1.2),t)
    add(tone(N[n]*1.5,q+0.6,0.06,partials=((1,1),),decay=2),t+q); add(tone(N[n]*2,q+0.6,0.05,partials=((1,1),),decay=2),t+2*q)
    t+=3*q
rng=np.random.default_rng(7)
for k in range(int(DUR/q)):
    d=int(SR*0.1); nz=np.diff(np.concatenate([[0],rng.standard_normal(d)])); env=np.exp(-np.arange(d)/SR*40)
    add(nz*env*(0.07 if k%3==0 else 0.035),0.3+k*q)
rev=out.copy()
for dl,g in [(0.06,.22),(0.12,.16),(0.2,.11),(0.31,.07)]:
    i=int(dl*SR); rev[i:]+=out[:-i]*g
out=rev[:int(SR*DUR)]; out/=np.abs(out).max()*1.2
fade=int(SR*1.5); out[-fade:]*=np.linspace(1,0,fade)
st=np.repeat((out*32767).astype(np.int16)[:,None],2,1)
w=wave.open('music.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes()); w.close()
