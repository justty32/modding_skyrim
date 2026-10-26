# 隨從換頭三頁（2026-10-26 刷新）

[wf/user 索引](README.md)

| 頁面 | 網址 | 用途 |
|------|------|------|
| 換臉挑選 | <https://claude.ai/artifact/BuhFtrZuiGJs8ARz8B5PeE> | 每個隨從現在用誰的臉；勾選後產出「【換臉變更單 LOOKS v1】」貼給 Claude |
| 隨從名冊 | <https://claude.ai/artifact/H1p9Y7YyXf8xmUsL7AcEtT> | 現在裝著的隨從 mod、臉是誰的、有沒有中文 |
| 換頭換身素材目錄 | <https://claude.ai/artifact/CmyAr9aceVnDKQRupkcPLg> | 09-05 的素材目錄與建議配對，10-26 起標上現況 |

10-26 這輪的實際變化：Varinia 換臉後「戴假髮就光頭、洋裝隱形」已修（新層 `Varinia-WoodElf-ARMA-Races-Dev-2026-10-26`）；名冊補上 Varinia／Yoana 漏掉的「外觀」行；素材目錄加了現況欄。其餘資料跟 10-10 版一樣（10-10 之後沒有新的換臉層）。詳情：[face3 REPORT](../../agentctl/handoffs/home-2026-10-26/face3/REPORT.md)。

## 怎麼重產（給 agent）

腳本留在產物所屬的 agentctl repo，沒有搬家：

- 挑選頁：`agentctl/handoffs/done/2026-09/home-2026-09-08/art/tools/build_pick.py`。底稿用線上版：先 Artifact `read` 挑選頁，把存下來的 HTML 傳給 `--src-html`；另外帶 `--modlist <profiles HEAD 抽出的 modlist>`、`--out-dir <當天交接目錄>/pages/pick`。
- 名冊：同目錄 `build_roster.py`，帶 `--pick-html <上一步輸出的 PICK-LOOKS.html>`、`--modlist`、`--out-dir`。
- 素材目錄：`agentctl/handoffs/done/2026-09/home-2026-09-05/hd/build_decision.py`，帶 `--looks-csv <挑選頁輸出的 data/looks-current.csv>`、`--stamp`、`--out`。縮圖不進版控，缺了就加 `--thumbs-from <線上版 HTML>` 抽回來。
- 三頁都用同一個 url 重發；重發前一定要先 `read` 線上版（挑選頁約 60k token）。
