#!/usr/bin/env python3
"""waituser_count 的 fixture 測試；全部走 tempdir，不讀真實 WAIT_USER.md／wait-user/。"""

from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import waituser_count  # noqa: E402


HUB_TEMPLATE = """# WAIT_USER — 等待使用者的事

| 類別 | open | 前次 | 清單 |
|---|---:|---:|---|
| 甲類 | {alpha} | 3 | [`wait-user/alpha.md`](wait-user/alpha.md) |
| 乙類 | {beta} | 1 | [`wait-user/beta.md`](wait-user/beta.md) |
| 自指類 | {selfrow} | 0 | [本檔下節](#push-排程) |

## Push 排程
{self_body}
"""

ALPHA = """# 甲類

## 條目一

內文。

## 條目二

內文。

## 條目三

內文。

## 已完成（封存）

### 封存掉的舊條目

不算 open。

### 另一個封存條目

也不算。
"""

BETA = """# 乙類

## 唯一條目

```markdown
## 這是 code fence 裡的假標題，不算條目
```

內文。

## 已裁示／已完成（封存）

已抽到 beta-closed.json（4 列）。
"""


def write_fixture(
    root: Path,
    *,
    alpha: int = 3,
    beta: int = 1,
    selfrow: int = 0,
    self_body: str = "\n目前沒有等使用者放行的 push 排程。\n",
    include_beta: bool = True,
) -> None:
    (root / "wait-user").mkdir(parents=True, exist_ok=True)
    (root / "WAIT_USER.md").write_text(
        HUB_TEMPLATE.format(alpha=alpha, beta=beta, selfrow=selfrow, self_body=self_body),
        encoding="utf-8",
    )
    (root / "wait-user" / "alpha.md").write_text(ALPHA, encoding="utf-8")
    if include_beta:
        (root / "wait-user" / "beta.md").write_text(BETA, encoding="utf-8")


def run(root: Path, *flags: str) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    code = waituser_count.main(["--root", str(root), *flags], stdout=out, stderr=err)
    return code, out.getvalue(), err.getvalue()


class WaitUserCountTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def test_counts_match_exits_zero(self) -> None:
        write_fixture(self.root)
        code, out, err = run(self.root, "--check")
        self.assertEqual(code, 0, err)
        self.assertIn("甲類 hub=3 actual=3 OK", out)
        self.assertIn("乙類 hub=1 actual=1 OK", out)
        self.assertNotIn("MISMATCH", out)

    def test_mismatch_exits_one_with_check(self) -> None:
        write_fixture(self.root, alpha=5)
        code, out, _ = run(self.root, "--check")
        self.assertEqual(code, 1)
        self.assertIn("甲類 hub=5 actual=3 MISMATCH", out)
        self.assertIn("乙類 hub=1 actual=1 OK", out)

    def test_mismatch_without_check_still_reports_but_exits_zero(self) -> None:
        write_fixture(self.root, alpha=5)
        code, out, _ = run(self.root)
        self.assertEqual(code, 0)
        self.assertIn("甲類 hub=5 actual=3 MISMATCH", out)

    def test_missing_subfile_is_error_exit_two(self) -> None:
        write_fixture(self.root, include_beta=False)
        code, out, err = run(self.root, "--check")
        self.assertEqual(code, 2)
        self.assertIn("乙類 hub=1 actual=- ERROR", err)
        self.assertIn("子檔不存在", err)
        self.assertIn("甲類 hub=3 actual=3 OK", out)

    def test_self_reference_row_counts_hub_own_section(self) -> None:
        # 自指節底下的條目是比該節深一層的標題（### ）。
        body = "\n### 等放行的 push 一\n\n內文。\n\n### 等放行的 push 二\n\n內文。\n"
        write_fixture(self.root, selfrow=2, self_body=body)
        code, out, _ = run(self.root, "--check")
        self.assertEqual(code, 0)
        self.assertIn("自指類 hub=2 actual=2 OK", out)

    def test_self_reference_row_detects_drift(self) -> None:
        body = "\n### 等放行的 push 一\n\n內文。\n"
        write_fixture(self.root, selfrow=0, self_body=body)
        code, out, _ = run(self.root, "--check")
        self.assertEqual(code, 1)
        self.assertIn("自指類 hub=0 actual=1 MISMATCH", out)

    def test_archive_section_and_code_fence_excluded(self) -> None:
        # alpha 的兩個 ### 封存條目與 beta 的 code fence 假標題都不得計入。
        write_fixture(self.root)
        _, out, _ = run(self.root)
        self.assertIn("甲類 hub=3 actual=3 OK", out)
        self.assertIn("乙類 hub=1 actual=1 OK", out)

    def test_json_output_structure(self) -> None:
        write_fixture(self.root, alpha=5)
        code, out, _ = run(self.root, "--check", "--json")
        self.assertEqual(code, 1)
        payload = json.loads(out)
        self.assertEqual(payload["hub"], "WAIT_USER.md")
        self.assertEqual(payload["mismatches"], 1)
        self.assertEqual(payload["errors"], 0)
        self.assertEqual(payload["exit_code"], 1)
        rows = {row["category"]: row for row in payload["rows"]}
        self.assertEqual(rows["甲類"]["actual"], 3)
        self.assertEqual(rows["甲類"]["status"], "MISMATCH")
        self.assertEqual(rows["甲類"]["source"], "wait-user/alpha.md")
        self.assertFalse(rows["甲類"]["self_reference"])
        self.assertTrue(rows["自指類"]["self_reference"])
        self.assertEqual(rows["自指類"]["source"], "WAIT_USER.md#push-排程")

    def test_json_output_carries_error_rows(self) -> None:
        write_fixture(self.root, include_beta=False)
        code, out, _ = run(self.root, "--json")
        self.assertEqual(code, 2)
        payload = json.loads(out)
        self.assertEqual(payload["errors"], 1)
        rows = {row["category"]: row for row in payload["rows"]}
        self.assertEqual(rows["乙類"]["status"], "ERROR")
        self.assertIsNone(rows["乙類"]["actual"])
        self.assertIn("子檔不存在", rows["乙類"]["error"])

    def test_missing_hub_is_error_exit_two(self) -> None:
        code, _, err = run(self.root, "--check")
        self.assertEqual(code, 2)
        self.assertIn("找不到 hub", err)

    def test_non_integer_open_cell_is_error(self) -> None:
        write_fixture(self.root)
        hub = self.root / "WAIT_USER.md"
        hub.write_text(
            hub.read_text(encoding="utf-8").replace("| 甲類 | 3 |", "| 甲類 | 三 |"),
            encoding="utf-8",
        )
        code, _, err = run(self.root, "--check")
        self.assertEqual(code, 2)
        self.assertIn("open 欄不是整數", err)

    def test_unresolvable_self_anchor_is_error(self) -> None:
        write_fixture(self.root)
        hub = self.root / "WAIT_USER.md"
        hub.write_text(
            hub.read_text(encoding="utf-8").replace("## Push 排程", "## 別的節名"),
            encoding="utf-8",
        )
        code, _, err = run(self.root, "--check")
        self.assertEqual(code, 2)
        self.assertIn("找不到錨點", err)

    def test_fix_is_not_implemented(self) -> None:
        write_fixture(self.root)
        code, out, err = run(self.root, "--fix")
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertIn("未實作", err)
        self.assertIn("P1-1", err)

    def test_help_exits_zero(self) -> None:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), self.assertRaises(SystemExit) as ctx:
            waituser_count.main(["--help"])
        self.assertEqual(ctx.exception.code, 0)
        self.assertIn("--check", buf.getvalue())

    def test_slugify_keeps_cjk(self) -> None:
        self.assertEqual(waituser_count.slugify("Push 排程"), "push-排程")
        self.assertEqual(waituser_count.slugify("已完成（封存）"), "已完成封存")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
