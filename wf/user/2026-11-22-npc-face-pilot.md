# NPC 換臉試點：把 Hatak 的臉做成 Muiri 的 patch（等你看圖決定）

[wf/user](README.md)｜工作流 [racemenu／bake](../workflows/racemenu/bake.md)｜實機紀錄 `agentctl/handoffs/home-2026-11-22/runtime-3/`｜舊段落 [history](2026-11-22-npc-face-pilot/history.md)

> **現況（2026-11-22 晚）**：使用者裁示「muiri那個就不管了，就這樣。」——Muiri 臉層維持已部署、已停用，不啟用、不刪；本頁以下內容保留作紀錄。

## 最新現況（runtime-3，2026-11-22 傍晚）

**一句話**：做成了。Muiri 的新臉已裝好、實機看過沒問題，但**目前是停用的**（Muiri 還是 JH NPC Beauty 的臉）。請看下面的圖，喜歡就一行指令啟用。

### 看圖

三方對照（左：原本的 Muiri，昏暗酒館；中：Hatak 套在主角身上；右：新 Muiri）：

三方對照（本機圖 `agentctl/handoffs/home-2026-11-22/runtime-3/shots/cmp-three-way.jpg`）

脖子接縫修前修後對照：

脖縫修前修後（本機圖 `agentctl/handoffs/home-2026-11-22/runtime-3/shots/cmp-neck-before-after.jpg`）

更多角度（同一夾 `agentctl/handoffs/home-2026-11-22/runtime-3/shots/`）：正面（`A4-01-front.jpg`）、左側（`A4-02-left.jpg`）、右側（`A4-03-right.jpg`）、頸部（`A4-04-neck-front.jpg`）、全身（`A4-06-body.jpg`）；體重試驗（上 100、中 0、下 50）：cmp-weight-test-grid（`cmp-weight-test-grid.jpg`）。圖是本機檔、不進版控，備份在 `~/skyrim_mods/_backups/runtime-3-2026-11-22/shots/`。

### 技術檢查（agent 實機看過）

| 項目 | 結果 |
|---|---|
| 黑臉（頭和身體顏色不一樣） | 沒有 |
| 脖子接縫 | 第一版有，已修好（見下）；正面、左右側、背面、裸頸都正常 |
| 頭部件（臉型、髮型、眉眼、疤） | 齊全，是 Hatak 的 |
| 貼圖 | 正確，沒有紫色或缺圖 |
| 體重 | 維持 Muiri 原本的 100，身材沒變 |
| 髮型、眉眼 | 灰髮、刀疤、Breton 臉型、Hatak 的濃妝都在 |
| 膚色 | 頭和身體一致 |

**脖縫是怎麼回事**：RaceMenu 匯出的頭，脖子是照「匯出當下主角的體型」做的。第一次匯出時主角載完 Hatak 體型是 0，Muiri 卻是 100，接不起來，脖子底部一圈縫、看得到後面的頭髮。agent 用主控台把 Muiri 體重試成 100／0／50，只有 0 時縫消失，證實是這個原因。重做時在 RaceMenu 把「體型」滑桿調到 1.00 再匯出，縫就沒了，體重也保住。工具也加了檢查，以後體型對不上會直接擋下。

存檔：每場前後 91 個存檔 sha256 全同、ini 全同，**沒有存檔**。

### 喜歡就這樣啟用

先關掉 MO2 和遊戲，在工作區根目錄跑：

```text
python3 instance/tools/layer_apply.py agentctl/handoffs/home-2026-11-22/runtime-3/data/muiri-enable.layer-apply.json --apply --take-lock user-enable-muiri
```

或者在 MO2 裡勾選 mod `Muiri-Look-From-Hatak-Dev-2026-11-22`，並在右邊 plugin 清單勾選同名 esp。

### 不要就這樣移除

**什麼都不用做**：現在就是停用狀態，Muiri 用的是 JH NPC Beauty 的臉。MO2 已自動把這顆停用 esp 從 plugin 清單拿掉，只剩 modlist 一行 `-Muiri-…`（停用）。想連 mod 資料夾都清掉，在 MO2 左邊清單對它按右鍵移除即可。

（不要用 `muiri-r3.revert.json` 的 `--revert --force`：它會把三個設定檔整份蓋回 r3 部署前的版本，若之後別的層改過 profile，會連帶被蓋掉。）

### 已知缺陷與審美

- Hatak 的眼妝、唇色、戰紋很黑很重，原樣帶到 Muiri。不喜歡的話要改 preset 再重做。
- 頸部有一點陰影是光照，不是接縫。
- 身形（胸部大小等）由 OBody／BodySlide 決定，不在這一層。
- 好不好看由你判斷，agent 不宣稱通過。

## 之前的經過（歷史，已過時）

- 第一次試點（4 場）沒做成：主控台改種族後頭不重建，匯出的都是舊部件；沒部署、沒存檔。
- face-pilot-2 改在 RaceMenu 介面點種族，匯出部件正確，做好層但還沒裝。
- 當時申請的三項授權（開遊戲匯出、暫放觸發元件、部署換臉層）都已用完。

完整舊內容（含當時截圖、授權細節、不會做的事）見 [history](2026-11-22-npc-face-pilot/history.md)。
