#!/usr/bin/env python3
"""Scan modpack-main load order for follower NPCs (winner records). Read-only.

Usage: python3 -I scan_followers.py OUT.json
Follower = winning NPC_ has PotentialFollowerFaction / CurrentFollowerFaction (Skyrim.esm 05C84D / 05C84E),
or is in the extra list (scripted followers like Serana), or in the voiced roster / 11-07 body table.
"""
import json, os, struct, sys
from pathlib import Path

S = Path("/home/lorkhan/repo/moddings/skyrim")
sys.path.insert(0, str(S / "agentctl/tools"))
sys.path.insert(0, str(S / "instance/tools"))
from esplib.core import Plugin  # noqa: E402
from esplib import fields  # noqa: E402
from esplib.formid import resolve as fk_resolve, FormKey  # noqa: E402
from esplib.strings import StringTables  # noqa: E402
import resolve_load_order as rlo  # noqa: E402

PROFILE = S / "instance/profiles/modpack-main"
MO2 = rlo.DEFAULT_MO2
DATA = rlo.DEFAULT_GAME_DATA
FOLLOWER_FACTIONS = {("skyrim.esm", 0x05C84D), ("skyrim.esm", 0x05C84E)}
EXTRA = {("dawnguard.esm", 0x002B6C)}  # Serana (DLC1Serana)


def main(out):
    resolved, missing, _, _ = rlo.resolve(PROFILE, MO2, DATA)
    mods = [l[1:] for l in rlo.lines(PROFILE / "modlist.txt") if l.startswith("+")]
    roots = [str(MO2 / "overwrite")] + [str(MO2 / "mods" / m) for m in mods] + [str(DATA)]
    extra = set(EXTRA)
    roster = json.load(open(S / "modpack-design/content-plan/followers/voiced-follower-overhaul/roster.json"))
    for r in roster["rows"]:
        try:
            extra.add(FormKey.parse(r["npc_formid"]).key())
        except Exception:
            pass
    bt = json.load(open(S / "agentctl/handoffs/home-2026-11-07/chronicon-kurone/data/body-final-targets.json"))
    body = {FormKey.parse(r["target"]).key(): r for r in bt["rows"]}
    extra |= set(body)

    touch = {}     # key -> list of plugin names (load order)
    winner = {}    # key -> (plugin, path)
    origin_rec = {}
    races = {}
    names = {}
    for name, path in resolved:
        try:
            p = Plugin.open(path)
        except Exception as e:
            print("skip", name, e, file=sys.stderr)
            continue
        for r in p.records({"RACE"}):
            k = fk_resolve(r.formid, p.masters, p.name).key()
            races[k] = fields.edid(r)
        for r in p.records({"NPC_"}):
            k = fk_resolve(r.formid, p.masters, p.name).key()
            touch.setdefault(k, []).append(name)
            winner[k] = (name, str(path), r, p.masters, p.header.is_localized)
            if not p.header.is_localized:
                nm = fields.full(r, False, None)
                if nm:
                    names.setdefault(k, []).append((name, nm))
        del p
    fg_index = {}
    for m in mods:
        base = MO2 / "mods" / m
        hit = None
        for cand in os.listdir(base) if base.is_dir() else []:
            if cand.lower() == "meshes":
                hit = base / cand
        if not hit:
            continue
        s_ = set()
        for dp, dn, fn in os.walk(hit):
            low = dp.lower()
            if "facegeom" not in low:
                if "facegendata" not in low and "character" not in low and low != str(hit).lower() and "actors" not in low:
                    dn[:] = []
                continue
            relbase = os.path.relpath(dp, base).lower().replace(os.sep, "/")
            for f in fn:
                s_.add(relbase + "/" + f.lower())
        fg_index[m] = s_
    rows = []
    st_cache = {}
    for k, (pname, path, r, masters, loc) in winner.items():
        facs = set()
        for s in r.get_all("SNAM"):
            facs.add(fk_resolve(struct.unpack_from("<I", s.data, 0)[0], masters, pname).key())
        is_f = bool(facs & FOLLOWER_FACTIONS)
        if not is_f and k not in extra:
            continue
        acbs = r.get("ACBS")
        flags = acbs.u32(0) if acbs else 0
        rn = r.get("RNAM")
        rk = fk_resolve(rn.u32(), masters, pname).key() if rn else None
        # name: from defining plugin's string tables if localized
        name = None
        if loc:
            if pname not in st_cache:
                st_cache[pname] = StringTables.from_dirs(pname, roots, "english")
            name = fields.full(r, True, st_cache[pname])
        else:
            name = fields.full(r, False, None)
        def_plugin = k[0]
        def_path = next((str(pp) for n, pp in resolved if n.lower() == def_plugin), None)
        def_mod = None
        if def_path and "/mods/" in def_path:
            def_mod = def_path.split("/mods/", 1)[1].split("/", 1)[0]
        win_mod = path.split("/mods/", 1)[1].split("/", 1)[0] if "/mods/" in path else "(game Data)"
        # original (lowest-priority) mod containing the defining plugin
        src_mod = None
        for m in reversed(mods):
            if (MO2 / "mods" / m / next((n for n, _ in resolved if n.lower() == def_plugin), def_plugin)).is_file():
                src_mod = m
                break
        cjk = [nm for _, nm in names.get(k, []) if any('\u4e00' <= ch <= '\u9fff' for ch in nm)]
        if name and any('\u4e00' <= ch <= '\u9fff' for ch in name):
            name_zh = name
        else:
            name_zh = cjk[-1] if cjk else None
        # facegen provider
        rel = f"meshes/actors/character/facegendata/facegeom/{def_plugin}/{k[1]:08x}.nif"
        fg = None
        for m in mods:
            if fg_index.get(m) and rel in fg_index[m]:
                fg = m
                break
        wn = r.get("WNAM")
        wnam = str(fk_resolve(wn.u32(), masters, pname)) if wn else None
        fkey = f"{k[1]:06X}:{next((n for n, _ in resolved if n.lower() == def_plugin), def_plugin)}"
        rows.append({
            "formkey": fkey,
            "edid": fields.edid(r),
            "name": name,
            "race": races.get(rk) if rk else None,
            "female": bool(flags & 1),
            "follower_faction": is_f,
            "in_extra": k in extra,
            "defining_mod": def_mod or "(game Data)",
            "winner_plugin": pname,
            "winner_mod": win_mod,
            "source_mod": src_mod or "(game Data)",
            "name_zh": name_zh,
            "names_seen": [nm for _, nm in names.get(k, [])],
            "facegen_mod": fg,
            "wnam": wnam,
            "touching_plugins": touch[k],
            "body_1107": body[k]["source"] if k in body else None,
        })
    json.dump(rows, open(out, "w"), ensure_ascii=False, indent=1)
    print(len(rows), "followers;", len(winner), "NPC_ total; missing plugins", len(missing))


if __name__ == "__main__":
    main(sys.argv[1])
