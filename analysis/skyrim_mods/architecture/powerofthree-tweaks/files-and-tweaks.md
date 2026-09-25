# powerofthree's Tweaks (v1.15.1) — files-and-tweaks

[返回入口](../powerofthree-tweaks.md)

## 檔案結構

來源：`~/skyrim_mods/powerofthree's Tweaks FOMOD Installer/`

這是 **FOMOD installer 格式**，不是攤平好可直接拖進 `Data/` 的目錄樹：

```
powerofthree's Tweaks FOMOD Installer/
├── fomod/
│   ├── info.xml              ← Name / Author / Version=1.15.1 / Nexus #51073
│   └── ModuleConfig.xml      ← 安裝腳本（決定哪些檔案最終落到哪）
├── Required/                 ← 不論 SE/AE 都會裝（共用 Papyrus）
│   ├── scripts/po3_Tweaks.pex
│   └── source/scripts/po3_Tweaks.psc
├── SE/SKSE/Plugins/          ← 二選一：Special Edition v1.5.97 用
│   ├── po3_Tweaks.dll        (約 1.03 MB)
│   └── po3_Tweaks.pdb        (約 23.8 MB 除錯符號)
└── AE/SKSE/Plugins/          ← 二選一：Anniversary Edition v1.6.629+ 用
    ├── po3_Tweaks.dll        (約 1.04 MB)
    └── po3_Tweaks.pdb        (約 23.9 MB 除錯符號)
```

關鍵點：`SE/` 與 `AE/` 各有一份**不同的 DLL**，因為 SE（1.5.97）與 AE（1.6.x）兩條引擎分支的記憶體位址/結構佈局不同，native plugin 必須各自編譯。FOMOD 的存在就是為了根據玩家的遊戲版本，自動只裝對的那一顆。`.pdb` 是除錯符號檔（讓 crash log 能解析成函式名），體積遠大於 DLL 本身；裝不裝不影響功能，只影響崩潰時的可讀性。

## 內容：tweak 清單（共 45 項）

以下完整逐項列出 `Required/source/scripts/po3_Tweaks.psc:2`–`44` 註解中的每一個 tweak，並分為四類。註：原始註解未分類，分類為本文歸納；少數項目跨類（如「Cast Added Spells on Load」既修 bug 也改行為），歸入主要性質。

### 一、穩定性 / Crash 修正

| Tweak | 說明（推斷） |
|---|---|
| Distant Ref Load Crash | 遠距 reference 載入導致的崩潰 |
| Light Attach Crash | 光源附掛到物件時的崩潰 |
| Skinned Decal Delete | 帶蒙皮 decal 刪除時的崩潰/錯誤 |

### 二、引擎 bug 修正

| Tweak | 說明（推斷） |
|---|---|
| Map Marker Placement Fix | 地圖標記放置錯誤 |
| Restore 'Can't Be Taken Book' Flag | 還原「不可拿取書籍」旗標被引擎吞掉的行為 |
| Projectile Range Fix | 投射物射程計算錯誤 |
| CombatToNormal Dialogue Fix | 由戰鬥轉回平常時的對話狀態錯誤 |
| Cast Added Spells on Load | 載入存檔後重新施放被加上的常駐法術（修「buff 掉了」） |
| Cast No-Death-Dispel Spells on Load | 載入後重放「死亡不解除」類法術 |
| IsFurnitureAnimType Fix | 家具動畫類型判定錯誤 |
| No Conjuration Spell Absorb | 召喚系法術不該被法術吸收（修錯誤吸收） |
| EffectShader Z-Buffer Fix | 特效 shader 的深度緩衝錯誤 |
| ToggleCollision Fix | `tcl` 主控台指令行為修正 |
| Jumping Bonus Fix | 跳躍加成計算錯誤 |
| Toggle Global AI Fix | `tai`（全域 AI 開關）行為修正 |
| VR CrosshairRefEvent Fix (VR only) | VR 準星 ref 事件修正（僅 VR 版） |

### 三、Gameplay 行為微調

多數是**選擇性**改變既有行為，偏好向工具/QoL，而非平衡性改動。

本表彙整「tweak-catalog」的原始記錄。已抽到 [files-and-tweaks-tweak-catalog.json](files-and-tweaks-tweak-catalog.json)（19 列）。

Tweak：原表「Tweak」欄值。

說明（推斷）：原表「說明（推斷）」欄值。

統計：19 列，2 欄。

### 四、效能優化

| Tweak | 說明（推斷） |
|---|---|
| Fast RandomInt() | 加速 `Utility.RandomInt()` 原生實作 |
| Fast RandomFloat() | 加速 `Utility.RandomFloat()` 原生實作 |
| Clean Orphaned ActiveEffects | 清理孤立的 ActiveEffect（減少存檔膨脹/卡頓） |
| Update GameHour Timers | 修正/優化 GameHour 計時器更新 |
| Stack Dump Timeout Modifier | 調整 Papyrus stack dump 的逾時門檻（緩解腳本壓力日誌） |

合計：穩定性 3 + 引擎 bug 16 + gameplay 21 + 效能 5 = **45 項**。

