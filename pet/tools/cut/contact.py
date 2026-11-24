import json,re
from PIL import Image
J=json.load(open('frames.json'));Z=4
rows={}
for k in J:
    s,r,f=re.match(r's(\d+)_r(\d+)_f(\d+)',k).groups();rows.setdefault((int(s),int(r)),[]).append(k)
W=1400;H=sum(max(J[k]['h'] for k in v)*Z+20 for v in rows.values())
im=Image.new('RGB',(W,H),(230,240,230));y=0
for key in sorted(rows):
    v=sorted(rows[key],key=lambda k:int(k.split('_f')[1]));x=10;hh=max(J[k]['h'] for k in v)
    for k in v:
        f=Image.open(f'f/{k}.png');f=f.resize((f.width*Z,f.height*Z),Image.NEAREST);im.paste(f,(x,y),f);x+=f.width+16
    y+=hh*Z+20
im.save('contact.png');print(im.size)
