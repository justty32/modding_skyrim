# 職業政策與固定接點

來源行號相對 FWM `971b8b5aba0c34c649e70307cebdaa4aaa7bf4de` 與 Paths `189f24c8a8e5b61cacfbc60b2347589c9f3eff61`；固定 URL 與名詞見 [職業入口](../CLASSES.md)。

## 必須審查的接點

身份與固定版型：FWM:`include/FWM/Orders.h:18` 宣告 Role `uint8_t`，現值 Fighter=0、Tank=1、Healer=2、Bruiser=3、Archer=4、Mage=5、Skald=6；`roles` 顯示資訊與預設 focus/position 在同檔 `:162`。`include/FWM/Paths.h:277` 固定每角色 15 節點（四主動技能各帶兩分支，另三 traits），`:321` 開始的 `paths` 陣列、`:451` 的 PathInfo 及 `:520` 的 ranks/slots/bonus 維度均依角色。不是 JSON/INI 的職業註冊機制。

UI：FWM:`src/Menu.cpp:2046` 的 `kRoleRow` 雖以 Role::kCount 作長度，初始化仍逐一列出七個角色；只增 enum 而不補初始化可能留下預設 Fighter 值。`:4247` glyphs 固定七個，`:4419` 背景圖 class 名單固定七個，`:4424`、`:4425` 的快取固定 21=三主題乘七角色。新角色需要補選單順序、標籤、圖示與背景資源／fallback；樹節點幾何和翻譯詳見技能/UI 線，不能只更新一張職業名稱表。

裝備 mask：這裡的 mask 是「某 Role 允許哪些武器種類」的 `uint32_t` 位元集合，不是七個角色的 bitset。FWM:`include/FWM/LoadoutPolicy.h:14` 的 RoleWeapons 用 one-handed、two-handed、bow、staff、shield bits；Skald 刻意回傳 0 表示只能拳頭，default 也回傳 0。`src/AbilityLink.cpp:78` 的 optional loadout mask 和 `src/Loadouts.cpp:25` 會區分「沒有 mask」與「有 mask 值為 0」；新 role 漏填不能理解成 unrestricted。跨 DLL export 在 FWM:`include/FightWithMePathsAPI.h:152` 與 Paths:`src/Main.cpp:611`。

普通法術與資源：FWM:`include/FWM/Orders.h:77` 的 ChoosesSpells 只認 Mage/Healer；`src/Rules.cpp:81` 的 SpellAllowed 只替這兩者允許不同類型法術，其他角色預設拒絕。`src/Abilities.cpp:113` 至 `:139` 又依 ChoosesSpells 選 Magicka 或 Stamina 支付技能成本。因此新增混合職業必須明確決定普通法術挑選與能力資源，單加技能樹不會自動獲得「戰法兼修」。

裝備自動識別與角色資格：FWM:`src/Party.cpp:88` 從 NFF rank、盾／雙手／弓／杖／法術推斷既有角色，`:116` 交給 Playable；`include/FWM/Orders.h:324` 的 LackFor 與 `:365` 的 Playable 決定裝備不足時的替代角色。`src/Party.cpp:151` Enforce 會因裝備不再適用而實際重設角色；`:362` 建立初始 orders，`:465` 處理 Skald/Bruiser 特殊資格。新角色要決定能否自動猜中、裝備不足是否允許留任、以及使用者指定是否優先，否則可能被自動改回既有角色。

戰鬥中換裝推斷也需審查，但有條件限制：FWM:`include/FWM/LoadoutPolicy.h:27` 的 BattleRole 只回傳既有近戰／弓／施法角色；`src/Loadouts.cpp:64` 在有 POTC loadout mask 時保留原 role，沒有 mask 才採用戰鬥選到的角色。不能把 BattleRole 說成所有 POTC 情況都會覆蓋職業。`:41` Effective 會依 role 枚舉可用法術／裝備池，`:95` 將 mask 是否存在傳給 keepRole。

成長與加成：FWM:`src/LevelRules.cpp:62` 為每個既有 role 指定每級 H/M/S 與技能成長；漏填的新角色落到 Fighter 的 default。`src/Rules.cpp:323`、`:343` 決定 path bonus 類型和上限，default bonus 為 0；`src/PathBonus.cpp:240` 取目前角色 kit，`:256` 與 `:285` 按角色實際施加被動加成。`src/Styles.cpp:169`、`src/StyleLayer.cpp:24` 負責角色戰鬥偏好，`include/FWM/Rules.h:239` 的 IsRanged 只認既有四種遠程／支援角色。這些都要有明確處理。


另見 [ABI／存檔](abi-save.md)與 [Skald 案例](skald.md)。
