import json,numpy as np,statistics,os
from PIL import Image
from seg2 import runs,S
from cut import grid,clean,PAL
OUT='/Users/apple/Documents/portfolio/pet/sprites/';os.makedirs(OUT,exist_ok=True)
J=json.load(open('frames.json'))
A=[ # name, source row, frames, fps, loop
 ('idle','s11_r2',None,3,1),('lie','s11_r0',None,3,1),('sleep','s11_r1',None,2,1),('sleepy','s6_r0',None,3,1),
 ('dash','s6_r1',None,10,1),('startle','s7_r0',None,8,0),('crouch','s7_r1',[0,1],6,0),('leap','s7_r1',[2,3,4],8,0),
 ('land','s7_r2',None,8,0),('happy','s7_r3',None,6,1),('liedown','s8_r0',None,5,0),('wake','s8_r1',None,6,0),
 ('wiggle','s8_r2',None,8,1),('held','s8_r3',None,5,1),('dizzy','s8_r4',None,5,1),('peek','s8_r5',None,5,0),
 ('lookup','s8_r6',None,4,0),('tilt','s9_r0',None,4,0),('curl','s9_r1',None,2,1),('dig','s9_r2',None,8,1),
 ('eat','s9_r3',None,5,1),('sniff','s9_r4',None,5,1),('sad','s9_r5',None,3,0)]
FW,FH,G=50,46,42
maxn=max(len(f) if f else sum(1 for k in J if k.startswith(r+'_')) for _,r,f,_,_ in A)
sheet=np.zeros((FH*len(A),FW*maxn,4),np.uint8);meta={}
for ai,(name,r,fl,fps,loop) in enumerate(A):
    keys=sorted([k for k in J if k.startswith(r+'_')],key=lambda k:int(k.split('_f')[1]))
    ground=statistics.median_high([J[k]['low'] for k in keys])
    if fl:keys=[keys[i] for i in fl]
    for fi,k in enumerate(keys):
        im=np.asarray(Image.open(f'f/{k}.png'));h,w,_=im.shape
        ox=(FW-w)//2;oy=G-ground
        y0=max(0,-oy);y1=min(h,FH-oy);x0=max(0,-ox);x1=min(w,FW-ox)
        dst=sheet[ai*FH+oy+y0:ai*FH+oy+y1,fi*FW+ox+x0:fi*FW+ox+x1]
        src=im[y0:y1,x0:x1];m=src[:,:,3]>0;dst[m]=src[m]
        if y0>0 or y1<h or x0>0 or x1<w:print('clipped',name,k,y0,y1,h,x0,x1,w)
    meta[name]=dict(row=ai,n=len(keys),fps=fps,loop=bool(loop))
Image.fromarray(sheet).save(OUT+'fox.png')
# effects
a=np.asarray(Image.open(S+'10.png').convert('RGB')).astype(int);m=a.min(2)<200
pieces=[]
for y0,y1 in runs(m.sum(1)>0,18):
    for x0,x1 in runs(m[y0:y1+1].sum(0)>0,22):
        cr=a[y0-3:y1+4,x0-3:x1+4];g=grid(cr,clean(cr),7.6,PAL)
        ys,xs=np.where(g[:,:,3]>0);pieces.append(g[ys.min():ys.max()+1,xs.min():xs.max()+1])
groups=[('zzz',0,3),('heart',3,3),('bang',6,2),('dust',8,4),('shake',12,2),('stars',14,4),('shadow',18,2)]
FX=28;fx=np.zeros((FX*len(groups),FX*4,4),np.uint8);fmeta={}
for gi,(n,s,c) in enumerate(groups):
    for i in range(c):
        p=pieces[s+i][:FX,:FX];h,w,_=p.shape;oy=(FX-h)//2 if n!='shadow' else FX-h-1;ox=(FX-w)//2
        fx[gi*FX+oy:gi*FX+oy+h,i*FX+ox:i*FX+ox+w]=p
    fmeta[n]=dict(row=gi,n=c)
print([p.shape[:2] for p in pieces])
Image.fromarray(fx).save(OUT+'fx.png')
json.dump(dict(frame=[FW,FH],ground=G,anims=meta,fx=dict(size=FX,anims=fmeta)),open(OUT+'fox.json','w'),indent=1)
print('ok',sheet.shape)
