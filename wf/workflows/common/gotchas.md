# 共通踩坑（跨工作流）

[common/README](README.md)

不專屬任一工作流的坑記 / 查這裡；工作流專屬的坑記在該工作流自己的 `gotchas.md`（長出來後在下表加一列導流）。

**何時用**：使用者說「記個踩坑」「上次也是這樣」；或動手前要查這個現象以前撞過沒。
**何時不用**：坑專屬某個工作流、而那個工作流已有自己的 `gotchas.md` → 記在那裡；**只撞過一次**的意外 → 不記（門檻是第二次撞到）。

## Done when

- 下表對應的檔多一條坑（粗體標題＋一兩句現象與對策），或查到既有條目並照它處理。

## 哪類坑記哪裡

| 坑的性質 | 記 / 查這裡 |
|---------|------------|
| 共通坑 | **本檔** |

---

- **FormID 有兩種語境，別混用**：引擎內部二進位 `FormID` 是 32 位，前兩位是插件在 load order 的索引（`0xFF` 開頭＝runtime 動態生成物件），詳見 [`analysis/skyrim_engine/architecture/Systems_TESForm_Detailed.md`](../../../analysis/skyrim_engine/architecture/Systems_TESForm_Detailed.md)。houseCARL MCP 工具對外走的是**文字格式** `XXXXXX:Plugin.esp`（6 位十六進位＋定義該記錄的 master 檔名），兩者概念相通但序列化方式不同。
