# Cắt khung thẳng từ ảnh gốc 12-16.webp: giữ nguyên từng điểm ảnh, không đổi cỡ, không đổi màu.
# Việc duy nhất: nền trắng bên ngoài con cáo được làm trong suốt.
import json,numpy as np,statistics,os
from PIL import Image
from seg3 import frames,runs,S
from cut import clean
OUT='/Users/apple/Documents/portfolio/pet/sprites/';os.makedirs(OUT,exist_ok=True)
A=[('idle','12',2,None,4,1),('wag','13',2,None,6,1),('lie','12',0,None,3,1),('sleep','12',1,None,3,1),
 ('sleepy','15',1,None,4,1),('dash','12',3,None,12,1),('startle','13',0,None,9,0),('crouch','13',1,[1,2],8,0),
 ('leap','13',1,[3,4,5],9,0),('land','13',1,[6],6,0),('happy','13',3,None,6,1),('liedown','14',0,None,5,0),
 ('wake','14',1,None,6,0),('wiggle','14',2,None,8,1),('held','14',3,None,6,1),('dizzy','14',4,None,5,1),
 ('peek','14',5,None,5,0),('lookup','14',6,None,4,0),('tilt','15',0,None,4,0),('dig','15',2,None,9,1),
 ('eat','15',3,None,5,1),('sniff','15',4,None,5,1),('sad','15',5,None,3,0)]
def rgba(cr):
    bg=clean(cr);out=np.zeros(cr.shape[:2]+(4,),np.uint8);out[:,:,:3]=cr;out[:,:,3]=np.where(bg,0,255);return out
cache={};meta={}
for name,sh,r,fl,fps,loop in A:
    if sh not in cache:cache[sh]=frames(sh)
    a,R=cache[sh];y0,y1,cols=R[r];P=2
    crops=[rgba(a[y0-P:y1+P+1,x0-P:x1+P+1]) for x0,x1 in cols]
    # đường đất: đáy thân cáo (bỏ qua vạch hiệu ứng mảnh) — lấy trung vị đáy các khung
    lows=[]
    for c in crops:
        body=(c[:,:,3]>0)&(c[:,:,0]>150)&(c[:,:,2]<150)   # phần lông cam
        ys=np.where(body.any(1))[0];lows.append(ys.max())
    ground=int(statistics.median(lows))+int(round(6*1.0))  # cộng một nét viền đen dưới bụng
    if fl:crops=[crops[i] for i in fl]
    W=max(c.shape[1] for c in crops);H=crops[0].shape[0]
    strip=np.zeros((H,W*len(crops),4),np.uint8)
    for i,c in enumerate(crops):
        ox=i*W+(W-c.shape[1])//2;strip[:,ox:ox+c.shape[1]]=c
    Image.fromarray(strip).save(OUT+f'{name}.png')
    meta[name]=dict(n=len(crops),w=W,h=H,ground=ground,fps=fps,loop=bool(loop))
a=np.asarray(Image.open(S+'16.png').convert('RGB')).astype(np.uint8);m=a.astype(int).min(2)<200;pieces=[]
for y0,y1 in runs(m.sum(1)>0,18):
    for x0,x1 in runs(m[y0:y1+1].sum(0)>0,22):pieces.append(rgba(a[y0-2:y1+3,x0-2:x1+3]))
fx={};i=0
for n,c in [('zzz',4),('heart',4),('bang',3),('dust',5),('shake',3),('stars',4),('shadow',3)]:
    ps=pieces[i:i+c];i+=c;W=max(p.shape[1] for p in ps);H=max(p.shape[0] for p in ps)
    strip=np.zeros((H,W*c,4),np.uint8)
    for j,p in enumerate(ps):
        oy=(H-p.shape[0])//2 if n!='shadow' else H-p.shape[0];ox=j*W+(W-p.shape[1])//2
        strip[oy:oy+p.shape[0],ox:ox+p.shape[1]]=p
    Image.fromarray(strip).save(OUT+f'fx-{n}.png');fx[n]=dict(n=c,w=W,h=H)
for f in ['fox.png','fx.png']:
    if os.path.exists(OUT+f):os.remove(OUT+f)
json.dump(dict(note='Khung cắt thẳng từ ảnh gốc, chỉ bỏ nền trắng',anims=meta,fx=fx),open(OUT+'fox.json','w'),indent=1)
print(json.dumps(meta)[:600]);print(fx)
