import numpy as np, wave
SR=44100; bpm=132; q=60/bpm
N={'C4':261.63,'D4':293.66,'E4':329.63,'F4':349.23,'G4':392.0,'A4':440.0,'B4':493.88,'C5':523.25,'D5':587.33,'E5':659.25,'F5':698.46,'G5':783.99,'C3':130.81,'F3':174.61,'G3':196.0,'E3':164.81,'B2':123.47}
# melody (note, beats) one octave up for music box
mel=[('E5',1),('E5',1),('E5',2),('E5',1),('E5',1),('E5',2),('E5',1),('G5',1),('C5',1.5),('D5',.5),('E5',4),
     ('F5',1),('F5',1),('F5',1.5),('F5',.5),('F5',1),('E5',1),('E5',1),('E5',.5),('E5',.5),('G5',1),('G5',1),('F5',1),('D5',1),('C5',4)]
bass=[('C3',4),('C3',4),('C3',4),('C3',4),('F3',4),('C3',4),('G3',4),('C3',4)]
total=sum(b for _,b in mel)*q+2.0
out=np.zeros(int(SR*total))
def tone(f,dur,amp,partials=((1,1),(2,.45),(3,.18),(4.2,.08)),decay=2.2):
    t=np.arange(int(SR*dur))/SR
    s=sum(a*np.sin(2*np.pi*f*m*t)*np.exp(-t*decay*(1+m*.6)) for m,a in partials)
    att=np.minimum(1,t/0.004); return amp*s*att
def add(sig,start):
    i=int(start*SR); j=min(len(out),i+len(sig)); out[i:j]+=sig[:j-i]
t=0
for n,b in mel:
    add(tone(N[n],max(b*q,0.6)+1.2,0.32),t); t+=b*q
t=0
for n,b in bass:
    for k,off in enumerate([0,2]):
        add(tone(N[n],b*q/2+1,0.18,partials=((1,1),(2,.3)),decay=1.5),t+off*q)
        add(tone(N[n]*1.5 if n!='G3' else N['D4'],b*q/2+1,0.08,partials=((1,1),),decay=1.8),t+off*q+q)
    t+=b*q
# sleigh bells on every beat (filtered noise bursts), soft
rng=np.random.default_rng(1)
nb=int((total-2)/q)
for k in range(nb):
    d=int(SR*0.12); nz=rng.standard_normal(d); nz=np.diff(np.concatenate([[0],nz]))  # highpass-ish
    env=np.exp(-np.arange(d)/SR*35); add(nz*env*(0.05 if k%2 else 0.08),k*q)
# reverb-ish: few echoes
rev=out.copy()
for dl,g in [(0.07,.25),(0.13,.18),(0.21,.12),(0.33,.08)]:
    i=int(dl*SR); rev[i:]+=out[:-i]*g
out=rev
out/=np.abs(out).max()*1.15
fade=int(SR*1.5); out[-fade:]*=np.linspace(1,0,fade)
pcm=(out*32767).astype(np.int16)
w=wave.open('music.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print(total)
