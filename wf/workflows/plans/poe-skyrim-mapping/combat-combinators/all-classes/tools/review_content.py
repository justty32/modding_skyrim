"""Build class navigation, subtype cards and rule sections from published rows."""
import os

from review_fields import text, val, effective, badges
from review_page import fragment

LEGACY_SUBTYPES = {'C': 'C3', 'D': 'D1', 'G': 'G1'}


def definition_list(fields):
    return '<dl>' + ''.join(
        '<dt>' + text(key) + '</dt><dd>' + text(value) + '</dd>'
        for key, value in fields
    ) + '</dl>'


def render_rule(rule, islegacy):
    high = rule['tier'] == 'high'
    if high:
        before = str(val(rule, 'high_before', 'before_play'))
        after = str(val(rule, 'high_after', 'after_play'))
        front = [
            ('選前 → 選後', before + ' → ' + after),
            ('得到', val(rule, 'high_gain', 'gain')),
            ('付出', val(rule, 'high_cost', 'loss')),
        ]
    else:
        front = [
            ('怎麼觸發', rule.get('trigger_condition')),
            ('得到什麼', rule.get('effect_formula')),
            ('成本與取捨', rule.get('cost_timing')),
        ]
    front += [
        ('正向情境', val(rule, 'positive_example', 'after_play')),
        ('無效／負向情境', val(rule, 'negative_example', 'loss')),
    ]
    technical = [
        ('來源與對象', str(rule.get('actor_source', rule.get('scope', '')))
         + '；' + str(rule.get('target_selector', '詳原actor/target條件'))),
        ('狀態／刷新消耗', str(rule.get('state_owner', '詳lifecycle'))
         + '；' + str(rule.get('state_refresh_consume', ''))),
        ('效果契約', rule.get('effect_formula')),
        ('清理與失效', str(rule.get('lifecycle', ''))
         + '；' + str(rule.get('invalid_cases', ''))),
        ('混買／共享', rule.get('compatibility')),
        ('未證能力', rule.get('capability', '依本職feasibility，所有新能力未ready')),
        ('為何不能只改數值', val(rule, 'high_not_numeric', 'mechanic_reason')
         if high else rule.get('mechanic_reason')),
        ('資料身分', '原樣板精確reference；不改payload' if islegacy
         else '新設計候選；所有新強度／成本／期限待過目'),
    ]
    return fragment(
        'rule', tier='high' if high else 'advanced',
        rule_id=text(rule['rule_id']), name=text(rule.get('name')),
        heading='高階 · 改變打法' if high else '進階 · 條件與收益',
        front=definition_list(front), technical=definition_list(technical),
    )


def render_content(data_root, repo, out, geometry_root, load):
    def link(path):
        return os.path.relpath(path, out.parent)

    roster_path = repo / 'wf/workflows/plans/poe-skyrim-mapping/combat-combinators/roster.json'
    roster = load(str(roster_path)).rows
    lookup = {row['id']: row for row in roster}
    classes = {row['id'][0]: row['class'] for row in roster}
    parts = []
    intro = []
    for class_id in 'VGDRCMSX':
        subtypes = [class_id + str(i) for i in (1, 2, 3)]
        intro.append('<div class="family"><h2>' + text(classes[class_id])
                     + '</h2><div class="cards">')
        for subtype in subtypes:
            row = lookup[subtype]
            intro.append(fragment('card', sub=subtype, name=text(row['name']),
                                  fantasy=text(row['fantasy']), loop=text(row['loop'])))
        intro.append('</div></div>')
        folder = data_root / class_id
        rows = load(str(folder / 'rules.json')).rows
        rules = [(effective(row, repo, load), row.get('row_kind') == 'legacy_reference')
                 for row in rows]
        parts.append(fragment(
            'class', class_id=class_id, name=text(classes[class_id]),
            report=link(folder / 'REPORT.md'), rules=link(folder / 'rules.json'),
            feasibility=link(folder / 'feasibility.json'),
        ))
        if geometry_root and (geometry_root / f'region-{class_id}.svg').exists():
            parts.append(fragment('geometry', name=text(classes[class_id]),
                                  image=link(geometry_root / f'region-{class_id}.svg')))
        for subtype in [None] + subtypes:
            title = ('職業通用 · 共用一池4進階／2高階' if subtype is None
                     else lookup[subtype]['name'] + ' · 6進階／2高階')
            parts.append('<h3 id="' + (subtype or class_id + 'common')
                         + '">' + text(title) + '</h3>')
            if subtype:
                parts.append(badges(subtype) + '<p>' + text(lookup[subtype]['loop']) + '</p>')
            for rule, islegacy in rules:
                owner = (None if rule.get('scope') == 'class_common'
                         else LEGACY_SUBTYPES.get(class_id) if islegacy
                         else rule.get('owner_subtype'))
                if owner == subtype:
                    parts.append(render_rule(rule, islegacy))
        parts.append('</details>')
    nav = ''.join('<a href="#' + class_id + '">' + text(classes[class_id]) + '</a>'
                  for class_id in 'VGDRCMSX')
    return nav, ''.join(intro), ''.join(parts)
