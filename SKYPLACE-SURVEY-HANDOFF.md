# 交接：SkyPlace 併入 in-game editor 調查線（2026-08-21）

執行者：codex gpt-sol。工作目錄 `~/repo/moddings/skyrim`（注意：**不是** notes repo）。

## 使用者的要求

使用者給了 [SkyPlace 149455](https://www.nexusmods.com/skyrimspecialedition/mods/149455)，
說「這東西放到 in game editor 那邊」。目標線是
[`analysis/tool-survey/findings/skyrim-ingame-editor.md`](analysis/tool-survey/findings/skyrim-ingame-editor.md)
—— 那份在評估 SkyrimIngameEditor 能不能擴展成 CK 場景/地景編輯的替代品。

**這不是安裝任務。** 是把 SkyPlace 併進同一條工具調查裡評估。

## 已查明（不必重查）

SkyPlace 1.4.1，作者 SkyrimThiago，2026-08-01 更新，Nexus 分類 Overhauls。
SKSE plugin，讓玩家搬動物件並帶著走（裝飾房屋等），自稱是
**Object Manipulation Overhaul 的精神續作**。Nexus 沒有列任何 requirements。
鍵位在 `Data/SKSE/Plugins/SkyPlaceKeyBindings.json`，支援鍵鼠與手把，
可設 `press` / `doubleTap`。頁面自列限制：可能讓玩家爬到不該去的地方而破壞其他 mod
或本體；可拾取判定是 heuristic，可能誤判。頁面說
「API for modders / Creating craftable placeable items — Coming soon」，
並有 Source Code 連結（頁面寫 QTR Github）。

## 要回答的問題

現有 findings 文件把 in-game editor 的價值拆成
**Feature 1：Reference / Object 放置與移動** 與 **Feature 2：Heightmap / LAND 地形編輯**，
並有「與 ModForge 的關係」與「擴展實作建議（優先序）」兩節。請在同一框架下評估 SkyPlace：

1. **它實際怎麼做 reference 放置／移動**：跟 SkyrimIngameEditor 的
   `TargetManager`（`Console::SelectReference` 螢幕座標選取）＋
   `ReferenceTransformEditor` 相比，是同一路數還是不同機制？
2. **能不能匯出成 ESP／持久化**？SkyrimIngameEditor 有 C# `EspGenerator`（Mutagen）
   把改動序列化匯出。SkyPlace 是只在存檔裡改 runtime state，還是有匯出路徑？
   這一題決定它對「取代 CK 編輯流程」有沒有用。
3. **原始碼是否可得、授權為何**？找出頁面所指的 Source Code repo。
   SkyrimIngameEditor 是 MIT。若 SkyPlace 授權不相容或閉源，直接影響能不能借用或擴充。
4. **對現有「擴展實作建議（優先序）」有沒有改變**？如果 SkyPlace 已經把 Feature 1
   做得比自製更好，就明講可以省下哪一段；如果它只是玩家向的擺設工具、
   沒有匯出與 record 編輯能力，也要明講它**不能**取代什麼，不要抬高它。
5. **與 `projects/godot-worldspace-editor` 和 ModForge 的關係**：
   是競品、是可借用的元件，還是無關。

## 硬性限制

1. 使用者現在人在電腦前，**鍵盤滑鼠螢幕的控制權完全歸他**。
   不要啟動 Skyrim、不要啟動 MO2 GUI、不要開瀏覽器、不要用 xdotool／spectacle
   或任何搶焦點、送按鍵、截圖的工具，不要取得遊戲鎖。
2. **不要安裝 SkyPlace、不要下載任何東西。** 需要下載就停下回報要哪個頁面／repo，
   由使用者自己載。Nexus 一律走 housecarl 工具，不要開瀏覽器。
3. 這是唯讀調查：**不改 MO2 mods、不改 profile、不改 load order。**
4. 成果寫進 `analysis/tool-survey/` 這條線；可以是新增一份 findings 檔並在
   `skyrim-ingame-editor.md` 交叉連結，也可以是在原檔加一節 —— 你判斷哪個更合理，
   但**兩邊必須互相連得到**。
5. commit 只包含你自己新增／修改的路徑，推送 `~/repo/moddings/skyrim` 的 origin。
   注意這是 **public repo**，不要寫入任何敏感內容（API key、路徑以外的個資）。

## 驗收（寫死，不要自行加碼）

回報只要這 5 條：

1. SkyPlace 的放置機制與 SkyrimIngameEditor 的差異一句話。
2. 能否匯出 ESP／持久化，依據是什麼。
3. 原始碼位置與授權（找不到就寫找不到，不要猜）。
4. 對「擴展實作建議（優先序）」的具體影響：省掉什麼、或不能取代什麼。
5. commit hash。

查不到就寫查不到。**不要因為它是新 mod 就假設它比較好**，也不要因為它是玩家向工具就先貶低；
用證據說話。遇到工具錯誤就停下回報。
