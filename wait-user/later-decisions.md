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
