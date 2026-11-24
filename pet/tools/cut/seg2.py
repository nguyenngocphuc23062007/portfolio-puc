import sys,numpy as np
from PIL import Image
S='/private/tmp/claude-501/-Users-apple-Documents-portfolio/7f890617-78a8-4118-95eb-35038151bf4d/sheets/'
def runs(v,gap):
    idx=np.where(v)[0];out=[]
    if len(idx)==0:return out
    s=p=idx[0]
    for i in idx[1:]:
        if i-p>gap:out.append([s,p]);s=i
        p=i
    out.append([s,p]);return out
def frames(n,minw=70):
    a=np.asarray(Image.open(S+n+'.png').convert('RGB')).astype(int)
    m=(a.min(2)<200)
    R=[]
    for (y0,y1) in runs(m.sum(1)>0,18):
        sub=m[y0:y1+1]
        # columns where the solid body exists: count of dark pixels >=1
        cols=runs(sub.sum(0)>0,3)
        big=[c for c in cols if c[1]-c[0]>=minw]
        for c in cols:
            if c[1]-c[0]>=minw:continue
            k=min(range(len(big)),key=lambda i:max(big[i][0]-c[1],c[0]-big[i][1]))
            big[k]=[min(big[k][0],c[0]),max(big[k][1],c[1])]
        R.append((y0,y1,big))
    return a,R
if __name__=='__main__':
  for n in sys.argv[1:]:
    a,R=frames(n);print('sheet',n)
    for y0,y1,b in R:print(f'  y{y0}-{y1} n={len(b)}: '+' '.join(f'{x0}-{x1}' for x0,x1 in b))
