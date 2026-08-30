# modpack-planning — 整合包規劃

「我想玩什麼、要哪些 mod、怎麼分批裝進去」。內容在
[`modpack-design/`](../../../modpack-design/)。

```text
Done when: <方向已定、mod 集合已選、分批順序與每批的 rollback 已寫、技術債已登記>
```

## 現役整包

現役 profile 是 **`modpack-main`**；Gameplay 下一步是
[`EnaiRim Batch 0–7`](../../../modpack-design/content-plan/gameplay/enairim-final-selection-2026-08-24.md)：

```text
來源 intake → 種族/立石 → 信仰/吼聲 → 魔法 → 附魔 → 戰鬥 → 終態驗收
```

每階段要有 **rollback 與完成條件**，不能只寫「裝這些」。

## 四份輸入

| 想知道 | 看哪裡 |
|---|---|
| 現在裝了什麼 | `instance/`（**唯讀盤點**，不要憑記憶或舊快照） |
| 有什麼可以玩 | `modpack-design/content-plan/` 的四份內容普查（主線／地城敵人／隨從戰鬥／進程結構） |
| 使用者最近想要什麼（未查證的 Nexus URL） | [`mod-url-inbox.md`](../../../modpack-design/sources/mod-url-inbox.md)——**這是未查證素材，不是判定結論；逐件事實查證後才進 `content-plan/`** |
| 決定要裝什麼、按什麼順序 | [`install-plan-2026-08-27.md`](../../../modpack-design/content-plan/install/install-plan-2026-08-27.md)（**整包唯一一份安裝計畫**，每列有 id／fileId／版本／bytes） |
| 哪些有中文、下一步做什麼 | [`zh-layer-coverage-master-2026-08-28.md`](../../../modpack-design/content-plan/zh-layer/zh-layer-coverage-master-2026-08-28.md)（中文層唯一決策層） |
| 這個 mod 技術上怎麼運作 | `analysis/mod-survey/`（136 份框架拆解）——**這不是遊玩規劃，別混在一起** |
| 已知的雷 | [`technical-debt.md`](../../../modpack-design/technical-debt.md)（單一權威清單） |

## 規劃時要先問的

- **這是選型還是執行？** 選型進 `modpack-design/`，執行紀錄進 `agentctl/logs/`。混在一起就再也分不清哪份是決定、哪份是流水帳。
- **這批會不會動到現役 profile？** 會的話走 [profile-change](../profile-change/README.md)，
  一批一個 `feat/*`，不要把好幾批塞進同一條分支。
- **前置相依查了嗎？** 用 houseCARL 查 requirements，不要讀 mod 頁的敘述就當事實。
- **中文層有嗎？** 沒有同版就照成本規則決定維持英文還是自己做，見
  [localization](../localization/README.md)。

## 遷移類規劃要特別小心

整套 gameplay ecosystem 的替換（例如 Simonrim → EnaiRim）**不會一次做完**，
中間會長期停在混合狀態。所以：

- 規劃文件要寫**現在做到哪一階段**，不要只寫終局
- 不要因為「已經在遷移了」就把舊系統的待辦當作廢——**去查 modlist**。
  2026-08-23 查過一次：Adamant／Mysticism／Thaumaturgy／Apothecary 都還啟用著，
  而 Apocalypse／Wintersun／Imperious 那批全是停用，遷移根本還沒過半

## 何時不用

- 只是想記一個「之後也許要玩」的念頭、或確定會做但不確定何時 → [planning](../planning.md)。
- 已經要動手裝了 → [nexus-intake](../nexus-intake/README.md) ＋ [profile-change](../profile-change/README.md)。
