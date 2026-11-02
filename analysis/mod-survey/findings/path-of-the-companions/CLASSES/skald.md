# Skald 新職業案例

來源行號相對 FWM `971b8b5aba0c34c649e70307cebdaa4aaa7bf4de` 與 Paths `189f24c8a8e5b61cacfbc60b2347589c9f3eff61`；固定 URL 與名詞見 [職業入口](../CLASSES.md)。

## Skald 案例

Skald 展示了「新增完整 Role」的實際範圍：enum 末尾身份 6、FWM:`include/FWM/Paths.h:430` 的完整 15 節點樹、`:464` 的名稱簡介、`src/LevelRules.cpp:68` 的專屬升級曲線，以及 Menu 的名稱／背景／圖示。可借用的是固定身份、單一樹描述、明確資格檢查與專用 runtime 模組的分工。

它也帶有大量題材專用分支：FWM:`include/FWM/Paths.h:522` 的 skaldUnlocked，`src/Paths.cpp:445` 把解鎖成本算進支出，`src/Party.cpp:467` 查解鎖與魯特琴；Paths:`src/Main.cpp:225` 用 `node == Paths::kNodes` 這個超出正常節點範圍的 sentinel 執行解鎖。FWM:`include/FWM/LoadoutPolicy.h:17` 的拳頭 mask、`src/Rules.cpp:83` 禁普通法術、`src/Loadouts.cpp:73` 不採普通戰鬥武器選擇，都是為演奏設計。

戰鬥方面還有 FWM:`src/Battle.cpp:1033` 的 SupportPosition、`:1278` 的演奏移動／恢復處理、`src/Styles.cpp:176` 的 TimidSkald，以及 `src/Skald.cpp:684,760,1075,1505` 的開演、退出職業恢復、kit 查詢與中止生命週期。這不是拿四技能填表就生成的新職業。若新職業不需要樂器、付點解鎖或表演鎖定，就不應複製這些 special-case；若未來很多職業都要資格／解鎖，再評估共通 policy，而非現在先造註冊框架。

