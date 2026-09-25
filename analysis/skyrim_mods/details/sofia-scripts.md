# Sofia Follower —— Papyrus 腳本架構

## 定位

`architecture/sofia-follower.md` 已從 ESP record 層解剖了 Sofia 這個成熟語音隨從（30 quest / 28 scene / 54 package / 57 GLOB），但當時註明「2 個 BSA 無工具解包，本分析聚焦 ESP record 層」。本篇補上缺的那一層：把 `SofiaFollower.bsa` 裡的 `scripts/` 解出來，分析其 Papyrus 腳本架構，印證 record 層觀察的「純引擎機制、零 SKSE 資料結構依賴」是否在程式碼層也成立，並整理出「一個真實隨從到底需要哪些常駐邏輯 script」——這正是 ModForge 若要生成完整隨從必須補的 script 模板清單。

BSA 內 `scripts/` 共 **323 個 `.pex`（編譯後 bytecode，無 `.psc` 原始碼）**，無任何 mesh/texture/voice 被本分析抽出。還原程度與解包方法見文末「解包方法與還原程度」。

<!-- wf-nav -->
- [腳本清單（323 個，分四群）](sofia-scripts/script-inventory-and-following.md)
- [B. comment 排程器（Sofia 之所以「會吐槽」的引擎）](sofia-scripts/comments-and-relationships.md)
- [E. 系統 / 基礎建設](sofia-scripts/infrastructure-and-state.md)
- [對 ModForge 的意義](sofia-scripts/modforge-and-extraction.md)
