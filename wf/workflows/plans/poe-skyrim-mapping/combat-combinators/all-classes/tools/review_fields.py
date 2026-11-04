"""Escape display fields and resolve legacy references for the review view."""
from pathlib import Path
import html
import json

def text(v):
    if isinstance(v, (list, dict)):
        v = json.dumps(v, ensure_ascii=False)
    v = str(v or '—').replace('design_candidate: ', '').replace('pending_review', '待過目')
    return html.escape(v).replace('\n', '<br>')

def val(r, new, old=''):
    return r.get(new) or r.get(old) or '詳原規則，未新增承諾'

def effective(r, repo, load):
    if r.get('row_kind') != 'legacy_reference':
        return r
    locator = r['source_path']
    locator = locator['$fmt'].replace('${gitRoot}', str(repo)) if isinstance(locator, dict) else locator
    p = Path(locator)
    p = p if p.is_absolute() else repo / p
    return next((x for x in load(str(p)).rows if x['rule_id'] == r['source_rule_id']))

def badges(sub):
    partial = sub == 'C3'
    return '<div class="badges"><span>設計：可審候選</span><span>source：' + ('部分來源已驗' if partial else '待實作') + '</span><span>build：' + ('已隔離建置' if partial else '未建置') + '</span><span>遊戲：未進實機</span></div>'
