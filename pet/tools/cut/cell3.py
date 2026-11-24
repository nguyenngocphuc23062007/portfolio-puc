import numpy as np,collections,sys
from PIL import Image
from seg3 import S,frames
for n in sys.argv[1:]:
    a=np.asarray(Image.open(S+n+'.png').convert('RGB')).astype(int)
    blk=a.max(2)<70;c=collections.Counter()
    for M in (blk,blk.T):
        for row in M:
            d=np.diff(np.concatenate([[0],row.astype(int),[0]]));s=np.where(d==1)[0];e=np.where(d==-1)[0]
            for L in e-s:
                if L<20:c[int(L)]+=1
    top=sorted(c.items(),key=lambda x:-x[1])[:3]
    a2,R=frames(n);print(n,a.shape[:2],top,[len(b) for _,_,b in R])
