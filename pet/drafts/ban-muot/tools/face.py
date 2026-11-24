# Tìm mõm và mắt trong từng khung để giữ khuôn mặt giống nhau giữa các khung.
import numpy as np
from PIL import Image
COL={0:(0,0,0),1:(0xF3,0x8C,0x1D),2:(0x54,0x4E,0x52),3:(255,255,255),4:(0xA6,0xA6,0xA6),5:(0xE8,0x5A,0x5A)}
def lab(im):
    L=np.full(im.shape[:2],-1,int)
    for k,c in COL.items():
        m=(im[:,:,3]>0)&(np.abs(im[:,:,:3].astype(int)-c).sum(2)<10);L[m]=k
    return L
def comps(mask):
    h,w=mask.shape;seen=np.zeros_like(mask);out=[]
    for y in range(h):
        for x in range(w):
            if mask[y,x] and not seen[y,x]:
                st=[(y,x)];seen[y,x]=1;pts=[]
                while st:
                    a,b=st.pop();pts.append((a,b))
                    for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
                        Y,X=a+dy,b+dx
                        if 0<=Y<h and 0<=X<w and mask[Y,X] and not seen[Y,X]:seen[Y,X]=1;st.append((Y,X))
                out.append(pts)
    return out
def find(L):
    h,w=L.shape;best=None
    for pts in comps(L==3):
        if not 2<=len(pts)<=16:continue
        ys=[p[0] for p in pts];xs=[p[1] for p in pts]
        nb=set()
        for a,b in pts:
            for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
                Y,X=a+dy,b+dx
                if 0<=Y<h and 0<=X<w:nb.add(L[Y,X])
                else:nb.add(-1)
        nb.discard(3)
        if -1 in nb or 2 in nb:continue
        t,l,r,bm=min(ys),min(xs),max(xs),max(ys)
        eyes=[]
        for side,(xa,xb) in (('L',(l-8,l-1)),('R',(r+1,r+8))):
            pix=[(y,x) for y in range(t-4,t+2) for x in range(max(0,xa),min(w,xb+1)) if 0<=y<h and L[y,x]==0
                 and 0<y<h-1 and L[y-1,x]==1 and L[y+1,x]==1]
            eyes.append(pix)
        if not eyes[0] or not eyes[1]:continue
        sc=len(eyes[0])+len(eyes[1])
        if best is None or sc>best[0]:best=(sc,dict(mz=(t,l,bm,r),mzpts=pts,eyeL=eyes[0],eyeR=eyes[1]))
    return best[1] if best else None
def shape(d):
    t,l,b,r=d['mz']
    rel=lambda pts:tuple(sorted((y-t,x-l) for y,x in pts))
    return rel(d['eyeL']),rel(d['mzpts']),rel(d['eyeR'])

# Khuôn mặt chuẩn, lấy từ khung đẹp nhất trong ảnh của bạn (mắt gạch 3 ô, mõm trắng có mũi).
# Tọa độ tính từ mũi: cột 0 là mũi, hàng 0 là hàng mắt.
FACE = {
 0: {-6:0,-5:0,-4:0,-3:1,-2:1,-1:1,0:3,1:1,2:1,3:1,4:0,5:0,6:0},
 1: {-3:1,-2:3,-1:3,0:0,1:3,2:3,3:1},
 2: {-3:1,-2:3,-1:3,0:3,1:3,2:3,3:1},
}
def eyes_of(L):
    """Trả về (hàng mắt, cột mũi) nếu thấy hai mắt gạch ngang nằm cùng hàng, ngược lại None."""
    d=find(L)
    if not d:return None
    def row_center(px):
        rows={}
        for y,x in px:rows.setdefault(y,[]).append(x)
        y=max(rows,key=lambda k:len(rows[k]));xs=rows[y]
        return y,sum(xs)/len(xs),len(xs)
    yl,xl,nl=row_center(d['eyeL']);yr,xr,nr=row_center(d['eyeR'])
    if abs(yl-yr)>1 or not 7<=xr-xl<=13:return None
    return (yl if nl>=nr else yr),int(round((xl+xr)/2))
def fix_face(im,skip=False):
    L=lab(im);e=eyes_of(L)
    if e is None:return im,None
    y0,nx=e
    if skip:return im,nx
    h,w=L.shape;out=im.copy()
    tr=lambda y,x:not(0<=y<h and 0<=x<w) or L[y,x]==-1
    interior=lambda y,x:not any(tr(y+dy,x+dx) for dy in(-1,0,1) for dx in(-1,0,1))
    # xóa mắt và mõm cũ
    for y in range(y0-1,y0+4):
        for x in range(nx-7,nx+8):
            if not(0<=y<h and 0<=x<w) or not interior(y,x):continue
            if (L[y,x]==3 and abs(x-nx)<=4) or (L[y,x]==0 and y<=y0+1):
                out[y,x,:3]=COL[1]
    for r,row in FACE.items():
        for dx,k in row.items():
            y,x=y0+r,nx+dx
            if 0<=y<h and 0<=x<w and interior(y,x):out[y,x,:3]=COL[k]
    return out,nx
