import numpy as np, wave, sys
SR=48000; bpm=116; q=60/bpm
def f(n):
    names={'C':-9,'D':-7,'E':-5,'F':-4,'G':-2,'A':0,'B':2}
    return 440*2**((names[n[0]]+12*(int(n[-1])-4))/12)
ph=[('G5',1.5),('F5',.5),('E5',1),('D5',1),('C5',1),('D5',1),('E5',1),('C5',1),
    ('D5',.5),('E5',.5),('F5',.5),('D5',.5),('E5',1.5),('D5',.5),('C5',1),('B4',1),('C5',2)]
mel=ph+ph
bass=['C3','G3','C3','G3','F3','C3','G3','C3']*2  # one per 2 beats
total=float(sys.argv[1])
out=np.zeros(int(SR*(total+2)))
def tone(fr,dur,amp,partials=((1,1),(2.0,.35),(3.0,.12),(5.4,.05)),decay=2.6):
    t=np.arange(int(SR*dur))/SR
    s=sum(a*np.sin(2*np.pi*fr*m*t)*np.exp(-t*decay*(1+m*.5)) for m,a in partials)
    return amp*s*np.minimum(1,t/0.003)
def add(sig,st):
    i=int(st*SR); j=min(len(out),i+len(sig)); 
    if i<len(out): out[i:j]+=sig[:j-i]
t=0.3
for n,b in mel: add(tone(f(n),1.4,0.30),t); t+=b*q
t=0.3
for n in bass:
    add(tone(f(n),2*q+0.8,0.16,partials=((1,1),(2,.25)),decay=1.4),t)
    add(tone(f(n)*2,q+0.6,0.06,partials=((1,1),),decay=2),t+q)
    t+=2*q
# celesta-ish sparkle every 4 beats + soft bells on offbeats
rng=np.random.default_rng(7)
k=0
while k*q< total:
    d=int(SR*0.09); nz=np.diff(np.concatenate([[0],rng.standard_normal(d)]))
    add(nz*np.exp(-np.arange(d)/SR*45)*(0.035 if k%2==0 else 0.06),0.3+k*q+q/2)
    if k%4==0: add(tone(f('C6')*(1 if k%8==0 else 1.5),1.2,0.05,decay=3),0.3+k*q)
    k+=1
rev=out.copy()
for dl,g in [(0.06,.25),(0.11,.18),(0.19,.12),(0.31,.08),(0.45,.05)]:
    i=int(dl*SR); rev[i:]+=out[:-i]*g
out=rev[:int(SR*total)]
out/=np.abs(out).max()*1.25
fd=int(SR*1.5); out[-fd:]*=np.linspace(1,0,fd)
pcm=(out*32767).astype(np.int16)
w=wave.open('music.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
