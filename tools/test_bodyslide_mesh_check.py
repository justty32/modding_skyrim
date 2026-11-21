"""bodyslide_mesh_check 的測試：fixture 全部在測試內合成，不含任何 mod 的 NIF／TRI。

真實檔 smoke：設 BODYSLIDE_REAL_NIF／BODYSLIDE_REAL_TRI 才跑。
"""
from __future__ import annotations

import contextlib
import io
import json
import os
import shutil
import struct
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bodyslide_mesh_check as m  # noqa: E402

VF_VERTEX, VF_UV, VF_SKINNED, VF_FULLPREC = 0x1, 0x2, 0x40, 0x400


def desc(vsize: int, uv_off: int, flags: int) -> int:
    return (vsize // 4) | ((uv_off // 4) << 8) | (flags << 44)


FULL = dict(vsize=20, desc=desc(20, 16, VF_VERTEX | VF_UV))        # float3+bitangent(4)+uv
HALF = dict(vsize=12, desc=desc(12, 8, VF_VERTEX | VF_UV))         # half3+bitangent(2)+uv


def vbytes(verts, fmt: dict) -> bytes:
    full = fmt["vsize"] == 20
    out = b""
    for v in verts:
        out += struct.pack("<3ff", *v, 0.0) if full else struct.pack("<3ee", *v, 0.0)
        out += struct.pack("<2e", 0.0, 0.0)
    return out


class NifBuilder:
    def __init__(self):
        self.blocks, self.strings = [], []

    def s(self, text: str) -> int:
        if text not in self.strings:
            self.strings.append(text)
        return self.strings.index(text)

    def add(self, typ: str, data: bytes = b"") -> int:
        self.blocks.append([typ, data])
        return len(self.blocks) - 1

    def set(self, idx: int, data: bytes) -> None:
        self.blocks[idx][1] = data

    def shape(self, name, verts=(), fmt=FULL, skin=-1, extra=(), typ="BSTriShape", tris=()):
        data = vbytes(verts, fmt) + b"".join(struct.pack("<3H", *t) for t in tris)
        b = struct.pack("<II", self.s(name), len(extra)) + b"".join(struct.pack("<i", e) for e in extra)
        b += struct.pack("<iI3f9ffi4f", -1, 14, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1.0, -1, 0, 0, 0, 50)
        b += struct.pack("<iiiQHHI", skin, -1, -1, fmt["desc"], len(tris), len(verts), len(data)) + data
        b += struct.pack("<I", 0)
        if typ == "BSDynamicTriShape":
            b += struct.pack("<I", 0)
        return self.add(typ, b)

    def skin(self, partition_idx: int, typ="BSDismemberSkinInstance") -> int:
        b = struct.pack("<iiiI", -1, partition_idx, -1, 0) + (struct.pack("<I", 0) if typ != "NiSkinInstance" else b"")
        return self.add(typ, b)

    def partition(self, verts, parts, fmt=FULL) -> int:
        vd = vbytes(verts, fmt)
        b = struct.pack("<IIIQ", len(parts), len(vd), fmt["vsize"], fmt["desc"]) + vd
        for vmap, ntri in parts:
            nv = len(vmap)
            b += struct.pack("<HHHHH", nv, ntri, 1, 0, 1) + struct.pack("<H", 0)
            b += struct.pack("<B", 1) + struct.pack(f"<{nv}H", *vmap)
            b += struct.pack("<B", 1) + struct.pack(f"<{nv}f", *([1.0] * nv))
            b += struct.pack("<B", 1) + struct.pack("<3H", 0, 1, 2) * ntri
            b += struct.pack("<B", 1) + bytes(nv)
            b += struct.pack("<BBQ", 0, 1, fmt["desc"]) + struct.pack("<3H", 0, 1, 2) * ntri
        return self.add("NiSkinPartition", b)

    def string_extra(self, name: str, value: str) -> int:
        return self.add("NiStringExtraData", struct.pack("<II", self.s(name), self.s(value)))

    def build(self, bs_version=100) -> bytes:
        types = []
        for t, _ in self.blocks:
            if t not in types:
                types.append(t)
        h = b"Gamebryo File Format, Version 20.2.0.7\n" + struct.pack("<IBII", 0x14020007, 1, 12, len(self.blocks))
        h += struct.pack("<I", bs_version) + b"\x01\x00" * 3
        h += struct.pack("<H", len(types)) + b"".join(struct.pack("<I", len(t)) + t.encode() for t in types)
        h += b"".join(struct.pack("<H", types.index(t)) for t, _ in self.blocks)
        h += b"".join(struct.pack("<I", len(d)) for _, d in self.blocks)
        h += struct.pack("<II", len(self.strings), max((len(x) for x in self.strings), default=0))
        h += b"".join(struct.pack("<I", len(x)) + x.encode() for x in self.strings) + struct.pack("<I", 0)
        return h + b"".join(d for _, d in self.blocks) + struct.pack("<Ii", 1, 0)


def skinned_nif(verts, fmt=FULL, parts=None, bodytri=None, shape="Body") -> bytes:
    nb = NifBuilder()
    root = nb.add("NiNode", b"\x00" * 12)  # 未知但合法的 block：只計數不解析
    sh = nb.shape(shape, (), fmt)          # inline count=0, data_size=0
    part = nb.partition(verts, parts or [(list(range(len(verts))), 1)], fmt)
    sk = nb.skin(part)
    extra = []
    if bodytri:
        extra = [nb.string_extra("BODYTRI", bodytri)]
    b = nb.blocks[sh][1]
    nb.set(sh, b[:4] + struct.pack("<I", len(extra)) + b"".join(struct.pack("<i", e) for e in extra)
           + b[8:88] + struct.pack("<i", sk) + b[92:])
    del root
    return nb.build()


def tri_bytes(shapes, uv=None, scale=1.0) -> bytes:
    def section(spec, dims):
        b = struct.pack("<H", len(spec))
        for sname, morphs in spec:
            b += struct.pack("<B", len(sname)) + sname.encode() + struct.pack("<H", len(morphs))
            for mname, entries in morphs:
                b += struct.pack("<B", len(mname)) + mname.encode() + struct.pack("<fH", scale, len(entries))
                b += b"".join(struct.pack("<H" + "h" * dims, *e) for e in entries)
        return b
    return b"PIRT" + section(shapes, 3) + (section(uv, 2) if uv is not None else b"")


V3 = [(0.0, 0.0, 0.0), (1.0, 2.0, 3.0), (4.5, -1.25, 8.0)]


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)

    def write(self, rel: str, data: bytes) -> Path:
        p = self.tmp / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
        return p

    def run_cli(self, *args):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = m.main([str(a) for a in args])
        return code, json.loads(buf.getvalue())


class NifTests(Base):
    def test_skinned_inline_zero_uses_partition_vertices(self):
        code, r = self.run_cli("nif", self.write("a.nif", skinned_nif(V3)))
        self.assertEqual(code, 0, r)
        s = r["shapes"][0]
        self.assertEqual((s["inline_num_vertices"], s["inline_data_size"]), (0, 0))
        self.assertEqual(s["vertex_count"], 3)
        self.assertEqual(s["vertex_source"], "skin_partition")
        self.assertEqual(s["skin_instance_type"], "BSDismemberSkinInstance")
        self.assertEqual(s["skin_partition"]["vertex_size"], 20)
        self.assertEqual(r["block_types"]["NiNode"], 1)

    def test_full_precision_positions(self):
        _rep, pos = m.parse_nif(self.write("a.nif", skinned_nif(V3, FULL)))
        self.assertEqual(pos["Body"], V3)

    def test_half_precision_positions(self):
        rep, pos = m.parse_nif(self.write("a.nif", skinned_nif(V3, HALF)))
        self.assertEqual(rep["shapes"][0]["skin_partition"]["position_format"], "half3")
        self.assertEqual(pos["Body"], V3)  # 這些值在 half 可精確表示

    def test_fullprec_flag_wins(self):
        self.assertTrue(m.position_full_precision(desc(8, 0, VF_VERTEX | VF_FULLPREC))[0])
        self.assertFalse(m.position_full_precision(desc(8, 0, VF_VERTEX))[0])

    def test_two_partitions(self):
        verts = V3 + [(9.0, 9.0, 9.0)]
        _c, r = self.run_cli("nif", self.write("a.nif", skinned_nif(verts, parts=[([0, 1, 2], 1), ([1, 2, 3], 2)])))
        p = r["shapes"][0]["skin_partition"]
        self.assertEqual(p["partition_count"], 2)
        self.assertEqual([(x["vertices"], x["triangles"]) for x in p["partitions"]], [(3, 1), (3, 2)])
        self.assertEqual(r["shapes"][0]["vertex_count"], 4)

    def test_inline_unskinned_shape(self):
        nb = NifBuilder()
        nb.shape("Static", V3, FULL, tris=[(0, 1, 2)])
        code, r = self.run_cli("nif", self.write("a.nif", nb.build()))
        self.assertEqual(code, 0, r)
        self.assertEqual((r["shapes"][0]["vertex_count"], r["shapes"][0]["vertex_source"]), (3, "inline"))

    def test_bodytri_string(self):
        _c, r = self.run_cli("nif", self.write("a.nif", skinned_nif(V3, bodytri="clothes\\x\\a.tri")))
        self.assertEqual(r["bodytri"][0]["value"], "clothes\\x\\a.tri")
        self.assertEqual(r["bodytri"][0]["attached_to"], ["Body"])

    def test_wrong_bs_version_exit2(self):
        nb = NifBuilder()
        nb.shape("S", V3)
        code, r = self.run_cli("nif", self.write("a.nif", nb.build(bs_version=83)))
        self.assertEqual(code, 2)
        self.assertIn("BS stream version 83", r["error"])

    def test_truncated_exit2(self):
        code, _r = self.run_cli("nif", self.write("a.nif", skinned_nif(V3)[:200]))
        self.assertEqual(code, 2)

    def test_unsupported_geometry_listed_exit2(self):
        nb = NifBuilder()
        nb.add("NiTriShape", b"\x00" * 8)
        code, r = self.run_cli("nif", self.write("a.nif", nb.build()))
        self.assertEqual(code, 2)
        self.assertTrue(any("NiTriShape" in u for u in r["unsupported"]))

    def test_missing_partition_is_error_not_zero(self):
        nb = NifBuilder()
        sh = nb.shape("S", ())
        sk = nb.skin(99)
        b = nb.blocks[sh][1]
        nb.set(sh, b[:88] + struct.pack("<i", sk) + b[92:])
        code, r = self.run_cli("nif", self.write("a.nif", nb.build()))
        self.assertEqual(code, 2)
        self.assertTrue(r["errors"])


class TriTests(Base):
    def nif(self, n=3):
        return self.write("a.nif", skinned_nif(V3[:n] if n <= 3 else V3 + [(0, 0, 0)] * (n - 3)))

    def test_normal_with_uv(self):
        t = self.write("a.tri", tri_bytes([("Body", [("Breasts", [(0, 1, 2, 3), (2, 0, 0, 0)])])],
                                          uv=[("Body", [("UVm", [(1, 5, 5)])])]))
        code, r = self.run_cli("tri", t, "--nif", self.nif())
        self.assertEqual(code, 0, r)
        mo = r["position_shapes"][0]["morphs"][0]
        self.assertEqual((mo["entries"], mo["nonzero"], r["trailing_unparsed_bytes"]), (2, 1, 0))
        self.assertEqual(r["uv"]["shapes"][0]["morph_count"], 1)

    def test_index_out_of_range_with_nif(self):
        t = self.write("a.tri", tri_bytes([("Body", [("Breasts", [(3, 1, 1, 1)])])]))
        self.assertEqual(self.run_cli("tri", t)[0], 0)  # 沒 --nif 無從判斷
        code, r = self.run_cli("tri", t, "--nif", self.nif())
        self.assertEqual(code, 1)
        self.assertIn("out of range", " ".join(r["check_failures"]))

    def test_nonfinite_scale(self):
        t = self.write("a.tri", tri_bytes([("Body", [("B", [(0, 1, 1, 1)])])], scale=float("nan")))
        code, r = self.run_cli("tri", t)
        self.assertEqual(code, 1)
        self.assertIn("non-finite scale", " ".join(r["check_failures"]))

    def test_duplicate_index(self):
        t = self.write("a.tri", tri_bytes([("Body", [("B", [(0, 1, 1, 1), (0, 2, 2, 2)])])]))
        self.assertEqual(self.run_cli("tri", t)[0], 1)

    def test_truncated_exit2(self):
        t = self.write("a.tri", tri_bytes([("Body", [("B", [(0, 1, 1, 1)])])])[:-3])
        self.assertEqual(self.run_cli("tri", t)[0], 2)

    def test_bad_magic_exit2(self):
        self.assertEqual(self.run_cli("tri", self.write("a.tri", b"XXXX\x00\x00"))[0], 2)

    def test_trailing_garbage_reported(self):
        t = self.write("a.tri", tri_bytes([("Body", [("B", [(0, 1, 1, 1)])])]) + b"\x07")
        code, r = self.run_cli("tri", t)
        self.assertEqual(code, 1)
        self.assertEqual(r["trailing_unparsed_bytes"], 1)


class CompareTests(Base):
    VB = [(0.0, 0.0, 0.0), (1.0, 2.5, 3.0), (4.5, -1.25, 8.0)]

    def make(self, label, verts=V3, extra=None, name="meshes/x/robef_0.nif"):
        self.write(f"{label}/{name}", skinned_nif(verts, shape="FC4"))
        self.write(f"{label}/meshes/x/robef.tri", tri_bytes([("FC4", [("Breasts", [(1, 0, 5, 0)])])]))
        if extra:
            self.write(f"{label}/{extra}", b"x")
        return self.tmp / label

    def cmp(self, *extra):
        return self.run_cli("compare", "--a", self.tmp / "a", "--b", self.tmp / "b", *extra)

    def test_pass(self):
        self.make("a"); self.make("b", self.VB); self.make("r", self.VB)
        code, r = self.cmp("--repeat", self.tmp / "r", "--expect-changed", "FC4", "--tri-check")
        self.assertEqual(code, 0, r["failures"])
        s = r["nif"][0]["shapes"][0]
        self.assertEqual(s["a_vs_b"]["changed"], 1)
        self.assertAlmostEqual(s["a_vs_b"]["max_distance"], 0.5)
        self.assertTrue(r["repeat_hash_identical"])

    def test_a_equals_b_fails(self):
        self.make("a"); self.make("b")
        code, r = self.cmp()
        self.assertEqual(code, 1)
        self.assertIn("preset probably not applied", " ".join(r["failures"]))

    def test_repeat_differs_fails(self):
        self.make("a"); self.make("b", self.VB); self.make("r", [(0.0, 0.0, 0.0), (1.0, 2.5, 3.0), (4.5, -1.25, 8.5)])
        code, r = self.cmp("--repeat", self.tmp / "r")
        self.assertEqual(code, 1)
        self.assertIn("repeat vertices differ", " ".join(r["failures"]))

    def test_path_set_differs_fails(self):
        self.make("a"); self.make("b", self.VB, extra="meshes/x/extra.nif.bak")
        code, r = self.cmp()
        self.assertEqual(code, 1)
        self.assertIn("path set", " ".join(r["failures"]))

    def test_case_insensitive_path_match(self):
        self.make("a"); self.make("b", self.VB, name="Meshes/X/ROBEF_0.NIF")
        self.assertEqual(self.cmp()[0], 0)

    def test_expect_changed_unchanged_shape_fails(self):
        self.make("a"); self.make("b", self.VB)
        code, r = self.cmp("--expect-changed", "Nope")
        self.assertEqual(code, 1)
        self.assertIn("Nope", " ".join(r["failures"]))

    def test_tri_check_index_out_of_range_fails(self):
        self.make("a"); self.make("b", self.VB)
        self.write("b/meshes/x/robef.tri", tri_bytes([("FC4", [("Breasts", [(7, 0, 5, 0)])])]))
        code, r = self.cmp("--tri-check")
        self.assertEqual(code, 1)
        self.assertIn("TRI check failed", " ".join(r["failures"]))

    def test_bad_file_exit2(self):
        self.make("a"); self.make("b", self.VB)
        self.write("b/meshes/x/robef_0.nif", b"Gamebryo File Format, Version 20.2.0.7\n\x00")
        self.assertEqual(self.cmp()[0], 2)

    def test_missing_dir_exit2(self):
        self.make("a")
        self.assertEqual(self.cmp()[0], 2)

    def test_no_nif_fails(self):
        self.write("a/readme.txt", b"x"); self.write("b/readme.txt", b"x")
        self.assertEqual(self.cmp()[0], 1)


class RealFileSmoke(unittest.TestCase):
    def test_real_files(self):
        nif, tri = os.environ.get("BODYSLIDE_REAL_NIF"), os.environ.get("BODYSLIDE_REAL_TRI")
        if not nif and not tri:
            self.skipTest("BODYSLIDE_REAL_NIF / BODYSLIDE_REAL_TRI not set")
        limits = None
        if nif:
            rep, pos = m.parse_nif(Path(nif))
            self.assertTrue(rep["ok"], rep["errors"] + rep["unsupported"])
            self.assertTrue(rep["shapes"])
            self.assertTrue(all(s["vertex_count"] > 0 for s in rep["shapes"]))
            limits = {k: len(v) for k, v in pos.items()}
        if tri:
            rep, _raw = m.parse_tri(Path(tri), limits)
            self.assertTrue(rep["ok"], rep["check_failures"])


if __name__ == "__main__":
    unittest.main()
