# 全 repo 重構拆檔與 tidy（瘦身後）

Done when: 各 repo `workflows/` 以 LF 量 >8192 bytes 與 >300 行文件歸零或列出保留理由；過時文件依「過時即刪」刪除；各 repo lint `broken=0`；母 repo 全庫 `check_markdown_links.py` 只剩 MANIFEST 鎖住的 4 條既有壞鏈；各 repo 在 main commit、不 push。

拆：ModForge 16 份 >8 KB 流程文檔（含 5 份 CODE_MAP 子 index，新增 74 檔）、my_skyrim_plugin_1 4 份 >300 行研究筆記（新增 11 檔）、darksouls-port `p1/P1-INGAME-FINDINGS.md`（新增 3 檔）；原路徑都保留當入口。

刪：instance `docs/archive/` 4 檔、sofia-patch `_archive/` 3 檔、ModForge 2 份過時調查／計畫、scene-capture-bridge 1 份已結案調查；仍有效結論先吸收進活文件。

修：agent-bridge AGENTS.md 測試數、godot 兩張導航表標 `wf-nav`、agentctl `user.md` 分工列、lessons `docs-organization` 去掉舊封存規則、母 repo analysis 一處已刪檔引註加取回指令。

lint（broken／oversize／biglist）：ModForge 0／25→7／252→250（剩 5 份連貫解碼筆記依 repo STRUCTURE 保留、2 份為 CRLF 假超標）；sofia biglist 209→192；scene-capture-bridge 7→2；godot 2→0；其餘不變。

保留不拆：完整 spec／連貫筆記（ModForge SPEC-* 9 份、`QUEST_ENGINE_SPEC.md`、sofia `_act1-conversion-spec.md`、母 repo PoE `phases-core.md`）、台詞內容、上游 fork 文件（houseCARL）、MANIFEST 鎖住的成品；>300 行程式無測試或屬程式重構，只列不拆。

收線殘項與待裁示見 agentctl `handoffs/home-2026-11-05/STATE.md` 末段與 [WAIT_USER](../../../../../WAIT_USER.md)。
