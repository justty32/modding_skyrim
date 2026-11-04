"""Inline templates and assets into the single-file offline review page.

Asset newlines are source formatting only; original output has no such newlines.
Substitution happens once so inserted user text is never interpreted as a token.
"""
from pathlib import Path
import re

ASSETS = Path(__file__).with_name('assets')


def asset(name):
    return (ASSETS / name).read_text().replace('\n', '')


def fragment(template_name, **fields):
    return re.sub(r'\{\{([a-z_]+)\}\}',
                  lambda match: fields[match.group(1)], asset(template_name + '.html'))


def render_page(nav, intro, parts, semantics_pass=False, geometry_verified=False):
    page = fragment('review', nav=nav, intro=intro, parts=parts,
                    css=asset('review.css'), js=asset('review.js'))

    semantics_pending = '設計首版已齊，獨立語義修稿中。'
    semantics_verified = '24型與通用池獨立語義審核已通過；新數值仍待使用者過目。'
    geometry_pending = '幾何由獨立owner掛點，完成前不宣稱真圖全部核收；原55候選/保護不動。'
    geometry_ready = (
        '240 slots與較強AND前置、24 closure與8 common入口已核；'
        '圖像為真圖subset，原55／保護不動。'
    )
    page = page.replace(semantics_pending,
                        semantics_verified if semantics_pass else semantics_pending)
    page = page.replace(geometry_pending,
                        geometry_ready if geometry_verified else geometry_pending)
    return page
