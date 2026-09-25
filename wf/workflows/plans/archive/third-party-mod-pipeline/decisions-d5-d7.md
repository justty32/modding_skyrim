# 設計決策 D5–D7

> 屬於 [第三方 mod 取得–安裝–驗證流水線](README.md)。

## 二、已定案的設計決策（續）


### D5：下載維持人工發動，不做瀏覽器自動化

免費帳號下 Nexus 的 download 端點是 Premium 限定，自由帳號的下載路徑**不在 API 裡**。驅動網頁的 Slow Download 按鈕違反 Nexus ToS、有封號風險，CAPTCHA 也無法代解。

改為：AI 產出**下載工作單**（mod 頁 URL、精確檔名 + 版本、依賴樹已解、安裝順序註記，Nexus 來源用 `housecarl_nexus_search` / `housecarl_nexus_mod`），使用者一次點完，檔案落 `~/Downloads`，AI 從那裡接手。**流水線從 `~/Downloads` 往後與來源無關。**

**多來源的分工**（使用者 2026-08-04 討論韓文站與俄語站後定案）：

| AI 做 | AI 不做 |
|---|---|
| 讀公開頁面、**翻譯外語**、整理需求／前置／安裝說明（語言隔閡是非英語站最大門檻，此處價值最高） | 需登入／入會審核的站（Naver cafe 等）的登入動作 |
| `~/Downloads` 之後的全流程（與來源無關） | 從匿名檔案空間（Mega／Drive 直鏈）代抓二進位檔 |
| 框架類（SKSE DLL、papyrus util）的技術資訊整理 | — |

**非 Nexus 來源的兩個實務差異**：(a) 無 API 可查版本與依賴 → `mo2ctl` 會填預設 `version=0.0.0` / `modid=0`，來源與版本必須靠 `manifest.json` 手記；(b) 社群站台的框架類常鎖 SKSE runtime 版本，本機鎖 1.6.1170 → `housecarl_skse_inventory` 的版本鎖偵測對這些來源**比對 Nexus 更關鍵**。

若日後上 Premium，API download 路徑就開了，D5 值得重新評估；目前不值得。

### D7：搜尋與抓取外包給 `agy`（使用者 2026-08-04 提議，同日實測可用）

`~/.local/bin/agy` 是另一套 agentic CLI，有 print mode (`-p`)、`--output-format json`、`--json-schema`（可強制結構化輸出）、`--model` 可選（gemini-3.6-flash / claude-sonnet-4-6 / gpt-oss-120b 等）。**候選調查與頁面抓取這類跑量的活外包給它**，主 session 只做 schema 設計與判斷取捨。

- 理由：搜尋抓取是 token 大戶但判斷含量低，用便宜模型跑量、貴模型收斂，成本結構才對。與既有慣例一致（簡單的事實查證／盤點交給便宜的 subagent）。
- 用法：`agy -p "<查詢>" --output-format json --json-schema <schema>` → 結構化候選清單。**schema 要自己出**，不然回來的是散文，還得再解析一次。
- **輸出一律當未驗證資料。** 2026-08-04 實測俄語站台調查，回報結構完整、內容看似合理，但「下載是否需登入」這類會變動的事實仍須在真正要用時現場確認。它的角色是把搜尋範圍收窄，不是提供事實裁決。

實測結果（俄語圈站台）記在下方附錄。

### D6：靜態關卡先行，遊戲啟動是最後一關

冷啟動一輪 20–30 秒，且 Proton 反覆冷啟動會累積不穩（上游五節風險）。第三方 mod 帶的問題大多不必開遊戲就能抓：

| 檢查 | 抓什麼 |
|---|---|
| `housecarl_load_order_status` | 缺 master、stale 條目、mod/plugin 啟用狀態對不上 |
| `housecarl_check_errors` | FormID 衝突、結構性錯誤 |
| `housecarl_skse_inventory` | **SKSE DLL 鎖死在別的 runtime 版本**、DLL 被兩個 mod 爭用、非 plugin DLL 混入 |
| `housecarl_validate_scripts` | 帶進來的 Papyrus 腳本能否成立 |
| `housecarl_validate_dialogue` | 對話條件／分支斷裂 |

**且一次只裝一個（或極小批）再跑一輪。** 一口氣裝十五個再測，紅燈時無法歸因——這也是 D3 分支制的前提。

houseCARL 目前是 explicit-paths mode，要先 `housecarl_set_mo2_instance` 指向 MO2 instance，並用 `housecarl_set_tool_path` 補上 `papyrus_logs` / `crash_logs` 兩個路徑（診斷時要讀）。
