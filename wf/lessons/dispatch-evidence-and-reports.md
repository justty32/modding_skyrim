# 調度：收線查證與報告證據

[lessons 索引](README.md)｜交接書寫法見 [dispatch-handoffs](dispatch-handoffs.md)

## dont-trust-subordinate-self-report-verify-yourself

> 下屬自報「檢查通過」「已完成」不能直接採信，收線要重算或要可查證依據

例：自報連結檢查通過，重跑同一腳本抓出斷鏈（2026-08-27，`agentctl/handoffs/done/2026-08-27/opus-gaps/_COMMON-LIMITS.md:29`）；自報「已內化」的換臉層逐層清點仍依賴素材 mod（2026-09-08，`agentctl/handoffs/done/2026-09/home-2026-09-08/face/REPORT.md:105`）。同類坑：`FAILED-not-started` 只是未開始非真失敗；沒收終局訊息也可能是延遲非沒做完；領隊自稱「使用者說過 X」同樣不算數。

**How to apply:** 逐條對可查證來源與驗收；缺證據、有矛盾或高風險才補算／派獨立覆核，不每步重做。見 [[verify-waituser-against-logs]] 與 [[trust-gpt-sol-more]]。

## cite-by-anchor-not-line-number

> 證據表／交接書引用檔案要用錨點字串定位，不能寫死行號——別線同時在改會讓行號整批漂移

被引用的現役檔有別線同時在改時，行號位移、整張證據表漂掉（2026-09-02，`agentctl/handoffs/done/2026-09-02/lorerim-2026-09-02/team-gap/REPORT.md:46-63`；`agentctl/handoffs/done/2026-09/home-2026-09-03/old/REPORT.md:52`）。另一面：跨行複合敘述塞一欄只引一行，被引行自己證不了主張。

**How to apply:** 證據表附錨點重定位腳本、commit 前再跑一次；每列主張要能被所引那一行單獨證實，跨行脈絡移進備註欄。

## dont-hardcode-mutable-snapshot-values

> 驗收斷言、共用計數表若寫死被裁示改變的快照值，值一變就連環 BLOCKED

例：驗收寫死「件數分佈 10/5/12」，裁示改件數後連環 BLOCKED（`agentctl/handoffs/done/2026-09/home-2026-09-03/dl/REPORT.md:133`）；「sha256 不變」寫成建包常數，多包套用同一 profile 時前包已改過，直接 FAIL（`inst/REPORT.md:94`）；兩線同改一張計數表，用「開工當下讀到的數字加減，不寫目標值」解掉（`agentctl/handoffs/done/2026-09-01/cx-land-plan/HANDOFF.md:55-57`）。

**How to apply:** 驗收只斷言總數與集合完整性；aux「未變」當下重算；計數表給增減量不給目標值。

## universal-claims-need-the-command-or-silence

> 報告裡的全稱命題（「全部都是」「無任何」）要麼附上產生它的指令與輸出，要麼不要寫（2026-10-23）

全稱命題多半來自「看了 top-N＋尾巴」的印象歸納（例：報「兩條連結」實際九條），讀報告的人卻會把它當已驗證的不變量去推論。

**How to apply:** ①寫「全部／無任何」前跑一條能證明它的指令（`grep -c`、集合 diff、`comm`），指令與輸出一起貼進報告；跑不出來就寫成「top-N 看到的都是…」。②安全性論證靠判準本身的構造（如「全歷史掃描 ∖ 全分支 HEAD 聯集」），不靠歸納。③驗收別人報告裡的全稱命題，視同未驗證，抽一條反例查。
