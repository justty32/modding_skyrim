#!/usr/bin/env python3
"""Build the review TSV from the exact 1.5/1.4.5 English and CHS sources.

This is a provenance tool, not part of normal package deployment.  The normal
build consumes only translation-source.tsv and the exact official 1.5 ESP.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import csv
from dataclasses import dataclass
from pathlib import Path
import struct

from opencc import OpenCC

from plugin_localizer import (
    form_key,
    iter_records,
    normalized_header,
    parse_subrecords,
    record_editor_id,
    sha256,
    tes4_masters,
    tokens,
    uncompressed_body,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "tools" / "translation-source.tsv"
PLUGIN = "Thaumaturgy.esp"
EXPECTED = {
    "source15": "3d1a1e2d2cf0d9b79b14574ff6e6b08cd2f4f188f6178f71c3f9b0b590a17e08",
    "source145": "fcb239d8bee484364267564ca4003ca6445264a11f9dd5fffe9f957e748eb741",
    "chs145": "8f6ebb5a6d5d69c74465fd6c8399e17c41666dd0c9f8bcfe49c45c4ac2d745a3",
}
FIELDS = {
    ("MGEF", "FULL"), ("MGEF", "DNAM"),
    ("ENCH", "FULL"),
    ("ARMO", "FULL"),
    ("WEAP", "FULL"),
    ("PERK", "FULL"), ("PERK", "DESC"),
    ("SPEL", "FULL"), ("SPEL", "DESC"),
    ("CELL", "FULL"),
}
GLOSSARY_ORDER = (
    "Adamant-Traditional-Chinese-6.0.2",
    "Apothecary-Traditional-Chinese-1.3.9",
    "Mysticism-Traditional-Chinese-2.5.0",
    "USSEP-Perks-Traditional-Chinese-4.3.8a",
    "CT77-Remodeled-Armor-SE-Traditional-Chinese-2.8.1-No-Physics-Vanilla-Replacer",
)


@dataclass(frozen=True)
class TextRow:
    form_key: str
    record_type: str
    editor_id: str
    field: str
    occurrence: int
    value: str

    @property
    def key(self) -> tuple[str, str, str, int]:
        return self.form_key, self.record_type, self.field, self.occurrence


def decode_text(payload: bytes, encoding: str) -> str:
    raw = payload[:-1] if payload.endswith(b"\0") else payload
    if b"\0" in raw:
        raise AssertionError("localized text contains an embedded NUL")
    return raw.decode(encoding)


def extract(path: Path, encoding: str) -> list[TextRow]:
    data = path.read_bytes()
    masters = tes4_masters(data)
    result: list[TextRow] = []
    for record in iter_records(data):
        signature = record.signature.decode("ascii")
        body = uncompressed_body(record.header, record.body)
        editor_id = record_editor_id(body)
        occurrences: dict[str, int] = defaultdict(int)
        for subrecord in parse_subrecords(body):
            field = subrecord.tag.decode("ascii")
            occurrence = occurrences[field]
            occurrences[field] += 1
            if (signature, field) not in FIELDS:
                continue
            result.append(TextRow(
                form_key(record.raw_form_id, masters, PLUGIN), signature,
                editor_id, field, occurrence,
                decode_text(subrecord.payload, encoding),
            ))
    return result


def record_map(path: Path) -> dict[tuple[str, str], object]:
    data = path.read_bytes()
    masters = tes4_masters(data)
    result = {}
    for record in iter_records(data):
        key = (
            record.signature.decode("ascii"),
            form_key(record.raw_form_id, masters, PLUGIN),
        )
        if key in result:
            raise AssertionError(f"duplicate record key: {key}")
        result[key] = record
    return result


def verify_seed_topology(source: Path, translated: Path) -> None:
    left = record_map(source)
    right = record_map(translated)
    if set(left) != set(right):
        raise AssertionError("1.4.5 English/CHS record keys differ")
    for key in left:
        a, b = left[key], right[key]
        if a.path != b.path or normalized_header(a.header) != normalized_header(b.header):
            raise AssertionError(f"1.4.5 record header/path differs: {key}")
        a_body = uncompressed_body(a.header, a.body)
        b_body = uncompressed_body(b.header, b.body)
        a_subs = parse_subrecords(a_body)
        b_subs = parse_subrecords(b_body)
        if [item.tag for item in a_subs] != [item.tag for item in b_subs]:
            raise AssertionError(f"1.4.5 subrecord topology differs: {key}")
        for a_sub, b_sub in zip(a_subs, b_subs):
            field = a_sub.tag.decode("ascii")
            if (key[0], field) not in FIELDS and a_sub.payload != b_sub.payload:
                raise AssertionError(f"1.4.5 non-text payload differs: {key} {field}")


def read_string_table(path: Path) -> dict[int, str]:
    data = path.read_bytes()
    count, data_size = struct.unpack_from("<II", data)
    data_start = 8 + count * 8
    if data_start + data_size != len(data):
        raise AssertionError(f"bad STRINGS size: {path}")
    result: dict[int, str] = {}
    for index in range(count):
        string_id, offset = struct.unpack_from("<II", data, 8 + index * 8)
        position = data_start + offset
        end = data.index(b"\0", position)
        result[string_id] = data[position:end].decode("utf-8")
    return result


def base_traditional_map(
    desired: set[tuple[str, str, str, int]], masters_dir: Path, strings_dir: Path,
) -> dict[tuple[str, str, str, int], str]:
    """Resolve exact Skyrim 8.20 FULL names for records owned by vanilla masters."""
    result: dict[tuple[str, str, str, int], str] = {}
    for owner in ("Skyrim.esm", "Update.esm", "Dawnguard.esm", "Dragonborn.esm"):
        table = read_string_table(strings_dir / f"{Path(owner).stem}_English.STRINGS")
        path = masters_dir / owner
        data = path.read_bytes()
        masters = tes4_masters(data)
        for record in iter_records(data):
            signature = record.signature.decode("ascii")
            if signature not in {"ARMO", "WEAP", "CELL"}:
                continue
            body = uncompressed_body(record.header, record.body)
            occurrences: dict[str, int] = defaultdict(int)
            for subrecord in parse_subrecords(body):
                field = subrecord.tag.decode("ascii")
                occurrence = occurrences[field]
                occurrences[field] += 1
                key = (
                    form_key(record.raw_form_id, masters, owner),
                    signature, field, occurrence,
                )
                if key not in desired:
                    continue
                if field != "FULL" or len(subrecord.payload) != 4:
                    raise AssertionError(f"unexpected base localization field: {key}")
                string_id = struct.unpack("<I", subrecord.payload)[0]
                # The 8.20 pack intentionally omits a few IDs that exist only
                # in the current runtime's refreshed master.  Those records
                # fall back to the version-matched CHS seed below.
                target = table.get(string_id)
                if target is not None:
                    result[key] = target
    return result


def curated_glossary(dist_root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for name in GLOSSARY_ORDER:
        path = dist_root / name / "tools" / "translation-source.tsv"
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            if not {"source", "target"}.issubset(reader.fieldnames or ()):
                continue
            for row in reader:
                source, target = row["source"], row["target"]
                if source and target and source != target and tokens(source) == tokens(target):
                    result.setdefault(source, target)
    return result


def normalise_seed(source: str, target: str, record_type: str) -> str:
    value = OpenCC("s2twp").convert(target)
    for old, new in (
        ("玻璃巖", "翠琉璃"),
        ("黑檀巖", "玄曜石"),
        ("鋼冰", "剛冰石"),
        ("甲殼", "硬殼"),
        ("鋼板", "鋼鈑"),
        ("高階", "高級"),
        ("體力", "耐力"),
        ("幻術", "幻象"),
        ("鏡子", "反射"),
        ("游俠", "散兵"),
        ("遊俠", "散兵"),
        ("冠軍", "勇士"),
        ("強盜", "盜賊"),
        ("太陽傷害", "日光傷害"),
        ("靈魂石", "靈魂寶石"),
        ("護甲值", "護具防禦力"),
    ):
        value = value.replace(old, new)
    if record_type in {"ARMO", "WEAP"}:
        if "Magicka" in source:
            value = value.replace("魔法", "法力")
        for old, new in (
            ("魔法頭盔", "法力頭盔"),
            ("魔法護腕", "法力護腕"),
            ("魔法腕甲", "法力腕甲"),
            ("魔法輕腕", "法力輕腕"),
            ("魔法重腕", "法力重腕"),
        ):
            value = value.replace(old, new)
        if "of Strength" in source:
            value = value.replace("強力", "荷重")
    if record_type == "ARMO":
        if "Gauntlets" in source:
            value = value.replace("護腕", "護手")
        value = value.replace("重腕", "重型護手")
        value = value.replace("輕腕", "輕型護腕")
        value = value.replace("腕甲", "護手")
        value = value.replace("戰靴", "靴子")
        if "Shield" in source and value.endswith("盾"):
            value += "牌"
        value = normalise_armor_tier(source, value)
    elif record_type == "WEAP":
        if "Greatsword" not in source and "Sword" in source and value.endswith("劍"):
            value = value[:-1] + "長劍"
        if "Bow" in source and value.endswith("弓"):
            value = value[:-1] + "戰弓"
    return value


def normalise_armor_tier(source: str, target: str) -> str:
    """Match 8.20's material-relative generic-enchantment tier wording."""
    rank3 = ("Daedric", "Dragonplate", "Dragonscale", "Stalhrim")
    rank2 = ("Orcish", "Glass", "Ebony", "Nordic Carved")
    rank1 = ("Dwarven", "Elven", "Steel Plate", "Chitin")
    if any(name in source for name in rank3):
        rank = 3
    elif any(name in source for name in rank2):
        rank = 2
    elif any(name in source for name in rank1):
        rank = 1
    else:
        rank = 0
    if " Minor " in f" {source} ":
        desired = "初級"
    elif " Peerless " in f" {source} ":
        desired = ("卓越", "卓越", "極致", "絕代")[rank]
    elif " Major " in f" {source} ":
        desired = ("高級", "高級", "卓越", "極致")[rank]
    else:
        desired = ("中級", "中級", "高級", "卓越")[rank]
    for tier in ("初級", "中級", "高級", "卓越", "極致", "絕代"):
        if tier in target:
            return target.replace(tier, desired, 1)
    prefixes = (
        "帝國鑲釘", "諾德鍛雕", "諾德雕文", "剛冰石", "翠琉璃",
        "玄曜石", "鋼鈑", "鋼製", "鐵製", "矮人", "精靈", "獸人",
        "魔族", "龍骨", "龍鱗", "硬殼", "骨模", "帝國", "革製",
        "皮製", "鋼鱗",
    )
    for prefix in prefixes:
        if target.startswith(prefix):
            return prefix + desired + target[len(prefix):]
    return target


EXACT = {
    "Absorb Magicka": "吸取法力",
    "Absorb Stamina": "吸取耐力",
    "Stagger Power Controller": "失衡強度控制器",
    "Stat Damage Controller": "屬性傷害控制器",
    "Huntsman's Prowess": "獵人勇氣",
    "Hunstman's Prowess": "獵人勇氣",
    "Fortify Potion Duration": "強化藥水持續時間",
    "Damage Armor": "削弱護甲",
    "Damage Weapon": "削弱武器",
    "Damage Construct": "構裝體損壞術",
    "Your Stamina Regeneration is increased by <mag>%.": "耐力恢復速度提高 <mag>%。",
    "You make <50>% less noise while moving.  ": "移動時發出的聲響減少 <50>%。",
    "Conjured Daedra up to level <mag> have a chance to be sent back to Oblivion.":
        "最高 <mag> 級的召喚魔族有機率被遣返湮滅。",
    "Daedra up to level <mag> have a chance to be sent back to Oblivion.":
        "最高 <mag> 級的魔族有機率被遣返湮滅。",
    "Living targets up to level <mag> have a chance to attack anyone nearby for <dur> seconds.":
        "最高 <mag> 級的活體目標有機率攻擊附近任何人，持續 <dur> 秒。",
    "Living targets up to level <mag> have a chance to be silenced for <dur> seconds.":
        "最高 <mag> 級的活體目標有機率陷入沉默，持續 <dur> 秒。",
    "Undead targets up to level <mag> have a chance to flee for <dur> seconds.":
        "最高 <mag> 級的亡靈有機率逃跑，持續 <dur> 秒。",
    "Absorbs <mag> Magicka.": "吸取 <mag> 點法力。",
    "Absorbs <mag> Stamina.": "吸取 <mag> 點耐力。",
    "At night, absorbs <mag> Health.": "夜間吸取 <mag> 點生命。",
    "If target dies within <dur> seconds, fills a soul gem.":
        "若目標在 <dur> 秒內死亡，則填充一顆靈魂寶石。",
    "You block <mag>% more damage.": "格擋時承受的傷害降低 <mag>%。",
    "Your Illusion spells cost <mag>% less.": "幻象系法術消耗減少 <mag>%。",
    "You reflect <mag>% of incoming melee damage back at your attacker.":
        "將承受的近戰傷害反射 <mag>% 給攻擊者。",
    "You deal <mag>% extra damage with ranged weapons.":
        "使用遠程武器時，造成的傷害提高 <mag>%。",
    "Has a <50>% chance to deal <mag> Fire, Frost or Shock damage.":
        "有 <50>% 機率造成 <mag> 點火焰、寒霜或閃電傷害。",
    "Targets up to level <mag> have a chance to be paralyzed for <10> seconds.  ":
        "最高 <mag> 級的目標有機率麻痺 <10> 秒。",
    "Living targets up to level <mag> have a chance to flee from combat for <dur> seconds.":
        "最高 <mag> 級的活體目標有機率逃離戰鬥，持續 <dur> 秒。",
    "Deals <mag> Magic damage per second for <dur> seconds to Dwarven automatons.":
        "每秒對矮人機械構裝體造成 <mag> 點魔法傷害，持續 <dur> 秒。",
    "When a target dies within <mag> feet, you fill a soul gem.":
        "當 <mag> 英尺內的目標死亡時，填充一顆靈魂寶石。",
    "You create a light that illuminates nearby objects.": "創造一道照亮附近物體的光芒。",
    "Deals <mag> Poison damage. Poisoned targets take extra damage over time.":
        "造成 <mag> 點毒素傷害。中毒的目標會持續受到額外傷害。",
    "Deals <mag> Frost damage to Health and Stamina, and leaves behind a hazard that deals extra damage over <10> seconds.  ":
        "對生命與耐力造成 <mag> 點寒霜傷害，並留下持續 <10> 秒的傷害區域。",
    "Deals <mag> Sun Damage per second for <dur> seconds to the undead.":
        "每秒對亡靈造成 <mag> 點日光傷害，持續 <dur> 秒。",
    "You deal <mag>% more damage with power attacks.":
        "使用強力攻擊時，造成的傷害提高 <mag>%。",
}
EXACT_NORMALIZED = {source.rstrip(): target for source, target in EXACT.items()}


def write_tsv(rows: list[tuple[str, ...]]) -> None:
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow((
            "string_id", "form_key", "record_type", "editor_id", "field",
            "occurrence", "source", "target", "provenance",
        ))
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source15", required=True, type=Path)
    parser.add_argument("--source145", required=True, type=Path)
    parser.add_argument("--chs145", required=True, type=Path)
    parser.add_argument("--masters-dir", required=True, type=Path)
    parser.add_argument("--strings-dir", required=True, type=Path)
    parser.add_argument("--dist-root", required=True, type=Path)
    args = parser.parse_args()
    for name in EXPECTED:
        actual = sha256(getattr(args, name))
        if actual != EXPECTED[name]:
            raise SystemExit(f"{name} SHA-256 mismatch: {actual}")
    verify_seed_topology(args.source145, args.chs145)
    current = extract(args.source15, "cp1252")
    old_english = {row.key: row for row in extract(args.source145, "cp1252")}
    old_chinese = {row.key: row for row in extract(args.chs145, "utf-8")}
    glossary = curated_glossary(args.dist_root)

    emitted: list[tuple[str, ...]] = []
    stats: dict[str, int] = defaultdict(int)
    for string_id, row in enumerate(current, 1):
        if not row.value:
            target, provenance = "", "empty internal field"
        elif row.value.rstrip() in EXACT_NORMALIZED:
            target = EXACT_NORMALIZED[row.value.rstrip()]
            provenance = "Thaumaturgy 1.5 terminology review"
        elif row.value in glossary:
            target, provenance = glossary[row.value], "existing curated Traditional Chinese exact phrase"
        elif row.key in old_chinese:
            target = normalise_seed(row.value, old_chinese[row.key].value, row.record_type)
            if old_english[row.key].value == row.value:
                provenance = "Thaumaturgy 1.4.5 CHS exact FormKey; OpenCC s2twp + terminology review"
            else:
                provenance = "Thaumaturgy 1.4.5 CHS FormKey; reviewed against 1.5 source delta"
        else:
            target, provenance = row.value, "new 1.5 internal field retained"
        stats[provenance] += 1
        emitted.append((
            f"{string_id:08X}", row.form_key, row.record_type, row.editor_id,
            row.field, str(row.occurrence), row.value, target, provenance,
        ))
    write_tsv(emitted)
    print(f"wrote {OUTPUT}: {len(emitted)} rows")
    for key in sorted(stats):
        print(f"{stats[key]:5d}  {key}")


if __name__ == "__main__":
    main()
