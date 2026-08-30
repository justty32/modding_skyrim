import json
import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(__file__))
import tabledb  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
CLI = os.path.join(HERE, "tabledb.py")


def run(*args):
    out = subprocess.run([sys.executable, CLI, *args], capture_output=True, text=True, check=True).stdout
    return json.loads(out)


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


if __name__ == "__main__":
    unittest.main()
