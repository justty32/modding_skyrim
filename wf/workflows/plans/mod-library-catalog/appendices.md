# 附錄 A 韓文站採集／附錄 B 漢化管理

> 屬於 [mod 下載庫建檔與清理（MongoDB）](README.md)。

## 附錄 A：韓文站採集工作流（使用者 2026-08-04 提出，待轉 `workflows/roadmap/`）

**需求**：使用者對韓文圈的**人物美化、獨立隨從、武器裝備、其他遊戲地圖 porting** 長期感興趣，想讓 `agy` 多次長時間爬，先抓**截圖與簡介**進一個資料夾供審閱，審過才下載；並要檢查**下載連結是否還有效**。

已定的形狀：

- **這是「發現階段」，接在流水線最前面**，產出 `candidates` collection（不是零散資料夾）。放 Mongo 的關鍵理由是**否決狀態要能持久**——長期多次爬，被否決過的不該再次出現在審閱清單裡。
- 審閱介面用**本機 HTML 圖庫**（截圖 + 翻譯後簡介 + 原始連結 + 連結存活狀態），對應本 repo 既有的 `html-guide` 工作流形狀。
- 執行者是 `agy`（姊妹計畫 D7），主 session 出 schema 與判準、收斂結果。爬取本身外包。
- 連結存活檢查：HEAD 請求，狀態寫 `link_status` + `link_checked_at`。
- **地圖 porting 類與 `projects/darksouls-port` 及 `analysis/port-source-survey/` 直接相關**，採集到的候選應該回饋那份調查。
- 邊界：需登入／入會審核的站（Naver cafe 類）不做；公開板（arca.live、公開部落格）可做。

## 附錄 B：漢化管理（使用者 2026-08-04 提出，待轉 `workflows/roadmap/`）

**需求**：Nexus 下載的東西要順便抓漢化；漢化版本不對要能補強；韓文站抓回來的也要檢查並做漢化。

已定的形狀：

- **起點不是零**：庫裡已有大量 `- CHS` / `- CHT` / `(Chinese Translation)` 檔（實查確認，如 `Honed Metal` 一組六個變體）。本計畫的 `is_translation` / `translates_mod_id` 就是給這件事鋪路的。
- **資料模型陷阱（2026-08-07 A4a）**：漢化包在 Nexus 上常有自己的 mod id，所以 `mods` 裡會出現純漢化包 stub（`archive_ids=[]`、`translation_archive_ids` 非空）。A4a 實掃有 255 個這種 stub。比對本體時必須排除它們，只比對 `archive_ids` 非空的真本體；否則會把漢化包配到另一個漢化包，實例是 `Beyond Skyrim - Bruma SE (CHT)` 被配到 `Beyond Skyrim Bruma - CNS`。
- **A4a 掃出的翻譯衍生標記**（剔除誤收的 `MCM`、`CLEAN`）：`CHINESE`、`CHS`、`CHT`、`CNS`、`Chinese`、`Chinese Localisation`、`Chinese Localisation Based on WOK`、`Chinese Simple`、`Chinese Translation`、`Chinese translation`、`Chinese version`、`Simpifity Chinese`、`Simplified Chinese`、`Simplified Chinese Translation`、`Simplified Chinese translation`、`Traditional Chinese`、`Traditional Chinese Translation`、`Traditional Chinese translation`、`ZH`、`\CHS\`、`\CHT\`、`\chs\`、`\cht\`、`chinese translation`、`chs`、`cht`、`cns`、`simplified Chinese`、`simplified Chinese translation`、`traditional Chinese`、`traditional Chinese translation`、`zh`、`zh_CN`、`汉化`、`汉化补丁`。
- **版本不對的正確解法不是換 esp。** 漢化包通常是整份 plugin 替換——拿 v1.0 的漢化 esp 蓋 v1.2 的本體，等於把 v1.2 的所有改動退回 v1.0。正確做法是**只把譯文欄位（FULL / DESC / 對話）forward 到當前版本的 plugin，輸出成 patch**。houseCARL 的 `forward_record` / `bulk_apply` / `set_field` / `cross_plugin_query` / `batch_record_detail` 正是這組工具，能力已經在手上。
- **最大的技術陷阱是編碼。** Skyrim plugin 的字串或內嵌（非 localized，Windows-1252）或走 `Strings/*.STRINGS`（localized）。中文無法用 Windows-1252 表示，所以漢化包要嘛走 localized strings、要嘛靠 codepage 詮釋的老 hack。**houseCARL 目前就有一條 `fix/dialogue-encoding-lint` 分支掛在 `WAIT_USER.md`**——編碼在自家工具鏈裡已經是活的議題，不是理論風險。動手前先把那條分支的結論確定。
- 非 plugin 的字串也要顧：MCM 的 `Interface/Translate_<name>_<lang>.txt`、SkyUI MCM 的 json、`.pex` 內硬編字串（難）、語音 `.fuz`（`projects/skyrim-voicegen` 是另一條路，屬 TTS 不屬翻譯）。
- 資料模型參考 RimWorld 的 `diy_translates`（`target_package_ids` / `target_details` / `translation_files` / `file_count`），結構可直接對應。
