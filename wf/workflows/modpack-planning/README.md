# modpack-planning — 整合包規劃

「我想玩什麼、要哪些 mod、怎麼分批裝進去」。內容在
[`modpack-design/`](../../../modpack-design/)。

```text
Done when: <方向已定、mod 集合已選、分批順序與每批的 rollback 已寫、技術債已登記>
```

## 現役整包

現役 profile 是 **`modpack-main`**；目前規劃入口是
[`LoreRim 借用段`](../../../modpack-design/content-plan/lorerim/)與
[`GO 19`](../../../modpack-design/content-plan/install-plans/go19-2026-09-02.md)。每階段都要有
**rollback 與完成條件**，不能只寫「裝這些」。

## 四份輸入

| 想知道 | 看哪裡 |
|---|---|
| 現在裝了什麼 | `instance/`（**唯讀盤點**，不要憑記憶或舊快照） |
| 有什麼可以玩 | [`modpack-design/content-plan/`](../../../modpack-design/content-plan/) 的領域 OPEN 帳與現役批次 |
| 來源與取得狀態 | [`modpack-design/sources/OPEN.md`](../../../modpack-design/sources/OPEN.md)；未查證素材不能當判定結論 |
| 決定要裝什麼、按什麼順序 | [`content-plan/`](../../../modpack-design/content-plan/)；現役批次見 [`GO 19`](../../../modpack-design/content-plan/install-plans/go19-2026-09-02.md) 與 [`LoreRim 借用段`](../../../modpack-design/content-plan/lorerim/) |
| 哪些有中文、下一步做什麼 | [`content-plan/zh-layer/`](../../../modpack-design/content-plan/zh-layer/)（缺口盤點與現成層拓撲 gate） |
| 這個 mod 技術上怎麼運作 | [`analysis/mod-survey/`](../../../analysis/mod-survey/)——**這不是遊玩規劃，別混在一起** |
| 已知的雷 | [`technical-debt.md`](../../../modpack-design/technical-debt.md)（單一權威清單） |

## 規劃時要先問的

- **這是選型還是執行？** 選型進 `modpack-design/`，執行紀錄進 `agentctl/logs/`。混在一起就再也分不清哪份是決定、哪份是流水帳。
- **這批會不會動到現役 profile？** 會的話走 [profile-change](../profile-change/README.md)，
  一批一個 `feat/*`，不要把好幾批塞進同一條分支。
- **前置相依查了嗎？** 用 houseCARL 查 requirements，不要讀 mod 頁的敘述就當事實。
- **中文層有嗎？** 沒有同版就照成本規則決定維持英文還是自己做，見
  [localization](../localization/README.md)。

## 遷移類規劃要特別小心

Gameplay 生態遷移的現行階段與回滾只看
[`content-plan/gameplay/`](../../../modpack-design/content-plan/gameplay/)；不要從歷史快照推論現役 `modlist.txt`。

## 何時不用

- 只是想記一個「之後也許要玩」的念頭、或確定會做但不確定何時 → [planning](../planning.md)。
- 已經要動手裝了 → [nexus-intake](../nexus-intake/README.md) ＋ [profile-change](../profile-change/README.md)。
