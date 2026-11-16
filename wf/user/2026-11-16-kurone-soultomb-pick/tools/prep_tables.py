#!/usr/bin/env python3
"""Turn raw dumps into the three wf-table/1 tables for the Soul Tomb pick page.

Usage: python3 -I prep_tables.py SOULTOMB_RAW.json FOLLOWERS_RAW.json OUT_DIR
Rules are written here so the tables can be rebuilt; see README.md next to the tables.
"""
import json, re, sys
from pathlib import Path

DATE = "2026-11-16"
PLAYABLE = {"NordRace", "ImperialRace", "BretonRace", "RedguardRace", "DarkElfRace", "HighElfRace",
            "WoodElfRace", "OrcRace", "KhajiitRace", "ArgonianRace", "ElderRace"}
CREATURE = re.compile(r"dog|husky|hound|riekling|fox|goblin|chicken|spebf|bear|wolf|sabre|horse|spider|troll|"
                      r"dragon|skeleton|draugr|atronach|spriggan|mammoth|horker|netch|boar|mudcrab|chaurus|"
                      r"giant|werewolf|lurker|mimic|wisp|figure_creature|creature", re.I)
CORPSE = re.compile(r"corp(s|se)es?|corpes", re.I)
VARIANT = {"AAA_ChaosSoul": "AAA_Chaos", "AAA_ChaosCorpse": "AAA_Chaos", "AAA_ChaosSoulIN": "AAA_Chaos",
           "AAA_FolenSoul": "AAA_Folen", "AAA_FolenSoulIN": "AAA_Folen"}
GENERIC_NAMES = {"贪婪的人", "狂乱之影", "水手", "调教师", "看守者", "贩子"}


def table(cols, rows, source):
    return {"contract": "wf-table/1", "source": source, "extracted": DATE, "columns": cols,
            "rows": [{c: r.get(c, "") for c in cols} for r in rows]}


def donors(raw):
    by = {}
    achr = {}
    for r in raw:  # plugin order = load order, later override wins
        by[r["formkey"]] = r
        achr[r["formkey"]] = achr.get(r["formkey"], 0) + r["achr_count_in_plugin"]
    keep, excl = [], []
    for fk, r in by.items():
        base = {
            "id": "d:" + fk, "formkey": fk, "edid": r["edid"], "name_zh": r["name_winner"] or "",
            "name_en": r["name_en"] or "", "plugin": fk.split(":", 1)[1], "race": r["race"] or "",
            "sex": "女" if r["female"] else "男", "placed": achr[fk],
        }
        race = r["race"] or ""
        if not r["facegen_layer"]:
            why = "生物或非人形種族、沒有臉部 facegen" if CREATURE.search(race) or race not in PLAYABLE else "沒有臉部 facegen"
            excl.append({**base, "reason": why})
            continue
        if r["edid"] in VARIANT:
            excl.append({**base, "reason": f"同一角色的劇情分身（幻影／靈魂／屍體版），挑本尊 {VARIANT[r['edid']]} 即可"})
            continue
        if CORPSE.search(r["edid"] or ""):
            excl.append({**base, "reason": "屍體道具 NPC（劇情擺設）"})
            continue
        custom = race not in PLAYABLE
        notes = []
        if custom:
            notes.append("自訂種族：換臉要走手寫 race 路線，工較大")
        if "BigHead" in race:
            notes.append("大頭比例種族")
        group = "雜兵" if (r["name_winner"] or "") in GENERIC_NAMES else "主要角色"
        keep.append({**base, "group": group, "custom_race": custom, "note": "；".join(notes),
                     "facegen_layer": r["facegen_layer"]})
    keep.sort(key=lambda d: (d["group"] != "主要角色", d["sex"] != "女", d["plugin"], d["edid"]))
    return keep, excl


def targets(raw):
    keep, excl = [], []
    for r in raw:
        sm = r["source_mod"] if r["source_mod"] != "(game Data)" else "原版 Skyrim／DLC／CC"
        name = r["name_zh"] or r["name"] or ""
        base = {"id": "t:" + r["formkey"], "formkey": r["formkey"], "edid": r["edid"] or "",
                "name": name, "name_en": r["name"] if r["name"] != name else "",
                "mod": sm, "race": r["race"] or "", "sex": "女" if r["female"] else "男"}
        if "Soul Tomb" in sm:
            excl.append({**base, "reason": "Soul Tomb 自己的角色（本頁當素材）"}); continue
        if "PROTEUS" in sm or "PROTEUS" in r["defining_mod"]:
            excl.append({**base, "reason": "PROTEUS 的玩家預設槽，不是角色"}); continue
        if not name:
            excl.append({**base, "reason": "沒有名字（範本／生成用記錄）"}); continue
        if CREATURE.search(r["race"] or ""):
            excl.append({**base, "reason": "動物／生物隨從"}); continue
        face = r["facegen_mod"] or "原版（BSA）"
        face_note = ""
        if r["facegen_mod"] and r["facegen_mod"] != sm and r["facegen_mod"] != r["defining_mod"]:
            face_note = "已換臉／換頭"
        body = ""
        if r["body_1107"]:
            body = {"native RimLydia": "Kurone 11-07：Rim Lydia", "native BigChangeV2": "Kurone 11-07：Big Change V2"}.get(
                r["body_1107"], "Kurone 11-07：MAIN " + r["body_1107"].replace("MAIN ", ""))
        elif r["wnam"] and "PrivateBody" in r["wnam"]:
            body = "私有身體 " + r["wnam"].split(":", 1)[1].replace(".esp", "")
        keep.append({**base, "face_now": face, "face_note": face_note, "body_now": body,
                     "kurone_1107": bool(r["body_1107"]), "follower_faction": r["follower_faction"]})
    keep.sort(key=lambda t: (t["mod"] == "原版 Skyrim／DLC／CC", t["mod"].lower(), t["sex"] != "女", t["name"]))
    return keep, excl


BODIES = [
    {"id": "none", "label": "不換", "kind": "none", "desc": "身體維持現狀（現在的身體欄怎麼寫就是怎樣）。"},
    {"id": "rimlydia", "label": "Kurone Big Change Body（Rim Lydia 預設）", "kind": "preset",
     "desc": "11-07 給 Aela、Camilla、Brelyna 等 9 人用的身形；作者 Rim Lydia RaceMenu 預設，CBBE 3BA 烘焙。"},
    {"id": "bigchange_v2", "label": "Kurone Big Change Body V2", "kind": "preset",
     "desc": "11-07 給 Jenassa、Frea、Jordis、Delphine 用的身形；V2 版，比 Rim Lydia 那版變化更大。"},
]
for who, users in [("Sasha", "Ryn"), ("Lili", "Vilja"), ("Lamia", "Morgaine"), ("Ela", "Katana、Katana Shade"),
                   ("Yumi", "Megara"), ("Coco", "Varinia"), ("Saya", "Yoana"), ("Nina", "Aniya"), ("Kyrie", "Melana")]:
    BODIES.append({"id": "main_" + who.lower(), "label": f"Kurone MAIN 原裝：{who}", "kind": "main",
                   "desc": f"Kurone Followers MAIN 裡 {who} 自帶的 3BA 身體與皮膚；11-07 給 {users} 用。"})
BODIES.append({"id": "kurone7", "label": "Kurone7 預設身形（Soul Tomb 現用）", "kind": "shared",
               "desc": "Soul Tomb 48 位女性 NPC 現在用的身體（10-10 私有身體層指向 Kurone7 的 46560 預設烘焙）。"})


def main(st_raw, fo_raw, out):
    out = Path(out)
    (out).mkdir(parents=True, exist_ok=True)
    dk, dx = donors(json.load(open(st_raw)))
    tk, tx = targets(json.load(open(fo_raw)))
    src = "../README.md"
    dcols = ["id", "formkey", "edid", "name_zh", "name_en", "plugin", "race", "sex", "group", "custom_race",
             "placed", "note", "facegen_layer"]
    xcols = ["id", "formkey", "edid", "name_zh", "name_en", "plugin", "race", "sex", "placed", "reason"]
    tcols = ["id", "formkey", "edid", "name", "name_en", "mod", "race", "sex", "face_now", "face_note",
             "body_now", "kurone_1107", "follower_faction"]
    txcols = ["id", "formkey", "edid", "name", "mod", "race", "sex", "reason"]
    json.dump(table(dcols, dk, src), open(out / "donors.json", "w"), ensure_ascii=False, indent=1)
    json.dump(table(xcols, dx, src), open(out / "donors-excluded.json", "w"), ensure_ascii=False, indent=1)
    json.dump(table(tcols, tk, src), open(out / "targets.json", "w"), ensure_ascii=False, indent=1)
    json.dump(table(txcols, tx, src), open(out / "targets-excluded.json", "w"), ensure_ascii=False, indent=1)
    json.dump(table(["id", "label", "kind", "desc"], BODIES, src), open(out / "bodies.json", "w"),
              ensure_ascii=False, indent=1)
    print("donors", len(dk), "excluded", len(dx), "| targets", len(tk), "excluded", len(tx), "| bodies", len(BODIES))


if __name__ == "__main__":
    main(*sys.argv[1:4])
