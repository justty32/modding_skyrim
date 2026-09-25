"""fix_moved_links 對 $fmt 路徑代號的重寫（common/data-files-fmt.md）。"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from test_tabledb import run_raw, wr  # noqa: E402
from test_tabledb_fmt import fmt, mkgit, wrjson  # noqa: E402

def text(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


FIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fix_moved_links.py")


class MovedFmtTest(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.TemporaryDirectory()
        self.base = os.path.realpath(self.d.name)
        self.data, self.vars = mkgit(self.base)
        self.top = self.vars["gitTop"]
        self.jp = os.path.join(self.data, "x.json")
        wrjson(self.jp, [
            {"id": "1", "doc_path": fmt("${gitTop}/a.md#錨"), "note": ""},
            {"id": "2", "doc_path": fmt("${gitRoot}/c.md"), "note": ""},
            {"id": "3", "doc_path": "",
             "note": fmt("見 [a](${gitTop}/a.md) 與 [c](${gitRoot}/c.md)")},
            {"id": "4", "doc_path": fmt("${fileDirname}/d.md"), "note": "見 [b](../../b.md)"},
        ], source=fmt("${gitParent}/b.md"))

    def tearDown(self):
        self.d.cleanup()

    def move(self, *pairs):
        """實際搬檔並套用 moves.tsv（路徑相對 top）；回 stdout。"""
        tsv = os.path.join(self.base, "moves.tsv")
        for old, new in pairs:
            dst = os.path.join(self.top, new)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.move(os.path.join(self.top, old), dst)
        wr(tsv, "".join("%s\t%s\n" % p for p in pairs))
        p = subprocess.run([sys.executable, FIX, "--root", self.top, "--apply", tsv],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        return p.stdout

    def rows(self, path):
        return json.loads(text(path))

    def test_moved_target_keeps_directive_and_switches_var(self):
        # ${gitRoot}/c.md 搬到 gitRoot 外 → 改用包含它的最內層代號 gitParent
        self.move(("mid/inner/c.md", "mid/c2.md"))
        raw = self.rows(self.jp)
        self.assertEqual(raw["rows"][1]["doc_path"], {"$fmt": "${gitParent}/c2.md"})
        # 同一模板裡兩個連結只搬一個：另一個原樣
        self.assertEqual(raw["rows"][2]["note"],
                         {"$fmt": "見 [a](${gitTop}/a.md) 與 [c](${gitParent}/c2.md)"})
        self.assertEqual(raw["rows"][0]["doc_path"], {"$fmt": "${gitTop}/a.md#錨"})
        self.assertEqual(raw["source"], {"$fmt": "${gitParent}/b.md"})
        self.assertEqual(run_raw(self.jp, "check"), (0, []))

    def test_json_moved_to_outer_repo_recomputes_vars(self):
        # json 從 inner repo 搬到 top 底下：gitRoot/gitParent 換了目錄，值要重算
        self.move(("mid/inner/data/x.json", "data2/x.json"))
        jp = os.path.join(self.top, "data2", "x.json")
        raw = self.rows(jp)
        self.assertEqual([r["doc_path"] for r in raw["rows"]], [
            {"$fmt": "${gitTop}/a.md#錨"},                  # gitTop 沒變 → 原樣
            {"$fmt": "${gitRoot}/mid/inner/c.md"},          # gitRoot 由 inner 變成 top
            "",
            {"$fmt": "${gitRoot}/mid/inner/data/d.md"},     # fileDirname 已不含目標
        ])
        self.assertEqual(raw["rows"][2]["note"],
                         {"$fmt": "見 [a](${gitTop}/a.md) 與 [c](${gitRoot}/mid/inner/c.md)"})
        self.assertEqual(raw["rows"][3]["note"], "見 [b](../mid/b.md)")  # 沒用代號的照舊
        self.assertEqual(raw["source"], {"$fmt": "${gitParent}/mid/b.md"})
        self.assertEqual(run_raw(jp, "check"), (0, []))

    def test_dry_run_reports_without_writing(self):
        before = text(self.jp)
        shutil.move(os.path.join(self.top, "a.md"), os.path.join(self.top, "mid", "a.md"))
        tsv = os.path.join(self.base, "m.tsv")
        wr(tsv, "a.md\tmid/a.md\n")
        p = subprocess.run([sys.executable, FIX, "--root", self.top, tsv],
                           capture_output=True, text=True)
        self.assertIn("dry-run", p.stdout)
        self.assertIn("${gitTop}/mid/a.md", p.stdout)  # 同代號、只換相對段
        self.assertEqual(text(self.jp), before)


if __name__ == "__main__":
    unittest.main()
