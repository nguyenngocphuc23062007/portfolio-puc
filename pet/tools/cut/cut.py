import numpy as np,json,os
from PIL import Image
from collections import deque
from seg2 import frames,runs,S
CELL={'6':6.6,'7':7.3,'8':4.8,'9':6.4,'10':7.6,'11':7.8}
PAL=np.array([(0,0,0),(0xF3,0x8C,0x1D),(0x54,0x4E,0x52),(255,255,255),(0xA6,0xA6,0xA6),
              (0xE8,0x5A,0x5A),(0xFF,0xB0,0xB0),(0xF5,0xD0,0x2A),(0xD8,0xD8,0xD8),(0x6E,0x6E,0x6E),(0xFC,0xC2,0x5E)])
def clean(crop):
    h,w,_=crop.shape;light=crop.min(2)>205
    bg=np.zeros((h,w),bool);q=deque()
    for x in range(w):
        for y in (0,h-1):
            if light[y,x]:bg[y,x]=1;q.append((y,x))
    for y in range(h):
        for x in (0,w-1):
            if light[y,x] and not bg[y,x]:bg[y,x]=1;q.append((y,x))
    while q:
        y,x=q.popleft()
        for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
            Y,X=y+dy,x+dx
            if 0<=Y<h and 0<=X<w and light[Y,X] and not bg[Y,X]:bg[Y,X]=1;q.append((Y,X))
    return bg
FOX=PAL[[0,1,2,3,4,5]]
def grid(crop,bg,cell,P=FOX):
    h,w,_=crop.shape;W=max(1,round(w/cell));H=max(1,round(h/cell))
    out=np.zeros((H,W,4),np.uint8)
    for j in range(H):
        for i in range(W):
            y0,y1=int(j*h/H),int((j+1)*h/H);x0,x1=int(i*w/W),int((i+1)*w/W)
            # sample the inner 60% of the cell to avoid edge blur
            cy0=y0+(y1-y0)//5;cy1=max(cy0+1,y1-(y1-y0)//5);cx0=x0+(x1-x0)//5;cx1=max(cx0+1,x1-(x1-x0)//5)
            m=~bg[cy0:cy1,cx0:cx1]
            if m.mean()<0.5:continue
            px=crop[cy0:cy1,cx0:cx1][m]
            d=((px[:,None,:]-P[None])**2).sum(2).argmin(1)
            k=np.bincount(d,minlength=len(P)).argmax()
            out[j,i,:3]=P[k];out[j,i,3]=255
    return out
if __name__=='__main__':
  res={}
  os.makedirs('f',exist_ok=True)
  for n in ['6','7','8','9','11']:
      a,R=frames(n)
      for r,(y0,y1,cols) in enumerate(R):
          for c,(x0,x1) in enumerate(cols):
              cr=a[max(0,y0-3):y1+4,max(0,x0-3):x1+4]
              g=grid(cr,clean(cr),CELL[n])
              ys,xs=np.where(g[:,:,3]>0);g=g[:,xs.min():xs.max()+1];low=int(ys.max())
              # baseline: distance from frame bottom to row bottom (in cells)
              drop=round((y1-(max(0,y0-3)+ys.max()*CELL[n]))/CELL[n]) if False else 0
              name=f's{n}_r{r}_f{c}';Image.fromarray(g).save(f'f/{name}.png')
              res[name]=dict(w=int(g.shape[1]),h=int(g.shape[0]),low=low)
  json.dump(res,open('frames.json','w'),indent=0)
  print(len(res))
