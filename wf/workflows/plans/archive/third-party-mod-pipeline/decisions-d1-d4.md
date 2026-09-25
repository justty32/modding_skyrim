# 設計決策 D1–D4

> 屬於 [第三方 mod 取得–安裝–驗證流水線](README.md)。

## 二、已定案的設計決策

### D1：FOMOD 走宣告式解析，不走 GUI 精靈

`mo2ctl` 補一層 `resolve_source()` 前置：archive → 檔案樹。

- **`.zip` 用 stdlib `zipfile`**。維持 `client/` 全 stdlib 的鐵律（理由同上游 2.1：治具自己還要先裝環境就會沒人用）。`.7z`/`.rar` 不做原生支援——偵測到就找系統 `7z`/`unar`，沒有就 `handoff_user` 請使用者自己解，不為少數情況引依賴。
- **FOMOD 解析 `fomod/ModuleConfig.xml`**：把選項樹（step / group / plugin / 依賴條件）攤成可讀摘要，選擇結果寫進 install spec 的 `fomod_choices`，安裝時據此 materialize 檔案。`fomod/info.xml` 取名稱與版本填 `meta.ini`。
- **同一機制順便吃「手動多資料夾」型**（`00 Core` / `01 Optional` 那種沒有 FOMOD 但要人挑資料夾的）。

理由：GUI 點選**永遠不可重現**——同一個 mod 半年後重裝，你不會記得當初勾了什麼。宣告式的選項是可 diff、可 review、可跟著 git 分支走的，這也是本工作區既有的哲學（宣告式 spec → 產物）。代價是要實作一份 ModuleConfig schema 的子集，但那份 schema 穩定且公開。

### D2：排序做插入式，不整合 LOOT

只決定**新 mod 插哪裡**，不重排既有 109 個。依據來源：mod 頁面自述的前後關係 + `housecarl` 的 conflict tree 實際衝突 + `housecarl_check_errors`。

理由：現有 load order 是使用者實際在玩的、能跑的。對一個能跑的 load order 做全域重排是純下行風險——壞掉的成本遠大於「順序更漂亮」的收益。LOOT 整合等到插入式排序真的不夠用再說。

### D3：MO2 profile 走 git，分支即實驗（使用者 2026-08-04 提案）

`main` = 已驗證的已知良好狀態。每個候選 mod（或極小批）開 `try/<mod-name>` 分支跑完整流水線，綠燈 merge 回 `main`，紅燈砍分支 + `checkout main` 復原。

這一項同時解掉兩個問題：**失敗歸因**（一分支一 mod，壞了就知道是誰）與**回滾**（不用備份、不用記得改了什麼）。

四個實作約束：

1. **`.gitattributes` 必須設 `* -text`。** `modlist.txt` / `loadorder.txt` 是 CRLF、`plugins.txt` 是 LF（同目錄同程式寫的就是不一致，見上游 2.1）。git 預設的 eol normalize 會產生滿版假 diff，且改壞了 MO2 不報錯、症狀只表現為「裝了卻沒載入」——與上游踩過的「`sed` 對 CRLF 靜默匹配不到」是同一家族的坑。
2. **只版控 profile 文字檔，不版控 `mods/`**（GB 級）。因此需要 `manifest.json` 當 lockfile：mod 資料夾名 ↔ 來源 URL ↔ 版本 ↔ archive sha256 ↔ `fomod_choices`。沒有這份，一個 branch 只是「一串指向可能不存在的資料夾的名字」，不可重放。
3. **commit / checkout 只在 MO2 與遊戲都沒跑時做。** MO2 把 profile 存在記憶體、退出時整份寫回，執行中改檔會被靜默回滾（上游五節風險已證）。直接複用 `mo2ctl` 的 `require_writable()`。
4. **repo 落點不在本工作區。** 依 `README.md`「本機部署狀態不在本資料夾」與 `AGENTS.md` 的目錄職責，modlist 是部署狀態。就地在 MO2 instance `git init`（不做 copy-in/copy-out，避免漂移），remote 若要開就開 **private**（modlist 內容本身即敏感）。**治具程式碼**則放 `agent-bridge/client/`，與 `mo2ctl` 同層同一份合約。

### D4：測試範圍先收到「到達地點 + 穿上裝備」（使用者 2026-08-04 決定）

使用者原本提的四項驗證需求，經查 `/state` 實際欄位（`agent-bridge/src/State.cpp`）後的可斷言性：

| 需求 | 可斷言 | 依據 |
|---|---|---|
| **到達該地點** | ✅ 納入本計畫 | `coc` / `player.moveto` → 斷言 `player.cell_form_id`（**不是 `cell`**，EDID 會被漏帶 EDID 的 override 抹掉，上游 3.x 首跑抓到過）+ `position` + `interior` |
| **穿上裝備** | ✅ 納入本計畫 | `player.additem` + `equipitem` → 盔甲斷言 `inventory[*].worn`（**不在 `equipped`**）、武器/法術斷言 `player.equipped.{right,left}` |
| 觸發該劇情 | ⏸ 延後 | `quests` 只列 active、只有數字 stage 無文字；`game.dialogue` 可斷 `topic`/`speaker`/`quest`。演出本身（語音/鏡頭/動畫）屬視覺 → handoff |
| 使用該技能 | ⏸ 延後 | **`/state` 沒有已知法術 / shout / perk 清單**，只有「當下拿在手上的」。要直接驗得擴 `State.cpp` 加一個 opt-in block；目前只能斷間接副作用（`nearby_actors[*].dead`、`actor_values.*.max` 變化） |

延後的兩項等第一批實際要裝的 mod 確定、看是否真的需要再回頭——先擴欄位是在猜。
