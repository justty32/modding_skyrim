# 審查問題：低嚴重度（8–23）

[審查總覽](README.md)；路徑縮寫見總覽「範圍」。

8. `$P/README.md:19` 指向已不存在的 `archive/`（過時即刪）。建議改純文字或 `git log --all -- $P/archive`。
9. 攻速餘裕兩口徑：`$P/decisions.md:54`「現在 48.9%，只剩 1.1」是 design 原校準口徑；converter 實際 gate 輸出 47.1625／26.4625（`phases-core.md:38`）。建議 decisions 註明之後重跑以 converter gate 為準。
10. `$P/data/family-rules.json` 第 9 條 regex 含 `Attack and Cast Speed`，但第 8 條 `Cast Speed` 先命中，該分支永遠不生效（第 8 條 note 看來是刻意；待確認）。建議刪分支或加 note。
11. 「PoE 凍結成品 10 條壞鏈（6 檔＋r2 README 4 條）」數字對不上：`wait-user/later-decisions.md:50`、`…home-2026-11-05/STATE.md:31` 說 10；`wf/workflows/tidy/reports/2026-11-05/README.md:3` 與 `…maintenance/REPORT.md:25` 只算 4（r2 `source/README.md:37×2,176,184`，指上游 docs，非 agentctl）。MANIFEST 鎖住、純文字引用已刪 agentctl 路徑的實際是 4 檔 5 處：1.2.2 `BUILD.md:16`、`research/S2-converter.md:22`；1.2.3 `research/Live-calibration-inputs.md:3`、`research/calibration/REPORT.md:10,12`（另 `analyse.py` 一處），都可從 bf38e9c9e017 取回。建議：統一成實際清單。
12. `CC/mixes.json` MX3「近身接戰立守勢」仍是被取代的固定圈版守衛者，`boundary` 沒標歷史；過目頁 `wf/user/2026-11-04-combat-playstyles.md:63` 已標。建議資料檔跟上。
13. `CC/README.md:11,13` 留「source／公司離線驗證進行中」「仍逐型看，不把 24 案全套全樹」，與 `:9` 24 型補齊、home-setup 1.2.4 已在家建成矛盾。建議刪改。
14. 1.2.4 `Spend`／`Reset`／`SetDebug` 先清該施法者刻印再購點，購點失敗印記已清（`PoeRuntime.cpp:145,152,158`）。建議成功後再清。
15. 1.2.4 換 POET4 圖時 1.2.3 存檔（share-v2）不遷移而隔離成不可編輯（`PoeRuntime.cpp:180`），符合 SPEC 但 README 沒說。建議補一句。
16. `PoeRuntime.cpp:132` `Update()` 拿鎖前讀 `ready`／`allocationsRejected`（主線程呼叫，風險小）；`PoeOverlay.h:11` `WeaponSpeedAmount` 沒檢查有限值。建議移進鎖內／補 isfinite。
17. 1.2.3 `source/tools/__pycache__/` 空目錄（11-04 14:29，未追蹤、不在 MANIFEST），與 `BUILD.md:21`「source 不得有 pycache」矛盾。建議使用者決定是否清（本次未動）。
18. 文件過時字句：1.2.4 `CODE_MAP.md:3`「離線驗收仍在進行」vs `evidence/status.json` sealed；1.2.4 `README.md:5`、`CC/inscription-sample/README.md:5` 留「16:50 前」時效語；r3 `DEPLOY.md:3,7`「尚未部署」、層名少 `-Default`（MANIFEST 鎖住，r3-ready README 已說以 DEPLOYED 為準）；r3 `tools/run_review_mutants.py:3` 寫 five 實跑 9；`audit/REPORT.md`「每職最多 2 項」vs `class-audit-status.json` 3。解凍重發時一併改。
19. 各職 JSON 欄位不統一（`D/rules.json` legacy `compiled` 空字串、M／X 缺頂層 compiled／runtime、`status` 5 種寫法、subtypes 鍵名三種）。建議 collect.py 加正規化。
20. 使用者原話一的每份數值（AR+3、HP 回復+10、CRIT+1、近戰+4、元素抗+3）與 atoms.json（6／5／2／2／2）不同，decisions 只寫「50 份校準反推」未逐項說明（待確認使用者看過完整 per_share 表）。
21. 全集調查狀態說法不一：`wf/user/2026-11-03-perk-units.md:5`「全集調查中」vs `$P/README.md:27`「收工停線、尚未完成」。S7 調查成果在 1.2.2 `research/S7-skill-tags.md`／`S7-rules.json`，phases 未連。
22. 1.2.x 與 r3 相容關係沒寫明：1.2.3 `BUILD.md:11` 說累積 patch 已含 r3、1.2.2 `SPEC.md:19` 說不可用 r3 DLL 代替；但部署 1.2.x 時要不要停 r3 層、ESL 配 r3 DLL 行為未寫（待確認）。
23. Varinia `PAYLOAD.sha256` 列 `FightWithMePaths.pdb` 但 repo 無（SOURCE.md:5 說刻意不進 git）。建議註明預期缺 1。
