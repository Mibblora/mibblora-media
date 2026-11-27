# "Jingle Bells" (J. Pierpont 1857, public domain), newly synthesized: glockenspiel/music box + sleigh bells, light pizzicato bass
import numpy as np, wave, sys
SR=48000; bpm=120; q=60/bpm; DUR=float(sys.argv[1]) if len(sys.argv)>1 else 16
N={'C4':261.63,'D4':293.66,'E4':329.63,'F4':349.23,'G4':392.0,'A4':440.0,'B4':493.88,'C5':523.25,'D5':587.33,
   'C3':130.81,'F3':174.61,'G3':196.0,'D3':146.83}
E,Fh,G=('E5',),None,None
mel=[('E4',1),('E4',1),('E4',2),('E4',1),('E4',1),('E4',2),('E4',1),('G4',1),('C4',1.5),('D4',.5),('E4',4),
     ('F4',1),('F4',1),('F4',1.5),('F4',.5),('F4',1),('E4',1),('E4',1),('E4',.5),('E4',.5),('E4',1),('D4',1),('D4',1),('E4',1),('D4',2),('G4',2),
     ('E4',1),('E4',1),('E4',2),('E4',1),('E4',1),('E4',2),('E4',1),('G4',1),('C4',1.5),('D4',.5),('E4',4)]
bass=['C3','C3','F3','C3','D3','G3','C3','C3','C3','C3']
out=np.zeros(int(SR*(DUR+4)))
def tone(f,dur,amp,partials=((1,1),(2.76,.35),(5.4,.12)),decay=2.6):
    t=np.arange(int(SR*dur))/SR
    s=sum(a*np.sin(2*np.pi*f*m*t)*np.exp(-t*decay*(1+m*.4)) for m,a in partials)
    return amp*s*np.minimum(1,t/0.003)
def add(sig,st):
    i=int(st*SR); j=min(len(out),i+len(sig))
    if i<len(out): out[i:j]+=sig[:j-i]
t0=0.25; t=t0
for n,b in mel:
    f=N[n]*2  # play an octave up, glockenspiel range
    add(tone(f,b*q+1.0,0.28),t); t+=b*q
t=t0
for n in bass:
    add(tone(N[n],q+0.5,0.18,partials=((1,1),(2,.3)),decay=4),t); add(tone(N[n]*1.5,q+0.4,0.10,partials=((1,1),(2,.2)),decay=4),t+2*q); t+=4*q
rng=np.random.default_rng(11)
k=0
while t0+k*q/2<DUR:  # sleigh bells on eighth notes, accent on beats
    d=int(SR*0.12); nz=rng.standard_normal(d); nz=np.diff(np.concatenate([[0],nz])); nz=np.diff(np.concatenate([[0],nz]))
    env=np.exp(-np.arange(d)/SR*35); add(nz*env*(0.05 if k%2==0 else 0.028),t0+k*q/2); k+=1
rev=out.copy()
for dl,g in [(0.05,.2),(0.11,.14),(0.19,.1),(0.29,.06)]:
    i=int(dl*SR); rev[i:]+=out[:-i]*g
out=rev[:int(SR*DUR)]; out/=np.abs(out).max()*1.2
fade=int(SR*1.5); out[-fade:]*=np.linspace(1,0,fade)
st=np.repeat((out*32767).astype(np.int16)[:,None],2,1)
w=wave.open('music.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes()); w.close()
