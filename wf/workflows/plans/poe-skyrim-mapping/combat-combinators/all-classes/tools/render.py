"""Render review-only HTML from per-class tables; no game or source mutations."""
from pathlib import Path
import sys,json,html,argparse,os
ap=argparse.ArgumentParser();ap.add_argument('--data-root',type=Path,default=Path(__file__).parent);ap.add_argument('--repo-root',type=Path,default=Path.cwd());ap.add_argument('--output',type=Path);ap.add_argument('--geometry-root',type=Path);ap.add_argument('--semantics-pass',action='store_true');ap.add_argument('--geometry-verified',action='store_true');args=ap.parse_args();B=args.data_root.resolve();repo=args.repo_root.resolve();out=(args.output or B/'REVIEW.html').resolve();link=lambda p:os.path.relpath(p,out.parent);sys.path.insert(0,str(repo/'wf/tools'));from tabledb import load
roster=load(str(repo/'wf/workflows/plans/poe-skyrim-mapping/combat-combinators/roster.json')).rows;lookup={r['id']:r for r in roster};classes={r['id'][0]:r['class'] for r in roster};legacy={'C':'C3','D':'D1','G':'G1'}
def text(v):
 if isinstance(v,(list,dict)):v=json.dumps(v,ensure_ascii=False)
 v=str(v or '—').replace('design_candidate: ','').replace('pending_review','待過目');return html.escape(v).replace('\n','<br>')
def val(r,new,old=''):return r.get(new) or r.get(old) or '詳原規則，未新增承諾'
def effective(r):
 if r.get('row_kind')!='legacy_reference':return r
 locator=r['source_path'];locator=locator['$fmt'].replace('${gitRoot}',str(repo)) if isinstance(locator,dict) else locator;p=Path(locator);p=p if p.is_absolute() else repo/p
 return next(x for x in load(str(p)).rows if x['rule_id']==r['source_rule_id'])
def badges(sub):
 partial=sub=='C3';return '<div class="badges"><span>設計：可審候選</span><span>source：'+('部分來源已驗' if partial else '待實作')+'</span><span>build：'+('已隔離建置' if partial else '未建置')+'</span><span>遊戲：未進實機</span></div>'
parts=[];intro=[]
for c in 'VGDRCMSX':
 intro.append('<div class="family"><h2>'+text(classes[c])+'</h2><div class="cards">')
 for sub in [c+str(i) for i in (1,2,3)]:
  r=lookup[sub];intro.append('<a class="intro" href="#'+sub+'"><b>'+sub+' · '+text(r['name'])+'</b><p>'+text(r['fantasy'])+'</p><small>'+text(r['loop'])+'</small></a>')
 intro.append('</div></div>')
 rr=load(str(B/c/'rules.json')).rows;rs=[(effective(r),r.get('row_kind')=='legacy_reference') for r in rr]
 parts.append(f'<details class="classgroup" id="{c}"><summary class="classhead">{text(classes[c])} · 展開通用池與三子型規則</summary><p><a href="{link(B/c/'REPORT.md')}">本職交接</a> · <a href="{link(B/c/'rules.json')}">規則資料</a> · <a href="{link(B/c/'feasibility.json')}">待證能力／混買</a></p>')
 if args.geometry_root and (args.geometry_root/f'region-{c}.svg').exists():
  parts.append('<details><summary>真PoE區域圖與入口</summary><p>原圖ID／邊／型別／權重保留；普通shared connector只買算一次。>8 ordinary入口是review警訊，非遊戲cap。G2=10、D3=10、S2=9，替代路未採用。</p><img style="max-width:100%;background:#fff" src="'+link(args.geometry_root/f'region-{c}.svg')+'" alt="'+text(classes[c])+'真圖subset"></details>')
 for sub in [None]+[c+str(i) for i in (1,2,3)]:
  title='職業通用 · 共用一池4進階／2高階' if sub is None else lookup[sub]['name']+' · 6進階／2高階'
  parts.append('<h3 id="'+(sub or c+'common')+'">'+text(title)+'</h3>')
  if sub:parts.append(badges(sub)+'<p>'+text(lookup[sub]['loop'])+'</p>')
  for r,islegacy in rs:
   who=None if r.get('scope')=='class_common' else legacy.get(c) if islegacy else r.get('owner_subtype')
   if who!=sub:continue
   high=r['tier']=='high';parts.append('<article class="rule '+('high' if high else 'advanced')+'"><h4>'+text(r['rule_id'])+' · '+text(r.get('name'))+'<span>'+('高階 · 改變打法' if high else '進階 · 條件與收益')+'</span></h4>')
   if high:
    front=[('選前 → 選後',str(val(r,'high_before','before_play'))+' → '+str(val(r,'high_after','after_play'))),('得到',val(r,'high_gain','gain')),('付出',val(r,'high_cost','loss'))]
   else:front=[('怎麼觸發',r.get('trigger_condition')),('得到什麼',r.get('effect_formula')),('成本與取捨',r.get('cost_timing'))]
   front += [('正向情境',val(r,'positive_example','after_play')),('無效／負向情境',val(r,'negative_example','loss'))]
   parts.append('<dl>'+''.join('<dt>'+text(k)+'</dt><dd>'+text(v)+'</dd>' for k,v in front)+'</dl>')
   tech=[('來源與對象',str(r.get('actor_source',r.get('scope','')))+'；'+str(r.get('target_selector','詳原actor/target條件'))),('狀態／刷新消耗',str(r.get('state_owner','詳lifecycle'))+'；'+str(r.get('state_refresh_consume',''))),('效果契約',r.get('effect_formula')),('清理與失效',str(r.get('lifecycle',''))+'；'+str(r.get('invalid_cases',''))),('混買／共享',r.get('compatibility')),('未證能力',r.get('capability','依本職feasibility，所有新能力未ready')),('為何不能只改數值',val(r,'high_not_numeric','mechanic_reason') if high else r.get('mechanic_reason')),('資料身分','原樣板精確reference；不改payload' if islegacy else '新設計候選；所有新強度／成本／期限待過目')]
   parts.append('<details><summary>技術、狀態與未驗界線</summary><dl>'+''.join('<dt>'+text(k)+'</dt><dd>'+text(v)+'</dd>' for k,v in tech)+'</dl></details></article>')
 parts.append('</details>')
css='.classgroup{margin-top:20px;border:1px solid #40515d;border-radius:8px}.classhead{font-size:1.3em;font-weight:bold}body{font-family:system-ui,sans-serif;background:#11171c;color:#e6edf2;max-width:1100px;margin:auto;padding:24px;line-height:1.65}a{color:#79c4ef}nav{display:flex;gap:16px;flex-wrap:wrap;position:sticky;top:0;background:#11171cf5;padding:12px 0;z-index:1}h2{border-bottom:1px solid #40515d;padding-top:30px}h3{color:#c5dce9;padding-top:20px}h4{margin:0;padding:14px;border-bottom:1px solid #344854}.notice{background:#283744;border-left:4px solid #e0b76c;padding:16px}.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.intro{background:#1b252d;border:1px solid #344854;border-radius:8px;padding:16px;text-decoration:none;color:inherit}.intro b{color:#9bd5f5}.rule{background:#1b252d;border:1px solid #344854;margin:14px 0;border-radius:8px}.rule.high{border-left:4px solid #e0b76c}h4 span{float:right;color:#b9d4e2;font-size:.8em}summary{padding:12px;cursor:pointer;background:#202e38}dl{padding:0 18px 12px}dt{font-weight:bold;color:#b9d3e1;margin-top:10px}dd{margin:3px 0 12px}.badges{display:flex;gap:8px;flex-wrap:wrap}.badges span{font-size:.8em;border:1px solid #49606f;border-radius:5px;padding:3px 8px}small{color:#b4c3ce}@media(max-width:700px){.cards{grid-template-columns:1fr}h4 span{float:none;display:block}}'
nav=''.join('<a href="#'+c+'">'+text(classes[c])+'</a>' for c in 'VGDRCMSX')
js="""function reveal(id){let t=document.getElementById(id);if(!t)return;let d=t.matches('details.classgroup')?t:t.closest('details.classgroup');if(d)d.open=true;setTimeout(()=>t.scrollIntoView(),0);}document.querySelectorAll('a[href^=\"#\"]').forEach(a=>a.addEventListener('click',()=>reveal(a.hash.slice(1))));window.addEventListener('hashchange',()=>reveal(location.hash.slice(1)));if(location.hash)reveal(location.hash.slice(1));"""
page='<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>八職業二十四型規則審閱</title><style>'+css+'</style><h1>八職業 × 二十四型</h1><p>每職共用4進階2高階，三子型各6進階2高階；共240規則，42原樣板精確承接、198新設計。</p><div class="notice"><b>24型設計已可過目，尚未進遊戲。</b>新強度、成本與期限皆待裁示。<details><summary>來源、建置與幾何狀態</summary><p>所有新能力未實作／未驗runtime。刻印只有partial來源與normal OFF build具證，正常功能未開，現役仍r3。<br>設計首版已齊，獨立語義修稿中。幾何由獨立owner掛點，完成前不宣稱真圖全部核收；原55候選/保護不動。</p></details></div><nav>'+nav+'</nav><h2>先選一種想玩的方式</h2>'+''.join(intro)+''.join(parts)+'<p><small>render.py從各職rules.json與legacy reference生成，inline內容可離線file://讀取。此頁為衍生視圖，資料檔才是真相；沒有遊戲選單、職業鎖或runtime操作。</small></p><script>'+js+'</script></html>'
page=page.replace('設計首版已齊，獨立語義修稿中。', '24型與通用池獨立語義審核已通過；新數值仍待使用者過目。' if args.semantics_pass else '設計首版已齊，獨立語義修稿中。');page=page.replace('幾何由獨立owner掛點，完成前不宣稱真圖全部核收；原55候選/保護不動。', '240 slots與較強AND前置、24 closure與8 common入口已核；圖像為真圖subset，原55／保護不動。' if args.geometry_verified else '幾何由獨立owner掛點，完成前不宣稱真圖全部核收；原55候選/保護不動。');out.write_text(page);assert out.stat().st_size<=1024**2;print('HTML bytes',out.stat().st_size)
