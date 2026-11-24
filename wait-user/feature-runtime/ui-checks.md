## ESL 旗標 6 支的 UI 功能順路確認（2026-10-26）

`ESLify-Overlay` r2 已正式套用（profiles `5a3d6af`）：RaceMenuPlugin、BetterContainerControls、NSV Spell Copies、WindhelmSegregation、DudestiaOutfitChanger、CompanionsTweaks 改成 light，FormID 不變。agent 已實測「light 狀態存檔→重開遊戲→讀回」背包／裝備／任務／Papyrus 讀檔段都一致，co-save 也接得上。沒測到的只有要真的點 UI 的部分，玩的時候順路看：

- **RaceMenu**：開得起來、滑桿能動（`showracemenu` 或鏡子）。
- **Better Container Controls**：開容器，全取／分類快捷鍵照舊。
- **換裝戒指（Dudestia Outfit Changer）**：對隨從用一次，換得上去。

agent 2026-11-22 傍晚（runtime-3）：RaceMenu 開得起來、滑桿能動（換臉場用真按鍵把「體型」調了 100 格，`runtime-3/shots/A3-06/07`）。容器快捷鍵、換裝戒指沒測。

還原：持 game.lock、MO2 關著，先取回 revert 檔 `git -C agentctl show 3db1b772:handoffs/home-2026-10-26/eslapply/data/layer-revert.json > /tmp/eslapply-layer-revert.json`，再跑 `python3 instance/tools/layer_apply.py --revert /tmp/eslapply-layer-revert.json`。它把 modlist 蓋回套用前、把舊 ESLify-Overlay 從 `~/skyrim_mods/_layer-apply/eslapply-r1-20261026T110518/mods/` 搬回、ESLify-Overlay-NSV 搬進備份（不刪），再 profiles `record --kind fix`。revert 沒有 dry-run；三檔被別線改過會拒絕，屆時手動刪 `+ESLify-Overlay-NSV` 那行、把 ESLify-Overlay 目錄換回備份。已用新 light 存檔再撤旗標的反向路徑沒測過，先拿存檔複本試；revert json 內若寫死來源路徑，執行前先確認（原 REPORT `agentctl/handoffs/home-2026-10-26/eslapply/REPORT.md` 已刪，可由同一 commit 取回）。

## VIGILANT 設定載入器 MCM 繁中＋停用 Falmer 重複中文層（2026-11-15）

已改 `modpack-main`（profiles `a363e2c`）：新增 `VIGILANT SE - Settings Loader Traditional Chinese 1.2.0 Dev 2026-11-15`，排在 Settings Loader 上面（mod-library `l10n/mods/VIGILANT-Settings-Loader-Traditional-Chinese-1.2.0`，30 句：10 句沿用 VIGILANT 繁中、2 句重譯、18 句新譯）；停用被完全蓋住的 `Falmer-Servant-Lines-Expansion-Traditional-Chinese-Dev-2026-09-03b`（不刪，遊戲內容不變，生效的仍是 `ZH-LR-LR-0069`）。只動 modlist，plugins 不變；缺 master 0、字型缺字 0，沒開過遊戲。玩的時候看：

- **MCM**：MCM 裡「Vigilant」的兩頁（一般／維護）標題、選項與下方說明都是繁中，沒有方塊字，也沒有 `$Vig...`、`$LoadSettings` 這類原始鍵名；選項改了能存。
- **Falmer**：遇到伐默僕從（Falmer Servant）時，戰鬥台詞字幕仍是繁中（例如「為了伐默！」）。

還原：持 game.lock、MO2 關著，跑 `python3 instance/tools/layer_apply.py --revert ~/skyrim_mods/_layer-apply/l10n-vigloader-falmer-r1-20261115T161650/revert.json`。

## Estates of Skyrim 0.1.8→0.1.21 更新後確認（2026-11-15）

profiles `7def9b0`：新資料夾 `Estates-Of-Skyrim-196696-0.1.21`（Nexus 196696 file 837519）啟用；舊 `Estates-Of-Skyrim-196696-0.1.8` 與過期的自製繁中層 `Estates-Of-Skyrim-196696-ZH-0.1.8-r2` 停用（資料夾留著）。esm 598→771 筆、沒刪記錄，changelog 每版寫「Safe to update mid-game」。繁中層已重做並疊在上面：`Estates-Of-Skyrim-196696-ZH-0.1.21-2026-11-15`（profiles `c2b46d9`，mod-library `6a8bf85`，35 檔逐檔勝出）。使用者已說接受不穩定。玩的時候看：

- **舊存檔讀得進來**：讀一個有 Estates 進度的存檔，Estates 畫面（Tab 選單或按鍵）打得開、你的莊園、國庫和工人都還在。
- **新功能**：Build Mode（MCM 的 Quick build 鍵，預設 G）出現半透明預覽、R 轉向、左鍵放置；雇人（Hire Position）照常。
- **Falkreath Shop**：灰松货行在 Estates 畫面上還在、還能賣東西（它以 Estates 為 master）。
- **中文**：天際領地畫面各分頁（總覽、工人、倉儲、升級）、建造列與快速建造選單、拆除兩段確認、尋找工人；MCM 新項目（快速建造按鍵、貨車遇襲）；聘任新職業的對話。看有沒有方框字、截斷、重疊。
- **崩潰**：讀檔或開 Estates 畫面崩潰就記下來。

還原：持 game.lock、MO2 關著，`python3 instance/tools/layer_apply.py --revert /tmp/skyrim-alt-modinstall/20261115-196696/revert.json`（在 `/tmp`，重開機會消失；先退中文層 `revert-zh.json` 再退本體；消失時手動把 modlist 的 ZH-0.1.21 與 0.1.21 改 `-`、0.1.8 與 ZH-0.1.8-r2 改回 `+`）。新版存過的檔退回舊版不保證能讀。**2026-11-22 已確認這個 `/tmp` 還原檔已不存在**（重開機清掉），只能走括號裡的手動退路。

agent 2026-11-22 已代驗第一點的前半：Save341（有 Estates 進度）讀得進來、沒崩、沒有新 crash log；Estates 畫面、Build Mode、分頁中文要開選單，agent 做不到，仍要你看。

