# 執行結果與未完成項

> 屬於 [工作區統整與四條新線（2026-08-23）](README.md)。

## 執行結果（2026-08-23，已完成）

使用者拍板：1／2／3 也升頂層（`projects/` 維持純軟體）；profiles 走 B1 symlink；
`~/games/skyrim-qa-baselines` 不搬；`~/code/capture` 別管。

### 落地佈局

```
skyrim/                    public 母 repo
├─ instance/               private submodule  ← profiles/ (private submodule)
├─ mod-library/            private submodule  ← 必須永遠 private
├─ modpack-design/         private submodule
├─ agentctl/               private submodule
├─ projects/               11 個軟體 repo，未動
└─ analysis/ external/ patches/ scripts/ tests/ workflows/
```

四個 repo：`skyrim_instance`、`skyrim_mod_library`、`skyrim_modpack_design`、`skyrim_agentctl`。
**全部先開 private**，避免未審內容有任何一刻躺在公開位置。

### 搬移驗證

以「size + basename」對 notes 側 1047 檔逐檔比對，未落地的只有 14 個：

- 10 個是**刻意排除**的 private profiles worktree 複本（`agent-archive/*/worktrees/`）
- `README.md` → 改寫成轉址 stub
- `CONSOLIDATION-TODO.md` → `agentctl/handoffs/superseded/`，標記已被取代
- 2 個 `.html`/`.csv` 驗證輸出 → 補進 `agentctl/logs/`

刻意留在 notes 不搬的：53 個實機截圖（66MB）、20 個 MongoDB 快照與 DLL 備份（57MB）、
28 個 `__pycache__`。notes 側留一份轉址 README 說明每樣東西去了哪。

### 順帶修掉的曝險

`dist/mods/` 的 34 個資料夾**幾乎全是他人 mod 的繁中翻譯層，內含完整原始 ESP 複本**
（`USSEP-Traditional-Chinese-4.3.8a/` 裡是 20MB 的完整 USSEP plugin），**一直躺在 public 母 repo**。
已移到 private 的 `mod-library/l10n/mods/`。

**但母 repo 的 git 歷史仍然保有它們**——HEAD 乾淨了，歷史沒有。

### profiles symlink

```
modorganizer2/profiles -> /home/lorkhan/repo/moddings/skyrim/instance/profiles
```

改動當下 MO2 與 Skyrim 都沒在跑（唯一的 wineserver 屬於 appid 553850，不是 Skyrim 的 489830），
也沒有行程開著該目錄。改完確認：透過 symlink 讀得到 290 個啟用 mod、`git status` 乾淨、
`selected_profile=@ByteArray(Modpack-KR)` 未受影響。備份在 scratchpad。
還原指令寫在 `instance/README.md`。

### 收工狀態

7 個 repo（母、四條線、profiles、notes）全部 `dirty=0 unpushed=0`；
`check_markdown_links.py` 433 檔 595 連結全綠。

## 還沒做的

### 使用者裁決（2026-08-23）

| 事項 | 裁決 |
|---|---|
| **從 Steam 啟動驗證 symlink** | ✅ **通過**。成功 redirect 到 MO2，Wine 跟得住 Linux symlink |
| `modpack-design` / `agentctl` 翻 public | **不翻**。使用者說「沒差，真的沒差」——維持 private，不做無謂的審查工 |
| `git filter-repo` 清母 repo 歷史 | **不做**。翻譯層已從 HEAD 移走，歷史留著 |
| `~/Downloads` 壓縮檔歸檔 | **要做**。歸進 `~/skyrim_mods/` |

### 仍未完成

| # | 事項 | 狀態 |
|---|---|---|
| 1 | ~~`~/Downloads` 壓縮檔歸檔~~ | ✅ **完成**，見下 |
| 2 | SCB camera-ray 15 條驗收 | 中斷於統整之前，證據只支持 2 條 |

### Downloads 歸檔結果（2026-08-23）

122 個壓縮檔逐一用 `7z l` 開來看內容判斷：

| 類別 | 數量 | 處置 |
|---|---|---|
| Skyrim mod | 113（7.1GB） | 見下 |
| 非 Skyrim | 9 | 留原地（兩本網路小說 txt、初音 PS2 ISO、三國志10、太閤5、遊戲素材包等） |

113 個 Skyrim mod 的去向：

| | 數量 | |
|---|---|---|
| 同檔名已在庫裡 | 47 | 移到 `~/Downloads/_已入庫-2026-08-23/`，**未刪除**，等使用者處置 |
| 改名但 SHA-256 相同 | 5 | 同上 |
| 全新 | 61（1.5GB） | 搬進 `~/skyrim_mods/hdd/` |

**踩到一個坑**：Downloads 裡本身有瀏覽器重複下載的 `X` 與 `X (1)` 配對，兩個都不在庫裡，
所以只比對「來源↔庫」會把兩份都收進去。搬完 `scan_mod_library.py stats` 的
`L1 exact duplicates` 從 0 跳到 6 組才抓到，已移出 3 個重複檔。剩下的 3 組是庫裡本來就有的。

**驗證**：61 個全部到位、抽查 7 個 `7z t` 完整；磁碟 1791 個 archive
− 隱藏目錄 3 個 = **1788，與 MongoDB 索引完全對上**；快照已備份到 repo 外。
