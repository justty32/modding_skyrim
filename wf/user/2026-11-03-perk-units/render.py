#!/usr/bin/env python3
"""Build the public review projection and offline page from the private research tables."""
import argparse
import hashlib
import html
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'wf/tools'))
from tabledb import load

FIELDS = ['id', 'tier', 'name', 'source_formkey', 'source_version', 'current_winner_status',
          'source_original_values', 'numeric_unit_proposal', 'scaling',
          'trigger_threshold_cooldown_limits', 'example', 'rule_capability', 'gap_fixed',
          'mixed_split', 'principle_conflict', 'balance_risk', 'implementation_dependencies',
          'validation', 'review_gate']
SPECIAL = {'M3': '雙參數模型', 'M6': '新量綱', 'A5': '乘法換算',
           'MA06': '倒數效率', 'MA05': '單目標限制'}
LABELS = [('gap_fixed', '玩法與補足'), ('rule_capability', '高級規則能力'),
          ('source_values_review', '來源原值（供比較，未採用）'), ('numeric_unit_proposal', '提案每份'),
          ('scaling_review', '提案如何疊加'), ('trigger_threshold_cooldown_limits', '觸發、冷卻與門檻'),
          ('example_review', '提案例子'), ('mixed_split', '規則與數值如何拆'),
          ('balance_risk', '風險'), ('principle_conflict', '原則與待裁示'),
          ('review_gate', '過目狀態')]

def clean(value):
    if isinstance(value, dict):
        return {k: clean(v) for k, v in value.items() if k not in ('file', 'installed_file', 'offset')}
    if isinstance(value, list):
        return [clean(v) for v in value]
    return value

def display(value):
    if isinstance(value, dict):
        return '；'.join(f'{k}: {display(v)}' for k, v in value.items() if v)
    if isinstance(value, list):
        return '、'.join(display(v) for v in value)
    return str(value or '未列；待確認')

def readable(value):
    text = display(value)
    replacements = {
        '沿record_evidence條件': '依上述玩法條件', '全局runtime cap': '額外總量上限',
        '星盤runtime數值cap': '星盤數值總量上限', '既定runtime cap': '既定總量上限',
        '不進atoms/family-rules/候選實作': '確認前不採用', '不增加常駐DMG atom': '不增加常駐傷害',
        '基本atoms': '基本效果單位', '新atom定案': '新效果單位定案', '非已定atom': '非既定效果單位',
        '數值atom': '數值單位', 'DMG_1H': '單手武器傷害', '基礎DMG百分比': '基礎傷害百分比',
        'trigger/閾值/CD/關係條件': '觸發／門檻／冷卻／關係條件', 'marker': '標記',
        'caster': '施加者', 'perk': '天賦', 'PERK': '天賦', 'runtime cap': '總量上限',
        'per_share': '每份數值', 'tether': '連結', 'owner': '主人',
        '原HasMagicEffect本身只認標記不分施法者': '來源的標記本身不分施加者',
        '先驗引擎AV讀值及耗耐時點': '先驗耐力讀值及消耗時點',
        '依據真script屬性判風險，未宣稱已完整解碼PEX': '腳本行為仍需驗證',
        '需證明ModSpellCost在staff充能路徑的實際效果，不可憑名字假定': '需驗證法杖充能的實際效果',
        '原天賦 Effects為0，不能因此判無效果；下游SPEL/MGEF以HasPerk判斷。不能只AddPerk後認為全mod防護都可共享': '來源依其他效果判斷，不能假定加入能力後所有防護都可共享',
        '及GetShouldAttack篩選，來源各MGEF條件略有差異需逐項保留': '及敵我篩選，來源條件略有差異需逐項保留',
        '；來源Proc 天賦×1.2': '', '；來源ModSpellMagnitude×−0.75': '',
        '；原SPERG四個ModSpellCost乘數0.4/0.8/0/0.5，由Global/IsInList/GetIsObjectType分流': '',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=Path, help='private installed-perks research directory')
    args = parser.parse_args()
    rows, hashes = [], {}
    for filename in ('advanced-units.json', 'high-units.json'):
        path = args.source / filename
        hashes[filename] = hashlib.sha256(path.read_bytes()).hexdigest()
        for item in load(str(path)).rows:
            row = {k: clean(item.get(k, '')) for k in FIELDS}
            detail = item.get('source_detail', {})
            row['source_values_review'] = item.get('source_values_review', '')
            row['scaling_review'] = item.get('scaling_review') or item.get('scaling', '')
            row['example_review'] = item.get('example_review') or item.get('example', '')
            row['gameplay'] = detail.get('gameplay', '')
            row['record_evidence'] = detail.get('record_evidence', '')
            row['dependency_chain'] = detail.get('dependency_chain', '')
            row['special_review'] = SPECIAL.get(row['id'], '')
            rows.append(row)
    data = {'contract': 'wf-table/1', 'source': '../2026-11-03-perk-units.md',
            'extracted': '2026-11-03', 'columns': list(rows[0]), 'link_columns': [],
            'source_sha256': hashes, 'rows': rows}
    (HERE / 'review-data.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    cards = []
    esc = lambda x: html.escape(display(x))
    for row in rows:
        fields = []
        seen = {}
        for key, label in LABELS:
            value = row[key]
            if key == 'numeric_unit_proposal' and row['tier'] == '高級' and not value:
                value = '不適用：純規則解鎖，混合數值另審'
            if not value:
                continue
            text = readable(value)
            if key in ('numeric_unit_proposal', 'scaling_review', 'example_review') and text in seen:
                text = f'同「{seen[text]}」'
            else:
                seen[text] = label
            fields.append(f'<dt>{esc(label)}</dt><dd>{esc(text)}</dd>')
        fields = ''.join(fields)
        detail = ''.join(f'<dt>{esc(label)}</dt><dd>{esc(row[key])}</dd>' for key, label in [
            ('source_formkey', 'FormKey'), ('source_version', '來源版本'), ('current_winner_status', '目前勝出'),
            ('source_original_values', '來源原始記錄'), ('record_evidence', '記錄證據'), ('dependency_chain', '來源依賴鏈'),
            ('implementation_dependencies', '移植依賴'), ('validation', '驗證')])
        badge = f'<strong class="special">另裁示：{esc(row["special_review"])}</strong>' if row['special_review'] else ''
        cards.append(f'<article data-tier="{esc(row["tier"])}" data-special="{bool(row["special_review"])!s}">'
                     f'<h2>{esc(row["id"])} · {esc(row["name"])}</h2><p>{esc(row["tier"])} · 待過目 {badge}</p>'
                     f'<p>{esc(row["gameplay"])}</p><dl>{fields}</dl><details><summary>來源與移植細節</summary><dl>{detail}</dl></details></article>')
    body = '\n'.join(cards)
    hash_text = html.escape('；'.join(f'{k}: {v}' for k, v in hashes.items()))
    page = '''<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>星盤效果單位｜候選過目</title><style>body{font:16px/1.65 system-ui,sans-serif;max-width:1050px;margin:auto;padding:1.5rem;color:#202934;background:#f5f4ef}h1{line-height:1.2}article{min-width:0;overflow-wrap:anywhere;background:white;border:1px solid #d8dedb;border-radius:12px;padding:1.2rem;margin:1rem 0}h2{font-size:1.25rem;margin:.2rem 0}dl{display:grid;grid-template-columns:minmax(0,12rem) minmax(0,1fr);gap:.35rem 1rem}dt{font-weight:700}dd{min-width:0;overflow-wrap:anywhere;margin:0;white-space:pre-wrap}details{min-width:0;overflow-wrap:anywhere}.special{color:#973c17}select{font:inherit;padding:.35rem}details{border-top:1px solid #ddd;padding-top:.7rem}footer{overflow-wrap:anywhere;font-size:.85rem}@media(max-width:650px){dl{display:block}dd{margin:0 0 .8rem}body{padding:.8rem}}</style>
<h1>星盤效果單位：候選過目</h1><p>全部是未採用的研究提案。進階數值須經你確認；高級能力也尚未選。來源原值與提案分開列出，例子不代表一定能實際取得該配點。</p><p>混合效果的規則能力與數值分開審閱；另裁示標記指出需要額外決定的原則差異。資料涵蓋已安裝但未勝出的樹。</p>
<label>篩選類型 <select id="tier"><option value="">全部</option><option>進階</option><option>高級</option></select></label>　<label>裁示狀態 <select id="status"><option value="">全部待過目</option><option value="special">需另裁示</option><option value="other">其他待過目</option></select></label><p id="count"></p>
''' + body + '''<footer><p>來源表 SHA-256：''' + hash_text + '''</p><p>由本目錄 render.py 從 private installed-perks 研究表重產；完整研究與證據見入口頁。</p></footer><script>function filter(){let t=document.querySelector('#tier').value,s=document.querySelector('#status').value,n=0;document.querySelectorAll('article').forEach(c=>{let show=(!t||c.dataset.tier===t)&&(!s||(s==='special')===(c.dataset.special==='True'));c.hidden=!show;if(show)n++});document.querySelector('#count').textContent='顯示 '+n+' 項'}document.querySelectorAll('select').forEach(e=>e.addEventListener('change',filter));filter()</script></html>'''
    (HERE / 'index.html').write_text(page)

if __name__ == '__main__':
    main()
