---
description: 跑 wf-lint 檢查文檔（壞連結 / 超標檔 / 佔位殘留 / inbox 堆積）
---

> 本檔是 **Claude Code 的 slash 指令適配層（可選）**：其他 agent 工具沒有對應機制就忽略 `.claude/`，直接跑 `wf/tools/wf-lint.sh`。

本 repo 是非侵入式佈局，腳本在 `wf/tools/wf-lint.sh`，檢查目標是 `wf`（母 repo 根還有 submodule 與 `external/`，不掃）：

```
bash wf/tools/wf-lint.sh $ARGUMENTS wf
```

回報 `BROKEN` 清單與各項計數。有 `BROKEN` 就修連結；殘留的佔位符與模板段表示導入未完成（`--strict` 會讓殘留算失敗）。`OVERSIZE` 是檢視訊號不是硬上限，已知 `wf/workflows/testing.md` 與 `wf/workflows/nexus-intake/README.md` 超標。
