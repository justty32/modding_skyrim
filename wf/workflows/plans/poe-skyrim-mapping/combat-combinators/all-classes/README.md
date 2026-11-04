# 八職業二十四型設計樣板

[可瀏覽審閱頁](../../../../../user/2026-11-04-all-classes/index.html)｜[主管驗收](REPORT.md)｜[語義審核](audit/REPORT.md)｜[幾何核驗](geometry/REPORT.md)

使用者明確選24設計樣板。每職common4A2H與三型各6A2H，共240規則；42原樣板精確reference、198新設計。所有新參數待過目；這輪沒有source/runtime施工。刻印局部source及normal OFF build不代表正常能力開放。

## 職業入口

- [V 先鋒](V/REPORT.md) — [規則](V/rules.json)／[三型摘要](V/subtypes.json)／[參數](V/parameters.json)／[能力與混買](V/feasibility.json)
- [G 近衛](G/REPORT.md) — [規則](G/rules.json)／[三型摘要](G/subtypes.json)／[參數](G/parameters.json)／[能力與混買](G/feasibility.json)
- [D 重裝](D/REPORT.md) — [規則](D/rules.json)／[三型摘要](D/subtypes.json)／[參數](D/parameters.json)／[能力與混買](D/feasibility.json)
- [R 狙擊](R/REPORT.md) — [規則](R/rules.json)／[三型摘要](R/subtypes.json)／[參數](R/parameters.json)／[能力與混買](R/feasibility.json)
- [C 術師](C/REPORT.md) — [規則](C/rules.json)／[三型摘要](C/subtypes.json)／[參數](C/parameters.json)／[能力與混買](C/feasibility.json)
- [M 醫療](M/REPORT.md) — [規則](M/rules.json)／[三型摘要](M/subtypes.json)／[參數](M/parameters.json)／[能力與混買](M/feasibility.json)
- [S 輔助](S/REPORT.md) — [規則](S/rules.json)／[三型摘要](S/subtypes.json)／[參數](S/parameters.json)／[能力與混買](S/feasibility.json)
- [X 特種](X/REPORT.md) — [規則](X/rules.json)／[三型摘要](X/subtypes.json)／[參數](X/parameters.json)／[能力與混買](X/feasibility.json)

## 資料與圖

rules.json是規則真相；legacy reference的source_path用gitRoot代號定位原payload並核row SHA，沒有重寫原3樣板。effective-rules.json是240條輕量索引。geometry/reservation.json保存slot→真ID與完整AND前置，connector/common/subtype分池；ordinary shared connector每ID唯一原payload，只買算一次。geometry/subtypes列完整局部pool普通成本與weight，不以H0短路藏成本。G2/D3/S2長入口警訊是review門檻，未採短替代不自動換位。

24 closure與8 common獨立路是compiled-ready假設下的設計幾何證據；normal新規則仍未ready。SVG/HTML是衍生視圖，不改1993原圖、原55候選、保護3或48keystone政策。完整GGG與私人原始provider資料未收錄。

## 重現工具

collect.py檢查240身份/分層、42legacySHA、資料契約/容量及完整較強requires映射；duplicate ID與缺strong AND反例已證會紅。render.py從資料產生離線HTML，不修改設計或遊戲。工具採明確data-root/repo-root/output/geometry-root參數；wrapper路徑可由gitRoot展開。細節見主管報告與validator-controls。
