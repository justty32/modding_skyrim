# 八職設計工具拆分與交接整理

Done when: 三個原 CLI、240 規則／42 legacy 身份與 HTML／八 SVG 重產不變；導航同步，最新交接與歷史快照分層，整理成果提交與推送完成。

[設計入口](../../../plans/poe-skyrim-mapping/combat-combinators/all-classes/README.md)的工具已依驗證、顯示欄位、視圖、模板與靜態資產拆分；三個原命令保留，輸出仍為離線單頁。[CODE_MAP](../../../common/code-map/CODE_MAP.md)與工具複製邊界同步更新。工具階段先獨立 commit，再整理文件。

正式 collector、240 有效規則／42 legacy、CLI help、HTML 與八張 SVG 原新等價，兩種負例持續拒絕；母 repo 68 項單元測試通過。設計資料與幾何未改，既有全庫檢查缺口保持原樣。詳細交接拆分、快照保全、衛生與遠端核對見 agentctl 本輪記錄（已刪，取回：`git -C agentctl show bf38e9c9e017:handoffs/home-2026-11-04/wrap-tidy/README.md`）。
