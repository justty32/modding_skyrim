#!/usr/bin/env python3
"""BodySlide 產物驗收解析器（stdlib-only、唯讀）。

子命令：
  nif FILE                 解析 Skyrim SE NIF（20.2.0.7／user 12／BS stream 100）的 shape 與 skin partition
  tri FILE [--nif FILE]    解析 BodySlide PIRT TRI（position＋可選 UV section）
  compare --a DIR --b DIR [--repeat DIR] [--expect-changed SHAPE ...] [--tri-check]

Exit code：0＝解析成功且全部檢查符合；1＝期望不符（index 越界、scale 非有限、A/B 無變動、
repeat 不同、路徑集合不同、指定 shape 沒變）；2＝輸入讀不到、格式錯誤或格式不支援。

格式依據（只讀、不 import）：
- NIF header：projects/model-converter/nif2gltf/nif_reader.py `_read_header`、_binreader.py。
- BSTriShape（SSE）：同 repo `_blocks.py` `_read_bstrishape`；nifly（ousnius/nifly）src/Geometry.cpp
  BSTriShape::Sync——stream 100 位置一律 float3、numTriangles 為 u16、之後 numVertices u16、
  dataSize u32、vertData、triangles、particleDataSize u32；BSDynamicTriShape 接 dynamicDataSize＋
  每頂點 vec4；BSSubIndexTriShape（SSE）接 segment 資料，前綴與 BSTriShape 相同。
  NiObjectNET＋NiAVObject 後 skin ref 位於 block 起點 +88+4*num_extra（11-18 validate-original.py）。
- NiSkinPartition（SSE）：nifly src/Skin.cpp NiSkinPartition::Sync——numPartitions、dataSize、
  vertexSize、vertexDesc（`<IIIQ`，頂點從 +20 起），每 partition：numVertices、numTriangles、numBones、
  numStrips、numWeightsPerVertex、bones、hasVertexMap＋map、hasVertexWeights＋weights、stripLengths、
  hasFaces＋strips/triangles、hasBoneIndices＋indices、lodLevel、globalVB、vertexDesc、trueTriangles。
  global vertex 位置：VF_FULLPREC（flags 0x400，flags=desc>>44）→ float3，否則 half3。
- NiSkinInstance：dataRef、skinPartitionRef、skeletonRoot、bones；BSDismemberSkinInstance 再接 partitions。
- vertex desc：nifly include/VertexData.hpp——vertex size=(desc&0xF)*4，flags=(desc>>44)&0xFFF。
- PIRT TRI：BodySlide-and-Outfit-Studio commit 033016464d31761bfaf6966db3ea9c3c3cb6105a
  src/files/TriFile.cpp TriFile::Read——magic "PIRT"、u16 shape 數；shape：u8 長度名、u16 morph 數；
  morph：u8 長度名、f32 mult、u16 頂點數、每筆 u16 index＋3×i16 delta。未到 EOF 時接 UV section：
  同結構但每筆 u16 index＋2×i16 delta（無 marker）。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import struct
import sys
from pathlib import Path

NIF_VERSION = 0x14020007
SSE_USER_VERSION = 12
SSE_BS_VERSION = 100
SHAPE_TYPES = {"BSTriShape", "BSDynamicTriShape", "BSSubIndexTriShape"}
UNSUPPORTED_SHAPE_TYPES = {"NiTriShape", "NiTriStrips", "BSLODTriShape", "BSMeshLODTriShape",
                           "BSSegmentedTriShape", "NiTriShapeData", "NiTriStripsData"}
SKIN_INSTANCE_TYPES = {"NiSkinInstance", "BSDismemberSkinInstance"}
VF_VERTEX = 0x001
VF_SKINNED = 0x040
VF_FULLPREC = 0x400
EPS = 1e-6


class FormatError(Exception):
    """輸入格式錯誤或不支援 → exit 2。"""


class Reader:
    __slots__ = ("d", "p", "end")

    def __init__(self, data: bytes, pos: int = 0, end: int | None = None):
        self.d, self.p = data, pos
        self.end = len(data) if end is None else end

    def take(self, n: int) -> bytes:
        if n < 0 or self.p + n > self.end:
            raise FormatError(f"unexpected end of data at offset {self.p} (need {n} bytes)")
        b = self.d[self.p:self.p + n]
        self.p += n
        return b

    def unpack(self, fmt: str):
        v = struct.unpack("<" + fmt, self.take(struct.calcsize("<" + fmt)))
        return v[0] if len(v) == 1 else v

    def remaining(self) -> int:
        return self.end - self.p


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# ---------------------------------------------------------------- NIF


def read_nif_header(r: Reader) -> dict:
    start = r.p
    nl = r.d.find(b"\n", start, min(len(r.d), start + 128))
    if nl < 0:
        raise FormatError("no NIF header line")
    header_string = r.take(nl - start + 1)[:-1].decode("latin-1")
    if not header_string.startswith("Gamebryo File Format"):
        raise FormatError(f"not a NIF header: {header_string[:40]!r}")
    version = r.unpack("I")
    if version != NIF_VERSION:
        raise FormatError(f"unsupported NIF version 0x{version:08X} (need 0x14020007)")
    if r.unpack("B") != 1:
        raise FormatError("big-endian NIF not supported")
    user_version = r.unpack("I")
    if user_version != SSE_USER_VERSION:
        raise FormatError(f"unsupported user version {user_version} (need 12)")
    num_blocks = r.unpack("I")
    bs_version = r.unpack("I")
    if bs_version != SSE_BS_VERSION:
        raise FormatError(f"unsupported BS stream version {bs_version} (need 100 = Skyrim SE)")
    # BSStreamHeader for stream 100: Author, Process Script (<131), Export Script; no Max Filepath (>=103).
    for _ in range(3):
        r.take(r.unpack("B"))
    block_types = [r.take(r.unpack("I")).decode("latin-1") for _ in range(r.unpack("H"))]
    type_idx = [r.unpack("H") & 0x7FFF for _ in range(num_blocks)]
    sizes = [r.unpack("I") for _ in range(num_blocks)]
    num_strings = r.unpack("I")
    r.unpack("I")  # max string length
    strings = [r.take(r.unpack("I")).decode("latin-1") for _ in range(num_strings)]
    for _ in range(r.unpack("I")):  # groups
        r.unpack("I")
    types = []
    for i, t in enumerate(type_idx):
        if t >= len(block_types):
            raise FormatError(f"block {i} type index {t} out of range")
        types.append(block_types[t])
    offsets, cur = [], r.p
    for sz in sizes:
        offsets.append(cur)
        cur += sz
    if cur > len(r.d):
        raise FormatError(f"block sizes exceed file length ({cur} > {len(r.d)})")
    return {"header_string": header_string, "version": f"0x{version:08X}", "user_version": user_version,
            "bs_version": bs_version, "num_blocks": num_blocks, "types": types, "sizes": sizes,
            "offsets": offsets, "strings": strings, "blocks_end": cur, "file_size": len(r.d)}


def string_at(h: dict, idx: int):
    if idx == 0xFFFFFFFF:
        return None
    if idx >= len(h["strings"]):
        raise FormatError(f"string index {idx} out of range")
    return h["strings"][idx]


def decode_positions(data: bytes, base: int, count: int, stride: int, full: bool) -> list:
    fmt = "<3f" if full else "<3e"
    need = 12 if full else 6
    if stride < need:
        raise FormatError(f"vertex stride {stride} too small for {'float3' if full else 'half3'} position")
    out = []
    for i in range(count):
        out.append(struct.unpack_from(fmt, data, base + i * stride))
    return out


def position_full_precision(desc: int) -> tuple[bool, str]:
    """float3 還是 half3。nifly 對 SSE（stream 100）的 BSTriShape 與 NiSkinPartition 一律當 float3
    （Skin.hpp `IsFullPrecision() { return true; }`），實檔也多半沒設 VF_FULLPREC；所以 flag 只是充分條件，
    主要看版面：位置後第一個 attribute offset（nifly `GetAttributeOffset`）≥12 只可能是 float3，
    ==8 是 half3（half3+bitangentX＝8 B，FO4 式版面）。"""
    flags = (desc >> 44) & 0xFFF
    if flags & VF_FULLPREC:
        return True, "VF_FULLPREC flag"
    offs = [(desc >> (4 * a + 2)) & 0x3C for a in range(1, 9) if flags & (1 << a)]
    offs = [o for o in offs if o > 0]
    first = min(offs) if offs else (desc & 0xF) * 4
    return first >= 12, f"first attribute offset {first}" if offs else f"vertex size {first}"


def desc_info(desc: int) -> dict:
    flags = (desc >> 44) & 0xFFF
    full, why = position_full_precision(desc)
    return {"vertex_desc": f"0x{desc:016X}", "vertex_size": (desc & 0xF) * 4, "flags": f"0x{flags:03X}",
            "has_vertex": bool(flags & VF_VERTEX), "skinned_flag": bool(flags & VF_SKINNED),
            "full_precision_flag": bool(flags & VF_FULLPREC),
            "position_format": "float3" if full else "half3", "position_format_reason": why}


def read_skin_partition(d: bytes, h: dict, idx: int) -> tuple[dict, list]:
    r = Reader(d, h["offsets"][idx], h["offsets"][idx] + h["sizes"][idx])
    num_parts, data_size, vsize, desc = r.unpack("IIIQ")
    info = desc_info(desc)
    out = {"block": idx, "data_size": data_size, **info}
    if vsize != info["vertex_size"]:
        raise FormatError(f"NiSkinPartition {idx}: vertexSize {vsize} != desc size {info['vertex_size']}")
    if data_size and (vsize == 0 or data_size % vsize):
        raise FormatError(f"NiSkinPartition {idx}: dataSize {data_size} not a multiple of vertexSize {vsize}")
    nverts = data_size // vsize if vsize else 0
    base = r.p
    r.take(data_size)
    positions = []
    if nverts:
        if not info["has_vertex"]:
            raise FormatError(f"NiSkinPartition {idx}: vertex data without VF_VERTEX flag")
        positions = decode_positions(d, base, nverts, vsize, position_full_precision(desc)[0])
    parts = []
    for p in range(num_parts):
        nv, nt, nb, ns, nw = r.unpack("HHHHH")
        r.take(2 * nb)
        if r.unpack("B"):
            vmap = struct.unpack(f"<{nv}H", r.take(2 * nv))
            if nverts and vmap and max(vmap) >= nverts:
                raise FormatError(f"NiSkinPartition {idx} partition {p}: vertex map index out of range")
        if r.unpack("B"):
            r.take(4 * nv * nw)
        strip_lengths = struct.unpack(f"<{ns}H", r.take(2 * ns))
        if r.unpack("B"):
            r.take(2 * sum(strip_lengths) if ns else 6 * nt)
        if r.unpack("B"):
            r.take(nv * nw)
        r.unpack("BB")  # lodLevel, globalVB
        r.unpack("Q")   # per-partition vertexDesc
        r.take(6 * nt)  # trueTriangles
        parts.append({"vertices": nv, "triangles": nt, "bones": nb, "strips": ns, "weights_per_vertex": nw})
    if r.remaining():
        raise FormatError(f"NiSkinPartition {idx}: {r.remaining()} unparsed bytes at block end")
    out.update(vertex_count=nverts, partition_count=num_parts, partitions=parts)
    return out, positions


def read_shape(d: bytes, h: dict, idx: int, errors: list) -> tuple[dict, list]:
    t, o, size = h["types"][idx], h["offsets"][idx], h["sizes"][idx]
    r = Reader(d, o, o + size)
    name = string_at(h, r.unpack("I"))
    ne = r.unpack("I")
    extra = list(r.unpack(f"{ne}i")) if ne > 1 else ([r.unpack("i")] if ne else [])
    r.take(4 + 4 + 12 + 36 + 4 + 4 + 16)  # controller, flags, translation, rotation, scale, collision, sphere
    skin_ref, _shader, _alpha = r.unpack("iii")
    desc = r.unpack("Q")
    ntri, nv, data_size = r.unpack("HHI")
    info = desc_info(desc)
    shape = {"block": idx, "type": t, "name": name, "inline_num_vertices": nv, "inline_num_triangles": ntri,
             "inline_data_size": data_size, **info, "extra_data_refs": extra}
    positions = []
    if data_size:
        stride = info["vertex_size"]
        if data_size != stride * nv + 6 * ntri:
            raise FormatError(f"{t} {name!r}: dataSize {data_size} != {stride}*{nv}+6*{ntri}")
        if info["has_vertex"]:
            positions = decode_positions(d, r.p, nv, stride, position_full_precision(desc)[0])
        r.take(data_size)
    particle = r.unpack("I")
    if particle:
        shape["unsupported"] = f"particleDataSize={particle}"
    if t == "BSDynamicTriShape":
        dyn = r.unpack("I")
        shape["dynamic_data_size"] = dyn
        if dyn:
            if dyn % 16:
                raise FormatError(f"BSDynamicTriShape {name!r}: dynamicDataSize {dyn} not a multiple of 16")
            base = r.p
            r.take(dyn)
            positions = [struct.unpack_from("<3f", d, base + 16 * i) for i in range(dyn // 16)]
            shape["position_source_dynamic"] = True
    if t == "BSTriShape" and not particle and r.remaining():
        errors.append(f"{t} {name!r}: {r.remaining()} unparsed bytes at block end")
    shape["has_skin"] = skin_ref != -1
    vertex_source = "inline" if data_size else "none"
    if skin_ref != -1:
        if not 0 <= skin_ref < h["num_blocks"]:
            raise FormatError(f"{t} {name!r}: skin ref {skin_ref} out of range")
        st = h["types"][skin_ref]
        shape["skin_instance_type"] = st
        if st not in SKIN_INSTANCE_TYPES:
            raise FormatError(f"{t} {name!r}: unsupported skin instance type {st}")
        part_ref = struct.unpack_from("<i", d, h["offsets"][skin_ref] + 4)[0]
        if not 0 <= part_ref < h["num_blocks"] or h["types"][part_ref] != "NiSkinPartition":
            raise FormatError(f"{t} {name!r}: skin instance {skin_ref} has no NiSkinPartition (ref {part_ref})")
        part, ppos = read_skin_partition(d, h, part_ref)
        shape["skin_partition"] = part
        if not positions and ppos:
            positions, vertex_source = ppos, "skin_partition"
        elif positions and ppos and len(ppos) != len(positions):
            errors.append(f"{name!r}: inline vertices {len(positions)} != partition vertices {len(ppos)}")
    if shape.get("position_source_dynamic"):
        vertex_source = "dynamic"
    bad = sum(1 for v in positions for c in v if not math.isfinite(c))
    if bad:
        errors.append(f"{name!r}: {bad} non-finite position components")
    shape["vertex_count"] = len(positions)
    shape["vertex_source"] = vertex_source
    if positions:
        shape["bbox"] = [[min(v[k] for v in positions) for k in range(3)],
                         [max(v[k] for v in positions) for k in range(3)]]
    return shape, positions


def parse_nif(path: Path) -> tuple[dict, dict]:
    """回傳 (JSON 報告, {shape 名: positions})。格式錯誤丟 FormatError。"""
    d = path.read_bytes()
    h = read_nif_header(Reader(d))
    rep = {"file": str(path), "sha256": sha256_bytes(d), "header": {
        k: h[k] for k in ("header_string", "version", "user_version", "bs_version", "num_blocks")},
        "block_types": {}, "shapes": [], "bodytri": [], "unsupported": [], "errors": []}
    for t in h["types"]:
        rep["block_types"][t] = rep["block_types"].get(t, 0) + 1
    positions = {}
    for i, t in enumerate(h["types"]):
        if t in SHAPE_TYPES:
            try:
                shape, pos = read_shape(d, h, i, rep["errors"])
            except FormatError as e:
                rep["errors"].append(f"block {i} {t}: {e}")
                continue
            if "unsupported" in shape:
                rep["unsupported"].append(f"block {i} {t} {shape['name']!r}: {shape['unsupported']}")
            if shape["name"] in positions:
                rep["errors"].append(f"duplicate shape name {shape['name']!r}")
            positions[shape["name"]] = pos
            rep["shapes"].append(shape)
        elif t in UNSUPPORTED_SHAPE_TYPES:
            rep["unsupported"].append(f"block {i} {t}: geometry type not supported")
        elif t == "NiStringExtraData":
            name_idx, val_idx = struct.unpack_from("<II", d, h["offsets"][i])
            if string_at(h, name_idx) == "BODYTRI":
                rep["bodytri"].append({"block": i, "value": string_at(h, val_idx)})
    for bt in rep["bodytri"]:
        bt["attached_to"] = [s["name"] for s in rep["shapes"] if bt["block"] in s["extra_data_refs"]]
    rep["ok"] = not rep["errors"] and not rep["unsupported"]
    return rep, positions


# ---------------------------------------------------------------- TRI

def _tri_section(r: Reader, dims: int) -> list:
    shapes = []
    for _ in range(r.unpack("H")):
        sname = r.take(r.unpack("B")).decode("latin-1")
        morphs = []
        for _ in range(r.unpack("H")):
            mname = r.take(r.unpack("B")).decode("latin-1")
            scale = r.unpack("f")
            n = r.unpack("H")
            raw = r.take(n * (2 + 2 * dims))
            entries = list(struct.iter_unpack("<H" + "h" * dims, raw))
            morphs.append({"name": mname, "scale": scale, "entries": entries})
        shapes.append({"name": sname, "morphs": morphs})
    return shapes


def parse_tri(path: Path, vertex_limits: dict | None = None) -> tuple[dict, list]:
    """回傳 (JSON 報告, position section 原始資料)。截斷／magic 錯丟 FormatError。"""
    d = path.read_bytes()
    r = Reader(d)
    if r.take(4) != b"PIRT":
        raise FormatError("not a PIRT TRI (bad magic)")
    pos_shapes = _tri_section(r, 3)
    rep = {"file": str(path), "sha256": sha256_bytes(d), "position_shapes": [], "uv": None,
           "trailing_unparsed_bytes": 0, "check_failures": []}
    if r.remaining():
        uv_start = r.p
        try:
            uv = _tri_section(r, 2)
            rep["uv"] = {"shapes": [{"name": s["name"], "morph_count": len(s["morphs"])} for s in uv]}
            rep["trailing_unparsed_bytes"] = r.remaining()
        except FormatError as e:
            rep["uv"] = {"error": str(e)}
            rep["trailing_unparsed_bytes"] = len(d) - uv_start
    fails = rep["check_failures"]
    if rep["trailing_unparsed_bytes"]:
        fails.append(f"{rep['trailing_unparsed_bytes']} trailing unparsed bytes")
    for s in pos_shapes:
        limit = None
        if vertex_limits is not None:
            limit = vertex_limits.get(s["name"])
            if limit is None:
                fails.append(f"shape {s['name']!r} not present in NIF")
        srep = {"name": s["name"], "morph_count": len(s["morphs"]), "nif_vertex_count": limit, "morphs": []}
        for m in s["morphs"]:
            idx = [e[0] for e in m["entries"]]
            nonzero = sum(1 for e in m["entries"] if any(e[1:]))
            mrep = {"name": m["name"], "scale": m["scale"] if math.isfinite(m["scale"]) else repr(m["scale"]),
                    "entries": len(idx), "nonzero": nonzero, "max_index": max(idx) if idx else None}
            tag = f"{s['name']!r}/{m['name']!r}"
            if not math.isfinite(m["scale"]):
                fails.append(f"{tag}: non-finite scale {m['scale']!r}")
            if len(set(idx)) != len(idx):
                fails.append(f"{tag}: {len(idx) - len(set(idx))} duplicate vertex indices")
            if limit is not None and idx and max(idx) >= limit:
                fails.append(f"{tag}: index {max(idx)} out of range (NIF has {limit} vertices)")
            srep["morphs"].append(mrep)
        rep["position_shapes"].append(srep)
    rep["ok"] = not fails
    return rep, pos_shapes


# ---------------------------------------------------------------- compare

def scan_dir(root: Path) -> dict:
    if not root.is_dir():
        raise FormatError(f"directory not readable: {root}")
    files = {}
    for dirpath, _dirs, names in os.walk(root):
        for n in names:
            p = Path(dirpath) / n
            rel = p.relative_to(root).as_posix()
            key = rel.lower()
            if key in files:
                raise FormatError(f"case-insensitive path collision in {root}: {files[key]} vs {p}")
            files[key] = p
    return files


def diff_positions(pa: list, pb: list) -> dict:
    dists = [math.dist(a, b) for a, b in zip(pa, pb)]
    return {"changed": sum(1 for x in dists if x > EPS), "max_distance": max(dists, default=0.0),
            "identical": pa == pb}


def nif_limits(nifs: dict) -> dict:
    lim = {}
    for _rep, pos in nifs.values():
        for name, p in pos.items():
            lim[name] = min(lim.get(name, len(p)), len(p))
    return lim


def compare(a: Path, b: Path, repeat: Path | None, expect: list, tri_check: bool) -> tuple[dict, int]:
    labels = {"a": a, "b": b} | ({"repeat": repeat} if repeat else {})
    sets = {k: scan_dir(v) for k, v in labels.items()}
    rep = {"dirs": {k: str(v) for k, v in labels.items()}, "failures": [], "files": [], "nif": [], "tri": []}
    fails = rep["failures"]
    keys_a = set(sets["a"])
    for k in sets:
        if k != "a" and set(sets[k]) != keys_a:
            fails.append(f"path set a vs {k} differs: only in a {sorted(keys_a - set(sets[k]))}, "
                         f"only in {k} {sorted(set(sets[k]) - keys_a)}")
    common = sorted(set.intersection(*(set(s) for s in sets.values())))
    parsed = {}  # (label, key) -> (rep, positions)
    for key in common:
        entry = {"path": key}
        for lab in sets:
            entry[f"sha256_{lab}"] = sha256_bytes(sets[lab][key].read_bytes())
        rep["files"].append(entry)
        if key.endswith(".nif"):
            for lab in sets:
                nrep, pos = parse_nif(sets[lab][key])
                if not nrep["ok"]:
                    raise FormatError(f"{sets[lab][key]}: {nrep['errors'] + nrep['unsupported']}")
                parsed[(lab, key)] = (nrep, pos)
    if repeat:
        rep["repeat_hash_identical"] = all(f["sha256_b"] == f["sha256_repeat"] for f in rep["files"])
    total_changed, shapes_seen, expect_changed = 0, 0, {s: 0 for s in expect}
    for key in [k for k in common if k.endswith(".nif")]:
        pa, pb = parsed[("a", key)][1], parsed[("b", key)][1]
        nrep = {"path": key, "shapes": []}
        if set(pa) != set(pb):
            fails.append(f"{key}: shape names differ a={sorted(pa)} b={sorted(pb)}")
        for name in sorted(set(pa) & set(pb)):
            shapes_seen += 1
            s = {"name": name, "vertices_a": len(pa[name]), "vertices_b": len(pb[name])}
            if len(pa[name]) != len(pb[name]):
                fails.append(f"{key}:{name}: vertex count a={len(pa[name])} b={len(pb[name])}")
            else:
                s["a_vs_b"] = diff_positions(pa[name], pb[name])
                total_changed += s["a_vs_b"]["changed"]
                if name in expect_changed:
                    expect_changed[name] += s["a_vs_b"]["changed"]
            if repeat:
                pr = parsed[("repeat", key)][1].get(name)
                if pr is None or len(pr) != len(pb[name]):
                    fails.append(f"{key}:{name}: repeat shape missing or vertex count differs")
                else:
                    s["b_vs_repeat"] = diff_positions(pb[name], pr)
                    if not s["b_vs_repeat"]["identical"]:
                        fails.append(f"{key}:{name}: repeat vertices differ from b "
                                     f"({s['b_vs_repeat']['changed']} changed)")
            nrep["shapes"].append(s)
        if repeat and set(parsed[("repeat", key)][1]) != set(pb):
            fails.append(f"{key}: repeat shape names differ from b")
        rep["nif"].append(nrep)
    if shapes_seen == 0:
        fails.append("no NIF shapes compared (nothing to verify)")
    elif total_changed == 0:
        fails.append("no vertex changed between a and b in any shape (preset probably not applied)")
    for name, n in expect_changed.items():
        if n == 0:
            fails.append(f"--expect-changed {name!r}: no changed vertices in any NIF")
    rep["expect_changed"] = expect_changed
    if tri_check:
        for key in [k for k in common if k.endswith(".tri")]:
            stem = key[:-4]
            for lab in sets:
                stems = (stem, stem + "_0", stem + "_1")
                sib = {k: v for k, v in parsed.items() if k[0] == lab and k[1].endswith(".nif")
                       and k[1][:-4] in stems}
                limits = nif_limits(sib) if sib else None
                trep, raw = parse_tri(sets[lab][key], limits)
                if limits is None:
                    trep["check_failures"].append("no matching NIF for TRI index check")
                    trep["ok"] = False
                if not trep["ok"]:
                    fails.append(f"{lab}:{key}: TRI check failed: {trep['check_failures']}")
                parsed[(lab, key)] = (trep, raw)
                rep["tri"].append({"label": lab, "path": key, "ok": trep["ok"], "sha256": trep["sha256"],
                                   "morph_counts": {s["name"]: s["morph_count"] for s in trep["position_shapes"]},
                                   "trailing_unparsed_bytes": trep["trailing_unparsed_bytes"]})
            if repeat and parsed[("b", key)][1] != parsed[("repeat", key)][1]:
                fails.append(f"{key}: repeat TRI position morphs differ from b")
    rep["ok"] = not fails
    return rep, (0 if not fails else 1)


# ---------------------------------------------------------------- CLI

def emit(obj: dict, out: str | None) -> None:
    text = json.dumps(obj, ensure_ascii=False, indent=2)
    print(text)
    if out:
        Path(out).write_text(text + "\n", encoding="utf-8")


def main(argv: list | None = None) -> int:
    ap = argparse.ArgumentParser(description="BodySlide NIF/TRI 驗收解析器（唯讀；exit 0 符合／1 期望不符／2 輸入錯誤）")
    ap.add_argument("--out", help="另外把 JSON 寫到此檔")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("nif", help="解析 SSE NIF 的 shape／skin partition／BODYTRI")
    p.add_argument("file")
    p = sub.add_parser("tri", help="解析 PIRT TRI；--nif 用 NIF 頂點數驗 index 界內")
    p.add_argument("file")
    p.add_argument("--nif", help="對照的 NIF")
    p = sub.add_parser("compare", help="A／B／B-repeat 目錄比對")
    p.add_argument("--a", required=True)
    p.add_argument("--b", required=True)
    p.add_argument("--repeat")
    p.add_argument("--expect-changed", nargs="+", default=[], metavar="SHAPE")
    p.add_argument("--tri-check", action="store_true", help="解析並驗證各目錄的 .tri")
    args = ap.parse_args(argv)
    try:
        if args.cmd == "nif":
            rep, _ = parse_nif(Path(args.file))
            emit(rep, args.out)
            return 0 if rep["ok"] else 2
        if args.cmd == "tri":
            limits = None
            if args.nif:
                nrep, pos = parse_nif(Path(args.nif))
                if not nrep["ok"]:
                    raise FormatError(f"{args.nif}: {nrep['errors'] + nrep['unsupported']}")
                limits = {k: len(v) for k, v in pos.items()}
            rep, _ = parse_tri(Path(args.file), limits)
            emit(rep, args.out)
            return 0 if rep["ok"] else 1
        rep, code = compare(Path(args.a), Path(args.b), Path(args.repeat) if args.repeat else None,
                            args.expect_changed, args.tri_check)
        emit(rep, args.out)
        return code
    except (FormatError, OSError) as e:
        emit({"ok": False, "error": f"{type(e).__name__}: {e}"}, args.out)
        return 2


if __name__ == "__main__":
    sys.exit(main())
