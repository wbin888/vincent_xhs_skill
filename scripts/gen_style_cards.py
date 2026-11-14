"""生成 README 风格色板卡片：python3 scripts/gen_style_cards.py（需 Pillow 与文泉驿正黑字体）"""
import re, os, sys
from PIL import Image, ImageDraw, ImageFont
ROOT=sys.argv[1] if len(sys.argv)>1 else os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'); OUT=os.path.join(ROOT,'assets/styles'); os.makedirs(OUT,exist_ok=True)
FONT='/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
F=lambda s: ImageFont.truetype(FONT,s)
# explicit names (longest match first)
N={'天青':'#A9C6C8','月白':'#D6ECF0','藕灰':'#C8B3B0','赭红':'#9B3B2A','石青':'#1E5E8C','石绿':'#3E8E6E','墨黑':'#1C1C1C','浓墨':'#111111','淡墨':'#8A8A8A','焦墨':'#0A0A0A',
'蜜黄木色':'#C89B5A','素灰':'#B5B2AC','青灰':'#7F8C8D','素白':'#F4F1EA','朱砂':'#C93B2B','朱红':'#E0442C','正红':'#C8102E','中国红':'#C8102E','宫墙红':'#A52A2A','鎏金':'#C9A14A','泥金':'#B8913E',
'描金':'#C9A14A','琉璃金':'#D9A531','黛瓦灰':'#5B5F66','黛瓦黑':'#2E3033','黛蓝':'#3B4A6B','青花蓝':'#1F3F8F','青瓷':'#9CC4B2','汉白玉白':'#F1EFE8','米白':'#F3EBDD','宣纸':'#F2E8D5',
'藤黄':'#F2B92B','花青':'#2F5C7A','靛蓝':'#1F3B73','靛青':'#22406B','藏青':'#1B2A4A','群青':'#3045A0','青金石蓝':'#26619C','孔雀蓝':'#00728C','钴蓝':'#0047AB','普鲁士蓝':'#003153',
'湛蓝':'#1E88E5','天蓝':'#6EC1E4','冰蓝':'#BFE6F5','雾蓝':'#9FB4C7','电蓝':'#1E4CFF','埃及蓝':'#1034A6','翡翠绿':'#1D9A6C','翠绿':'#1FAF5A','松绿':'#3F8F7A','竹青':'#789262',
'苔绿':'#6B7A3A','橄榄绿':'#708238','森林绿':'#228B22','薄荷绿':'#A8E6CF','鼠尾草绿':'#9CAF88','墨绿':'#1F3D2B','芭蕉绿':'#5E9B3B','军绿':'#4B5320','荧光绿':'#39FF14','荧光黄绿':'#C6F432',
'荧光粉':'#FF3EA5','荧光青':'#00F0FF','荧光红':'#FF2442','霓虹':'#FF2E9A','电紫':'#8F00FF','香芋紫':'#B9A3D0','紫罗兰':'#8A5CC9','雪青':'#B0A4E3','灰紫':'#8E8299','暗紫':'#3D2352','深紫':'#3B1F5C',
'樱粉':'#F7C6D0','桃粉':'#F7A8B8','玫瑰粉':'#E8879C','糖果粉':'#FF9EC7','灰粉':'#D8B4B4','柔粉':'#F4C9C9','肉粉':'#F2C1AE','马卡龙':'#F8C8DC','珊瑚橙':'#FF7F50','珊瑚红':'#F26B5B',
'万寿菊橙':'#F2A20C','番茄红':'#E5472E','柠檬黄':'#FFF44F','芒果黄':'#FFC324','芥末黄':'#D8A31A','奶油黄':'#F8E6A0','奶油白':'#FAF3E3','奶白':'#F7F2E8','鹅黄':'#FFF1A8','明黄':'#FFD400',
'铬黄':'#FFA700','镉黄':'#FFC000','土黄':'#C79A3A','沙黄':'#D9C08C','赭石':'#A0522D','赭黄':'#C08A3E','赭土':'#9C6B3E','土红':'#9E4A2F','砖红':'#B5452F','陶土红':'#C46A4A','锈红':'#8E3B2A',
'酒红':'#722F37','暗红':'#6E1E1E','血红':'#8A0303','猩红':'#D1001C','绯红':'#E03C5A','洋红':'#E0218A','品红':'#D41872','宝石红':'#9B111E','宝石绿':'#00785A','象牙白':'#F6F0E1','骨白':'#E9E2D0',
'燕麦灰':'#D6CFC2','暖灰':'#A8A097','冷灰':'#9AA0A6','浅灰':'#D3D3D3','深灰':'#3A3A3A','炭黑':'#232323','石墨黑':'#2B2B2B','纯黑':'#000000','纯白':'#FFFFFF','雪白':'#FAFAFA','纸白':'#F5F1E8',
'木色':'#B58B5A','橡木':'#B7905A','深棕':'#4A2E1F','木褐':'#7A5233','灰褐':'#8B7D6B','琥珀':'#C8781E','金黄':'#F2C230','暖金':'#D9A74A','黄铜金':'#B5913B','银':'#C0C0C0','铬银':'#D0D4D8','镭射银':'#D7DCE6',
'莫兰迪':'#B7A99A','低饱':'#A9A39B','深蓝':'#1A2A4F','幽蓝':'#14254A','冷紫':'#7B6EB0','灰蓝':'#7C8DA6','灰绿':'#8EA290','青碧':'#2E8B7A','青绿':'#2E9C8A','褪青绿':'#7FA89A','褪粉':'#E7C3C0','暖橙':'#F28C28','灰白':'#E5E3DE','枯黄':'#C9B37E','粉墙白':'#F4F1EA','粉白':'#F7EEEE','鬼火绿':'#7FD99A','幽青':'#1F5F5B','幽绿':'#1E4D3A','暖黄':'#F2C66D','暖肤':'#E8B898','冷白':'#EEF3F7','韩纸米白':'#F2EBDD','煤烟灰':'#4A4A4A','油污黑':'#1A1712','旧报纸黄':'#E3D3A8','金箔':'#D4AF37','青蓝':'#1F7A9C','粉彩':'#F6D6E0','糖果':'#FF9EC7','暮色':'#5B4B7A','橘金':'#F2A541','橘黄':'#F5A623','篝火橙':'#E8641B','血橙':'#E2492F','警示橙':'#FF6A00','大理石白':'#F2F0EB','羊毛白':'#F4EFE6','蛤白':'#F7F4EC','藏红黄':'#F4B400','沙漠赭黄':'#D2A15A','金发':'#E8C46A','铜':'#B87333'}
H={'红':'#D13B32','橙':'#F08A24','黄':'#F2C94C','绿':'#4CAF50','青':'#2F8F8F','蓝':'#2E6BD1','紫':'#8155BA','粉':'#F2A6B8','棕':'#7A4E2D','褐':'#7A5A3A','赭':'#A0522D','灰':'#9E9E9E','白':'#F5F3EE','黑':'#151515','金':'#D4A73A','银':'#C0C0C0','墨':'#222222','肤':'#E8B898'}
def shade(h,f):
    r,g,b=[int(h[i:i+2],16) for i in (1,3,5)]
    if f>0: r,g,b=[int(c+(255-c)*f) for c in (r,g,b)]
    else: r,g,b=[int(c*(1+f)) for c in (r,g,b)]
    return '#%02X%02X%02X'%(r,g,b)
KEYS=sorted(N,key=len,reverse=True)
def colors(text):
    out=[]
    for t in re.split(r'[、，,/＋+→]| vs |与|和',text):
        t=t.strip(); 
        if not t: continue
        if '单一色相多明度' in t: out+=['#1F3B73','#3E6BB5','#8FB0E0','#DCE7F7']; continue
        if '16 色复古' in t: out+=['#1A1C2C','#B13E53','#EF7D57','#FFCD75','#38B764','#41A6F6']; continue
        if '黑白' in t: out+=['#111111','#F2F2F2']; continue
        if '原色' in t and '红蓝黄' in t: out+=['#D7261E','#1F4FA8','#F6C700']; continue
        hit=[k for k in KEYS if k in t]
        if hit:
            used=''
            for k in hit:
                if k in used: continue
                used+=k; out.append(N[k])
            continue
        c=next((H[ch] for ch in t if ch in H),None)
        if not c: continue
        if any(m in t for m in '深暗浓'): c=shade(c,-.45)
        elif any(m in t for m in '浅淡柔奶褪'): c=shade(c,.5)
        elif '灰' in t and c!=H['灰']: c=shade(c,.25)
        out.append(c)
    seen=[]; [seen.append(c) for c in out if c not in seen]
    return seen[:5] or ['#B7A99A','#E8E2D6','#4A4A4A']
def lum(h): r,g,b=[int(h[i:i+2],16) for i in (1,3,5)]; return .299*r+.587*g+.114*b
def wrap(d,txt,font,w):
    lines=['']
    for ch in txt:
        if d.textlength(lines[-1]+ch,font=font)>w:
            if len(lines)==2: lines[-1]=lines[-1][:-1]+'…'; break
            lines.append(ch)
        else: lines[-1]+=ch
    return lines
CW,CH,COLS,PAD=300,250,5,16
def sheet(title,items,fn,showc=True):
    rows=(len(items)+COLS-1)//COLS
    W=COLS*CW+(COLS+1)*PAD; Hh=90+rows*(CH+PAD)+PAD
    im=Image.new('RGB',(W,Hh),'#FAF8F4'); d=ImageDraw.Draw(im)
    d.text((PAD+4,26),title,font=F(36),fill='#1D1D1F')
    for i,(num,name,pal,sub) in enumerate(items):
        x=PAD+(i%COLS)*(CW+PAD); y=90+(i//COLS)*(CH+PAD)
        d.rounded_rectangle([x,y,x+CW,y+CH],14,fill='#FFFFFF',outline='#E4E0D8')
        sw=(CW-24)/len(pal)
        for j,c in enumerate(pal):
            d.rectangle([x+12+j*sw,y+12,x+12+(j+1)*sw,y+122],fill=c)
        d.rectangle([x+12,y+12,x+CW-12,y+122],outline='#00000022')
        d.rounded_rectangle([x+12,y+134,x+64,y+164],8,fill='#1D1D1F')
        d.text((x+38,y+149),str(num),font=F(18),fill='#FDFFA7',anchor='mm')
        name=name.replace('†','').strip()
        nf=F(22)
        while d.textlength(name,font=nf)>CW-90 and nf.size>14: nf=F(nf.size-1)
        d.text((x+74,y+149),name,font=nf,fill='#1D1D1F',anchor='lm')
        for k,l in enumerate(wrap(d,sub,F(15),CW-24)):
            d.text((x+12,y+178+k*22),l,font=F(15),fill='#6B6B6B')
    im.save(os.path.join(OUT,fn),optimize=True); return fn
lib=open(os.path.join(ROOT,'vincent-xhs-cover/references/styles/22-194-aesthetic-library.md')).read()
made=[]
# 1-21
base=[(1,'爆款大字压顶风',['#FDFFA7','#FFFFFF','#111111','#E63946'],'强钩子标题、经验公开'),
(2,'巨字拆分冲击风',['#1B1F2A','#FDFFA7','#FFFFFF','#3A86FF'],'概念、身份、能力类主题'),
(3,'小白科普问答风',['#202326','#FDFFA7','#2ECC71','#FFFFFF'],'“什么是 / 怎么理解”'),
(4,'教程清单风',['#F4F4F2','#2ECC71','#FDFFA7','#222222'],'安装、部署、上手教程'),
(5,'产品测评榜单风',['#14171C','#FDFFA7','#FF5E1A','#FFFFFF'],'横评、榜单、红黑榜'),
(6,'种草推荐风',['#F6EBDD','#FDFFA7','#FFFFFF','#C88A5A'],'资源、播客、工具推荐'),
(7,'贴纸拼贴入门风',['#F7F3EC','#FDFFA7','#FF8FAB','#4D96FF'],'入门、搭建、工具组合'),
(8,'黑底效率工作流风',['#0E0F12','#2ECC71','#FDFFA7','#FFFFFF'],'工作法、自动化效率流'),
(9,'苹果极简杂志风·名师私教',['#F5F5F7','#1D1D1F','#002FA7','#FF5E1A','#FDFFA7'],'高客单 1v1、主理人大师课'),
(10,'备忘录手写便签风·课表',['#FFFDF5','#FDFFA7','#E63946','#333333'],'课表发布、入门班、陪跑营'),
(11,'多巴胺高饱和插画风·团课',['#FF4D8D','#2EE59D','#002FA7','#FDFFA7'],'燃脂团课、有氧舞蹈'),
(12,'醒目大字报纯享风·特训',['#D90429','#FDFFA7','#111111','#FFFFFF'],'早鸟、周年庆、特训营'),
(13,'Bento 卡片网格风·课程',['#F2F0EC','#DAD6CE','#1D1D1F','#FDFFA7'],'体系课、教培、套餐卡'),
(14,'自然疗愈呼吸感·瑜伽',['#F7F4EF','#7A9A8B','#2C3E35','#FDFFA7'],'流瑜伽、阴瑜伽、工作坊'),
(15,'精准体态美学·普拉提',['#E8ECEF','#F4A298','#22252A','#FDFFA7'],'器械私教、体态矫正、产后修复'),
(16,'手绘版',['#FAF3E3','#F4A261','#8AB17D','#FDFFA7'],'知识图解、动作要点、亲和力招生'),
(17,'纯文本版',['#EFEAE0','#1D1D1F','#FDFFA7','#8C7B6B'],'金句观点、干货提纲、不露脸通知'),
(18,'简约版',['#F3EFE8','#D6CFC2','#1D1D1F','#FDFFA7'],'高审美生活方式、高端工作室'),
(19,'贴图版',['#F5EFE6','#FFFFFF','#FDFFA7','#C9B79C'],'多图合集、场馆/课程多维展示'),
(20,'对比版',['#8A8F96','#E63946','#2ECC71','#FDFFA7'],'Before/After、正误对比、避坑'),
(21,'单色印刷版',['#F2EDE3','#173AE3','#242321'],'读书/观点/文化活动、孔版网点质感')]
made.append(('1–21 专属版式',sheet('风格 1–21 · 专属版式',base,'01-21-layouts.png')))
for sec in re.split(r'\n## ',lib)[1:]:
    head=sec.split('\n',1)[0]
    m=re.search(r'（(\d+)–(\d+)）',head)
    if not m: continue
    items=[]
    for l in sec.split('\n'):
        if re.match(r'^\| \d+ \|',l):
            c=[x.strip() for x in l.strip().strip('|').split('|')]
            items.append((int(c[0]),c[1],colors(c[2]),c[2]+'｜'+c[3]))
    t=re.sub(r'^[一二三四五六七八九十]+、','',head)
    made.append((t,sheet(f'风格 {m[1]}–{m[2]} · '+t.split('（')[0],items,f'{int(m[1]):03d}-{int(m[2]):03d}.png')))
for t,f in made: print(f,'|',t)
