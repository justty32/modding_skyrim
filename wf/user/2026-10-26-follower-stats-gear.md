# 語音隨從：能力值與裝備審批頁（2026-10-26）

[wf/user 索引](README.md)

| 頁面 | 網址 | 用途 |
|------|------|------|
| 隨從能力裝備審批 | <https://claude.ai/artifact/AtsEuJcAXgHDFrGNG2fZj1> | 59 位語音隨從逐人一張卡：現在的等級／class／武器／服裝、作者有沒有刻意設計、能力值（S0–S5）與裝備（E0–E3）各挑一個；按「產生變更單」得到「【隨從能力裝備變更單 VFSTATS v1】」貼給 Claude |

這輪只調查，沒有改任何 esp 或 profile。結論一句話：多數隨從作者都設計過，推薦以不動為主；真的有毛病、推薦要改的是 Remiel（第三方戰鬥改造被外觀 mod 蓋回原版）、Secunda（等級倍率 ×10）、Cheryl／Sela（作者的衣服在背包、預設穿原版衣服）、Fastred（等級上限 40）、Rosetta（作者講的水系魔法沒實裝）；另有 8 人推薦「遊戲內自己給裝備」就好。

詳情與逐人理由：[vfstats REPORT](../../agentctl/handoffs/home-2026-10-26/vfstats/REPORT.md)。

## 怎麼重產（給 agent）

`python3 -I agentctl/handoffs/home-2026-10-26/vfstats/tools/scan_vf_stats.py --out-dir <目錄>` 重掃現況（約 1 分鐘），判斷表在同目錄 `tools/proposals_src.py`，`tools/build_proposals.py` 併出 `data/vf-proposals.tsv` 與頁面；用同一個檔案路徑或 url 重發，重發前先 `read` 線上版。頁面的選擇存在頁面資料庫 `picks/main`（ArtifactData 可讀）。
