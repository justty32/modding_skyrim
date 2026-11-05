# PoE 星盤一次性審查（2026-11-05，Fable，只讀不改）

Fable 2026-11-05 只讀審查；PoE 仍暫凍，此為解凍前待辦參考。

問題清單分檔：[中嚴重度 1–7](issues-mid.md)、[低嚴重度 8–23](issues-low.md)。問題 1（r3／Varinia 補 .gitattributes）與問題 2（r3 報告取回指令）已於 2026-11-05 處理，其餘未動。

範圍：設計一致性、實作對照、部署／回退、解凍阻礙。方法：頂層親自讀規矩與計畫核心檔、核對資料檔與取回指令；三條子線分別審設計資料、IndependentSkills 1.2.1→1.2.4 原始碼、NativeCombat r2／r3 部署與回退；子線的中嚴重度主張由頂層逐條復核。未改、未刪、未 commit；未 build、未部署、未碰 instance／MO2／遊戲／DB／網路；只跑了不寫檔的 Python assert 段與 `sha256sum -c`。路徑相對 `/mnt/c/code/mine/modding_skyrim`；`P`＝`wf/workflows/plans/poe-skyrim-mapping`、`CC`＝`$P/combat-combinators`、`PL`＝`mod-library/plugins`。

**整體結論**：沒有高嚴重度問題。設計資料（27 atom／49 規則／48 keystone／240 規則／24 型）內部一致，四版 IndependentSkills 沒有回退、無明顯 bug，r3 現役部署事實與文件一致、r1／r2 回退來源與回退 json 都取得到。真正要處理的是：r3 成品夾少了 `.gitattributes` 導致 Windows checkout 核 hash 會假失敗；r3 部署報告已刪但多處沒附取回指令；守衛者多 giver 規則舊提案未撤；兩條 1.2.4 程式邊界問題；若干文件數字／狀態過時。

## 已核對無誤

- 資料檔：atoms 27（AV 22／ESL 4／SKILL 1）、family-rules 49 條份額加總皆 1、keystones 48（29／9／9／1；批次 18／8／8／2／2；互斥 18 個 6 組與 X1–X6 逐一吻合）、mechanic-decisions 11 列；effective-rules 240 條 ID 唯一、=8 份 rules.json 聯集、176 進階＋64 高階、legacy G14／D14／C14＝42、24 型全有規則、collection-status 全 checked。
- 點數：每級 1 點、1／3／5 份在 decisions／design／phases／過目頁一致；1.2.1 `PoeGraph.cpp:43` ×5 是當時授權，1.2.2 起 `kPointsPerLevel=1`；存檔 tag 鏈 unit-v1→share-v1→share-v2→share-rule-v1 遷移保留高水位、未知 tag 隔離；POEC 存讀對稱。
- 1.2.3 起玩家入口／零 companion 路徑符合 phases-core S3；1.2.4 刻印 normal 關閉（`kNativeHitBoundaryValidated`／`kMarkerLifecycleValidated` false）、experimental tag 另加後綴；版號 1.2.1–1.2.4 一致、f510836／fc9a7f6 與 153 筆 snapshot 一致；INI 四版 byte 相同；四包 MANIFEST 92／115／239／241 全綠（LF 工作樹）；payload 無 PE，與「PE NOT BUILT」一致。
- r3 部署：DLL `c299ecb…`、INI `b2881bf…`（git blob）、層名、備份路徑、profile `4857a8c`（存在、在 origin/main）與已刪報告 3db1b772 版一致；r2 payload DLL `87148ff…`／INI `0949a39…` 與 HOME-DEPLOY 吻合；回退 json 四檔與 r2 rollback 兩檔都在 `3db1b772`；`instance/tools/layer_apply.py` 有 `--revert`／`--apply`／`--revert-out`。八組 host（`evidence/offline.log`）與九個 mutation（`evidence/mutation-results.json` 9 列）證據在。
- 取回指令：所有 `bf38e9c9e017:` 與 `3db1b772:` 路徑 `cat-file -e` 全 OK；三個 commit 都在 agentctl origin/main；mod-library pin 7a75e89 在 origin/main；1.2.3 聲稱的 bdaa1a12 存在。`waituser_count.py --check` 8／12／13／7 全 OK；S16 8 項與計畫一致。Markdown 超連結（計畫、過目頁、四包、r2／r3）壞鏈 0（除 r2 source README 4 條上游 docs）。

## 跑了什麼

- `python3 -I` 解析所有 JSON／CSV 統計；1.2.2／1.2.3／1.2.4 `source/tests/test_poe_converter.py` 純記憶體 assert 段 PASS（`-I -B`）；r2／r3 8 個 Python 腳本 `ast.parse` OK；`sha256sum -c` 與 git blob 比對。
- 未跑（會寫檔／需外部依賴）：converter 測試後半、`carriers/test_payload.py`、`test_reference_scan.py`、`run_checks.py`／`prepare_source.py`、`run_nativecombat_offline.py`、`run_review_mutants.py`、`verify-pe.py`。

## 解凍前必須先處理

1. r3／Varinia 補 `.gitattributes` 或驗收指南註明 Linux／git blob 核 hash（問題 1）。
2. 補 r3 部署報告取回指令（問題 2）。
3. 審閱證據（RUBRIC 等）收進 repo 或宣告不存在，否則 24 型 readiness gate 無法續（問題 6、7）。
4. model.md 舊提案標廢，mixes MX3 標歷史（問題 3、12）。
5. 1.2.4 兩條程式邊界（epoch、SkillPercent）排進下一候選（問題 4、5）。
6. 壞鏈數字統一成實際清單，重發時一併修（問題 11、18）。
