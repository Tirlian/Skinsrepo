from __future__ import annotations
import math,json,base64,io,os
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from build import ROOT,OLD,ROSTER,D,LAYOUT,boxes,get_face

# World-space cuboids. Units are texture pixels, not arbitrary stretched sprites.
CUBES={
 'head':(-4,24,-4,4,32,4),
 'body':(-4,12,-2,4,24,2),
 'arm_r':(-8,12,-2,-4,24,2),
 'arm_l':(4,12,-2,8,24,2),
 'leg_r':(-4,0,-2,0,12,2),
 'leg_l':(0,0,-2,4,12,2)
}
NORMALS={'front':(0,0,1),'back':(0,0,-1),'right':(-1,0,0),'left':(1,0,0),'top':(0,1,0),'bottom':(0,-1,0)}
def quad_bounds(box,face):
 x0,y0,z0,x1,y1,z1=box
 # tl,tr,br,bl; head front pixels retain the exact on-skin orientation.
 return {
  'front':[(x0,y1,z1),(x1,y1,z1),(x1,y0,z1),(x0,y0,z1)],
  'back':[(x1,y1,z0),(x0,y1,z0),(x0,y0,z0),(x1,y0,z0)],
  'right':[(x0,y1,z0),(x0,y1,z1),(x0,y0,z1),(x0,y0,z0)],
  'left':[(x1,y1,z1),(x1,y1,z0),(x1,y0,z0),(x1,y0,z1)],
  'top':[(x0,y1,z0),(x1,y1,z0),(x1,y1,z1),(x0,y1,z1)],
  'bottom':[(x0,y0,z1),(x1,y0,z1),(x1,y0,z0),(x0,y0,z0)],
 }[face]

def model_pixels(tex,outer=True,neutral=False):
 output=[]
 for part,bounds in CUBES.items():
  for layer in [0,1] if outer else [0]:
   box=list(bounds);extent=(.5 if part=='head' else .25)*layer
   box[:3]=[v-extent for v in box[:3]];box[3:]=[v+extent for v in box[3:]]
   for face in NORMALS:
    tile=np.array(get_face(tex,part+('_o' if layer else ''),face));h,w=tile.shape[:2]
    quad=np.array(quad_bounds(box,face),float);tl,tr,br,bl=quad
    dx=(tr-tl)/w;dy=(bl-tl)/h
    n=np.array(NORMALS[face],float)
    for yy,xx in zip(*np.nonzero(tile[:,:,3]>0)):
     p=tl+xx*dx+yy*dy
     qs=np.array([p,p+dx,p+dx+dy,p+dy])
     # A gentle arm stance is rigid cuboid rotation, not texture deformation.
     nn=n.copy()
     if part.startswith('arm') and not neutral:
      a=math.radians(-4 if part=='arm_r' else 4)
      pivot=np.array([-6 if part=='arm_r' else 6,24,0]);c,s=math.cos(a),math.sin(a)
      mat=np.array([[c,-s,0],[s,c,0],[0,0,1]])
      qs=(qs-pivot)@mat.T+pivot;nn=mat@nn
     output.append((qs,nn,tuple(int(v) for v in tile[yy,xx])))
 return output

def render(tex,yaw=0,pitch=0,size=(288,440),outer=True,neutral=False):
 aa=2;W,H=size;im=Image.new('RGBA',(W*aa,H*aa),(0,0,0,0));draw=ImageDraw.Draw(im)
 yaw=math.radians(yaw);pitch=math.radians(pitch)
 right=np.array([math.cos(yaw),0,-math.sin(yaw)])
 view=np.array([math.sin(yaw)*math.cos(pitch),math.sin(pitch),math.cos(yaw)*math.cos(pitch)])
 up=np.cross(view,right)
 scale=min(W/24,H/38)*aa;cx=W*aa/2;cy=H*aa*.51
 items=[]
 for qs,n,color in model_pixels(tex,outer,neutral):
  if n@view<=1e-5:continue
  centered=qs-np.array([0,16,0])
  pr=np.stack([cx+centered@right*scale,cy-centered@up*scale],axis=1)
  depth=float(centered.mean(axis=0)@view)
  # Soft display-only lighting, camera-relative to avoid a black rear preview.
  shade=.85+.10*max(0,n@view)+.05*max(0,n[1])
  col=tuple(round(v*shade) for v in color[:3])+(color[3],)
  items.append((depth,pr,col))
 for depth,pr,col in sorted(items,key=lambda a:a[0]):draw.polygon([tuple(p) for p in pr],fill=col)
 return im.resize(size,Image.Resampling.LANCZOS)

FONT_PATH=os.environ.get('NOVORIAMON_FONT','C:/Windows/Fonts/segoeui.ttf' if Path('C:/Windows/Fonts/segoeui.ttf').exists() else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
BOLD_PATH=os.environ.get('NOVORIAMON_FONT_BOLD','C:/Windows/Fonts/segoeuib.ttf' if Path('C:/Windows/Fonts/segoeuib.ttf').exists() else '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')
def font(s,bold=False):
 path=BOLD_PATH if bold else FONT_PATH
 return ImageFont.truetype(path,s) if Path(path).exists() else ImageFont.load_default(size=s)
BG=(18,23,33);PANEL=(26,33,46);FG=(231,234,238);MUTED=(151,166,184);ACCENT=(103,180,163)
def make_previews():
 sheet=Image.new('RGB',(1800,5*345+126),BG);sd=ImageDraw.Draw(sheet)
 sd.text((35,24),'NOVORIAMON  /  CHARAKTERTEXTUREN',font=font(30,True),fill=FG)
 sd.text((36,72),'45 Skins · 64 × 64 PNG · Classic · gerenderte Texturen, keine Konzeptbilder',font=font(17),fill=MUTED)
 for i,d in enumerate(D):
  tex=Image.open(ROOT/'skins'/f'{d.id}.png');name=ROSTER[d.id]['npc_name']
  panel=Image.new('RGB',(1500,620),BG);pd=ImageDraw.Draw(panel)
  pd.text((30,20),f'{name}  /  {d.id}.png',font=font(25,True),fill=FG)
  pd.text((30,61),'Native Textur: 64 × 64 · Classic/Steve · äußere Ebene eingeschaltet',font=font(15),fill=MUTED)
  angles=[(0,0,'VORNE'),(180,0,'HINTEN'),(90,0,'LINKS'),(-90,0,'RECHTS'),(32,16,'3/4-ANSICHT')]
  for j,(yaw,pitch,label) in enumerate(angles):
   r=render(tex,yaw,pitch)
   x=6+j*298;pd.rounded_rectangle((x+8,94,x+282,572),radius=14,fill=PANEL)
   panel.paste(r,(x,110),r);pd.text((x+90,543),label,font=font(12,True),fill=MUTED)
  panel.save(ROOT/'previews'/f'{d.id}_5ansichten.png',optimize=True)
  # individually render both front and back three-quarter for cast board
  x=(i%9)*200;y=126+(i//9)*345
  sd.rounded_rectangle((x+8,y+4,x+192,y+335),radius=10,fill=PANEL)
  r=render(tex,24,10,size=(184,246));sheet.paste(r,(x+8,y+12),r)
  sd.text((x+16,y+270),name.replace(' – Top 4','')[:22],font=font(12,True),fill=FG)
  role=ROSTER[d.id]['gruppe'].replace('Arenaleiter · ','').replace('Team Nova – Rüpel','Team Nova')
  sd.text((x+16,y+293),role[:23],font=font(11),fill=MUTED)
  sd.text((x+16,y+314),d.id,font=font(10),fill=ACCENT)
  if i%9==0:print('preview',i+1,'/',45,flush=True)
 sheet.save(ROOT/'KONTROLLTAFEL_45.png',optimize=True)
 # Key-character comparison against real input textures.
 ids=['gym_fire','freya','kian','nova_aster','gym_ice','gym_poison']
 comp=Image.new('RGB',(6*300,720),BG);cd=ImageDraw.Draw(comp)
 cd.text((28,20),'DIREKTER VERGLEICH  /  V4 → NEU',font=font(28,True),fill=FG)
 cd.text((28,63),'Gleiche Darstellung, gleiche Beleuchtung. Links der bisherige Skin, rechts die neu gezeichnete Textur.',font=font(16),fill=MUTED)
 for i,ident in enumerate(ids):
  x=i*300;name=ROSTER[ident]['npc_name']
  cd.text((x+18,110),name,font=font(18,True),fill=FG)
  for j,base in enumerate([OLD,ROOT]):
   r=render(Image.open(base/'skins'/f'{ident}.png'),20,10,size=(150,385))
   comp.paste(r,(x+j*150,160),r);cd.text((x+j*150+45,565),'V4' if j==0 else 'NEU',font=font(14,True),fill=MUTED if j==0 else ACCENT)
 comp.save(ROOT/'VERGLEICH_V4_NEU.png',optimize=True)
 # Explicit fire base/outer regression proof from real head UVs.
 tex=Image.open(ROOT/'skins/gym_fire.png');hair=Image.new('RGB',(1200,510),BG);hd=ImageDraw.Draw(hair)
 hd.text((28,22),'FEUERARENA / Kael · Haarprüfung',font=font(26,True),fill=FG)
 for i,face in enumerate(['front','back','left','right','top']):
  base=get_face(tex,'head',face);comp=base.copy();comp.alpha_composite(get_face(tex,'head_o',face))
  x=20+i*236
  hd.text((x,72),face,font=font(16,True),fill=MUTED)
  hair.paste(base.resize((160,160),Image.Resampling.NEAREST),(x,110));hair.paste(comp.resize((160,160),Image.Resampling.NEAREST),(x,302))
 hd.text((20,277),'Oben: Grundebene · Unten: Grundebene + äußere Haarebene',font=font(13),fill=MUTED)
 hair.save(ROOT/'qa/FEUER_HAARPRUEFUNG.png',optimize=True)

if __name__=='__main__':make_previews()
