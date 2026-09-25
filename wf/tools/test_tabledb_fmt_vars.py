"""fmt-vars.json（wf-fmt-vars/1）：變數名字是資料，程式只實作 how。"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from test_tabledb import run, run_raw, wr  # noqa: E402
from test_tabledb_fmt import fmt, mkgit, wrjson  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(HERE, "fix_moved_links.py")
KERNEL = json.load(open(os.path.join(HERE, "fmt-vars.json"), encoding="utf-8"))


def var(name, how, aliases=()):
    return {"name": name, "how": how, "doc": name, "aliases": list(aliases)}


def put(d, vars_, name="fmt-vars.json", ns=None):
    """把一份 fmt-vars(.local).json 放到目錄 d。"""
    os.makedirs(d, exist_ok=True)
    body = {"contract": "wf-fmt-vars/1", "vars": vars_}
    if ns is not None:
        body["namespaces"] = ns
    wr(os.path.join(d, name), json.dumps(body, ensure_ascii=False))


class FmtVarsTest(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.TemporaryDirectory()
        self.base = os.path.realpath(self.d.name)
        self.data, self.vars = mkgit(self.base)
        self.tools = os.path.join(self.vars["gitRoot"], "tools")   # json 所在 repo 的 tools/
        self.jp = os.path.join(self.data, "x.json")

    def tearDown(self):
        self.d.cleanup()

    def rows(self, *rows):
        wrjson(self.jp, list(rows))

    def test_alias_and_load_order_from_json_repo(self):
        # 變數檔放在 json 所在 repo 的 tools/：別名 gitSelf 只有這份有，腳本同目錄那份沒有
        put(self.tools, [var("gitRoot", "git-self", ["gitSelf"])] + KERNEL["vars"][:1])
        self.rows({"id": "1", "doc_path": fmt("${gitSelf}/c.md")},
                  {"id": "2", "doc_path": fmt("${fileDirname}/d.md")})
        es = run(self.jp, "links")
        self.assertEqual([(e["target"], e["exists"]) for e in es],
                         [("../c.md", True), ("d.md", True)])
        self.assertEqual(run(self.jp, "fmt", "--vars")["files"],
                         [os.path.join(self.tools, "fmt-vars.json")])
        # 這份沒有 gitTop → 未知名字，訊息要指路
        self.rows({"id": "1", "doc_path": fmt("${gitTop}/a.md")})
        code, bad = run_raw(self.jp, "check")
        self.assertEqual(code, 1)
        self.assertIn("fmt --vars", bad[0]["error"])

    def test_local_overrides_and_appends(self):
        put(self.tools, KERNEL["vars"], ns=KERNEL["namespaces"])
        # local 整筆取代同名（gitRoot 改成 git-top）、並追加新變數
        put(self.tools, [var("gitRoot", "git-top"), var("here", "file-dir")],
            name="fmt-vars.local.json")
        self.rows({"id": "1", "doc_path": fmt("${gitRoot}/a.md")},   # a.md 只在 top
                  {"id": "2", "doc_path": fmt("${here}/d.md")})
        self.assertEqual(run_raw(self.jp, "check"), (0, []))
        self.assertEqual([e["target"] for e in run(self.jp, "links")],
                         ["../../../a.md", "d.md"])
        got = run(self.jp, "fmt", "--vars")
        self.assertEqual([(v["name"], v["how"], v["source"]) for v in got["vars"]],
                         [("fileDirname", "file-dir", "kernel"),
                          ("gitRoot", "git-top", "local"),
                          ("gitParent", "git-parent", "kernel"),
                          ("gitTop", "git-top", "kernel"),
                          ("here", "file-dir", "local")])
        self.assertEqual([os.path.basename(f) for f in got["files"]],
                         ["fmt-vars.json", "fmt-vars.local.json"])
        self.assertEqual(got["namespaces"][0]["prefix"], "env")

    def test_wf_tools_wins_over_tools(self):
        put(self.tools, [var("only", "file-dir")])
        put(os.path.join(self.vars["gitRoot"], "wf", "tools"), [var("both", "file-dir")])
        self.rows({"id": "1", "doc_path": fmt("${both}/d.md")})
        self.assertEqual(run_raw(self.jp, "check"), (0, []))
        self.assertIn(os.path.join("wf", "tools"), run(self.jp, "fmt", "--vars")["files"][0])

    def test_unknown_how_is_a_load_error(self):
        put(self.tools, KERNEL["vars"])
        put(self.tools, [var("gitRoot", "git-elsewhere")], name="fmt-vars.local.json")
        self.rows({"id": "1", "doc_path": fmt("${gitRoot}/c.md")})
        code, bad = run_raw(self.jp, "check")
        self.assertEqual(code, 1)
        self.assertIn("fmt-vars.local.json", bad[0]["error"])
        self.assertIn("gitRoot", bad[0]["error"])
        self.assertIn("git-elsewhere", bad[0]["error"])

    def test_vars_cli_without_file_uses_script_dir(self):
        got = run("fmt", "--vars")
        # 沒給 FILE 就以腳本所在 repo 為準；repo 同時有 wf/tools/（非侵入式自用）與 tools/ 時 wf/tools/ 優先。
        self.assertEqual(len(got["files"]), 1)
        self.assertEqual(os.path.basename(got["files"][0]), "fmt-vars.json")
        self.assertEqual(json.load(open(got["files"][0], encoding="utf-8")), KERNEL)
        self.assertEqual([v["name"] for v in got["vars"]],
                         ["fileDirname", "gitRoot", "gitParent", "gitTop"])
        self.assertTrue(all(v["source"] == "kernel" for v in got["vars"]))
        # 兩種順序等價；FILE 給了就以那份 json 的 repo 為準
        put(self.tools, [var("only", "file-dir")])
        self.rows({"id": "1", "doc_path": "d.md"})
        self.assertEqual(run("fmt", "--vars", self.jp), run(self.jp, "fmt", "--vars"))
        self.assertEqual([v["name"] for v in run("fmt", "--vars", self.jp)["vars"]], ["only"])

    def test_fix_moved_links_keeps_alias_then_switches_to_canonical(self):
        put(self.tools, [var("gitRoot", "git-self", ["gitSelf"])] + KERNEL["vars"][2:])
        self.rows({"id": "1", "doc_path": fmt("${gitSelf}/c.md")})
        top, inner = self.vars["gitTop"], self.vars["gitRoot"]

        def move(old, new):
            dst = os.path.join(top, new)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.move(os.path.join(top, old), dst)
            tsv = os.path.join(self.base, "m.tsv")
            wr(tsv, "%s\t%s\n" % (old, new))
            p = subprocess.run([sys.executable, FIX, "--root", top, "--apply", tsv],
                               capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            with open(self.jp, encoding="utf-8") as f:
                return json.load(f)["rows"][0]["doc_path"]

        # 還在 git-self 底下 → 保留 raw 用的別名
        self.assertEqual(move("mid/inner/c.md", "mid/inner/sub/c.md"),
                         {"$fmt": "${gitSelf}/sub/c.md"})
        self.assertEqual(run_raw(self.jp, "check"), (0, []))
        # 搬出 git-self → 換算法，用該算法的正式名
        self.assertEqual(move("mid/inner/sub/c.md", "mid/c2.md"),
                         {"$fmt": "${gitParent}/c2.md"})
        self.assertEqual(run_raw(self.jp, "check"), (0, []))
        self.assertEqual(os.path.basename(inner), "inner")


if __name__ == "__main__":
    unittest.main()
