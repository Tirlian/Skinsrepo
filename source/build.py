from __future__ import annotations
import json, hashlib, shutil, colorsys, sys, csv, math, re, os
from pathlib import Path
from dataclasses import asdict
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from designs import D

HERE=Path(__file__).resolve().parent
ROOT=Path(os.environ.get('NOVORIAMON_OUTPUT', str(HERE.parent)))
OLD=Path(os.environ.get('NOVORIAMON_V4_DIR', str(HERE.parent/'reference_v4')))
for sub in ['skins','previews','qa','source']:(ROOT/sub).mkdir(parents=True,exist_ok=True)
ROSTER_PATH=OLD/'SKIN_ZUORDNUNG.json'
if not ROSTER_PATH.exists(): ROSTER_PATH=HERE/'ORIGINAL_ZUORDNUNG.json'
ROSTER={r['id']:r for r in json.loads(ROSTER_PATH.read_text(encoding='utf-8'))}
assert set(ROSTER)=={d.id for d in D} and len(D)==45
# U,V,W,H,D for modern classic model; first index is anatomical right.
LAYOUT={
 'head':(0,0,8,8,8), 'body':(16,16,8,12,4),
 'arm_r':(40,16,4,12,4),'arm_l':(32,48,4,12,4),
 'leg_r':(0,16,4,12,4),'leg_l':(16,48,4,12,4),
 'head_o':(32,0,8,8,8),'body_o':(16,32,8,12,4),
 'arm_r_o':(40,32,4,12,4),'arm_l_o':(48,48,4,12,4),
 'leg_r_o':(0,32,4,12,4),'leg_l_o':(0,48,4,12,4),
}
def boxes(part):
 u,v,w,h,d=LAYOUT[part]
 return {'top':(u+d,v,w,d),'bottom':(u+d+w,v,w,d),'right':(u,v+d,d,h),'front':(u+d,v+d,w,h),'left':(u+d+w,v+d,d,h),'back':(u+2*d+w,v+d,w,h)}
def rgb(h):return tuple(int(h[i:i+2],16) for i in (0,2,4))
def mix(a,b,t):return tuple(round(x*(1-t)+y*t) for x,y in zip(a,b))
def ramp(h):
 c=rgb(h);return [mix(c,(26,24,43),.58),mix(c,(35,32,48),.29),c,mix(c,(245,222,189),.22),mix(c,(255,238,209),.43)]
def hair_ramp(d):
 if d.id=='gym_fire':return [(87,19,36),(137,24,42),(190,39,46),(226,61,33),(249,111,35)]
 return ramp(d.hair)
def palette(d):
 return {'a':ramp(d.main),'b':ramp(d.second),'c':ramp(d.accent),'w':ramp('ece2ce'),'k':ramp('282a3a'),
         's':ramp(d.skin),'l':ramp('866048'),'m':ramp('a6b3b8'),'p':ramp(d.pants),'x':ramp('222330'),
         'h':hair_ramp(d),'z':ramp(d.boots)}

def cloth(grid,d,face='front'):
 rows=grid.split('/') if isinstance(grid,str) else grid
 h=len(rows);w=len(rows[0]);im=Image.new('RGBA',(w,h));pa=palette(d)
 for y,row in enumerate(rows):
  assert len(row)==w,(d.id,row)
  for x,ch in enumerate(row):
   if ch=='.':continue
   r=pa[ch];level=2
   # Large material clusters, sparse coherent highlights; never random dither/noise.
   if ch in 'abpkzl':
    if x==0 or x==w-1:level=1
    elif w>=4 and x==1 and y>1:level=3
    elif w>=6 and x==w-3 and y>4:level=1
    if y==h-1:level=max(0,level-1)
    if y in (5,9) and 1<x<w-1 and rows[y-1][x]==ch:
     if x in (2,3,w-2):level=max(1,level-1)
   elif ch=='s':
    if x in (0,w-1):level=1
    elif y<2:level=1
    else:level=2 if x%3 else 3
   elif ch in 'cm':
    level=3 if (x+y)%3 else 1
   elif ch=='h':level=min(4,1+((x+int(y/3))%3))
   elif ch=='w':
    level=3 if x not in (0,w-1) and y<4 else 2
   elif ch=='x':level=1
   im.putpixel((x,y),(*r[level],255))
 return im

def paste_face(im,part,face,src):
 x,y,w,h=boxes(part)[face];assert src.size==(w,h),(part,face,src.size,(w,h));im.paste(src,(x,y))
def get_face(im,part,face):
 x,y,w,h=boxes(part)[face];return im.crop((x,y,x+w,y+h))

LONG={'braid','braid_left','long','long_side','long_straight','twintail','bob','bowl','fringe_right','fringe','undercut_long'}
def draw_head(skin,d):
 pa=palette(d);hc=hair_ramp(d);sc=pa['s'];feature=d.feature
 # A complete face beneath the optional shell; no inherited colors from old textures.
 face=Image.new('RGBA',(8,8),(*sc[2],255));dr=ImageDraw.Draw(face)
 dr.line((0,0,0,7),fill=(*sc[1],255));dr.line((7,0,7,7),fill=(*sc[1],255))
 dr.line((1,7,6,7),fill=(*sc[1],255));dr.rectangle((2,2,5,3),fill=(*sc[3],255))
 eye=rgb(d.eyes);wh=(243,236,224,255)
 # White corners and darker inner irises leave a readable 8-pixel face.
 dr.point((1,4),fill=wh);dr.point((2,4),fill=(*eye,255));dr.point((5,4),fill=(*eye,255));dr.point((6,4),fill=wh)
 if d.id in ['freya','gym_water','gym_ice','gym_fairy','gym_psychic','league_cassia','nova_lyra','quest_healer']:
  dr.point((2,5),fill=(*mix(eye,(60,46,55),.3),255));dr.point((5,5),fill=(*mix(eye,(60,46,55),.3),255))
  dr.point((1,3),fill=(*hc[0],255));dr.point((6,3),fill=(*hc[0],255))
 elif feature not in ['glasses','roundglasses','goggles_face']:
  dr.point((2,3),fill=(*hc[0],255));dr.point((5,3),fill=(*hc[0],255))
 dr.point((3,5),fill=(*sc[1],255));dr.point((4,5),fill=(*sc[2],255))
 dr.point((3,6),fill=(*mix(sc[1],(119,54,61),.25),255))
 if d.id in ['freya','kian','gym_water','quest_healer','quest_guide']:dr.point((4,6),fill=(*sc[1],255))
 # Individually specified fringe profile and clustered strands.
 fmask=np.zeros((8,8),dtype=bool)
 for x,end in enumerate(d.fringe):
  for y in range(end):
   fmask[y,x]=True
   idx=2
   if (x+2*y)%6 in (1,2):idx=3
   if (x+2*y)%6==0:idx=1
   if y==end-1:idx=1 if x%3 else 3
   if y==0:idx=2
   if d.id=='gym_fire' and ((x,y) in [(1,1),(2,1),(3,0),(6,1),(6,2)]):idx=4
   face.putpixel((x,y),(*hc[idx],255))
 # Sideburns are paired with the hairstyle, never beige rectangles.
 if d.hair_style in LONG:
  for y in (5,6):
   for x in ([0,7] if d.hair_style not in ['fringe','fringe_right','undercut_long'] else [7]):
    face.putpixel((x,y),(*hc[1+(y%2)],255));fmask[y,x]=True
 if feature in ('beard','beard_trim','beard_long','moustache'):
  coords=[]
  if feature!='moustache':coords += [(0,5),(7,5),(0,6),(1,6),(6,6),(7,6)]+[(x,7) for x in range(8)]
  coords += [(2,6),(3,6),(4,6),(5,6)]
  if feature=='beard_long':coords += [(1,5),(6,5)]
  for x,y in coords:face.putpixel((x,y),(*hc[1+(x%3==0)],255))
  face.putpixel((3,6),(*sc[0],255));face.putpixel((4,6),(*sc[0],255))
 paste_face(skin,'head','front',face)
 hmask={'front':fmask.copy()}
 for side in ['back','right','left','top','bottom']:
  tile=Image.new('RGBA',(8,8),(*sc[1],255));mask=np.zeros((8,8),dtype=bool)
  for y in range(8):
   for x in range(8):
    ishair=True
    if side=='bottom':ishair=d.hair_style in LONG and (x<2 or x>5 or y==0)
    elif side=='back':
     style=d.hair_style
     if style in ['braid','braid_left']:
      bx=3 if style=='braid' else 5
      end=8 if x in (bx,bx+1) else 5+(x in (0,7))
     elif style=='twintail':end=8 if x in (0,1,6,7) else 5
     elif style=='topknot':end=6 if x in (3,4) else 4
     elif style in ['long','long_side','long_straight']:end=8
     elif style=='bob':end=7 if x in (0,1,6,7) else 6
     elif style=='bowl':end=5+(x in (0,7))
     elif style in ['undercut','undercut_long','buzz']:end=3+(x in (2,3,4))
     elif style=='receding':end=5+(x in (0,7))
     else:end=5+(d.fringe[7-x]%2)
     ishair=y<end
    elif side in ('left','right'):
     atfront=x if side=='left' else 7-x
     end=7 if d.hair_style in ['long','long_side','long_straight','twintail','fringe_right','fringe','undercut_long'] else 5
     if d.hair_style in ['braid','braid_left','topknot']:end=5
     if d.hair_style=='bob':end=6+(atfront<3)
     if d.hair_style=='bowl':end=5
     if d.hair_style in ['undercut','undercut_long'] and side=='right':end=2
     if d.hair_style=='buzz':end=2
     if atfront<=1:end=d.fringe[-1] if side=='left' else d.fringe[0]
     ishair=y<end
    elif side=='top' and d.hair_style=='receding':
     ishair=not(x in (2,3,4,5) and y>3)
    if ishair:
     if side=='top':idx=2+(((x+int(y/2))%5) in (1,2))
     else:idx=1 if (x-int(y/3))%4==0 else (3 if (x-int(y/3))%4==1 and y<6 else 2)
     if d.id=='gym_fire' and (x+int(y/2))%7==2 and y<5:idx=4
     tile.putpixel((x,y),(*hc[idx],255));mask[y,x]=True
    elif side!='bottom':
     base_skin=sc[1 if y>5 or x in (0,7) else 2]
     if d.hair_style in ['buzz','undercut','undercut_long'] and side in ['back','right'] and y<5:
      base_skin=mix(base_skin,hc[1],.32)
     tile.putpixel((x,y),(*base_skin,255))
  if side in ['left','right']:
   ex=2 if side=='left' else 5
   for yy in (4,5):tile.putpixel((ex,yy),(*sc[2],255));mask[yy,ex]=False
   if feature in ['earstud','goldstud','earrings','pearl','nova_clip']:
    ec=pa['c'][3] if feature!='pearl' else (231,226,206)
    tile.putpixel((ex,6),(*ec,255))
  paste_face(skin,'head',side,tile);hmask[side]=mask
 # Outer hair mesh: opaque at real locks, open at the face and ears.
 for side in ['front','back','right','left','top','bottom']:
  tile=get_face(skin,'head',side).copy();mask=hmask[side]
  for y in range(8):
   for x in range(8):
    if not mask[y,x]:tile.putpixel((x,y),(0,0,0,0))
  if side=='bottom':tile=Image.new('RGBA',(8,8))
  # Transparent gaps at tips create a non-uniform fringe on the larger shell.
  if side=='front':
   for x in range(8):
    end=d.fringe[x]
    if x%3==0 and end>1:tile.putpixel((x,end-1),(0,0,0,0))
  paste_face(skin,'head_o',side,tile)
 # Accessories are small, intentional islands on the outer layer.
 o=get_face(skin,'head_o','front');od=ImageDraw.Draw(o)
 ca=(*pa['c'][2],255);cb=(*pa['b'][2],255);metal=(*pa['m'][3],255);dark=(*pa['k'][0],255)
 if feature in ['clip','leaf','snowclip','leafpin','hairpin','ribbon','nova_clip','diadem','laurel']:
  if feature in ('diadem','laurel'):
   od.line((1,1,6,1),fill=ca);od.point((3,2),fill=(*pa['c'][4],255))
  elif feature=='ribbon':
   od.rectangle((0,1,1,2),fill=ca);od.point((2,2),fill=(*pa['c'][4],255));od.rectangle((3,1,3,2),fill=ca)
  else:
   od.point((6,1),fill=ca);od.point((6,2),fill=(*pa['c'][4],255));od.point((7,2),fill=ca)
 if feature in ['glasses','roundglasses','goggles_face','monocle']:
  if feature=='monocle':
   for p in [(4,3),(5,3),(6,3),(4,4),(6,4),(5,5),(7,5),(7,6)]:od.point(p,fill=metal)
  else:
   c=(*pa['b'][0],255) if feature!='goggles_face' else metal
   for p in [(0,3),(1,3),(2,3),(4,3),(5,3),(6,3),(0,4),(3,4),(4,4),(7,4),(1,5),(2,5),(5,5),(6,5)]:od.point(p,fill=c)
 if feature in ['goggles','aviator','visor_up']:
  od.line((0,1,7,1),fill=(*pa['l'][0],255))
  if feature=='visor_up':od.rectangle((1,1,6,2),fill=(*pa['b'][1],255));od.line((2,1,5,1),fill=metal)
  else:
   od.rectangle((1,0,2,1),fill=(*pa['m'][1],255));od.rectangle((5,0,6,1),fill=(*pa['m'][1],255));od.point((2,0),fill=ca);od.point((5,0),fill=ca)
 if feature in ['headband','bandana','bandana_low']:
  by=2 if feature!='bandana_low' else 1;od.line((0,by,7,by),fill=ca);od.point((1,by),fill=(*pa['c'][3],255))
 if feature in ['nova_cap','hardhat','beret','ranger_hat','nurseclip']:
  co=pa['a'][2] if feature not in ['hardhat','nurseclip'] else (pa['c'][2] if feature=='hardhat' else pa['w'][2])
  for side in ['top','left','right','back']:
   t=get_face(skin,'head_o',side);td=ImageDraw.Draw(t)
   if side=='top':td.rectangle((0,0,7,7),fill=(*co,255));td.rectangle((2,1,5,5),fill=(*mix(co,(240,225,190),.12),255))
   else:td.rectangle((0,0,7,1),fill=(*co,255));td.line((0,2,7,2),fill=(*mix(co,(25,25,40),.25),255))
   paste_face(skin,'head_o',side,t)
  od.rectangle((0,0,7,1),fill=(*co,255));od.line((0,2,7,2),fill=(*mix(co,(25,25,40),.2),255))
  if feature=='hardhat':od.rectangle((3,0,4,1),fill=metal);od.point((3,0),fill=(255,237,182,255))
  elif feature=='nurseclip':od.point((3,0),fill=ca);od.line((2,1,4,1),fill=ca)
  elif feature=='beret':od.rectangle((0,2,2,2),fill=(*co,255));od.point((6,1),fill=ca)
  elif feature=='nova_cap':od.point((3,1),fill=ca);od.point((4,0),fill=ca)
 if feature=='scar':od.line((6,3,7,5),fill=(*mix(sc[1],(130,66,66),.3),255))
 if feature=='eyeline':od.point((1,3),fill=dark);od.point((6,3),fill=dark)
 paste_face(skin,'head_o','front',o)
 if feature in ['headphones','earpiece']:
  for side in ['right'] if feature=='earpiece' else ['right','left']:
   t=get_face(skin,'head_o',side);dd=ImageDraw.Draw(t);dd.rectangle((2,2,4,5),fill=(*pa['k'][1],255));dd.line((3,3,3,4),fill=ca);paste_face(skin,'head_o',side,t)
 if d.hair_style=='topknot':
  t=get_face(skin,'head_o','top');dd=ImageDraw.Draw(t);dd.rectangle((2,1,5,4),fill=(*hc[1],255));dd.rectangle((3,1,4,3),fill=(*hc[3],255));dd.line((2,4,5,4),fill=ca);paste_face(skin,'head_o','top',t)
 return hmask

SLEEVES={
 'jacket':('aaaaaaaaacss','aaaaaaaaabss'),
 'bomber':('baaaaaaabbss','baaaaaaabbss'),
 'racing':('bbaaaaaabbss','aaabaaaabbss'),
 'fire':('bbabbaackkss','aaabaaackkss'),
 'rolled':('aaaaaabsssss','aaaaaabsssss'),
 'nautical':('abaaaabccsss','abaaaabccsss'),
 'tech':('abbacaackkss','aabacaackkss'),
 'linen':('bbbbbbbbscss','bbbbbbbbscss'),
 'fur':('wwaaaaaawwkz','wwaaaaaawwkz'),
 'wraps':('sssssswwwsww','sssssswwwwsw'),
 'poison':('abaaaabckkss','ssssbbssccss'),
 'expedition':('bbaaaaaabkss','bbaaaaaabkss'),
 'wide':('abbbaaaacass','abbbaaaacass'),
 'short':('bbbassssssss','bbbassssssss'),
 'coat':('baaaaaaacwss','baaaaaaacwss'),
 'bracer':('bbbbaaabbcss','aabbaaaabcss'),
 'asym':('baaaaaaakkss','sssssssskmss'),
 'mechanic':('bbbbabbaakkk','bbbbabbaakkk'),
 'puff':('bbbbbasccsss','bbbbbasccsss'),
 'formal':('baaaaaaacwss','baaaaaaacwss'),
 'champion':('ccaaaaacwwss','baaaaaacwwss'),
 'aster':('bbaaaacakkks','bbaaaacakkks'),
 'lyra':('bbaaacaakkkk','baaaa caakkkk'.replace(' ','')),
 'lab_nova':('aaaaaaabcbbb','aaaaaaabcbbb'),
 'armor':('bbbaabbbakkz','bbbaabbbakkz'),
 'uniform':('abaaacaabkks','abaaacaabkks'),
 'uniform_short':('abbaasssbkss','abbaasssbkss'),
 'uniform_rolled':('abaaabssbkss','abaaabssbkss'),
 'lab':('aaaaaaaaawss','aaaaaaaaawss'),
 'cardigan':('aaaaaaaawwss','aaaaaaaawwss'),
 'work':('bbbbbbasssss','bbbbbbasssss'),
 'engineer':('bbbbbassssss','bbbbbassssss'),
}

def draw_body(skin,d):
 f=d.front.split('/');b=d.back.split('/')
 paste_face(skin,'body','front',cloth(f,d));paste_face(skin,'body','back',cloth(b,d,'back'))
 for face in ['right','left']:
  fi=0 if face=='right' else 7;bi=7 if face=='right' else 0
  rows=[]
  for y in range(12):
   # Side strip follows the two bordering material edges, preserving hem height.
   rows.append((b[y][bi]+b[y][bi]+f[y][fi]+f[y][fi]) if face=='right' else (f[y][fi]+f[y][fi]+b[y][bi]+b[y][bi]))
  paste_face(skin,'body',face,cloth(rows,d,face))
 paste_face(skin,'body','top',cloth(['aaaaaaaa','aaassaaa','aaassaaa','aaaaaaaa'],d,'top'))
 paste_face(skin,'body','bottom',cloth([f[-1]]*4,d,'bottom'))
 # Jacket, tunic and pocket shell. Both layers have fully coherent designs separately.
 for face in ['front','back','right','left','top','bottom']:
  base=get_face(skin,'body',face);out=Image.new('RGBA',base.size)
  if face in ['front','back']:
   rows=f if face=='front' else b
   for y in range(12):
    for x in range(8):
     c=rows[y][x]
     outer=c in 'abchl' and (x in (0,1,6,7) or c in 'hl' or y in (0,1,8,9))
     if c in 'mc' and y>=5:outer=True
     if outer:out.putpixel((x,y),base.getpixel((x,y)))
  elif face in ['right','left']:
   for y in range(12):
    for x in range(4):
     if y<10:out.putpixel((x,y),base.getpixel((x,y)))
  elif face=='top':out=base.copy()
  paste_face(skin,'body_o',face,out)
 # Small chest insignia and back signatures are already encoded in individual maps.
 for i,part in enumerate(['arm_r','arm_l']):
  pattern=SLEEVES[d.sleeves][i];assert len(pattern)==12,(d.id,d.sleeves,pattern)
  rows=[]
  for y,c in enumerate(pattern):
   row=[c]*4
   if c=='a' and d.sleeves in ['racing','fire','tech','asym']:
    row[0 if i==0 else 3]='c' if d.sleeves=='tech' else 'b'
   if c=='b' and d.sleeves in ['armor','bracer','mechanic'] and y in (1,2):row[1]='m'
   if d.id.startswith('nova_') and y in (2,3) and i==0:row[1]='c'
   rows.append(''.join(row))
  for face in ['front','back','right','left']:
   grid=list(rows)
   if face in ['left','right'] and d.sleeves in ['fire','tech','racing','expedition','work','engineer']:
    for y in (2,3):
     rr=list(grid[y]);rr[1]='c' if d.sleeves not in ['work','engineer','expedition'] else 'm';grid[y]=''.join(rr)
   tile=cloth(grid,d,face);paste_face(skin,part,face,tile)
   outer=Image.new('RGBA',(4,12))
   for y,row in enumerate(grid):
    for x,c in enumerate(row):
     if c!='s' and (y<9 or d.sleeves in ['fur','armor','bracer']):outer.putpixel((x,y),tile.getpixel((x,y)))
   paste_face(skin,part+'_o',face,outer)
  for face,y in [('top',0),('bottom',11)]:
   tile=cloth([rows[y]]*4,d,face);paste_face(skin,part,face,tile)
   if face=='top' and pattern[0]!='s':paste_face(skin,part+'_o',face,tile)
 # Legs, including lower coat panels. Separate right/left straps rather than mirrored copies.
 for i,part in enumerate(['leg_r','leg_l']):
  style=d.leg_style;rows=['pppp']*12
  if style in ['coat','robe','skirt']:
   hem=5 if style=='coat' else (7 if style=='robe' else 5)
   for y in range(hem):
    rows[y]='aaab' if i==0 else 'baaa'
   if style=='robe':
    for y in range(hem):rows[y]='aaba' if i==0 else 'abaa'
  if style=='shorts':
   rows=['pppp']*5+['bbbb']+['ssss']*3+['wwww']+['zzzz']*2
  else:
   bootstart=7 if style in ['tallboots','winter','strapboots','martial'] else 9
   for y in range(bootstart,12):rows[y]='zzzz'
   if style=='sneakers':rows[9]='zcz z'.replace(' ','');rows[10]='zwwz';rows[11]='bbbb'
   elif style=='winter':rows[7]='wwww';rows[8]='wzzw';rows[10]='zbbz'
   elif style=='martial':rows[6]='aaaa';rows[7]='aaaa';rows[8]='ssss';rows[9]='bbbb';rows[10]='zzzz';rows[11]='bzzb'
   elif style in ['workboots','hiking']:rows[9]='zl lz'.replace(' ','');rows[10]='zm mz'.replace(' ','');rows[11]='zzzz'
   elif style=='strapboots':rows[7]='bbbb';rows[8]='zlzl';rows[9]='zmmz';rows[10]='zbzz';rows[11]='cccc'
   elif style=='loafers':rows[9]='pppp';rows[10]='zm mz'.replace(' ','');rows[11]='zzzz'
   elif style=='tallboots':rows[7]='bbbb';rows[9]='zmmz';rows[11]='zzzz'
  if style=='cargo':rows[2]='pllp' if i==0 else 'pppp';rows[3]='plmp' if i==0 else 'pbbp';rows[4]='pllp' if i==0 else 'pbbp'
  if d.id=='kian':rows[0]='bppp' if i==0 else 'pppp';rows[1]='bppp' if i==0 else 'pppp'
  for face in ['front','back','left','right']:
   grid=list(rows)
   if face=='back':
    grid=[r.replace('m','z') if j>=7 else r for j,r in enumerate(grid)]
    if style in ['trousers','cargo','sneakers','hiking','workboots','strapboots','tallboots']:grid[1]='pxxp';grid[2]='pxxp'
   if face in ['left','right']:
    grid=[(r[0]*2+r[-1]*2) for r in grid]
   tile=cloth(grid,d,face);paste_face(skin,part,face,tile)
   outer=Image.new('RGBA',(4,12))
   for y,row in enumerate(grid):
    for x,c in enumerate(row):
     if (c in 'ab' and y<7) or c in 'cm' or (style in ['winter','tallboots','workboots','strapboots'] and y in (7,8,9,10)):
      outer.putpixel((x,y),tile.getpixel((x,y)))
   paste_face(skin,part+'_o',face,outer)
  for face,y in [('top',0),('bottom',11)]:paste_face(skin,part,face,cloth([rows[y]]*4,d,face))

def build():
 records=[]
 for d in D:
  im=Image.new('RGBA',(64,64))
  draw_body(im,d);masks=draw_head(im,d)
  path=ROOT/'skins'/f'{d.id}.png';im.save(path,optimize=True)
  old=ROSTER[d.id]
  records.append({'id':d.id,'npc_name':old['npc_name'],'gruppe':old['gruppe'],'skin_datei':f'skins/{d.id}.png','github_datei':f'{d.id}.png','modell':'Classic/Steve (4 px Arme)','design':d.note,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'format':'64x64 RGBA PNG','base_layer':'vollständig blickdicht','ingame_test':'nicht durchgeführt'})
  if d.id=='gym_fire':
   # Regression artifact: every labelled hair pixel uses only the explicit red palette.
   report={'expected_palette_rgb':hair_ramp(d),'checks':{}}
   for face,mask in masks.items():
    tile=np.asarray(get_face(im,'head',face));colors={tuple(c[:3]) for c in tile[mask]}
    report['checks'][face]={'hair_pixels':int(mask.sum()),'foreign_colors':[list(c) for c in colors if c not in hair_ramp(d)]}
   (ROOT/'qa/fire_hair_regression.json').write_text(json.dumps(report,indent=2))
 (ROOT/'SKIN_ZUORDNUNG.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
 with (ROOT/'SKIN_ZUORDNUNG.csv').open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(records[0]),delimiter=';');w.writeheader();w.writerows(records)
 if (HERE/'designs.py').resolve() != (ROOT/'source/designs.py').resolve():
  shutil.copy(HERE/'designs.py',ROOT/'source/designs.py')
 return records

if __name__=='__main__':
 r=build();print('Written',len(r),'skins to',ROOT)
 # Native front assembly for early art review, not a fake 3D rendering.
 sheet=Image.new('RGB',(9*150,5*242),(20,25,34));draw=ImageDraw.Draw(sheet)
 font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',11)
 for i,d in enumerate(D):
  tex=Image.open(ROOT/'skins'/f'{d.id}.png')
  char=Image.new('RGBA',(16,32))
  for part,pos in [('head',(4,0)),('body',(4,8)),('arm_r',(0,8)),('arm_l',(12,8)),('leg_r',(4,20)),('leg_l',(8,20))]:
   base=get_face(tex,part,'front');over=get_face(tex,part+'_o','front');base.alpha_composite(over);char.paste(base,pos)
  x=(i%9)*150;y=(i//9)*242
  sheet.paste(char.resize((96,192),Image.Resampling.NEAREST),(x+27,y+24),char.resize((96,192),Image.Resampling.NEAREST))
  draw.text((x+10,y+5),ROSTER[d.id]['npc_name'][:22],font=font,fill=(222,225,229))
 sheet.save(ROOT/'qa/contact_front.png')
