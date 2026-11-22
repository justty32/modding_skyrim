# racemenu／loop — 看結果：離線預覽、遊戲內確認、使用者選定

[racemenu](README.md)｜[WORKFLOWS](../../WORKFLOWS.md)

段 3–5。**段 4 有工具、已實機跑通，但取景重現性還不夠好**；段 3 未做；段 5 沿用 `wf/user/` 模式。現況依據：`agentctl/handoffs/home-2026-11-22/face-loop/REPORT.md`（2026-11-22，6 場）。

| 迴路 | 看得到什麼 | 每輪成本（實測） | 定位 |
|---|---|---|---|
| ③ 純數值（[author](author.md)） | 只有數值 | 秒級 | 產生候選、插值 |
| ② 離線出圖（段 3） | — | — | **未實作**（計畫 R1／R2） |
| ① 遊戲內截圖（段 4） | 真實畫面 | 開場 2.5 分鐘（主選單 110 秒＋設定 40 秒）；之後每份 12–20 秒（選單內）或 30–36 秒（世界取景） | agent 自己篩、最後 1–3 份給使用者看 |

## 3. 離線預覽

**未實作**。需要 FRTRI003 解析與渲染器（計畫 R1／R2），SUV 路線要使用者授權裝 PyQt6。

## 4. 遊戲內確認（閉環）

工具：`agentctl/tools/face_loop/cli.py`（[tool-index](../../../agentctl/docs/tool-index.md)「RaceMenu 看圖閉環」列）。授權同 [README](README.md#授權邊界)：開遊戲、取鎖、送按鍵（使用者不在電腦前或當場同意）、暫放 jslot、不存檔。

一條指令：

```text
python3 agentctl/tools/face_loop/cli.py run --race Breton --sex female --out <輸出夾> --list <清單.txt>
```

分步：`start`（開場、設定角色）→ `shoot`（可重複呼叫，沿用同一場）→ `stop`（退出＋保護比對＋收回＋放鎖）。`calib-gen` 產校準變體，`sheet` 產對照圖。

### start 做的事

1. 資源閘：load ≤ 核心數×0.8、可用記憶體 ≥ 8 GB。取 desktop→game 鎖（`--wait-lock` 可等別條實機線）。
2. 存檔、三個 ini、profile 三檔取 sha256。
3. **暫放 slot 檔**：overwrite 的 `SKSE/Plugins/CharGen/Presets/0_FL.jslot`，只建這一個檔，`stop` 收回並刪掉本工具建的空目錄。
4. `launch-mo2.sh --skse` → 主選單 → 主控台 `coc QASmoke` 開**新角色**（不讀任何存檔）→ 自動按掉單一按鈕的訊息框（`Done Writing`）。
5. `setini` 關計時自動存檔並回讀。
6. 女性先 `player.sexchange`，再 `showracemenu`，在 **Sliders→種族** 用滑鼠點種族（頭才會重建，見 [lessons](../../lessons/faces-racemenu-runtime.md)），用 `player.getisrace` 驗。LCtrl 關 RaceMenu 補光。

### shoot 每份做的事

把 jslot **覆寫進同一個 slot 檔** → Presets 分頁 F9 → 點清單第 1 列（場內外部改寫同名檔，再載入讀到的是新內容，S1 實證）→ 等 3 秒 → 拍。每份輸出 `<名>/<角度>.png`、`meta.json`（來源 jslot 雜湊、耗時、挑幀紀錄），`run.json` 彙整耗時與重現性。

兩種取景（`--mode`）：

| 模式 | 做法 | 每份 | 問題 |
|---|---|---|---|
| `menu`（預設） | 留在 RaceMenu，切 Camera 分頁（沒有左欄），`player.setangle` 轉身 | 12–20 秒 | 待機動作會晃；**頭會追相機**，轉身角度不等於臉的角度，拍不到真側面 |
| `world`（實驗） | 關 RaceMenu，第三人稱＋`fov 30`，`tfc` 凍相機，主角移到相機前轉身；背景板相減找頭頂、以頭為中心裁切 | 30–36 秒 | 光線自然、角度真；但第三人稱相機每份停的位置不固定，姿勢也會變 |

兩種都用連拍挑幀（`--burst`，挑和該角度參考圖最像的一張）壓姿勢雜訊。

### 重現性（同一份 preset 重拍兩次）

量測：整張裁切圖的 `changed`（任一通道差 >24 的像素比例）與 `mean_abs`（0–255）。

| 取景 | 正面 changed | 側／斜 changed |
|---|---|---|
| 選單內，連拍 1 張（S2） | 0.40 | 0.22–0.41 |
| 選單內，連拍 6 張挑幀（S3） | 0.18 | 0.20–0.37 |
| 世界，以頭對齊（S5） | 0.31 | 0.10 |

**還不到「幾乎一致」**（目標應在 0.05 以下）。±0.5 的大幅變化（如下顎寬窄）看得出來；±0.1 這種一輪步幅的差異，目前的雜訊會蓋掉，比較時要同場、同角度、看多張。

### 已知坑（6 場實機）

- 載了女性 preset 之後再 `sexchange`＋UI 點別的種族，skee64 崩潰（S1，`SkyrimSE.exe+0CEC5E9`，RaceSexMenu 重建臉時）。**一場只做一種性別**；男性要另開一場、不先載女性 preset。
- 主控台 `tfc 1` 在 RaceMenu 內會把相機丟回第一人稱、RaceMenu 相機回不來（只能關選單重開）。
- 第一人稱下 `tfc` 看不到自己的身體；世界取景要先按 F 切第三人稱。
- 新角色第一次關 RaceMenu 會觸發一串 mod 開場任務與通知（只在這個不存檔的新角色上，退出即消失）；通知會疊在臉上，世界取景時用 `tm` 關 HUD。
- 送輸入一律走 `menu_drive` 的焦點／游標閘；使用者回來動了鍵鼠，工具就停（exit 4）。

### 禁區

不存檔、不讀使用者存檔、不改 ini（`setini`／`fov` 只動記憶體，場後 ini 雜湊比對）；不在沒開 RaceMenu 時送 F5／F9。

Done when：每份候選有截圖與 `meta.json`；`stop` 的 `guard-compare.json` 存檔與 ini 不變；slot 檔已收回；兩把鎖都放了。

## 5. 使用者選定

美醜由使用者判定。挑選頁沿用 `wf/user/` 模式：每份候選一格，放圖和 author 的回報表那一列；回報表的「看過圖嗎」改填「是（遊戲內，<模式>）」。使用者回覆前在 [WAIT_USER](../../../WAIT_USER.md) 記一行。

Done when：使用者回覆選哪一份，或要求再調一輪（回到 [author](author.md#2-合成文字需求滑桿)）。
