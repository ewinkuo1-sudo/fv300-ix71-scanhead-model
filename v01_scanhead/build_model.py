from pathlib import Path
import sys,json,math,csv
ROOT=Path(__file__).resolve().parent
OLD=ROOT.parent.parent/'FV5000_IX85_Model_25cm'
sys.path.insert(0,str(OLD/'.deps'))
import numpy as np
import manifold3d as md
import trimesh
M=md.Manifold
parts=[]
def box(x,y,z,a,b,c): return M.cube((a,b,c)).translate((x,y,z))
def cyl(x,y,z,r,h): return M.cylinder(h,r,r,40).translate((x,y,z))
def ring(x,y,z,r,t,h): return cyl(x,y,z,r,h)-cyl(x,y,z-1,r-t,h+2)
def rod(a,b,r):
    v=np.array(b)-a; l=np.linalg.norm(v); z=v/l
    x=np.cross([0,1,0] if abs(z[1])<.9 else [1,0,0],z);x/=np.linalg.norm(x);y=np.cross(z,x)
    return M.cylinder(l,r,r,24).transform(np.column_stack((x,y,z,a)))
def add(name,s,col='#30343a',source='20260910_153030.jpg',note='照片可見外形；位置與尺寸按比例估算，非原廠 CAD。',group='structure',ex=(0,0,0)):
    meshdata=s.to_mesh()
    mesh=trimesh.Trimesh(np.asarray(meshdata.vert_properties)[:,:3],np.asarray(meshdata.tri_verts),process=True)
    assert mesh.is_watertight and mesh.is_winding_consistent and mesh.volume>0,name
    p=dict(id=f'{len(parts)+1:02d}',name=name,color=col,group=group,note=note,evidence=source,explode=list(ex),vertices=mesh.vertices.round(4).tolist(),faces=mesh.faces.tolist())
    parts.append(p)
    return s
silver='#a6aaac';gold='#a78c48';dark='#282c31'
# Model coordinates: x left/right in overview; y front/rear; z up.
# 180 x 125 is an arbitrary review scale, NOT a measured physical size.
outer=box(0,0,0,180,125,47)
# round the four interior corners by offsetting a rectangular section
inner=md.CrossSection.square((170,115)).offset(2,md.JoinType.Round).extrude(49).translate((5,5,3))
shell=outer-inner
for x,y in [(3,3),(177,3),(3,122),(177,122)]:
    shell=shell-cyl(x,y,40,1.2,9)
add('開蓋鑄造外框與底板',shell,silver,group='cover',ex=(0,0,-30))
# structural dividers seen in overview
add('右側掃描區縱向隔牆',box(119,3,3,3,119,42),silver)
add('後方電子區隔牆',box(3,85,3,116,3,42),silver)
add('電子區分隔肋',box(77,88,3,3,34,42),silver)
# top metal bridge with two real openings approximated
bridge=box(2,84,45,120,39,2)
for x,w in [(9,63),(83,31)]:
    hole=md.CrossSection.square((w-4,27)).offset(2,md.JoinType.Round).extrude(5).translate((x+2,92,44))
    bridge=bridge-hole
add('雙開窗上方金屬橋板',bridge,'#c4c5bf',ex=(0,0,22))
# optical plate and divider aperture, not glass modeled behind unseen structures
plate=box(6,42,5,105,4,30)-rod((55,40,23),(55,49,23),4)
add('帶圓孔的橫向黑色支架',plate,dark,'20260910_153102.jpg')
add('左側圓筒座',rod((25,48,22),(25,81,22),10),dark,'20260910_153102.jpg')
add('圓筒端部綠色環',rod((25,79,22),(25,81,22),10.6)-rod((25,78,22),(25,82,22),8.6),'#397557','20260910_153102.jpg')
add('左側黃銅支柱',rod((42,48,15),(42,81,15),3),gold,'20260910_153102.jpg')
# wheel / bevel gear assembly visible in front left
add('轉動機構底座',box(51,17,3,22,23,4),dark,'20260910_153102.jpg')
wheel=rod((63,25,10),(63,25,28),10)-rod((63,25,9),(63,25,29),3)
add('可見金屬轉輪（功能待核對）',wheel,silver,'20260910_153102.jpg')
add('轉輪中央軸',rod((63,25,3),(63,25,31),2.1),gold,'20260910_153102.jpg')
add('前方水平傳動軸',rod((31,14,12),(63,14,12),2),gold,'20260910_153102.jpg')
gear=rod((61,10,12),(61,18,12),5)
for i in range(12):
    t=i*2*math.pi/12
    gear=gear+rod((61+4.7*math.cos(t),10,12+4.7*math.sin(t)),(61+4.7*math.cos(t),18,12+4.7*math.sin(t)),.8)
add('可見齒輪外輪廓',gear,dark,'20260910_153102.jpg',note='齒輪位置有照片依據；齒數與齒形未量測，僅供外形檢查。')
hood=box(84,29,4,26,40,30)-box(86,28,4,22,39,29)
add('三面黑色遮光罩',hood,dark,'20260910_153102.jpg',ex=(0,0,25))
# right chamber: visible scanning mounting plate and two motor shapes
add('右側機構安裝底板',box(128,57,3,39,49,3),'#706b50','20260910_153051.jpg')
for x,y,axis in [(143,83,0),(150,68,1)]:
    add('掃描區圓柱機構 '+str(axis+1),rod((x,y,9),(x+12 if axis else x,y if axis else y+12,9),4.5),silver,'20260910_153051.jpg',note='依照片可見圓柱與配置重建；振鏡軸向與隱藏鏡面待核對。')
    add('掃描區黑色固定座 '+str(axis+1),box(x-5,y-4,5,10,9,10),dark,'20260910_153051.jpg')
# label-bearing slider unit and support; avoid asserting optical function
add('標示 FV-FCBGR 的滑座外形',box(135,34,3,25,20,10),dark,'20260910_153051.jpg')
add('滑座側向調整桿',rod((165,33,4),(165,33,39),1.6),silver,'20260910_153051.jpg')
add('調整桿方形托座',box(160,28,17,10,10,4),silver,'20260910_153051.jpg')
add('前側銀色水平筒件',rod((133,18,13),(161,18,13),5.5),silver,'20260910_153051.jpg')
add('前側帶孔片架',box(126,9,4,3,16,19)-rod((124,17,15),(131,17,15),4),gold,'20260910_153051.jpg')
# external coupling visible at right
add('側向連接鏡筒的可見段',rod((177,48,22),(199,48,22),10)-rod((176,48,22),(200,48,22),7.5),dark,'20260910_153030.jpg',note='照片中可見段；端部和內部鏡片無資料，留空。')
# electronics: only visible plates and bodies, no guessed PCB traces
add('後方直立電路板外形',box(111,94,7,1.3,24,32),'#3c6251')
add('中央金屬盒可見外形',box(84,94,5,20,22,31),'#b2b1a6')
add('左後方電路板可見段',box(10,95,7,25,1.2,11),'#467761')
# cables from traced approximate visible routes, individual segment paths remain simple
routes=[
([(134,104,13),(137,113,21),(156,114,25),(167,101,24),(164,89,22),(153,88,17),(142,98,18),(143,83,16)],'#35373b',1.6),
([(130,106,16),(138,118,28),(162,117,30),(172,101,27),(167,83,25),(152,79,16)],'#56595c',1.5),
([(21,100,20),(18,113,30),(40,120,29),(59,113,27),(44,99,19),(30,99,16)],'#d3c8aa',1.0),
([(100,111,20),(106,100,32),(111,86,35),(113,62,20),(108,40,9)],'#b54336',.65),
([(97,113,21),(104,98,31),(110,85,36),(112,65,22),(107,40,10)],'#445587',.65)]
for i,(points,col,r) in enumerate(routes):
    s=rod(points[0],points[1],r)
    for a,b in zip(points[1:-1],points[2:]): s=s+rod(a,b,r)
    add('照片可見配線 '+str(i+1),s,col,note='線束走向按照片近似；未重建被遮蔽的接線。',ex=(0,0,12))
for x,y in [(130,62),(162,62),(130,100),(162,100),(54,20),(72,20),(5,80),(116,80)]:
    add('可見固定螺絲',cyl(x,y,7,1.7,1.3)-box(x-1.5,y-.3,7.8,3,.6,1),silver)
payload=json.dumps(dict(parts=parts,paths=[],decals=[]),ensure_ascii=False,separators=(',',':'))
(ROOT/'model.json').write_text(payload,encoding='utf-8')
template=(OLD/'v03_photo_review'/'viewer.html').read_text(encoding='utf-8')
js=template[template.index('const $='):template.rindex('</script>')]
js=js.replace('az=.418879','az=.12').replace('el=.174533','el=1.05').replace('[59,59,125]','[100,62,22]').replace('Math.min(W/245,H/305)','Math.min(W/245,H/195)')
js=js.replace('外罩可移除；缺少原廠圖面的內部保持空白。','依實拍重建可見機構；尺寸未量測、功能待逐項核對。')
prefix="""<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><title>FV300 掃描頭內構 v0.1</title>
<style>*{box-sizing:border-box}body{margin:0;font:15px system-ui;color:#22323c;background:#f5f7f9}header{padding:16px 22px;background:#1c303c;color:white}h1{font-size:21px;margin:0 0 6px}main{display:flex;height:calc(100vh - 90px)}#view{position:relative;flex:1;min-width:0}canvas{position:absolute;inset:0;width:100%;height:100%}#overlay{pointer-events:none}#fallback{position:absolute;inset:0;width:100%;height:100%;object-fit:contain}aside{width:310px;padding:22px;background:white;overflow:auto}label{display:block;margin:14px 0}button,select{padding:8px;margin:3px;max-width:100%}p{line-height:1.6}.muted{color:#626d76}a{color:#167087}</style>
<header><h1>FV300 掃描頭｜照片內構模型 v0.1</h1>依你的實機開蓋照片建立 · 尚未量測尺寸</header>
<main><div id="view"><img id="fallback" alt="模型載入中"><canvas id="c"></canvas><canvas id="overlay"></canvas></div><aside>
<p>拖曳旋轉，滾輪縮放。預設從開蓋角度查看內部。</p>
<button id="iso">開蓋視角</button><button id="top">俯視</button><button id="front">正面</button><button id="reset">重設</button>
<label><input id="covers" type="checkbox" checked>顯示外框與底板</label>
<label style="display:none"><input id="supports" type="checkbox">支撐</label>
<label><input id="labels" type="checkbox">顯示全部名稱</label>
<label>分解距離<input id="explode" type="range" min="0" max="1" step=".01" value="0"></label>
<select id="part"><option value="">選擇零件</option></select>
<label><input id="solo" type="checkbox">只顯示選取零件</label>
<p id="info">可見機構有照片依據；精確尺寸及部分元件功能尚待核對。</p>
<p class="muted">此版只含掃描頭，尚未整合 IX71。座標為暫定比例，整機 25 公分縮尺會在整合時設定。不可直接送印。</p>
<a href="../20260910_153030.jpg">開蓋全景照片</a><br><a href="../20260910_153051.jpg">右側機構照片</a><br><a href="../20260910_153102.jpg">左側機構照片</a><br><a href="parts.csv">元件與依據清單</a>
</aside></main><script>window.onerror=(msg)=>{document.body.dataset.errors=String(msg);document.getElementById('info').textContent=String(msg)};"""
(ROOT/'viewer.html').write_text(prefix+'const DATA='+payload+';\n'+js+'</script></html>',encoding='utf-8')
with (ROOT/'parts.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.writer(f);writer.writerow(['ID','名稱','依據照片','限制'])
    for p in parts: writer.writerow([p['id'],p['name'],p['evidence'],p['note']])
report=dict(parts=len(parts),all_parts_watertight=True,print_ready=False,scale_measured=False,scope='Visible scan head geometry only; unknown internal surfaces omitted')
(ROOT/'validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
(ROOT/'README.md').write_text('# FV300 掃描頭內構 v0.1\n\n開啟 viewer.html。依 20260910 三張開蓋照片建立可見隔間、支架、輪軸、滑座與線束。\n\n尺寸、隱藏面、齒數與部分機構功能未核實；不是原廠 CAD，也不是列印成品。IX71 未建模。暫定模型單位並非實機尺寸。缺資料處留空；不建立臆測光路。\n\nbuild_model.py 可重新產生模型，使用相鄰歷史專案的 .deps 與 Canvas2D 預覽程式。\n',encoding='utf-8')
print(json.dumps(report))
