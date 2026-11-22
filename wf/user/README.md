# wf/user/ — 給使用者本人看的頁面

這裡放**濃縮結果**：開玩前清單、審批頁、裁示單——使用者要親自讀、親自裁示的東西。
Agent 之間交接的內部報告（各線 `REPORT.md`、`STATE.md` 等）仍留在 [`agentctl/handoffs/`](../../agentctl/handoffs/)；本目錄的檔案只做摘要，連結要連回原始報告。

檔名格式：`YYYY-MM-DD-<主題>.md`。已用完或過時的頁**用畢 30 天直接刪**（[STRUCTURE](../STRUCTURE.md) local 段「過時即刪」）；還被 WAIT_USER open 項或 open 驗收清單引用的頁不刪。產頁腳本產出的 HTML **不進版控**（`.gitignore`），只留腳本與資料。

**門檻**：單頁 ≤ 8 KB，超過就按主題／地點拆子資料夾、原路徑留入口頁；長清單用小節（`###`）切開，不用一張大表。

## 目前檔案

<!-- wf-nav -->
| 檔案 | 內容 |
|------|------|
| [2026-11-22-waituser-runtime.md](2026-11-22-waituser-runtime.md) | 11-22 agent 不存檔代驗 WAIT_USER 結果（S0–S3）：已結案／請看一眼／仍要你本人、EngineFixes 新取捨 |
| [2026-11-22-npc-face-pilot.md](2026-11-22-npc-face-pilot.md) | NPC 換臉試點（Hatak→Muiri）：runtime-3 做成、脖縫已修、已部署但停用，看三方對照圖決定啟用或移除；舊段落拆到子資料夾 |
| [2026-11-16-kurone-soultomb-pick.md](2026-11-16-kurone-soultomb-pick.md) | Kurone Soul Tomb 換臉挑選：68 素材×256 隨從×13 身形，桌面離線頁、可匯出 JSON |
| [2026-11-05-agent-bridge-screenshot.md](2026-11-05-agent-bridge-screenshot.md) | AgentBridge 0.10.0已部署：雙鏡頭目視、20次連拍與切出恢復結果，補充未驗邊界 |
| [2026-11-04-all-classes.md](2026-11-04-all-classes.md) | 八職×三子類24設計樣板：240規則、真圖與High正負情境，可離線過目；新能力未實作／未部署 |
| [2026-11-04-heavy-warden-sample.md](2026-11-04-heavy-warden-sample.md) | 重裝通用＋守衛者：19真點、可攜隊友護援／持盾承諾，純設計無runtime |
| [2026-11-04-guard-double-beat-sample.md](2026-11-04-guard-double-beat-sample.md) | 近衛通用＋浪潮鬥士：19真點、14條規則與原生操作情境；命名一浪接一浪，純設計待過目 |
| [2026-11-04-native-spell-templates.md](2026-11-04-native-spell-templates.md) | Skyrim原生法術三層、10組效果與47有名ID，分清原生配置／腳本／新hook |
| [2026-11-04-inscription-sample.md](2026-11-04-inscription-sample.md) | 術師通用＋刻印：17真點／14候選規則，H0→A4隔離source離線通過，normal未開／未live |
| [2026-11-04-combat-playstyles.md](2026-11-04-combat-playstyles.md) | 八職業×三子類的24原創玩法全貌，含法術遠程恢復召喚及四跨類混搭 |
| [2026-11-04-sword-shield-design.md](2026-11-04-sword-shield-design.md) | 戰鬥組合子與劍盾攻防輔三條可混搭循環提案，數值未定 |
| [2026-11-03-perk-units.md](2026-11-03-perk-units.md) | 星盤效果候選初步抽樣（非完整清單；戰鬥效果全集調查中、皆未採用） |
| [2026-11-02-follower-options.md](2026-11-02-follower-options.md) | 當前隨從可點名方向、五位優先候選與結案排除；附 29 列選項資料 |
| [2026-10-26-follower-stats-gear.md](2026-10-26-follower-stats-gear.md) | 語音隨從能力值／裝備審批頁（59 人逐人勾選、產 VFSTATS 變更單）與重產方法 |
| [2026-10-26-follower-look-pages.md](2026-10-26-follower-look-pages.md) | 隨從換頭三頁（換臉挑選／隨從名冊／素材目錄）的網址、10-26 刷新內容與重產方法 |
| [2026-10-26-mod-library-viewer.md](2026-10-26-mod-library-viewer.md) | 天際儲藏庫（mod 資產庫頁）10-26 刷新：線上頁連結、這次更新了什麼、舊命名檔來源辨識怎麼看 |
| [2026-10-10-play-checklist-mo2-reverify.json](2026-10-10-play-checklist-mo2-reverify.json) | 資料檔（`wf-table/1`）：MO2 首開後要重驗的 plugins.txt 行（行號、該不該有 `*`、順序要求）；`instance/tools/reverify.py` 的輸入，10-10 總頁已於 2026-11-21 刪除 |
| [2026-10-26-moveset-pages.md](2026-10-26-moveset-pages.md) | 招式五頁（姿態配置、裝備分配、總覽、MCO 挑選表、候選）10-26 現況版入口 |
