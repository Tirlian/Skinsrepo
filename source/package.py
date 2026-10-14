from __future__ import annotations
import json,base64,hashlib,csv,zipfile,shutil,html,ast
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
from build import ROOT,OLD,HERE,D,ROSTER,LAYOUT,boxes,get_face,hair_ramp
from render import render,font,BG,PANEL,FG,MUTED,ACCENT,CUBES,NORMALS,quad_bounds

records=json.loads((ROOT/'SKIN_ZUORDNUNG.json').read_text())
checks=[];hashes=set();base_masks=np.zeros((64,64),bool);outer_masks=np.zeros((64,64),bool)
for part in LAYOUT:
 mask=outer_masks if part.endswith('_o') else base_masks
 for x,y,w,h in boxes(part).values():
  assert not mask[y:y+h,x:x+w].any(),('overlap',part,x,y)
  mask[y:y+h,x:x+w]=True
assert not (base_masks & outer_masks).any()
assert int(base_masks.sum())==1632
assert len(list((ROOT/'skins').glob('*.png')))==45
frontset=set();maskfrontset=set();backset=set()
for d in D:
 p=ROOT/'skins'/f'{d.id}.png';raw=p.read_bytes()
 with Image.open(p) as verify:verify.verify()
 im=Image.open(p);a=np.array(im);previous=np.array(Image.open(OLD/'skins'/p.name).convert('RGBA'))
 assert im.size==(64,64) and im.mode=='RGBA' and im.format=='PNG'
 assert (a[:,:,3][base_masks]==255).all()
 assert (a[:,:,3][~(base_masks|outer_masks)]==0).all()
 assert set(np.unique(a[:,:,3]))<={0,255}
 hh=hashlib.sha256(raw).hexdigest();assert hh not in hashes;hashes.add(hh)
 delta=int(np.any(a!=previous,axis=2).sum());assert delta>1000,(d.id,delta)
 facehash=hashlib.sha256(get_face(im,'head','front').tobytes()).hexdigest();frontset.add(facehash)
 maskfrontset.add(d.front);backset.add(d.back)
 assert (ROOT/'previews'/f'{d.id}_5ansichten.png').exists()
 checks.append({'id':d.id,'sha256':hh,'size_px':[64,64],'mode':'RGBA','base_opaque_pixels':1632,'outer_opaque_pixels':int(np.sum(a[:,:,3][outer_masks]==255)),
                'changed_pixels_vs_v4':delta,'format_ok':True,'base_opaque_ok':True,'unused_uv_transparent_ok':True,'alpha_binary_ok':True,'preview_views':5})
assert len(frontset)==45
fire=json.loads((ROOT/'qa/fire_hair_regression.json').read_text())
assert all(not a['foreign_colors'] for a in fire['checks'].values())
summary={'skins':45,'distinct_skin_hashes':len(hashes),'distinct_head_fronts':len(frontset),'individual_torso_front_masks':len(maskfrontset),'individual_torso_back_masks':len(backset),
 'previews':45,'rendered_views':225,'all_automated_checks_passed':True,'ingame_test':'not_run','github_published':False,
 'note':'Automatische Prüfungen belegen Dateieigenschaften, nicht eine objektive künstlerische Qualitätsstufe.','files':checks}
(ROOT/'qa/VALIDIERUNG.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
(ROOT/'SHA256SUMS.txt').write_text('\n'.join(f"{r['sha256']}  skins/{r['id']}.png" for r in records)+'\n')

# Complete rear and opposite-side cast inspection sheets.
for key,yaw in [('RUECKSEITEN',155),('RECHTE_SEITEN',-65)]:
 sheet=Image.new('RGB',(1800,126+5*305),BG);sd=ImageDraw.Draw(sheet)
 sd.text((30,24),f'NOVORIAMON / {key}',font=font(30,True),fill=FG)
 sd.text((30,73),'UV-Texturen auf 3D-Quadern · Außenschicht aktiv',font=font(16),fill=MUTED)
 for i,d in enumerate(D):
  x=i%9*200;y=126+i//9*305
  sd.rounded_rectangle((x+8,y+4,x+192,y+296),radius=10,fill=PANEL)
  r=render(Image.open(ROOT/'skins'/f'{d.id}.png'),yaw,12,size=(184,238));sheet.paste(r,(x+8,y+9),r)
  sd.text((x+15,y+258),ROSTER[d.id]['npc_name'][:23],font=font(12,True),fill=FG)
  sd.text((x+15,y+278),d.id,font=font(10),fill=MUTED)
 sheet.save(ROOT/'qa'/f'{key}_45.png',optimize=True)

# Offline HTML viewer: all PNG bytes are embedded, so file:// works on Windows.
viewer_data=[]
for r in records:
 ident=r['id']
 viewer_data.append({**r,'png':base64.b64encode((ROOT/'skins'/f'{ident}.png').read_bytes()).decode(),
   'oldpng':base64.b64encode((OLD/'skins'/f'{ident}.png').read_bytes()).decode()})
viewer=r'''<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Novoriamon · 45 Skintexturen</title>
<style>
:root{color-scheme:dark;--bg:#111620;--panel:#1b2330;--line:#303d4c;--text:#e5ebf0;--muted:#9aaaBA;--accent:#8fd1bc}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:15px/1.5 system-ui,Segoe UI,sans-serif}header{padding:24px 30px;border-bottom:1px solid var(--line);display:flex;align-items:center;justify-content:space-between;gap:20px}h1{font-size:23px;margin:0;letter-spacing:.025em}.sub{color:var(--muted);font-size:13px}.badge{border:1px solid #4e8171;border-radius:20px;padding:5px 12px;color:var(--accent);font-size:12px}.layout{display:grid;grid-template-columns:260px 1fr 300px;max-width:1680px;margin:auto;min-height:calc(100vh - 95px)}aside{padding:20px;border-right:1px solid var(--line)}input[type=search]{width:100%;background:var(--panel);border:1px solid var(--line);padding:10px;color:var(--text);border-radius:8px;font:inherit}nav{height:calc(100vh - 185px);overflow:auto;margin-top:16px}nav button{display:block;width:100%;text-align:left;background:transparent;border:0;border-radius:8px;color:var(--text);padding:9px 10px;margin-bottom:4px;font:inherit;cursor:pointer}nav button small{display:block;color:var(--muted);font-size:11px}nav button.active{background:#2a423e;border-left:3px solid var(--accent)}nav button:hover{background:#253142}main{padding:25px 26px;min-width:0}h2{font-size:25px;margin:0}.canvasbox{margin-top:18px;background:radial-gradient(ellipse at center,#273647 0,#192331 65%,#17202b 100%);border:1px solid var(--line);border-radius:16px;overflow:hidden;position:relative}#view{display:block;width:100%;height:min(61vh,610px);min-height:360px;touch-action:none;cursor:grab}.hint{position:absolute;bottom:12px;width:100%;text-align:center;color:var(--muted);font-size:12px;pointer-events:none}.toolbar{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}button.tool,a.download{background:var(--panel);border:1px solid var(--line);color:var(--text);font:inherit;border-radius:7px;padding:8px 12px;text-decoration:none;cursor:pointer}a.download{display:block;margin-top:16px;background:#2b544a;border-color:#487f6d;text-align:center;color:#f0fff7}.toggles{display:flex;gap:18px;flex-wrap:wrap;margin:16px 0;color:var(--muted);font-size:13px}input[type=checkbox]{accent-color:#80c7b0}section.details{padding:25px 22px;border-left:1px solid var(--line)}section.details h3{font-size:16px;margin:0 0 12px}#native{width:256px;max-width:100%;height:auto;aspect-ratio:1;image-rendering:pixelated;background:repeating-conic-gradient(#293241 0 25%,#364253 0 50%) 0/16px 16px;border:1px solid var(--line);border-radius:5px}p{color:var(--muted)}code{font-size:11px;overflow-wrap:anywhere;color:#bdd7cd}.fact{margin:16px 0;padding-top:15px;border-top:1px solid var(--line)}#status{color:var(--accent)}@media(max-width:1000px){.layout{grid-template-columns:210px 1fr}.details{grid-column:1/-1;border-top:1px solid var(--line)}#view{height:520px}nav{height:640px}}@media(max-width:650px){header{padding:18px}.layout{display:block}aside{border:0}nav{height:150px}main{padding:18px}#view{min-height:400px}section.details{padding:18px}}</style></head>
<body><header><div><h1>NOVORIAMON / SKINATELIER</h1><div class="sub">45 neue Pixeltexturen · native 64 × 64 PNGs · Offline-Kontrolle</div></div><div class="badge">Classic / 4-Pixel-Arme</div></header>
<div class="layout"><aside><input id="filter" type="search" placeholder="Name, Rolle oder ID suchen …" aria-label="NPC suchen"><nav id="list"></nav></aside>
<main><h2 id="name"></h2><div class="sub" id="role"></div><div class="canvasbox"><canvas id="view" aria-label="Drehbare dreidimensionale Skin-Vorschau"></canvas><div class="hint">Ziehen zum Drehen · Original-PNG rechts · Keine Internetverbindung nötig</div></div><div class="toolbar" id="angles"><button class="tool" data-yaw="0" data-pitch="0">Vorne</button><button class="tool" data-yaw="180" data-pitch="0">Hinten</button><button class="tool" data-yaw="90" data-pitch="0">Links</button><button class="tool" data-yaw="-90" data-pitch="0">Rechts</button><button class="tool" data-yaw="32" data-pitch="16">3/4</button></div><div class="toggles"><label><input type="checkbox" id="outer" checked> Äußere Ebene</label><label><input type="checkbox" id="old"> Mit altem V4-Skin vergleichen</label></div><div id="status"></div><p id="description"></p></main>
<section class="details"><h3>Die tatsächliche Skin-Datei</h3><canvas id="native" width="64" height="64"></canvas><a class="download" id="download">64×64-PNG speichern</a><div class="fact"><strong id="filename"></strong><p>Grundkörper und Außenschicht liegen vollständig im klassischen 64×64-Layout. Die vergrößerte Darstellung verändert die gespeicherte PNG nicht.</p></div><div class="fact"><strong>Dateiprüfung</strong><p>PNG · RGBA · 1.632 blickdichte Grundkörperpixel · 45 unterschiedliche Texturen</p><code id="checksum"></code></div><div class="fact"><p>Dies ist eine lokale UV-Modellvorschau. Sie ersetzt keinen Test in deiner EasyNPC-Installation. Dein GitHub-Repository wird von dieser Seite nicht verändert.</p></div></section></div>
<script>
const DATA=__DATA__;
const UV=__UV__;
const BOX=__BOX__;
const NOR={front:[0,0,1],back:[0,0,-1],right:[-1,0,0],left:[1,0,0],top:[0,1,0],bottom:[0,-1,0]};
let selected=DATA.find(x=>x.id==='gym_fire'), yaw=32,pitch=16,mesh=[],requestNo=0;
const cv=document.getElementById('view'),ct=cv.getContext('2d'),native=document.getElementById('native'),nc=native.getContext('2d');
const dot=(a,b)=>a[0]*b[0]+a[1]*b[1]+a[2]*b[2];
function faceQuads(b,f){const[x0,y0,z0,x1,y1,z1]=b;return{front:[[x0,y1,z1],[x1,y1,z1],[x1,y0,z1],[x0,y0,z1]],back:[[x1,y1,z0],[x0,y1,z0],[x0,y0,z0],[x1,y0,z0]],right:[[x0,y1,z0],[x0,y1,z1],[x0,y0,z1],[x0,y0,z0]],left:[[x1,y1,z1],[x1,y1,z0],[x1,y0,z0],[x1,y0,z1]],top:[[x0,y1,z0],[x1,y1,z0],[x1,y1,z1],[x0,y1,z1]],bottom:[[x0,y0,z1],[x1,y0,z1],[x1,y0,z0],[x0,y0,z0]]}[f]}
function buildMesh(pix){let out=[];for(const[part,base]of Object.entries(BOX)){for(let layer=0;layer<2;layer++){const e=layer*(part==='head'?.5:.25);const b=base.map((v,i)=>v+(i<3?-e:e)),uv=UV[part+(layer?'_o':'')];for(const[f,n0]of Object.entries(NOR)){const[x,y,w,h]=uv[f];const q=faceQuads(b,f),tl=q[0],dx=q[1].map((v,i)=>(v-tl[i])/w),dy=q[3].map((v,i)=>(v-tl[i])/h);for(let iy=0;iy<h;iy++)for(let ix=0;ix<w;ix++){const at=((y+iy)*64+x+ix)*4;if(!pix[at+3])continue;let p=tl.map((v,i)=>v+dx[i]*ix+dy[i]*iy),pts=[p,p.map((v,i)=>v+dx[i]),p.map((v,i)=>v+dx[i]+dy[i]),p.map((v,i)=>v+dy[i])];let n=[...n0];if(part.startsWith('arm')){const a=(part==='arm_r'?-4:4)*Math.PI/180,s=Math.sin(a),c=Math.cos(a),pivot=[part==='arm_r'?-6:6,24,0];pts=pts.map(v=>{const x=v[0]-pivot[0],y=v[1]-pivot[1];return[pivot[0]+x*c-y*s,pivot[1]+x*s+y*c,v[2]]});n=[n[0]*c-n[1]*s,n[0]*s+n[1]*c,n[2]]}out.push({pts:pts.map(p=>[p[0],p[1]-16,p[2]]),n,layer,col:[pix[at],pix[at+1],pix[at+2]]})}}}}return out}
function redraw(){const W=cv.clientWidth,H=cv.clientHeight,dpr=Math.min(devicePixelRatio||1,2);cv.width=W*dpr;cv.height=H*dpr;ct.setTransform(dpr,0,0,dpr,0,0);ct.clearRect(0,0,W,H);const a=yaw*Math.PI/180,p=pitch*Math.PI/180,right=[Math.cos(a),0,-Math.sin(a)],view=[Math.sin(a)*Math.cos(p),Math.sin(p),Math.cos(a)*Math.cos(p)],up=[-Math.sin(a)*Math.sin(p),Math.cos(p),-Math.cos(a)*Math.sin(p)],scale=Math.min(W/26,H/38),out=[];for(const t of mesh){if(t.layer&&!document.getElementById('outer').checked)continue;const lit=dot(t.n,view);if(lit<=0)continue;const pts=t.pts.map(v=>[W/2+dot(v,right)*scale,H*.51-dot(v,up)*scale]),depth=t.pts.reduce((s,v)=>s+dot(v,view),0)/4,shade=.85+.10*Math.max(0,lit)+.05*Math.max(0,t.n[1]);out.push({pts,depth,color:'rgb('+t.col.map(v=>Math.round(v*shade)).join(',')+')'})}out.sort((a,b)=>a.depth-b.depth);for(const t of out){ct.beginPath();ct.moveTo(...t.pts[0]);for(let i=1;i<4;i++)ct.lineTo(...t.pts[i]);ct.closePath();ct.fillStyle=t.color;ct.fill()}}
function load(){const ticket=++requestNo,old=document.getElementById('old').checked,img=new Image();img.onload=()=>{if(ticket!==requestNo)return;nc.clearRect(0,0,64,64);nc.drawImage(img,0,0);mesh=buildMesh(nc.getImageData(0,0,64,64).data);redraw()};img.src='data:image/png;base64,'+(old?selected.oldpng:selected.png);document.getElementById('name').textContent=selected.npc_name;document.getElementById('role').textContent=selected.gruppe+' / '+selected.id;document.getElementById('description').textContent=selected.design;document.getElementById('status').textContent=old?'Vergleich: bisheriger V4-Skin':'Aktiv: neu gezeichnete Textur';document.getElementById('filename').textContent=selected.id+'.png';document.getElementById('checksum').textContent='SHA-256 (neu): '+selected.sha256;const dl=document.getElementById('download');dl.href='data:image/png;base64,'+selected.png;dl.download=selected.id+'.png';for(const b of document.querySelectorAll('nav button'))b.classList.toggle('active',b.dataset.id===selected.id)}
function list(){const f=document.getElementById('filter').value.toLowerCase(),nav=document.getElementById('list');nav.replaceChildren();for(const d of DATA){if(!(d.id+' '+d.npc_name+' '+d.gruppe).toLowerCase().includes(f))continue;const b=document.createElement('button');b.dataset.id=d.id;b.textContent=d.npc_name;const s=document.createElement('small');s.textContent=d.gruppe;b.appendChild(s);b.classList.toggle('active',d.id===selected.id);b.onclick=()=>{selected=d;load()};nav.appendChild(b)}}
let drag=null;cv.onpointerdown=e=>{drag=[e.clientX,e.clientY,yaw,pitch];cv.setPointerCapture(e.pointerId)};cv.onpointermove=e=>{if(!drag)return;yaw=drag[2]+(e.clientX-drag[0])*.5;pitch=Math.max(-60,Math.min(70,drag[3]+(e.clientY-drag[1])*.3));redraw()};cv.onpointerup=cv.onpointercancel=()=>{drag=null};document.getElementById('filter').oninput=list;document.getElementById('outer').onchange=redraw;document.getElementById('old').onchange=load;for(const b of document.querySelectorAll('#angles button'))b.onclick=()=>{yaw=+b.dataset.yaw;pitch=+b.dataset.pitch;redraw()};window.onresize=redraw;list();load();
</script></body></html>'''
viewer=viewer.replace('__DATA__',json.dumps(viewer_data,ensure_ascii=False)).replace('__UV__',json.dumps({p:boxes(p)for p in LAYOUT})).replace('__BOX__',json.dumps(CUBES))
(ROOT/'SKINS_ANSEHEN.html').write_text(viewer,encoding='utf-8')

# Plain-text documentation, written only after verified outputs exist.
readme='''# Novoriamon – Pixel-Neuzeichnung, 14.10.2026

Dieses Paket enthält 45 neu aufgebaute Skintexturen mit den IDs und Namen des vorhandenen V4-Pakets. Die PNGs wurden direkt als 64×64-Pixel-Flächen gezeichnet: separate Materialmasken pro Charakter, exakte UV-Zuordnung und getrennte Grund-/Außenschichten. Keine heruntergerechneten Bildgenerator-Ausgaben.

## Schnell ansehen unter Windows

Das ZIP vollständig entpacken und **SKINS_ANSEHEN.html** doppelklicken. Die Ansicht funktioniert offline: links eine Figur auswählen, zum Drehen ziehen, Grund- und Außenschicht vergleichen. Über „Mit altem V4-Skin vergleichen“ ist der tatsächliche Vorgänger bei gleicher Darstellung sichtbar. „64×64-PNG speichern“ speichert immer den neuen Skin.

## Dateien

- `skins/`: genau 45 installierbare PNGs, identische Dateinamen wie zuvor.
- `previews/`: 45 Tafeln mit je fünf gerenderten Modellansichten.
- `KONTROLLTAFEL_45.png`: gesamte Besetzung.
- `VERGLEICH_V4_NEU.png`: sechs Figuren im direkten Vorher-Nachher-Vergleich.
- `SKIN_ZUORDNUNG.csv` / `.json`: Namen, Rollen, Dateipfade und Prüfsummen.
- `DESIGN_NOTIZEN.md`: konkrete Gestaltung aller 45 Figuren.
- `qa/`: maschinenlesbare Prüfungen und zusätzliche Kontrollbilder.
- `SHA256SUMS.txt`: SHA-256 der 45 Skin-Dateien.
- `source/`: nachvollziehbare native Masken und Erstellungs-/Prüfcode. Keine Schriftdateien enthalten.

Alle Skins verwenden das **Classic-Modell mit vier Pixel breiten Armen**, nicht Slim. Die Grundtextur funktioniert auch ohne äußere Ebene; die zusätzliche Ebene ergänzt Haarvolumen, Jacken, Kragen, Taschen und Manschetten.

## Klarer Teststatus

PNG-Integrität, Bildmaße, RGBA, UV-Abdeckung, Alpha, eindeutige Dateien und Zuordnung sind automatisiert geprüft. 225 Ansichten wurden direkt aus den PNGs auf Texturquadern gerendert. Ein Laufzeittest in Minecraft/EasyNPC wurde hier nicht ausgeführt. Die Darstellung hängt auch von NPC-Modell, aktivierten Ebenen und Beleuchtung im Spiel ab.

Es wurde keine fremde Skin-Kollektion als Quelle übernommen. Die Namen und Rollen stammen aus dem bereitgestellten Projektpaket. Die fiktive Figur `league_tirlian` bleibt ein Trainerdesign, kein realistisches Porträt.

GitHub wurde bei dieser Auslieferung nicht verändert. Die in `github_datei` angegebenen Namen bewahren die bisherigen Root-Pfade, sobald die neuen PNGs dort bewusst ersetzt werden.
'''
(ROOT/'README.md').write_text(readme,encoding='utf-8')
(ROOT/'INSTALLATION.md').write_text('''# Verwendung der Dateien

1. ZIP in einen neuen Ordner entpacken, nicht über die bisherige Kopie.
2. Für den NPC die einzelne Datei aus `skins/` verwenden. Die Bilder aus `previews/` und die Kontrolltafeln sind keine Skins.
3. Das klassische Spieler-Modell / Classic (4 Pixel breite Arme) verwenden. Grundkörper und zweite Ebene sind dafür angelegt.
4. Bei einem Skin-Upload auf GitHub bleiben die vorhandenen Root-Dateinamen bestehen: zum Beispiel `gym_fire.png`, **nicht** eine normale GitHub-HTML-Seite als Bildinhalt. `SKIN_ZUORDNUNG.json` enthält beide Pfade (lokal und GitHub).
5. Diese Ausgabe selbst installiert keine Mods und verändert keine Serverdateien, NPC-Daten, Questfortschritte oder GitHub-Dateien.

## Windows-Kontrolle ohne Installation

`SKINS_ANSEHEN.html` lokal im Browser öffnen. Keine PowerShell-Freigaben, Git-DLLs, Tokens, Node.js oder zusätzlichen Bibliotheken erforderlich. Die 45 Skin-PNGs und ihre V4-Vergleichstexturen sind in der Datei eingebettet. Die Seite arbeitet ohne Netzabfragen.

## Feuer-Arenaleiter

Kaels neues Haar wurde auf Grund- und Außenschicht neu aufgebaut. Die Haarfarben lauten RGB (87,19,36), (137,24,42), (190,39,46), (226,61,33), (249,111,35). Die hellen Flächen des Gesichts sind Haut, keine verbliebene blonde Haarlage. `qa/FEUER_HAARPRUEFUNG.png` zeigt Vorderseite, Rückseite, beide Seiten und Scheitel jeweils mit und ohne äußere Ebene.

Die konkrete Menüführung deiner EasyNPC-Version wurde nicht im laufenden Spiel getestet. Das Paket behauptet keinen abgeschlossenen Ingame-Test.
''',encoding='utf-8')
notes=['# Gestaltung der 45 Figuren','', 'Die IDs und Namen stammen aus dem bereitgestellten V4-Paket. Die nachfolgenden Kleidungsmasken, Farbpaletten und Details sind neu.','']
for d in D:
 notes += [f"## {ROSTER[d.id]['npc_name']} – `{d.id}`",'',d.note,'',f"Haargrundton: `#{d.hair}`. Kleidung: `#{d.main}`, `#{d.second}`; Akzent: `#{d.accent}`. Modell: Classic. Eigene Front- und Rückenmaske; durchgehende Seitenflächen; individuelle Kopf-/Accessoirekombination.",'']
(ROOT/'DESIGN_NOTIZEN.md').write_text('\n'.join(notes),encoding='utf-8')
(ROOT/'QUALITY_REPORT.md').write_text(f'''# Prüfbericht

## Automatische Dateiprüfungen – bestanden

- 45 PNG-Dateien, jeweils 64×64 Pixel, RGBA.
- Je 1.632 Grundkörperpixel vollständig blickdicht.
- Keine Füllung außerhalb der definierten Grund-/Außen-UV-Flächen.
- Alpha ausschließlich 0 oder 255, keine unbeabsichtigten halbtransparenten Körperstellen.
- 45 unterschiedliche PNG-Prüfsummen und 45 unterschiedliche Kopf-Vorderseiten.
- {len(maskfrontset)} individuell definierte Torso-Vorderseiten und {len(backset)} unterschiedliche Torso-Rückenmasken. Team-Nova-Uniformen teilen bewusst das Fraktionsmotiv.
- Alle 45 Texturen weichen um mehr als 1.000 Pixel von der bereitgestellten V4 ab.
- Dieselben 45 IDs und Dateinamen wie im Ausgangspaket.
- 45 Einzeltafeln mit je fünf Ansichten, insgesamt 225 Modellansichten.
- Feuer-Haarregression: Keine Fremdfarbe in den markierten Haarflächen der Grundebene.

Detaillierte Messwerte: `qa/VALIDIERUNG.json`, `qa/fire_hair_regression.json`.

## Künstlerische Kontrolle

Front-/Dreiviertel-Gesamtansicht, Rückseiten und rechte Seiten wurden als Kontrolltafeln ausgegeben. Separate Nahkontrolle des Feuer-Arenaleiters einschließlich seiner beiden Haarebenen. Vorher-Nachher-Vergleiche verwenden tatsächlich die V4-PNGs und die neuen PNGs bei gleicher Darstellung.

Künstlerische Qualität wird nicht mit einem erfundenen Prüfsiegel oder einem objektiven Prozentwert versehen. Die Vorschauen erlauben die direkte Beurteilung der gelieferten Dateien.

## Nicht durchgeführt

- Laufzeittest auf dem Novoriamon-Server bzw. in EasyNPC.
- Prüfung der URL-Zwischenspeicherung des Clients.
- Veröffentlichung der neuen Dateien auf GitHub.

## Herstellungsverfahren

Die 45 Front-/Rücken-Kleidungsentwürfe sind einzeln als native Pixelmasken ausgearbeitet. Gemeinsamer Code übernimmt UV-Zuordnung, Materialfarben, Oberflächen-Schattierung, Arme/Beine und Kontrolle. Die Bilder sind kein behauptetes Werk eines extern beauftragten Skin-Artists. Kein hochauflösendes Illustrationsbild wurde in ein Skinformat heruntergerechnet.
''',encoding='utf-8')
for f in ['build.py','render.py','package.py','designs.py']:
 if (HERE/f).resolve()!=(ROOT/'source'/f).resolve():
  shutil.copy(HERE/f,ROOT/'source'/f)
print(json.dumps({k:v for k,v in summary.items() if k!='files'},ensure_ascii=False,indent=2))
print('Viewer bytes',(ROOT/'SKINS_ANSEHEN.html').stat().st_size)
