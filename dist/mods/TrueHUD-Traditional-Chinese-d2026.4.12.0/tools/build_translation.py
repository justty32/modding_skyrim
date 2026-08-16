#!/usr/bin/env python3
"""Build TrueHUD's ENGLISH-named Traditional Chinese override from its exact source."""

from __future__ import annotations

import argparse
import codecs
import hashlib
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "Interface" / "Translations" / "TrueHUD_english.txt"
SOURCE_SHA256 = "01d296193388d2c22662e407349940ce99efd69be201730a6b61ac6af2dc936a"

# This ordered glossary is the reviewable translation source.  Replacements operate
# only on visible text, never on XML tags or colour values.  Long phrases precede
# their component terms to retain natural, consistent MCM wording.
GLOSSARY = (
    ("Not taken", "未佔用"), ("Taken", "已佔用"),
    ("On combat start", "戰鬥開始時"), ("On hit", "受擊時"),
    ("When changed from default", "數值變動時"), ("When another displayed", "顯示其他元件時"),
    ("Hostiles and teammates", "敵對角色與隊友"), ("Target only", "僅目標"),
    ("Enemy & Team", "敵人與隊友"), ("Top, Replace Compass", "畫面上方，取代羅盤"),
    ("Bottom of the Screen", "畫面底部"), ("Vanilla Style", "原版樣式"),
    ("Square difficulty icon", "方形難度圖示"), ("Soul icon", "靈魂圖示"),
    ("Level text", "等級文字"), ("Move subtitles", "移動字幕"),
    ("Hide compass", "隱藏羅盤"), ("Force hide vanilla bars", "強制隱藏原版條"),
    ("Hide vanilla bars", "隱藏原版條"), ("Hide Vanilla Message", "隱藏原版訊息"),
    ("Hide Vanilla Target Bar", "隱藏原版目標條"), ("Hide In Inventory Menus", "在物品欄選單中隱藏"),
    ("Hide In Crafting Menus", "在製作選單中隱藏"), ("Combine Widget", "合併 HUD 元件"),
    ("Combined", "合併"), ("Special Bars Control", "特殊條控制"),
    ("General Settings", "一般設定"), ("Display Criteria", "顯示條件"),
    ("Alignment Settings", "對齊設定"), ("Miscellaneous Settings", "其他設定"),
    ("Display Settings", "顯示設定"), ("Recent Loot Settings", "近期戰利品設定"),
    ("Health Bar Colors", "生命條顏色"), ("Magicka Bar Colors", "魔力條顏色"),
    ("Stamina Bar Colors", "耐力條顏色"), ("Special Bar Colors", "特殊條顏色"),
    ("Miscellaneous Colors", "其他顏色"), ("Color Bar Outline by Difficulty", "依難度變更條外框顏色"),
    ("Default Color (Outline)", "預設顏色（外框）"), ("Weaker Color (Outline)", "較弱顏色（外框）"),
    ("Stronger Color (Outline)", "較強顏色（外框）"), ("Teammate Color (Outline)", "隊友顏色（外框）"),
    ("Default Color", "預設顏色"), ("Weaker Color", "較弱顏色"),
    ("Stronger Color", "較強顏色"), ("Teammate Color", "隊友顏色"),
    ("Phantom Bars Duration", "殘影條持續時間"), ("Damage Counter Duration", "傷害計數器持續時間"),
    ("Damage Counter Alignment", "傷害計數器對齊"), ("Resource Bars Alignment", "資源條對齊"),
    ("Name Alignment", "名稱對齊"), ("Bar Fill Direction", "條填滿方向"),
    ("Loot Message Stack Direction", "戰利品訊息堆疊方向"), ("Multiple Bars Stack Direction", "多條堆疊方向"),
    ("Multiple Bars Offset", "多條間距"), ("Maximum Bar Width", "最大條寬度"),
    ("Minimum Bar Width", "最小條寬度"), ("Max Boss Bars", "首領條最大數量"),
    ("Max Loot Message Count", "戰利品訊息最大數量"), ("Loot Message Duration", "戰利品訊息持續時間"),
    ("Display Enchantment Charge Meter", "顯示附魔充能計量條"),
    ("Enchantment Meter Anchor", "附魔計量條錨點"), ("Player Widget Anchor", "玩家 HUD 元件錨點"),
    ("Recent Loot Anchor", "近期戰利品錨點"), ("Health Bar Anchor", "生命條錨點"),
    ("Magicka Bar Anchor", "魔力條錨點"), ("Stamina Bar Anchor", "耐力條錨點"),
    ("Boss Bar Anchor", "首領條錨點"), ("Info Bar Anchor", "資訊條錨點"),
    ("Health Bar Fill Direction", "生命條填滿方向"), ("Magicka Bar Fill Direction", "魔力條填滿方向"),
    ("Stamina Bar Fill Direction", "耐力條填滿方向"),
    ("Health Bar Scale Mult", "生命條縮放倍率"), ("Magicka Bar Scale Mult", "魔力條縮放倍率"),
    ("Stamina Bar Scale Mult", "耐力條縮放倍率"),
    ("Health Bar Background Color", "生命條背景顏色"), ("Magicka Bar Background Color", "魔力條背景顏色"),
    ("Stamina Bar Background Color", "耐力條背景顏色"), ("Special Bar Background Color", "特殊條背景顏色"),
    ("Health Bar Phantom Color", "生命條殘影顏色"), ("Magicka Bar Phantom Color", "魔力條殘影顏色"),
    ("Stamina Bar Phantom Color", "耐力條殘影顏色"), ("Special Bar Phantom Color", "特殊條殘影顏色"),
    ("Health Bar Penalty Color", "生命條懲罰顏色"), ("Magicka Bar Penalty Color", "魔力條懲罰顏色"),
    ("Stamina Bar Penalty Color", "耐力條懲罰顏色"), ("Special Bar Penalty Color", "特殊條懲罰顏色"),
    ("Health Bar Flash Color", "生命條閃爍顏色"), ("Magicka Bar Flash Color", "魔力條閃爍顏色"),
    ("Stamina Bar Flash Color", "耐力條閃爍顏色"), ("Special Bar Flash Color", "特殊條閃爍顏色"),
    ("Health Bar Color", "生命條顏色"), ("Magicka Bar Color", "魔力條顏色"),
    ("Stamina Bar Color", "耐力條顏色"), ("Special Bar Color", "特殊條顏色"),
    ("Health Bar Width", "生命條寬度"), ("Special Bar Width", "特殊條寬度"),
    ("Player Widget Uses HUD Opacity", "玩家 HUD 元件使用 HUD 不透明度"),
    ("Boss Bar Uses HUD Opacity", "首領條使用 HUD 不透明度"),
    ("Info Bar Uses HUD Opacity", "資訊條使用 HUD 不透明度"),
    ("Recent Loot Uses HUD Opacity", "近期戰利品使用 HUD 不透明度"),
    ("Player Widget Opacity", "玩家 HUD 元件不透明度"), ("Boss Bar Opacity", "首領條不透明度"),
    ("Info Bar Opacity", "資訊條不透明度"), ("Recent Loot Opacity", "近期戰利品不透明度"),
    ("Player Widget Scale", "玩家 HUD 元件縮放"), ("Boss Bar Scale", "首領條縮放"),
    ("Info Bar Scale", "資訊條縮放"), ("Recent Loot Scale", "近期戰利品縮放"),
    ("Display Phantom Bar for Special Bar", "顯示特殊條殘影條"),
    ("Display Special Bar", "顯示特殊條"), ("Display Phantom Bars", "顯示殘影條"),
    ("Display Damage Counter", "顯示傷害計數器"), ("Display Indicator", "顯示指示器"),
    ("Display Resources", "顯示資源"), ("Display Health", "顯示生命"),
    ("Display Magicka", "顯示魔力"), ("Display Stamina", "顯示耐力"),
    ("Display Mount Stamina", "顯示坐騎耐力"), ("Display Shout Indicator", "顯示龍吼指示器"),
    ("Display Name", "顯示名稱"), ("Display for Hostiles", "為敵對角色顯示"),
    ("Display for Teammates", "為隊友顯示"), ("Display for Others", "為其他角色顯示"),
    ("Enable Actor Info Bars", "啟用角色資訊條"), ("Enable Boss Bars", "啟用首領條"),
    ("Enable Player Widget", "啟用玩家 HUD 元件"), ("Enable Recent Loot Widget", "啟用近期戰利品 HUD 元件"),
    ("Display Shout Widget With Compass Hidden", "羅盤隱藏時顯示龍吼 HUD 元件"),
    ("Scale With Distance", "依距離縮放"), ("Scale Bars", "縮放條"),
    ("Indicator Mode", "指示器模式"), ("Modify HUD", "修改 HUD"),
    ("Bar Width", "條寬度"), ("Opacity", "不透明度"), ("Presets", "預設"),
    ("Special Bar", "特殊條"), ("Boss Bars", "首領條"), ("Actor Info Bars", "角色資訊條"),
    ("Player Widget", "玩家 HUD 元件"), ("Recent Loot", "近期戰利品"),
    ("Colors", "顏色"), ("General", "一般"), ("Normal", "正常"), ("Center", "置中"),
    ("Reverse", "反向"), ("Never", "永不"), ("Always", "總是"), ("Dynamic", "動態"),
    ("Combat", "戰鬥"), ("In combat", "戰鬥中"), ("Together", "一起"),
    ("Hostiles", "敵對角色"), ("Everyone", "所有人"), ("Enemy", "敵人"),
    ("Left", "左"), ("Right", "右"), ("Up", "上"), ("Down", "下"),
    ("Torso", "軀幹"), ("Head", "頭部"), ("Load", "載入"), ("No", "否"),
    ("TrueHUD", "TrueHUD"), ("HUD", "HUD"),
)

# Fallback vocabulary for the repeated sentence templates.  It is intentionally
# word-boundary based so a source key, XML tag, colour code, or numeric token can
# never be changed as a side effect.
WORDS = {
    "Changed": "已變更", "Enable": "啟用", "Select": "選擇", "Set": "設定", "Load": "載入",
    "The": "", "the": "", "a": "", "an": "", "of": "", "for": "供", "to": "以",
    "in": "於", "on": "在", "at": "於", "with": "並", "and": "與", "or": "或",
    "if": "若", "when": "時", "while": "時", "from": "自", "by": "依", "as": "作為",
    "is": "為", "are": "", "will": "", "be": "", "been": "", "being": "", "that": "",
    "which": "", "where": "其中", "their": "其", "them": "其", "they": "其", "them": "其",
    "actor": "角色", "actors": "角色", "player": "玩家", "character": "角色", "target": "目標",
    "boss": "首領", "bars": "條", "bar": "條", "info": "資訊", "Info": "資訊",
    "resource": "資源", "resources": "資源", "health": "生命", "magicka": "魔力", "stamina": "耐力",
    "special": "特殊", "widget": "HUD 元件", "widgets": "HUD 元件", "vanilla": "原版",
    "displaying": "顯示", "displayed": "顯示", "display": "顯示", "show": "顯示", "shown": "顯示",
    "hide": "隱藏", "hidden": "隱藏", "change": "變更", "replace": "取代", "replaced": "取代",
    "scale": "縮放", "scaled": "縮放", "width": "寬度", "color": "顏色", "Color": "顏色",
    "outline": "外框", "difficulty": "難度", "level": "等級", "indicator": "指示器",
    "counter": "計數器", "damage": "傷害", "name": "名稱", "names": "名稱", "alignment": "對齊",
    "criteria": "條件", "mode": "模式", "direction": "方向", "stack": "堆疊", "fill": "填滿",
    "duration": "持續時間", "seconds": "秒", "second": "秒", "recent": "近期", "loot": "戰利品",
    "message": "訊息", "messages": "訊息", "maximum": "最大", "minimum": "最小", "max": "最大",
    "amount": "數量", "count": "數量", "same": "相同", "time": "時間", "screen": "畫面",
    "top": "上方", "bottom": "底部", "left": "左", "right": "右", "edge": "邊緣", "axis": "軸",
    "position": "位置", "anchor": "錨點", "offset": "偏移", "point": "點", "base": "基本",
    "entire": "整個", "elements": "元素", "element": "元素", "floating": "浮動", "single": "單一",
    "mount": "坐騎", "mounted": "騎乘時", "instead": "改為", "cooldown": "冷卻", "shout": "龍吼",
    "enchantment": "附魔", "charge": "充能", "meter": "計量條", "camera": "鏡頭", "distance": "距離",
    "slightly": "略微", "below": "下方", "above": "上方", "beneath": "下方", "progress": "進度",
    "lazy": "殘影", "representing": "表示", "last": "上次", "taken": "受到", "reset": "重設",
    "considered": "視為", "stronger": "較強", "weaker": "較弱", "allowed": "允許", "once": "一次",
    "modify": "修改", "way": "方式", "small": "小型", "next": "旁", "temporarily": "暫時",
    "replacing": "取代", "offsetting": "上移", "subtitles": "字幕", "upwards": "向上",
    "new": "新", "ones": "項目", "locations": "位置", "also": "也", "added": "加入",
    "visible": "可見", "combined": "合併", "separated": "分離", "after": "後", "rescaling": "重新縮放",
    "reached": "達到", "other": "其他", "proportionally": "按比例", "additional": "額外",
    "multiplier": "倍率", "force": "強制", "still": "仍", "there": "存在", "even": "即使",
    "checking": "勾選", "above": "上方", "option": "選項", "each": "每個", "frame": "畫面更新",
    "meters": "計量條", "controlled": "控制", "any": "任何", "not": "未", "disabled": "停用",
    "enabled": "啟用", "Check": "請查看", "mod": "模組", "description": "說明", "more": "更多",
    "Survival": "生存", "survival": "生存", "background": "背景", "phantom": "殘影", "penalty": "懲罰",
    "flash": "閃爍", "default": "預設", "text": "文字", "icon": "圖示", "teammate": "隊友",
    "current": "目前", "only": "僅", "up": "出現", "using": "使用", "feature": "功能",
    "plugin": "外掛", "body": "身體", "part": "部位", "should": "應", "attached": "附著",
    "tweak": "微調", "uses": "使用", "inherit": "繼承", "setting": "設定", "settings": "設定",
    "normal": "正常", "every": "所有", "together": "一起", "combat": "戰鬥", "never": "永不",
    "always": "總是", "dynamic": "動態", "no": "否", "up": "上", "down": "下",
    "hostiles": "敵對角色", "teammates": "隊友", "others": "其他角色", "everyone": "所有人",
    "Target": "目標", "Teammates": "隊友", "Others": "其他角色", "soul": "靈魂",
    "another": "另一個", "based": "依據", "difference": "差異", "relative": "相對於",
    "Difficulty": "難度", "Threshold": "門檻", "since": "自", "before": "前",
    "Bar": "條", "Boss": "首領", "Health": "生命", "Magicka": "魔力", "Stamina": "耐力",
    "Offset": "偏移", "Resources": "資源", "Width": "寬度", "Base": "基本", "Tweak": "微調",
    "preset": "預設", "compass": "羅盤", "A": "一個", "empty": "空白", "space": "空間",
    "between": "之間", "two": "兩個", "placed": "放置", "This": "這將", "one": "一個",
    "combine": "合併", "into": "為", "When": "當", "item": "物品", "log": "紀錄",
    "inventory": "物品欄", "crafting": "製作", "menus": "選單", "Barter": "交易", "Container": "容器",
    "Gift": "贈禮", "By": "依", "Soul": "靈魂", "Level": "等級",
}


def translate_visible(text: str) -> str:
    for english, chinese in GLOSSARY:
        text = text.replace(english, chinese)
    # Remaining complete sentences are deliberately expressed as templates; this
    # handles source punctuation without ever altering structural tags/tokens.
    replacements = {
        "Enable the actor info bar module, displaying info bars above actors.": "啟用角色資訊條模組，在角色上方顯示資訊條。",
        "Enable the boss bar module, displaying boss bars for certain actors.": "啟用首領條模組，為特定角色顯示首領條。",
        "Enable the player widget module, displaying bars for the player's health, magicka and stamina as well as an optional shout cooldown indicator.": "啟用玩家 HUD 元件模組，顯示玩家的生命、魔力與耐力條，以及可選的龍吼冷卻指示器。",
        "Enable the recent loot module, displaying messages for a short while for each item you acquire.": "啟用近期戰利品模組，短暫顯示每件取得物品的訊息。",
        "The special bars are controlled by another plugin. The feature is enabled.": "特殊條由其他外掛控制；此功能已啟用。",
        "The special bars are not controlled by any plugin. The feature is disabled. (Check mod description for more info)": "特殊條未由任何外掛控制；此功能已停用。（詳情請見模組說明）",
        "Enable to display \"lazy\" bars (representing recent change) beneath progress bars.": "啟用以在進度條下方顯示「殘影」條（表示最近變動）。",
        "Enable to display a \"lazy\" bar (representing recent change) beneath the special bar.": "啟用以在特殊條下方顯示「殘影」條（表示最近變動）。",
        "Enable to have the widget inherit the vanilla HUD opacity setting.": "啟用以讓 HUD 元件繼承原版 HUD 不透明度設定。",
        "The direction in which the bar will fill up.": "條填滿的方向。",
        "The duration in seconds that the phantom bars will lag behind the progress bars.": "殘影條落後進度條的持續秒數。",
        "Opacity of the widget.": "HUD 元件的不透明度。",
    }
    text = replacements.get(text, text)
    for english, chinese in WORDS.items():
        text = re.sub(rf"\b{re.escape(english)}\b", chinese, text)
    text = text.replace("'s", "的").replace("'", "")
    text = re.sub(r" {2,}", "", text).replace(".", "。").replace(",", "，")
    text = text.replace("選擇條件供顯示", "選擇顯示").replace("供敵對角色", "給敵對角色")
    text = text.replace("供隊友", "給隊友").replace("供其他角色", "給其他角色")
    text = text.replace("供目標", "給目標")
    return text


def translate(value: str) -> str:
    parts = re.split(r"(<[^>]+>)", value)
    return "".join(part if part.startswith("<") else translate_visible(part) for part in parts)


def read_source(path: Path) -> tuple[bytes, list[str]]:
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != SOURCE_SHA256:
        raise SystemExit("source SHA-256 is not the active TrueHUD d2026.4.12.0 file")
    if not data.startswith(codecs.BOM_UTF16_LE):
        raise SystemExit("source lacks UTF-16 LE BOM")
    text = data[2:].decode("utf-16-le")
    if "\n" in text.replace("\r\n", "") or "\r" in text.replace("\r\n", ""):
        raise SystemExit("source must use CRLF line terminators")
    return data, text.split("\r\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True, help="active TrueHUD_english.txt")
    args = parser.parse_args()
    _, lines = read_source(args.source)
    output: list[str] = []
    for number, line in enumerate(lines, 1):
        if not line:
            output.append(line)
            continue
        if line.count("\t") != 1:
            raise SystemExit(f"source line {number}: expected exactly one tab")
        key, value = line.split("\t")
        translated = translate(value)
        if re.search(r"[A-Za-z]", re.sub(r"<[^>]+>|TrueHUD|HUD|[XYZ]", "", translated)):
            raise SystemExit(f"line {number}: untranslated visible English: {translated!r}")
        output.append(f"{key}\t{translated}")
    payload = codecs.BOM_UTF16_LE + "\r\n".join(output).encode("utf-16-le")
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_bytes(payload)
    print(f"wrote {TARGET.relative_to(ROOT)} ({len(output)} lines, sha256={hashlib.sha256(payload).hexdigest()})")


if __name__ == "__main__":
    main()
