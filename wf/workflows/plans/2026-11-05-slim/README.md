# 2026-11-05 slim — 整個 repo 瘦身（刪封存、止增長、拆檔＋tidy）

[plans](../README.md)｜[planning](../../planning.md)｜[tidy](../../tidy/README.md)

使用者 2026-11-05 原話：「總之整個repo我都想瘦身」「整個repo都檢查一下吧，該清的清、該刪的刪，尤其是那種無限增長的紀錄。然後封存的其實也可以刪掉了。該來把整個repo做瘦身」「順便做重構拆檔+tidy」。

本計畫只規劃、不執行；每個刪檔批次都要使用者勾選（鐵律 2），下方「決策清單」是勾選單。刪掉的東西 git history 都在：`git log --all -- <路徑>`、`git show <hash>:<路徑>`。**歷史不改寫、不 gc**（母 repo public；pack 縮小另案）。

```text
Done when: 下列各階段的 Done when 全過；五個 repo 的 wf-lint broken=0；母 repo 根 check_markdown_links.py OK；
           STRUCTURE.md local 段已載明「過時即刪」與各紀錄的保留期；本目錄在 plans/README「已結案」表登記一列。
```

## 現況（HEAD 追蹤檔；instance/ 排除）

| repo | 檔數 | bytes | 其中可刪（本計畫確定項） | 需使用者決定的額外項 |
|---|---:|---:|---|---|
| 母 repo | 1,121 | 6.4 MB | 95 檔／1.0 MB（B1–B7） | — |
| agentctl | 12,522 | 271.5 MB | 11,560 檔／257 MB（A1–A10） | — |
| modpack-design | 952 | 22.0 MB | 525 檔／4.1 MB（C1–C2） | C3 2.6 MB、C4 11.7 MB |
| mod-library（文件／工具層） | 826（不含成品 2,970 檔 680 MB） | 37 MB | 24 檔／5.0 MB（D1） | D2 58 MB、D3 8.9 MB、D4 1.1 MB、D5 |
| projects/*（我們加的文檔） | wf/ 骨架 ×10 ＋ 文檔 | ≈ 2.5 MB | 70 檔／0.9 MB（E1–E2） | E3 |

紀錄／文件層合計約 15,400 檔／337 MB；確定項刪約 **12,300 檔／268 MB（檔數與 bytes 各約 80%）**，使用者全選加項再 −82 MB。各項明細（路徑、檔數、bytes、要清的連結）在 [deletions.csv](deletions.csv)（30 列）；增長型紀錄的現況、一次性清法、保留規則與要改的規則檔在 [growth-records.csv](growth-records.csv)（22 列）。

## 階段（按 repo 切開，彼此不撞同一 repo）

<!-- wf-nav -->
| 階段 | 檔 | repo | 做什麼 | 派給 |
|---|---|---|---|---|
| 0 規則 | [rules.md](rules.md) | 母 repo `wf/`（＋三載點 local 段） | archive 規則改「過時即刪」、各紀錄保留期、lint local hook | Opus |
| 1 agentctl | [agentctl.md](agentctl.md) | agentctl | A1–A10 刪封存與紀錄、精簡 SESSION-LOG／NEXT-SESSION | 刪檔 Sonnet；吸收結論與改規則 Opus |
| 2 母 repo | [mother.md](mother.md) | 母 repo | B1–B7、wait-user／wf/user 瘦身、analysis 清理、超標檔 | Sonnet（B3 wait-user 改寫 Opus） |
| 3 子 repo | [subrepos.md](subrepos.md) | modpack-design → mod-library → projects/* | C／D／E 批次 | Sonnet；D2／C4 判定 Opus |
| 4 測試刪減 | [subrepos.md#4-測試刪減](subrepos.md#4-測試刪減) | 各 repo | 照另一條線的 `test-audit.csv`（280 列：留 205／待議 52／刪 16／瘦身 7） | Sonnet |
| 5 收尾 | [subrepos.md#5-收尾](subrepos.md#5-收尾) | 全部 | 連結檢查、INDEX／README 同步、逐 repo commit、pin | Opus |

順序：0 → 1 與 2 可平行（不同 repo）→ 3 依序 → 4 → 5。階段 1 的 A2 等階段 0 規則定稿後才動（刪場次夾要先有保留期規則）。

## 決策清單（請勾選；每條附建議）

<!-- wf-nav -->
1. **archive 規則改「過時即刪」**（取代 STRUCTURE「不刪」）— 建議採；條文見 rules.md。
2. **A1 `handoffs/done/` 整刪**（9,217 檔／203 MB）— 建議刪；lessons 的 204 處引用是 code span 不是連結，不會斷。
3. **A2 場次夾保留 30 天／最近 5 場，10-17～11-02 共 8 夾刪**（947 檔／16 MB）— 建議刪；11-03～11-05 留（PoE 凍結資料＋現役續行點）。
4. **A6 `agentctl/logs/` 整刪**（275 檔／1.8 MB，2026-08 凍結證據）— 建議刪，17 條連結降純文字。
5. **A7 `qa/reports/` 全刪**（278 檔／14.7 MB，全為 2026-08）— 建議刪，留 baselines／specs。
6. **A4 `inbox/done/`＋roster-history 刪；inbox 系統本身留**（218 檔／10 MB）— 建議刪；是否連 inbox 工具一起退役另議（五通道 9-25 起無流量）。
7. **B1 wf/user 產出 HTML 不進版控**（642 KB）— 建議刪並 .gitignore；render.py／review-data.json 留，PoE 解凍時重產。
8. **B3 wait-user 結案項改「刪」**（closed json 4 檔 79 列＋archive）— 建議採。
9. **C4 modpack-design `content-plan/dialogue/`**（205 檔／11.7 MB，53% 的 modpack-design）— 建議刪 `dialogue.json.gz` 只留 PROFILE／SUMMARY；前提：可由 game-data 重抽（執行線先驗）。
10. **C3 zh-layer 09-11 缺口快照與 data/**（2.6 MB）— 建議刪，前提：11-05 audit 已涵蓋（執行線先驗）。
11. **D2 mod-library `l10n/mods-superseded/` 整刪**（555 檔／58 MB）— 建議刪；注意 pack 不縮。
12. **D3 POTC 舊版成品（IS 1.2.1／1.2.2-dev、Varinia r1）**（230 檔／8.9 MB）— 建議留到 PoE 解凍；r2 留作回退。
13. **D4 mod-library viewer 產出 .gz**（1.1 MB）— 建議不進版控。
14. **E3 model-converter 根層 10 份 md 精簡**（暫緩專案）— 建議只精簡 SESSION-LOG；其餘不動。
15. **analysis/ 暫緩專案研究**（followers-patch 48 檔、chim 4 檔、port-source-survey 6 檔）— 建議保留（知識正本），只刪 archive/。
16. **projects/* wf/ 骨架副本**（10 份 ×39 檔）— 建議保留不縮（是 AGENTS 路由；縮了升級更難）。
17. **git 歷史不改寫、不 gc** — 建議不做；要縮 pack 另開計畫。
