# 日後素材／清理決定

## 夜貓－無心 3.1.0（可選精確替換）

目前 JH People 1.1.3＋NPC Plugin Chooser 2 的 536 NPC patch 已滿足方向，不阻塞整包。若仍要精確
3.1.0，只提供作者百度網盤中名稱含「人物美化」與「頭模替換」的 archive，放入既有
`/home/lorkhan/skyrim_mods/`；未取得完整資產許可不得公開重打包。見
[`相容性調查`](../wf/workflows/investigation/findings/wuxin-character-overhaul-se-ae-compatibility.md)。

## BG3 場景佈局實檔驗證

有合法遊戲資料時，以小型 `Levels/*.lsf` 做 `.lsf → .lsx`，記錄位置／旋轉／尺度／resource identity
能否無損對映 ModForge placements，再決定是否開 converter/spec；沒有實檔前不宣稱 pipeline 可行。
見 [`port-source-survey`](../analysis/port-source-survey/README.md)。

## Downloads 重複壓縮檔

`~/Downloads/_已入庫-2026-08-23/` 內 55 項共 5.7GB，內容已在 `~/skyrim_mods/`，是同 SHA-256 或
瀏覽器重複件。由使用者決定是否刪除；agent 不自行執行不可逆刪除。

## L4 146 個 legacy 命名壓縮檔

174 筆中 28 筆已用 Nexus `md5_search` 還原；剩 146 筆需判斷想留／想裝／沒興趣，不必逐行填表。
清單見 [`l4-md5-resolution`](../mod-library/audits/l4-md5-resolution.md#仍需人工辨識146-筆)。

## 16 個現役 mod 的自製來源已被清掉

`~/skyrim_agent_out/`（15 筆）與 `~/notes/…/artifacts/`（1 筆）是當時 codex 線的產出目錄，
收工自清時連著被刪；這 16 個 mod 現在**只剩 MO2 `mods/` 裡的安裝副本**，沒有獨立來源可以
重建或校驗。內容沒有遺失，遺失的是可還原性。主要是 Vokriinator Black／Ordinator／
Path of Sorcery／Vokrii／Adamant 的簡中修正層，加兩個 houseCARL patch。

三個選項，擇一：**(a)** 把安裝副本原樣收進 `mod-library/`（連 `MANIFEST.sha256` 一起產），
`source_path` 改指過去——可還原性補回來，代價是 private repo 變大；**(b)** 保留現狀，
在 manifest 標明「來源即安裝副本」，接受不可重建；**(c)** 重跑當初的產生器重建來源，
但那些腳本本身是否還在、輸入 archive 是否同版都要先查。

清單與判定依據見
[`checkpoint 紀錄`](../agentctl/logs/modpack-main-checkpoint-2026-08-26.md#仍未解決需要決定不是查得出來的)。

## 中文層五個裁示（2026-08-27 深夜起手清單第 5 條，仍未裁）

來源 [`resume-2026-08-28.md`](../agentctl/docs/resume-2026-08-28.md)（已標過期，只剩這條活著）；
逐項細節在 [`中文層覆蓋總表`](../modpack-design/content-plan/zh-layer-coverage-master-2026-08-28.md)的
「等使用者裁示」節：

1. **Bandolier NPC 層三選一**——注意覆寫陷阱不在 `BandolierForNPC.esp`，而在其後的
   `- No disenchant.esp`（70）與 `- Realistic Enchantements.esp`（23），forward patch 選項要照這個改設計。
2. **Reforging 綁 SkyPatcher** 要不要接受。
3. **AA（Armor Add-on）三個同版中文層選哪個流派**。
4. **`sLanguage` 要不要動**——現在是 `ENGLISH` 把中文塞英文槽；只附 `_chinese` 的層會靜默失效。
5. **Steam 2.5MB 補丁（TargetBuild 24914197）接不接受**——目前 acf 已搬出、exe 釘 1.6.1170。

## CCA 中文層已建好、未安裝、未 commit

`opus-selfmade-zh` 2026-08-28 做好 `Common Clothes and Armors Traditional Chinese 2.0.0`
（ESP 檔案替換層，164 筆＝33 筆 vanilla 迴歸回復＋131 筆新增，sha256 `4dcb6c32…`），
產物只在 [`agentctl/handoffs/done/2026-08-28/opus-selfmade-zh/`](../agentctl/handoffs/done/2026-08-28/opus-selfmade-zh/)，
**沒進 `mod-library/l10n/mods/`、沒裝進 MO2**。請裁：(a) 入庫＋照 install-plan 安裝，(b) 只入庫不裝，(c) 丟棄。
Bandolier 同線判定不必自製（見上一項）。
