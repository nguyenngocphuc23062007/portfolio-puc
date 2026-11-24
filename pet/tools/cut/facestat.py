import json,glob,re,collections
import numpy as np
from PIL import Image
from face import lab,find,shape
for p in sorted(glob.glob('f/s*.png'),key=lambda s:[int(x) for x in re.findall(r'\d+',s)]):
    L=lab(np.asarray(Image.open(p)));d=find(L)
    if not d:print(p[2:-4],'-');continue
    e1,m,e2=shape(d)
    f=lambda pts:' '.join(f'{y},{x}' for y,x in pts)
    print(p[2:-4],'mz',d['mz'],'| L',f(e1),'| M',len(m),'| R',f(e2))
