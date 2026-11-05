# 星盤效果單位：候選過目

[使用者頁面索引](README.md)｜[星盤計畫](../workflows/plans/poe-skyrim-mapping/README.md)

離線過目頁 `2026-11-03-perk-units/index.html` 不進版控，跑同夾 `render.py` 重產（PoE 暫凍中不重產）：目前 10 個進階數值候選、10 個高級能力候選是**初步抽樣，非完整清單；全集調查中**，可篩選類型與需另裁示的項目。每項列出來源原值與提案、觸發和疊加、例子及風險；技術證據可展開。

全集調查限戰鬥相關效果；新增互動選項暫緩，非戰鬥效果排除。原樣本中屬於這兩類的項目目前不採用、不繼續深入。H3「格擋走位」的全速能力仍待證，不算已確定的高級效果。

這些都是調查提案，**尚未採用**。進階效果的數值與混合效果的數值部分需請你過目確認；高級能力也尚未選定。M3、M6、A5、MA06、MA05 涉及額外原則或限制，頁面特別標為「另裁示」。已安裝但未勝出的天賦樹也可參考。

初步研究與證據見 private 研究報告（已刪，取回：`git -C agentctl show bf38e9c9e017:handoffs/home-2026-11-03/installed-perks/REPORT.md`）。離線頁及 [公開用資料摘錄](2026-11-03-perk-units/review-data.json) 可由研究表重產；來源 SHA-256 顯示於頁尾。研究表已隨場次夾刪除，重產前先從 git 取回到暫存目錄 `$T`，再從母 repo 執行：

```sh
git -C agentctl archive bf38e9c9e017 handoffs/home-2026-11-03/installed-perks | tar -x -C "$T"
python wf/user/2026-11-03-perk-units/render.py "$T"/handoffs/home-2026-11-03/installed-perks
```
