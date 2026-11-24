# Đo cỡ cáo từng hàng (theo diện tích lông cam) để mọi hàng ra cùng một cỡ.
import numpy as np,statistics
from seg3 import frames
SIT=['12_2','13_2','13_3','14_6','15_0','15_3','15_5']
LIE=['12_0','12_1','14_2','14_4','15_1','15_4']
def areas():
    A={}
    for n in ['12','13','14','15']:
        a,R=frames(n)
        for r,(y0,y1,cols) in enumerate(R):
            v=[]
            for x0,x1 in cols:
                c=a[y0:y1+1,x0:x1+1];m=(c[:,:,0]>200)&(c[:,:,2]<120)&(c[:,:,1]>100)&(c[:,:,1]<190)
                v.append(m.sum())
            A[f'{n}_{r}']=statistics.median(v)
            A[f'{n}_{r}_first']=v[0]
    return A
def cells():
    A=areas();out={}
    for grp,ref in ((SIT,'12_2'),(LIE,'12_0')):
        tgt=A[ref]/6.3**2
        for k in grp:out[k]=(A[k]/tgt)**0.5
    # hàng bắt đầu bằng dáng ngồi: đo theo khung ngồi đầu tiên
    tgt=A['12_2']/6.3**2
    for k in ['13_1','14_0','14_1']:out[k]=(A[k+'_first']/tgt)**0.5
    for k in A:
        if k.endswith('_first'):continue
        if k not in out:
            sheet=[out[j] for j in out if j.split('_')[0]==k.split('_')[0]]
            out[k]=statistics.median(sheet) if sheet else 6.3
    return out
if __name__=='__main__':
    for k,v in sorted(cells().items(),key=lambda x:[int(i) for i in x[0].split('_')]):print(k,round(v,2))
