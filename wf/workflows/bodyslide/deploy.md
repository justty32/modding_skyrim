# 授權部署與回退

[入口](README.md)｜[工具鏈](tools.md)

隔離建置與驗收通過後才進這頁。沿 [profile-change](../profile-change/README.md) 與 [safe-apply](../safe-apply.md) 的施工窗：授權、遊戲／MO2 停止、鎖、實體磁碟備份先到位；不直接覆寫來源 mod、Data 或 overwrite。

## 1. 先查現役贏家

**每個輸出路徑都要先查現役實檔贏家，連非 BodySlide 的檔也算。** planner 只比 OSP 之間的衝突，看不到「同路徑、但不是 BodySlide 產物」的檔。

- 資產贏家：`instance/tools/whichmod.py '<相對路徑>' --chain`。它會建／刷 `$XDG_CACHE_HOME/skyrim-kit/whichmod.sqlite`（本機快取），**不是 mod-library 的 MongoDB**；交接書的「不准動 DB」不擋它。它列鬆散檔與 BSA 提供者，BSA 內容以它的索引為準；索引沒涵蓋的封裝要在 REPORT 列為缺口。
- 啟用狀態：`instance/tools/profile_query.py <mod 名>`——只回啟用、priority、目錄存在與 `.mohidden`，**不解資產贏家**，不能拿來當贏家證據。
- 贏家不是 BodySlide 產物（例如私有身體層）時，**由使用者決定取代還是不動**；沒有決定就不部署該路徑。

2026-11-21 現役實況（審查 F4）：現役身體家族是 **CBBE 2.0.3**，寫 `femalebody` 的是 `CBBE 2.0.3 Vanilla General` 的 `CBBE Body`／`Physics`／`Special`／`NeverNude`／`NeverNude Physics`／`Underwear` 六個同輸出變體；現役 `femalebody_0/1.nif` 的實檔贏家是 `Sofia-Body-CBBE-Dev-2026-09-05`（全域路徑、非 BodySlide 層），沒有 loose `femalebody.tri`。新 output 層排在 Sofia 之下＝沒效果，排在之上＝換掉使用者的全域身體，兩者都要使用者拍板。3BA 只出現在 11-18 的隔離能力試驗，不是現役家族。部署前重查，這段只是當天快照。

## 2. 最小 manifest

output 層用 `instance/tools/layer_apply.py`（`--schema` 印格式；預設 dry-run）。三個關鍵參數：

```json
{
  "schema": "layer-apply/1",
  "name": "bodyslide-cbbe-body",
  "round": "r1",
  "mods": [{"name": "BodySlide Output CBBE Body 2026-11-21",
            "src": "/abs/staging/run1/rounds/b/output", "replace": false}],
  "modlist": [{"mod": "BodySlide Output CBBE Body 2026-11-21", "enabled": true,
               "before": "<第 1 步查到的現役贏家 mod 名>"}]
}
```

- **層名純 ASCII**：MO2 遇非 ASCII 資料夾名會整包靜默停用（[lessons/mo2-behavior-quirks](../../lessons/mo2-behavior-quirks.md#mo2-silent-collision-failure-modes)）。
- **`before` 錨點＝第 1 步查到的現役贏家**，不是 BodySlide 本體旁邊；錨點放錯，部署「成功」卻沒生效。
- 只有資產、沒有 plugin 的層不寫 `plugins` 段；`layer_apply` 仍會跑 check_masters 基準與比對。
- 先 dry-run 看 diff，授權後 `--apply --revert-out <本輪 data/>/revert.json`，revert 檔另存一份在本輪證據。之後照 profile-change 跑 MO2 開關一輪的驗證（`mo2_cycle_verify`），只有資產的層也照跑。

## 3. 部署後驗證

- 用 whichmod 重查每個目標 NIF／TRI 的 winner＝新層，不用左欄位置的直覺判優先權；確認私有 ARMA 模型路徑真的指向本輪產物。
- 只改資產不代表 NPC_、ARMO／ARMA、體重、裝備骨架與物理相容性已驗證。再接 [runtime-qa](../runtime-qa/README.md)，分別看裸身、目標服裝及需要的體重／動作；離線通過不能替代遊戲觀察，實機由使用者做。

## 4. 回退

`layer_apply.py --revert <revert.json>`：三檔現況要等於套用後的 sha256（有人後來改過就拒絕）；新層目錄被搬進備份不刪。回退後重查 winner／hash；備份保留與清理按 safe-apply，不自行刪除。
