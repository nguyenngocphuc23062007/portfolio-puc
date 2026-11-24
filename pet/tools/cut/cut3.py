# Cắt bộ ảnh đã chỉnh mượt (12-16.webp) thành khung pixel, giữ nguyên nét vẽ.
import numpy as np,json,os,sys
from PIL import Image
from seg3 import frames,runs,S
from cut import grid,clean,PAL
from scale3 import cells
CELL={'12':6.3,'13':6.4,'14':5.9,'15':7.1}
if __name__=='__main__':
    res={};os.makedirs('f3',exist_ok=True);CR=cells()
    for n in CELL:
        a,R=frames(n)
        for r,(y0,y1,cols) in enumerate(R):
            for c,(x0,x1) in enumerate(cols):
                cr=a[max(0,y0-3):y1+4,max(0,x0-3):x1+4]
                g=grid(cr,clean(cr),CR[f'{n}_{r}'])
                ys,xs=np.where(g[:,:,3]>0);g=g[:,xs.min():xs.max()+1]
                name=f's{n}_r{r}_f{c}';Image.fromarray(g).save(f'f3/{name}.png')
                res[name]=dict(w=int(g.shape[1]),h=int(g.shape[0]),low=int(ys.max()))
    json.dump(res,open('frames3.json','w'),indent=0);print(len(res))
    for k in ['s12_r0_f0','s12_r1_f0','s12_r2_f0','s13_r2_f0','s13_r3_f1','s14_r0_f0','s14_r0_f2','s14_r2_f0','s14_r6_f0','s15_r0_f0','s15_r1_f0','s15_r3_f0','s15_r5_f0','s12_r3_f0','s13_r0_f0']:print(k,res[k])
