# Ghép bộ khung đã chỉnh mượt thành pet/sprites/fox.png, fx.png, fox.json.
import json,numpy as np,statistics,os
from PIL import Image
from seg3 import runs,S
from cut import grid,clean,PAL
OUT='/Users/apple/Documents/portfolio/pet/sprites/';os.makedirs(OUT,exist_ok=True)
J=json.load(open('frames3.json'))
A=[ # tên, hàng nguồn, chọn khung, khung/giây, lặp
 ('idle','s12_r2',None,4,1),('wag','s13_r2',None,6,1),('lie','s12_r0',None,3,1),('sleep','s12_r1',None,3,1),
 ('sleepy','s15_r1',None,4,1),('dash','s12_r3',None,12,1),('startle','s13_r0',None,9,0),('crouch','s13_r1',[1,2],8,0),
 ('leap','s13_r1',[3,4,5],9,0),('land','s13_r1',[6],6,0),('happy','s13_r3',None,6,1),('liedown','s14_r0',None,5,0),
 ('wake','s14_r1',None,6,0),('wiggle','s14_r2',None,8,1),('held','s14_r3',None,6,1),('dizzy','s14_r4',None,5,1),
 ('peek','s14_r5',None,5,0),('lookup','s14_r6',None,4,0),('tilt','s15_r0',None,4,0),('dig','s15_r2',None,9,1),
 ('eat','s15_r3',None,5,1),('sniff','s15_r4',None,5,1),('sad','s15_r5',None,3,0)]
FW,FH,G=50,46,42
maxn=max(len(f) if f else sum(1 for k in J if k.startswith(r+'_')) for _,r,f,_,_ in A)
sheet=np.zeros((FH*len(A),FW*maxn,4),np.uint8);meta={}
for ai,(name,r,fl,fps,loop) in enumerate(A):
    keys=sorted([k for k in J if k.startswith(r+'_')],key=lambda k:int(k.split('_f')[1]))
    ground=statistics.median_high([J[k]['low'] for k in keys])
    if fl:keys=[keys[i] for i in fl]
    for fi,k in enumerate(keys):
        im=np.asarray(Image.open(f'f3/{k}.png'));h,w,_=im.shape
        ox=(FW-w)//2;oy=G-ground
        y0=max(0,-oy);y1=min(h,FH-oy);x0=max(0,-ox);x1=min(w,FW-ox)
        src=im[y0:y1,x0:x1];m=src[:,:,3]>0
        sheet[ai*FH+oy+y0:ai*FH+oy+y1,fi*FW+ox+x0:fi*FW+ox+x1][m]=src[m]
        lost=int(im[:,:,3].astype(bool).sum()-m.sum())
        if lost:print('clipped',name,k,lost,'px')
    meta[name]=dict(row=ai,n=len(keys),fps=fps,loop=bool(loop))
Image.fromarray(sheet).save(OUT+'fox.png')
a=np.asarray(Image.open(S+'16.png').convert('RGB')).astype(int);m=a.min(2)<200;pieces=[]
for y0,y1 in runs(m.sum(1)>0,18):
    for x0,x1 in runs(m[y0:y1+1].sum(0)>0,22):
        cr=a[y0-3:y1+4,x0-3:x1+4];g=grid(cr,clean(cr),7.0,PAL)
        ys,xs=np.where(g[:,:,3]>0);pieces.append(g[ys.min():ys.max()+1,xs.min():xs.max()+1])
groups=[('zzz',4),('heart',4),('bang',3),('dust',5),('shake',3),('stars',4),('shadow',3)]
FX=28;fx=np.zeros((FX*len(groups),FX*5,4),np.uint8);fmeta={};i=0
for gi,(n,c) in enumerate(groups):
    for j in range(c):
        p=pieces[i][:FX,:FX];i+=1;h,w,_=p.shape;oy=(FX-h)//2 if n!='shadow' else FX-h-1;ox=(FX-w)//2
        fx[gi*FX+oy:gi*FX+oy+h,j*FX+ox:j*FX+ox+w]=p
    fmeta[n]=dict(row=gi,n=c)
assert i==len(pieces),(i,len(pieces))
Image.fromarray(fx).save(OUT+'fx.png')
json.dump(dict(frame=[FW,FH],ground=G,anims=meta,fx=dict(size=FX,cols=5,anims=fmeta)),open(OUT+'fox.json','w'),indent=1)
print('ok',sheet.shape,maxn,[p.shape[:2] for p in pieces])
