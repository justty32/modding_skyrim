#!/usr/bin/env python3
"""Dump NPC_ records of Kurone Soul Tomb plugins (modpack-main winners) as JSON.

Read-only. Usage: python3 -I dump_soultomb_npcs.py OUT.json
"""
import json, os, struct, sys
from pathlib import Path

sys.path.insert(0, "/home/lorkhan/repo/moddings/skyrim/agentctl/tools")
from esplib.core import Plugin  # noqa: E402
from esplib import fields  # noqa: E402
from esplib.formid import resolve  # noqa: E402
from esplib.strings import StringTables  # noqa: E402

MODS = Path("/home/lorkhan/games/mod-organizer-2-skyrimspecialedition/modorganizer2/mods")
GAME_DATA = Path("/home/lorkhan/.local/share/Steam/steamapps/common/Skyrim Special Edition/Data")
# MO2 priority high -> low (modlist.txt order); first hit wins
LAYERS = [
    "KuroneSoulTomb-PrivateBody-Dev-2026-10-10",
    "Kurone Soul Tomb Teleport CHS-153397-2.1",
    "Kurone Soul Tomb Teleport Add-on-150859-2.1",
    "Kurone Soul Tomb CHS-153397-2.0Fix15",
    "KuroneSoulTomb-NIFSE-Collision-Dev-2026-10-10",
    "Kurone Soul Tomb Update Patch-150859-2.0Fix15",
    "Kurone Soul Tomb-150859-2.0fix9",
]
PLUGINS = ["KuroneSoulTomb.esp", "KuroneSoulTomb_EX1.esp", "KuroneSoulTomb_EX2.esp",
           "KuroneSoulTomb_EX3.esp", "KuroneSoulTomb_EX4.esp", "KuroneSoulTomb_Teleport_Addon.esp"]


def find(rel: str, skip_chs=False):
    for L in LAYERS:
        if skip_chs and "CHS" in L:
            continue
        p = MODS / L / rel
        if p.exists():
            return L, p
        # case-insensitive fallback
        cur = MODS / L
        ok = True
        for part in Path(rel).parts:
            if not cur.is_dir():
                ok = False
                break
            m = [c for c in os.listdir(cur) if c.lower() == part.lower()]
            if not m:
                ok = False
                break
            cur = cur / m[0]
        if ok and cur.exists():
            return L, cur
    return None, None


def race_names():
    out = {}
    cands = [GAME_DATA / "Skyrim.esm", GAME_DATA / "Dawnguard.esm", GAME_DATA / "Dragonborn.esm"]
    for c in cands:
        if c.exists():
            p = Plugin.open(c)
            for r in p.records({"RACE"}):
                fk = resolve(r.formid, p.masters, p.name)
                out[fk.key()] = fields.edid(r)
    return out


def main(out_path):
    races = race_names()
    rows = []
    for plug in PLUGINS:
        layer, path = find(plug)
        en_layer, en_path = find(plug, skip_chs=True)
        p = Plugin.open(path)
        pen = Plugin.open(en_path) if en_path else None
        loc = p.header.is_localized
        en_names = {}
        if pen:
            for r in pen.records({"NPC_"}):
                en_names[r.formid] = fields.full(r, pen.header.is_localized, None)
        # local races
        for r in p.records({"RACE"}):
            races[resolve(r.formid, p.masters, p.name).key()] = fields.edid(r)
        achr = {}
        for r in p.records({"ACHR"}):
            n = r.get("NAME")
            if n:
                k = resolve(n.u32(), p.masters, p.name).key()
                achr[k] = achr.get(k, 0) + 1
        for r in p.records({"NPC_"}):
            fk = resolve(r.formid, p.masters, p.name)
            acbs = r.get("ACBS")
            flags = acbs.u32(0) if acbs else 0
            tflags = struct.unpack_from("<H", acbs.data, 18)[0] if acbs and len(acbs.data) >= 20 else 0
            rn = r.get("RNAM")
            race_fk = resolve(rn.u32(), p.masters, p.name) if rn else None
            tplt = r.get("TPLT")
            rel = f"meshes/actors/character/FaceGenData/FaceGeom/{fk.plugin}/{fk.local:08X}.nif"
            fg_layer, _ = find(rel)
            wn = r.get("WNAM")
            rows.append({
                "formkey": str(fk),
                "defined_here": fk.plugin.lower() == p.name.lower(),
                "plugin_record_in": p.name,
                "edid": fields.edid(r),
                "name_winner": fields.full(r, loc, None),
                "name_en": en_names.get(r.formid),
                "race": (races.get(race_fk.key()) or str(race_fk)) if race_fk else None,
                "race_formkey": str(race_fk) if race_fk else None,
                "female": bool(flags & 1),
                "unique": bool(flags & 0x20),
                "essential": bool(flags & 2),
                "template": str(resolve(tplt.u32(), p.masters, p.name)) if tplt else None,
                "template_traits": bool(tflags & 1) if tplt else False,
                "hdpt_count": len(r.get_all("PNAM")),
                "wnam": str(resolve(wn.u32(), p.masters, p.name)) if wn else None,
                "facegen_layer": fg_layer,
                "achr_count_in_plugin": achr.get(fk.key(), 0),
                "winner_layer": layer,
            })
    json.dump(rows, open(out_path, "w"), ensure_ascii=False, indent=1)
    print(len(rows), "rows")


if __name__ == "__main__":
    main(sys.argv[1])
