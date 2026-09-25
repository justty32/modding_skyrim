import json
import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(__file__))
import tabledb  # noqa: E402
import tabledb_links  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
CLI = os.path.join(HERE, "tabledb.py")


def wr(path, text):
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def run_raw(*args):
    p = subprocess.run([sys.executable, CLI, *args], capture_output=True, text=True)
    return p.returncode, (json.loads(p.stdout) if p.stdout.strip() else None)


def run(*args):
    code, out = run_raw(*args)
    assert code == 0, (code, out)
    return out


class TableDBTest(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.TemporaryDirectory()
        self.json_path = os.path.join(self.d.name, "t.json")
        self.csv_path = os.path.join(self.d.name, "t.csv")
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump({"source": "x.md", "columns": ["id", "name", "body"],
                       "rows": [{"id": "1", "name": "甲", "body": "多行\n正文"},
                                {"id": "2", "name": "乙", "body": ""}]}, f, ensure_ascii=False)
        with open(self.csv_path, "w", encoding="utf-8", newline="") as f:
            f.write("id,name\n1,甲\n2,乙\n")

    def tearDown(self):
        self.d.cleanup()

    def test_json_crud_roundtrip(self):
        t = tabledb.load(self.json_path)
        self.assertEqual(len(t), 2)
        self.assertEqual(t.get(0)["body"], "多行\n正文")
        self.assertEqual(t.find(name="乙")[0]["id"], "2")
        i = t.add({"id": "3", "name": "丙", "extra": "new"})
        self.assertEqual(i, 2)
        self.assertIn("extra", t.columns)
        t.update(0, name="甲改")
        t.delete(1)
        t.save()
        t2 = tabledb.load(self.json_path)
        self.assertEqual([r["id"] for r in t2.rows], ["1", "3"])
        self.assertEqual(t2.get(0)["name"], "甲改")
        self.assertEqual(t2.meta["source"], "x.md")

    def test_csv_roundtrip(self):
        t = tabledb.load(self.csv_path)
        self.assertEqual(t.columns, ["id", "name"])
        t.add({"id": "3", "name": "丙"})
        t.save()
        self.assertEqual(len(tabledb.load(self.csv_path)), 3)

    def test_cli(self):
        self.assertEqual(run(self.json_path)["count"], 2)
        self.assertEqual(run(self.json_path, "get", "1")["name"], "乙")
        self.assertEqual(run(self.json_path, "find", "id=1")[0]["index"], 0)
        self.assertEqual(run(self.json_path, "grep", "正文")[0]["id"], "1")
        self.assertEqual(run(self.json_path, "add", "id=9", "name=新")["index"], 2)
        self.assertEqual(run(self.json_path, "update", "2", "name=改")["name"], "改")
        self.assertEqual(run(self.json_path, "delete", "2")["id"], "9")
        self.assertEqual(run(self.json_path)["count"], 2)
        self.assertEqual(run(self.json_path, "--slice", "0", "1")[0]["index"], 0)

    def test_kv_stores_fmt_directive_as_object(self):
        # k=v 的 v 恰好是合法 $fmt 指示詞 JSON 才存成物件，其他（含別的 JSON）一律字串
        run(self.json_path, "add", "id=9", 'name={"$fmt": "${gitRoot}/a.md"}',
            'body={"a": 1}', "extra=$fmt")
        r = run(self.json_path, "get", "2")
        self.assertEqual(r["name"], {"$fmt": "${gitRoot}/a.md"})
        self.assertEqual((r["body"], r["extra"]), ('{"a": 1}', "$fmt"))
        run(self.json_path, "update", "2", 'body={"$fmt": "見 [a](a.md)"}', 'name=["y"]')
        r = run(self.json_path, "get", "2")
        self.assertEqual((r["body"], r["name"]), ({"$fmt": "見 [a](a.md)"}, '["y"]'))

    def test_legacy_file_without_contract(self):
        # 舊檔沒有 contract 也要能開，只是 contract 報 null
        self.assertIsNone(run(self.json_path)["contract"])
        self.assertEqual(run(self.json_path, "links"), [])


class LinksTest(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.TemporaryDirectory()
        d = self.d.name
        os.mkdir(os.path.join(d, "sub"))
        wr(os.path.join(d, "a.md"), "AAA\n")
        wr(os.path.join(d, "sub", "b.md"), "BBB\n")
        self.jp = os.path.join(d, "l.json")
        with open(self.jp, "w", encoding="utf-8") as f:
            json.dump({"contract": "wf-table/1", "source": "x.md", "extracted": "2026-08-30",
                       "columns": ["id", "doc_path", "note", "site", "extra"],
                       "link_columns": ["doc_path"],
                       "rows": [{"id": "1", "doc_path": "a.md#用法",
                                 "note": "見 [b](sub/b.md)", "site": "https://example.com",
                                 "extra": {"ref": "[a](a.md)"}},
                                {"id": "2", "doc_path": "missing.md", "note": "",
                                 "site": "", "extra": ""}]}, f, ensure_ascii=False)
        self.cp = os.path.join(d, "l.csv")
        wr(self.cp, "id,doc_path\n1,a.md\n2,nope.md\n")

    def tearDown(self):
        self.d.cleanup()

    def test_links_extraction(self):
        es = run(self.jp, "links")
        got = [(e["index"], e["column"], e["target"], e["exists"]) for e in es]
        self.assertEqual(got, [
            (0, "doc_path", "a.md#用法", True),      # 連結欄裸值 + #anchor
            (0, "note", "sub/b.md", True),           # md 連結
            (0, "extra", "a.md", True),              # 巢狀物件裡的字串，報最上層欄名
            (1, "doc_path", "missing.md", False),    # 壞連結
        ])
        # http(s): 不算連結、空字串不算
        self.assertNotIn("site", [e["column"] for e in es])
        self.assertTrue(es[0]["resolved"].endswith(os.sep + "a.md"))

    def test_check_and_exit_code(self):
        code, bad = run_raw(self.jp, "check")
        self.assertEqual(code, 1)
        self.assertEqual([b["target"] for b in bad], ["missing.md"])
        # 把壞的修好 → 結束碼 0
        run(self.jp, "update", "1", "doc_path=a.md")
        self.assertEqual(run_raw(self.jp, "check"), (0, []))
        # 命令在前的寫法也接受
        self.assertEqual(run_raw("check", self.jp)[0], 0)

    def test_csv_path_suffix_column(self):
        # csv 沒地方放 link_columns，靠 _path 後綴
        t = tabledb.load(self.cp)
        self.assertEqual(tabledb_links.link_columns(t), {"doc_path"})
        code, bad = run_raw("check", self.cp)
        self.assertEqual((code, [b["target"] for b in bad]), (1, ["nope.md"]))

    def test_open_and_resolve(self):
        self.assertEqual(run(self.jp, "open", "0")["content"], "AAA\n")   # 第一個連結
        self.assertEqual(run("open", self.jp, "0", "note")["content"], "BBB\n")
        r = run(self.jp, "resolve", "0", "note")
        self.assertEqual((r["index"], r["column"], r["target"]), (0, "note", "sub/b.md"))
        # 指定的欄沒有連結 → 結束碼非 0 並印 error
        code, err = run_raw(self.jp, "resolve", "0", "site")
        self.assertEqual(code, 1)
        self.assertIn("error", err)

    def test_meta_preserved_on_save(self):
        t = tabledb.load(self.jp)
        t.add({"id": "3", "doc_path": "a.md"})
        t.save()
        with open(self.jp, encoding="utf-8") as f:
            raw = json.load(f)
        self.assertEqual(list(raw)[:4], ["contract", "source", "extracted", "link_columns"])
        self.assertEqual(list(raw)[-2:], ["columns", "rows"])
        self.assertEqual(run(self.jp)["contract"], "wf-table/1")


if __name__ == "__main__":
    unittest.main()
