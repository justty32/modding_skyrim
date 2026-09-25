import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(__file__))
import find_big_lists  # noqa: E402


def write(d, name, text):
    p = os.path.join(d, name)
    open(p, "w", encoding="utf-8").write(text)
    return p


class FindBigListsTest(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.d.cleanup()

    def test_blank_line_between_items_is_one_block(self):
        items = [f"- item {i} " + "x" * 60 for i in range(20)]
        joined = "\n\n".join(items)  # 每項之間一個空行
        p = write(self.d.name, "a.md", "# t\n\n" + joined + "\n")
        hits = find_big_lists.scan(p, 1024)
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0][2], "list")
        self.assertEqual(hits[0][3], 20)

    def test_two_blank_lines_split_and_nav_exempts(self):
        items = [f"- item {i} " + "x" * 60 for i in range(20)]
        p = write(self.d.name, "b.md", "\n".join(items[:10]) + "\n\n\n" + "\n".join(items[10:]) + "\n")
        self.assertEqual(find_big_lists.scan(p, 1024), [])  # 兩塊各 <1 KB
        p2 = write(self.d.name, "c.md", "<!-- wf-nav -->\n" + "\n".join(items) + "\n")
        self.assertEqual(find_big_lists.scan(p2, 1024), [])

    def test_table_links_and_links_only(self):
        rows = ["| a | b |", "|---|---|"] + [f"| r{i} " + "y" * 30 + " | [x](c.md) |" for i in range(30)]
        p = write(self.d.name, "d.md", "\n".join(rows) + "\n")
        (size, loc, kind, n, links, linked), = find_big_lists.scan(p, 1024)
        self.assertEqual((kind, links, linked), ("table", 30, "all"))
        self.assertEqual(len(find_big_lists.scan(p, 1024, links_only=True)), 1)


if __name__ == "__main__":
    unittest.main()
