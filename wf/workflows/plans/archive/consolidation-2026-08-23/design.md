# 提議的佈局與內容分流

> 屬於 [工作區統整與四條新線（2026-08-23）](README.md)。

## 提議的佈局

```
skyrim/                          ← public 母 repo
├─ README.md  AGENTS.md  CLAUDE.md        入口三件套
├─ wf/                                    工作流骨架（8 個骨架 md + 現 workflows/）
│
├─ agentctl/          ★4  AI 操控總控     public submodule，頂層
│
├─ projects/
│  ├─ instance/       ★1  本地 Skyrim 管理  private submodule
│  │   └─ profiles/                        → modpack-kr-profiles (private)
│  ├─ mod-library/    ★2  本地 mod 管理     private submodule
│  ├─ modpack-design/ ★3  整合包設計        public submodule
│  └─ （原有 11 個軟體開發 repo 不動）
│
├─ analysis/                              引擎／SKSE 知識（扣掉 mod-survey）
├─ external/                              他人素材落點
└─ patches/
```

### 為什麼 1／2 要 private

- **`mod-library`**：我們做的漢化層是**他人 mod 譯文的衍生作品**。放 public repo 是散布問題，
  不是隱私問題，但一樣不能做。
- **`instance`**：本身不算機密，但它掛的 `profiles` 已經是 private，且內容是從 private 的
  `~/notes` 搬過來的。維持 private 才不會在搬移過程中降級。
- **`modpack-design`** 是調查與規劃，public 沒問題。
- **`agentctl`** 是工作流與工具，public 沒問題（Nexus API key 一律走環境變數，不進 repo）。

### 一點保留意見：`projects/` 的語意被稀釋

`projects/` 現在的定義是「獨立**軟體**開發 repo，彼此靠協議／CLI 對接、不整合」
（見根 README）。1／2／3 是**狀態與知識**，不是軟體。混在一起後這層分類就不再說明任何事。

我照使用者說的放進 `projects/`，但建議在根 README 把表格拆成
**開發線**（ModForge、scene-capture-bridge…）與**管理線**（instance、mod-library、modpack-design）
兩張，讓分類重新有意義。若你偏好乾淨切開，替代方案是 1／2／3 也升頂層，`projects/` 維持純軟體。

## 內容怎麼分流

這四條線**不是四個新空資料夾**——三條的內容已經散在現有各處，這次是重新分割：

| 新線 | 從哪裡來 |
|---|---|
| `instance` | `~/notes/.../skyrim/` 的 `logs/` `backups/` `qa/`；MO2 設定備份；`WAIT_USER.md` 的部署類條目；profiles submodule |
| `mod-library` | 現 `dist/`（59MB／393 檔，自製成品）→ `mine/`；漢化層產物 → `l10n/`；`~/skyrim_mods/`（125GB 留原地）只放 manifest → `downloads/`；現 `external/` 的職責併入 |
| `modpack-design` | 現 `analysis/mod-survey/`（136 份他人 mod 調查）；`workflows/plans/` 的選型類計畫；新增「想玩什麼」的規劃 |
| `agentctl` | 現 `inbox/` `tools/agent_inbox/` `scripts/` `tests/`；`workflows/` 的 agent 相關部分；`~/notes/.../skyrim/` 的 `agents/` `agent-archive-2026-08-22/` `tools/`；Nexus 下載流程的工程化 |

### `agent-bridge` 怎麼辦

`mo2ctl` 在 `projects/agent-bridge/client/`，它就是「AI 操控 Skyrim」的核心。兩種做法：

- **建議：留在 `projects/agent-bridge`**，`agentctl` 只做編排層（工作流、交接書範本、inbox、
  Nexus 下載器、runbook），README 指過去說明哪幾個 `projects/` repo 是它的插件。
  這符合根 README 已宣示的「靠協議對接、不整合」原則，churn 最小。
- 替代：`agent-bridge`／`scene-capture-bridge`／`houseCARL` 變成 `agentctl` 的巢狀 submodule。
  分類更漂亮，但巢狀 submodule 日常更新很煩。
