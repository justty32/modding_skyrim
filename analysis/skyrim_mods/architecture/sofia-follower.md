# Sofia Follower v2.51

## 定位

完整的**語音隨從（voiced follower）mod**，作者 John Jarvis（配音 Christine Slagman）。和 JContainers 那種「純 library、零內容」相反——Sofia 是**滿載內容**的單一 ESP：1741 個 record，其中超過 1100 條對白回應、近 30 個 quest、28 個 scene、54 個 AI package。它幾乎只用**原版引擎機制**（quest / scene / dialogue / package / GlobalVariable）堆出一個有個性、會吐槽、能結婚、能喝醉的隨從，**不掛任何 SKSE 資料結構依賴**（dump 中 `jcontainer/jvalue/jformdb` 出現次數為 0；readme 也明說「Do I need SKSE? No」，SKSE 只用於選配的 MCM 選單）。

對 ModForge 而言，Sofia 是「一個成熟隨從 mod 在 record 層長什麼樣」的黃金樣本，特別適合對照 ModForge 既有的 QuestSpec / SceneSpec / NpcSpec / GlobalSpec / PACK templates。

<!-- wf-nav -->
- [檔案結構](sofia-follower/files-and-quests.md)
- [2. Scene 解剖](sofia-follower/scene-anatomy.md)
- [3. Package（54 個）—— 隨從行為骨架](sofia-follower/packages-and-state.md)
- [關鍵設計](sofia-follower/design-and-modforge.md)
