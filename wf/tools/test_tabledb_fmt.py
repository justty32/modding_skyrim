"""$fmt 路徑代號（common/data-files-fmt.md）的測試；搬檔那半在 test_fix_moved_links.py。"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from test_tabledb import CLI, run, run_raw, wr  # noqa: E402


def mkgit(base):
    """top/.git（目錄）／top/mid/.git（檔）／top/mid/inner/.git（目錄），json 放 inner/data/。

    回 (data 目錄, {代號: 目錄})。
    """
    top = os.path.join(base, "top")
    mid, inner = os.path.join(top, "mid"), os.path.join(top, "mid", "inner")
    data = os.path.join(inner, "data")
    os.makedirs(os.path.join(inner, ".git"))
    os.makedirs(os.path.join(top, ".git"))
    os.makedirs(data)
    wr(os.path.join(mid, ".git"), "gitdir: ../../elsewhere/.git\n")
    for d, name in ((top, "a.md"), (mid, "b.md"), (inner, "c.md"), (data, "d.md")):
        wr(os.path.join(d, name), name + "\n")
    return data, {"gitTop": top, "gitParent": mid, "gitRoot": inner, "fileDirname": data}


def wrjson(path, rows, **meta):
    m = {"contract": "wf-table/1", "columns": ["id", "doc_path", "note"],
         "link_columns": ["doc_path"]}
    m.update(meta)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(dict(m, rows=rows), f, ensure_ascii=False)


def fmt(s):
    return {"$fmt": s}


class FmtTest(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.TemporaryDirectory()
        self.data, self.vars = mkgit(os.path.realpath(self.d.name))
        self.jp = os.path.join(self.data, "x.json")
        wrjson(self.jp, [
            {"id": "1", "doc_path": fmt("${gitTop}/a.md#錨"),
             "note": fmt("見 [b](${gitParent}/b.md)")},
            {"id": "2", "doc_path": fmt("${gitRoot}/c.md"),
             "note": fmt("見 [d](${fileDirname}/d.md)")},
            {"id": "3", "doc_path": fmt("${gitTop}/no1.md"),
             "note": fmt("[x](${gitParent}/no2.md)、[y](${gitRoot}/no3.md)"
                         "、[z](${fileDirname}/no4.md)")},
        ])

    def tearDown(self):
        self.d.cleanup()

    def test_fmt_command_expands_four_vars(self):
        es = run(self.jp, "fmt")
        self.assertEqual(len(es), 6)
        e = es[0]
        self.assertEqual((e["index"], e["column"], e["raw"]),
                         (0, "doc_path", "${gitTop}/a.md#錨"))
        self.assertEqual(e["expanded"], os.path.join(self.vars["gitTop"], "a.md#錨"))
        self.assertEqual(es[3]["expanded"],
                         "見 [d](%s)" % os.path.join(self.vars["fileDirname"], "d.md"))
        self.assertEqual(run_raw(self.jp, "fmt")[0], 0)

    def test_links_are_relative_to_json_dir(self):
        es = run(self.jp, "links")
        got = [(e["index"], e["column"], e["target"], e["exists"]) for e in es[:4]]
        self.assertEqual(got, [
            (0, "doc_path", "../../../a.md#錨", True),   # gitTop，連結欄裸值 + 錨點
            (0, "note", "../../b.md", True),             # gitParent，md 連結
            (1, "doc_path", "../c.md", True),            # gitRoot
            (1, "note", "d.md", True),                   # fileDirname
        ])
        self.assertEqual(es[0]["resolved"], os.path.join(self.vars["gitTop"], "a.md"))
        self.assertEqual(es[0]["raw"], "${gitTop}/a.md#錨")
        # open／resolve 行為不變
        self.assertEqual(run(self.jp, "open", "1")["content"], "c.md\n")
        self.assertEqual(run("resolve", self.jp, "1", "note")["target"], "d.md")

    def test_check_lists_only_missing_with_raw(self):
        code, bad = run_raw(self.jp, "check")
        self.assertEqual(code, 1)
        self.assertEqual([(b["index"], b["target"]) for b in bad], [
            (2, "../../../no1.md"), (2, "../../no2.md"),
            (2, "../no3.md"), (2, "no4.md")])
        self.assertEqual(bad[0]["raw"], "${gitTop}/no1.md")
        self.assertTrue(all(not b["exists"] and b["resolved"] for b in bad))

    def test_get_returns_directive_verbatim(self):
        self.assertEqual(run(self.jp, "get", "0")["doc_path"], {"$fmt": "${gitTop}/a.md#錨"})
        self.assertEqual(run(self.jp, "grep", "gitRoot")[0]["id"], "2")
        self.assertEqual(run(self.jp, "--slice", "0", "1")[0]["doc_path"],
                         {"$fmt": "${gitTop}/a.md#錨"})

    def test_meta_source_directive(self):
        # source 由 fmt 列出（index null），但 entries／check 不列它
        wrjson(self.jp, [{"id": "1", "doc_path": "d.md"}], source=fmt("${gitParent}/no.md"))
        self.assertEqual(run(self.jp, "fmt"), [
            {"index": None, "column": "source", "raw": "${gitParent}/no.md",
             "expanded": os.path.join(self.vars["gitParent"], "no.md")}])
        self.assertEqual(run_raw(self.jp, "check"), (0, []))

    def test_env_variable(self):
        os.environ["WF_FMT_T"], os.environ["WF_FMT_E"] = self.vars["gitTop"], ""
        os.environ.pop("WF_FMT_MISSING", None)
        wrjson(self.jp, [{"id": "1", "doc_path": fmt("${env:WF_FMT_T}/a.md")},
                         {"id": "2", "note": fmt("空[<${env:WF_FMT_E}>]")},
                         {"id": "3", "doc_path": fmt("${env:WF_FMT_MISSING}/a.md")}])
        es = run_raw(self.jp, "fmt")[1]
        self.assertEqual(es[0]["expanded"], os.path.join(self.vars["gitTop"], "a.md"))
        self.assertEqual(es[1]["expanded"], "空[<>]")
        self.assertIsNone(es[2]["expanded"])
        self.assertIn("WF_FMT_MISSING", es[2]["error"])
        code, bad = run_raw(self.jp, "check")
        self.assertEqual((code, len(bad)), (1, 1))
        self.assertEqual((bad[0]["target"], bad[0]["resolved"]), (None, None))

    def test_bad_directives_and_unknown_var(self):
        wrjson(self.jp, [
            {"id": "1", "doc_path": {"$fmt": 1}},
            {"id": "2", "doc_path": {"$fmt": "${gitRoot}/c.md", "y": 1}},
            {"id": "3", "note": fmt("[a](${nope}/c.md)")},
            {"id": "4", "note": {"ref": "[c](../c.md)"}, "doc_path": "d.md"},
        ])
        code, bad = run_raw(self.jp, "check")
        self.assertEqual(code, 1)
        self.assertEqual([b["index"] for b in bad], [0, 1, 2])
        self.assertTrue(all(b["error"] and b["exists"] is False for b in bad))
        self.assertIn("$fmt", bad[0]["error"])
        self.assertIn("${nope}", bad[2]["error"])
        self.assertEqual(run_raw(self.jp, "fmt")[0], 1)
        code, err = run_raw(self.jp, "resolve", "2")   # pick 跳過 error 項
        self.assertEqual((code, "error" in err), (1, True))
        # 普通巢狀物件照舊抽連結、不受影響
        ok = [e for e in run_raw(self.jp, "links")[1] if e["index"] == 3]
        self.assertEqual([(e["column"], e["target"], e["exists"]) for e in ok],
                         [("doc_path", "d.md", True), ("note", "../c.md", True)])

    def test_no_git_falls_back_to_filedirname(self):
        with tempfile.TemporaryDirectory() as bare:
            bare = os.path.realpath(bare)
            wr(os.path.join(bare, "e.md"), "E\n")
            jp = os.path.join(bare, "y.json")
            wrjson(jp, [{"id": "1", "doc_path": fmt("${gitRoot}/e.md"),
                         "note": fmt("[p](${gitParent}/e.md)、[t](${gitTop}/e.md)")}])
            p = subprocess.run([sys.executable, CLI, jp, "check"],
                               capture_output=True, text=True)
            self.assertEqual((p.returncode, json.loads(p.stdout)), (0, []))
            self.assertEqual(p.stderr.count("no .git"), 1)
            self.assertIn(bare, p.stderr)
            for e in run(jp, "fmt"):
                self.assertIn(os.path.join(bare, "e.md"), e["expanded"])


if __name__ == "__main__":
    unittest.main()
