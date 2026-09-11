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
def add(name,s,col='#30343a',source='20260910_171623.jpg；高度參考 153030 / 153051 / 153102',note='照片可見外形；位置與尺寸按比例估算，非原廠 CAD。',group='structure',ex=(0,0,0)):
    meshdata=s.to_mesh()
    mesh=trimesh.Trimesh(np.asarray(meshdata.vert_properties)[:,:3],np.asarray(meshdata.tri_verts),process=True)
    assert mesh.is_watertight and mesh.is_winding_consistent and mesh.volume>0,name
    p=dict(id=f'{len(parts)+1:02d}',name=name,color=col,group=group,note=note,evidence=source,explode=list(ex),vertices=mesh.vertices.round(4).tolist(),faces=mesh.faces.tolist())
    parts.append(p)
    return s

silver='#adb1b3';gold='#b29758';dark='#24292e'
# XY traced in image pixel coordinates. Uniform arbitrary 7.3 px/model-unit.
# Photo perspective and height remain uncalibrated. Not physical dimensions.
def pt(u,v,z):return ((u-210)/7.3,(950-v)/7.3,z)
def pb(u,v,w,h,z,t):
    x,y,_=pt(u,v+h,z)
    return box(x,y,z,w/7.3,h/7.3,t)
def rr(u,v,w,h,z,t,r=1):
    x,y,_=pt(u,v+h,z)
    return md.CrossSection.square((w/7.3-2*r,h/7.3-2*r)).offset(r,md.JoinType.Round).extrude(t).translate((x+r,y+r,z))
def pr(a,b,r): return rod(pt(*a),pt(*b),r)
def pc(u,v,z,r,h):return cyl(*pt(u,v,z),r,h)
def screw(u,v,z):
    return pc(u,v,z,1.15,.7)-pb(u-6,v-1.6,12,3.2,z+.4,.5)
# Outer rim footprint from full overhead view; inner cavity is hollow.
shell=rr(210,230,1470,720,0,33,2)-rr(232,250,1426,680,2.5,34,2)
for u,v in [(250,254),(1642,257),(240,907),(1650,912)]:
    shell=shell-pc(u,v,29,1.05,6)
add('外框與底板｜比例依新俯視照',shell,silver,group='cover',ex=(0,0,-18))
# The formerly omitted left longitudinal bay.
add('左側狹長區內隔牆',pb(443,255,26,669,3,29),silver)
leftpanel=pb(300,358,5,530,4,23)-pr((297,629,17),(309,629,17),3.5)
add('左側狹長區黑色板件',leftpanel,dark)
add('中央與右側縱向隔牆',pb(1224,258,30,668,3,29),silver)
add('中央電子區橫向隔牆',pb(476,550,748,24,3,28),silver)
add('兩電子開窗間的隔肋',pb(958,270,23,280,3,28),silver)
bridge=rr(448,245,800,332,32,1.8,1.5)
bridge=bridge-rr(512,270,425,263,31,4,2)
bridge=bridge-rr(998,273,222,238,31,4,1.5)
add('雙開窗上方橋板',bridge,'#c5c6c0',ex=(0,0,20))
# Cast stepped support visible left of central lengthwise black plate.
cast=pb(510,712,205,115,3,19)+pb(680,689,30,155,3,19)
add('中央左側階梯狀鑄造支座',cast,silver)
add('左圓筒可見段',pr((649,593,15),(649,682,15),8.4),dark)
add('左圓筒後緣',pr((649,581,15),(649,595,15),8.9),dark)
add('支座前方圓筒可見段',pr((649,827,12),(649,860,12),7.8),dark)
add('左側黃銅桿',pr((757,608,19),(757,698,19),2.4),gold)
# Long plate spans front/rear and its round top opening is vertical.
plate=rr(784,603,137,326,23,3,1.4)-pc(841,775,22,2.8,6)
add('中央前後向帶圓孔長板',plate,dark,ex=(0,0,14))
add('中央長板左側折邊',pb(710,694,68,232,8,19),dark)
add('中央長板右側折邊',pb(921,603,12,101,9,17),dark)
# Upright wheel has X axis, not vertical axis.
add('立式轉輪金屬座',pb(933,748,42,139,3,13),silver)
wheel=pr((971,812,16),(1015,812,16),11.6)-pr((969,812,16),(1017,812,16),2.2)
add('立式轉輪｜軸向左右',wheel,dark,note='輪盤軸向依新俯視與舊斜拍校正；輪緣細節未量測。')
add('轉輪側向黃銅轴',pr((920,812,16),(1073,812,16),1.55),gold)
add('右下前後向黃銅軸套',pr((1102,847,12),(1102,922,12),2.8),gold)
# Only gear envelopes: do not invent tooth counts.
add('側向傘齒輪外形包絡',pr((1070,812,16),(1082,812,16),3.1),dark,note='照片可見齒輪包絡；齒數、齒形未知，未製作齒。')
add('前後向傘齒輪外形包絡',pr((1102,832,12),(1102,847,12),3.0),dark,note='照片可見齒輪包絡；齒數、齒形未知，未製作齒。')
# Small exposed actuator at upper right of central compartment.
add('中央右上銀色托板',rr(1029,619,100,78,8,2,.8),silver)
add('中央右上圓筒機構',pr((1051,650,14),(1117,650,14),3.8),dark)
add('中央右上直立薄板',pb(1128,609,10,132,5,19),silver)
add('中央橫向金屬連桿',pb(936,697,177,11,8,1.7),gold)
# Right upper mounting plate and visible crossed cylindrical mechanisms.
base=rr(1266,390,198,188,3,2,2)
add('右上掃描區金屬底板',base,'#79766a')
add('右上前後向圓柱',pr((1425,426,11),(1425,475,11),3.9),silver)
add('右上橫向圓柱',pr((1267,530,11),(1339,530,11),3.7),dark)
add('右上前後向圓柱夹座',rr(1392,461,69,53,5,9,.8),dark)
add('右上橫向圓柱夹座',rr(1335,497,70,58,5,9,.8),dark)
add('右上斜向固定臂',pr((1357,500,14),(1393,474,14),2.1),dark)
# Middle right slider, rails, bevel bracket and horizontal adjustment rod.
add('右中滑座底板',rr(1370,613,223,107,3,3,1),dark)
for v in (620,700):
    add('右中滑座導軌',pb(1385,v,186,10,6,3),silver)
add('右中開口框架',pb(1481,631,80,60,7,8)-pb(1497,642,49,40,6,11),dark)
slant=pr((1387,683,11),(1452,625,11),2.3)
add('右中斜向片架',slant,silver)
add('右中標籤承載片',pb(1390,629,47,27,14,1), '#c5c8c5')
add('右中水平調整軸',pr((1514,652,12),(1668,652,12),1.35),silver)
add('右中調整軸端座',pb(1570,627,51,57,6,11)-pr((1568,652,12),(1623,652,12),1.5),silver)
add('右中圓形旋鈕',pr((1499,652,12),(1514,652,12),2.2),gold)
# Lower right silver T-shaped body; main cylinder points fore/aft.
add('右下銀色前後向筒件',pr((1470,755,11),(1470,869,11),4.1),silver)
add('右下銀色橫向分支',pr((1410,783,11),(1528,783,11),2.6),silver)
add('右下黃銅支座',pr((1322,816,12),(1322,857,12),4.1),gold)
add('右下黑色圓筒',pr((1322,860,12),(1322,912,12),4.4),dark)
aperture=pb(1290,738,59,78,18,2)-pc(1316,775,17,2.6,4)
add('右下帶圓孔黃銅片架',aperture,gold)
# Coupler and two front knobs visible in new view.
add('右側連接鏡筒',pr((1678,547,17),(1837,547,17),11)-pr((1676,547,17),(1840,547,17),8.2),dark)
add('前側大旋鈕可見段',pr((1105,947,15),(1105,1019,15),8.7),dark)
add('前側小調整桿',pr((770,947,13),(770,1013,13),1.7),gold)
# Rear electronics visible envelopes.
add('後方金屬盒',rr(1007,287,89,218,6,20,1), '#b6b8b3')
add('後方右側電路板',pb(1162,289,8,216,4,25),'#477760')
add('左後方水平小電路板',pb(526,506,141,17,10,1.2),'#477760')
for u in (565,657,688,752,836):
    add('左後方可見接頭',pr((u,476,14),(u,510,14),1.4),gold if u in (565,688,836) else '#d8d7c7')
# Smooth interpolating spline for visible cable routes only.
def wire(points,r):
    a=np.array([pt(*p) for p in points]); q=np.vstack((a[0],a,a[-1])); samples=[]
    for i in range(len(a)-1):
        p0,p1,p2,p3=q[i:i+4]
        for t in np.linspace(0,1,7,endpoint=False):
            samples.append(.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t*t*t))
    samples.append(a[-1])
    vertices=[];faces=[];n=12
    for i,p in enumerate(samples):
        tangent=samples[min(i+1,len(samples)-1)]-samples[max(i-1,0)]
        tangent/=np.linalg.norm(tangent)
        u=np.cross(tangent,[0,0,1]);u/=np.linalg.norm(u);v=np.cross(tangent,u)
        for j in range(n):
            t=2*math.pi*j/n
            vertices.append(p+r*(u*math.cos(t)+v*math.sin(t)))
    for i in range(len(samples)-1):
        for j in range(n):
            a=i*n+j;b=i*n+(j+1)%n;c=b+n;d=a+n
            faces.extend([(a,b,c),(a,c,d)])
    for j in range(1,n-1):
        faces.append((0,j+1,j))
        k=(len(samples)-1)*n
        faces.append((k,k+j,k+j+1))
    return M(md.Mesh(np.array(vertices,dtype=np.float32),np.array(faces,dtype=np.uint32)))

routes=[
([(1270,420,19),(1380,361,26),(1480,286,29),(1380,266,30),(1270,286,27)],dark,1.15),
([(1280,391,20),(1394,313,27),(1450,294,28),(1340,286,27),(1260,313,24)],'#858b88',.85),
([(1310,474,15),(1350,385,21),(1410,327,23)],dark,1.0),
([(565,471,17),(592,363,26),(675,303,27),(820,325,28),(934,280,30)],'#bfc0b6',.8),
([(688,480,15),(678,390,22),(780,387,23),(872,327,25),(926,283,28)],'#ddd5be',.75),
([(836,486,16),(850,412,25),(827,353,27),(748,340,27)],'#d9d3c2',.75),
([(579,426,22),(629,349,30),(751,315,31),(926,273,33)],'#3e4b87',.6),
([(584,430,22),(634,353,30),(756,319,31),(930,277,33)],'#be443b',.6),
([(1112,286,28),(1142,396,29),(1145,502,26),(1127,595,19)],'#c74737',.55)]
for i,(points,col,r) in enumerate(routes):
    add('可見平滑線束 '+str(i+1),wire(points,r),col,note='依照片描出可見線束大致走向；遮住的接線留空。',ex=(0,0,8))
for u,v,z in [(1238,594,32),(1239,852,32),(1358,470,15),(1385,549,15),(1058,631,15),(1104,687,15),(945,790,17),(945,842,17)]:
    add('照片可見固定螺絲',screw(u,v,z),silver)
payload=json.dumps(dict(parts=parts,paths=[],decals=[]),ensure_ascii=False,separators=(',',':'))
(ROOT/'model.json').write_text(payload,encoding='utf-8')
template=(OLD/'v03_photo_review'/'viewer.html').read_text(encoding='utf-8')
js=template[template.index('const $='):template.rindex('</script>')]
js=js.replace('az=.418879','az=0').replace('el=.174533','el=1.57079632679').replace('[59,59,125]','[111,49,16]').replace('Math.min(W/245,H/305)','Math.min(W/245,H/145)')
js=js.replace("$('iso').onclick=()=>{az=0;el=1.57079632679;dirty=true}","$('iso').onclick=()=>{az=.15;el=1.0;dirty=true}")
js=js.replace('外罩可移除；缺少原廠圖面的內部保持空白。','依實拍重建可見機構；尺寸未量測、功能待逐項核對。')
prefix="""<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><title>FV300 掃描頭內構 v0.2</title>
<style>*{box-sizing:border-box}body{margin:0;font:15px system-ui;color:#22323c;background:#f5f7f9}header{padding:16px 22px;background:#1c303c;color:white}h1{font-size:21px;margin:0 0 6px}main{display:flex;height:calc(100vh - 90px)}#view{position:relative;flex:1;min-width:0}canvas{position:absolute;inset:0;width:100%;height:100%}#overlay{pointer-events:none}#fallback{position:absolute;inset:0;width:100%;height:100%;object-fit:contain}aside{width:310px;padding:22px;background:white;overflow:auto}label{display:block;margin:14px 0}button,select{padding:8px;margin:3px;max-width:100%}p{line-height:1.6}.muted{color:#626d76}a{color:#167087}</style>
<header><h1>FV300 掃描頭｜照片內構模型 v0.2</h1>依你的實機開蓋照片建立 · 尚未量測尺寸</header>
<main><div id="view"><img id="fallback" alt="模型載入中"><canvas id="c"></canvas><canvas id="overlay"></canvas></div><aside>
<p>拖曳旋轉，滾輪縮放。預設俯視；可切換斜視，或與新照片並排核對。</p>
<button id="iso">斜視</button><button id="top">俯視</button><button id="front">正面</button><button id="reset">重設</button>
<label><input id="covers" type="checkbox" checked>顯示外框與底板</label>
<label style="display:none"><input id="supports" type="checkbox">支撐</label>
<label><input id="labels" type="checkbox">顯示全部名稱</label>
<label>分解距離<input id="explode" type="range" min="0" max="1" step=".01" value="0"></label>
<select id="part"><option value="">選擇零件</option></select>
<label><input id="solo" type="checkbox">只顯示選取零件</label>
<p id="info">可見機構有照片依據；精確尺寸及部分元件功能尚待核對。</p>
<p class="muted">此版只含掃描頭，尚未整合 IX71。座標為暫定比例，整機 25 公分縮尺會在整合時設定。不可直接送印。</p>
<a href="comparison.html">照片與模型並排對照</a><br><a href="../20260910_171623.jpg">新俯視照片</a><br><a href="../20260910_153030.jpg">開蓋全景照片</a><br><a href="../20260910_153051.jpg">右側機構照片</a><br><a href="../20260910_153102.jpg">左側機構照片</a><br><a href="parts.csv">元件與依據清單</a>
</aside></main><script>window.onerror=(msg)=>{document.body.dataset.errors=String(msg);document.getElementById('info').textContent=String(msg)};"""
(ROOT/'viewer.html').write_text(prefix+'const DATA='+payload+';\n'+js+"if(new URLSearchParams(location.search).has('iso'))$('iso').click();if(new URLSearchParams(location.search).has('embed')){document.querySelector('aside').style.display='none';document.querySelector('header').style.display='none';document.querySelector('main').style.height='100vh';resize();dirty=true;}"+'</script></html>',encoding='utf-8')
with (ROOT/'parts.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.writer(f);writer.writerow(['ID','名稱','依據照片','限制'])
    for p in parts: writer.writerow([p['id'],p['name'],p['evidence'],p['note']])
report=dict(parts=len(parts),all_parts_watertight=True,print_ready=False,scale_measured=False,scope='Visible scan head geometry only; unknown internal surfaces omitted')
(ROOT/'validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
(ROOT/'README.md').write_text('# FV300 掃描頭內構 v0.2\n\n開啟 viewer.html。依 20260910 新俯視照與三張斜拍照片建立可見隔間、支架、輪軸、滑座與線束。\n\n尺寸、隱藏面、齒數與部分機構功能未核實；不是原廠 CAD，也不是列印成品。IX71 未建模。暫定模型單位並非實機尺寸。缺資料處留空；不建立臆測光路。\n\nbuild_model.py 可重新產生模型，使用相鄰歷史專案的 .deps 與 Canvas2D 預覽程式。\n',encoding='utf-8')
print(json.dumps(report))

(ROOT/'comparison.html').write_text('''<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><title>FV300 照片與 v0.2 對照</title><style>body{margin:0;font:16px system-ui;background:#e9edef}header{padding:12px}main{display:flex;height:88vh}section{width:50%}img{width:100%;height:92%;object-fit:contain}iframe{width:100%;height:100%;border:0}</style><header>左：新俯視照片　右：可旋轉模型 v0.2。高度與精確尺寸仍未量測。</header><main><section><img src="../20260910_171623.jpg"></section><section><iframe src="viewer.html?embed=1"></iframe></section></main></html>''',encoding='utf-8')

