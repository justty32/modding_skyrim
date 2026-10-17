# analysis — Skyrim 研究與分析

這裡放引擎、SKSE、mod、素材來源與工具的研究筆記。要找開發中的原始碼，請看 [`../projects/`](../projects/README.md)；要看部署或現役整合包狀態，請從[根目錄](../README.md)進對應工作線。

| 資料夾 | 內容 |
|---|---|
| [`skyrim_engine/`](skyrim_engine/) | CommonLibSSE-NG 引擎手冊與 Skyrim 引擎研究 |
| [`skyrim_mods/`](skyrim_mods/) | 七個參考 mod 的拆解 |
| [`houseCARL/`](houseCARL/) | houseCARL 的 Linux 適配 runbook 與相關結論 |
| [`mod-survey/`](mod-survey/) | 他人 mod 的結構化調查 |
| [`tool-survey/`](tool-survey/) | Skyrim 製作工具調查 |
| [`followers-patch/`](followers-patch/) | 八份隨從人設 brief |
| [`port-source-survey/`](port-source-survey/) | 移植素材來源候選調查 |

外部 mod、框架與參考素材的實體放在 `~/skyrim_mods/`，目前約 125 GB；外部框架原始碼放在 [`../external/`](../external/README.md)。

`mod-survey/` 底下有幾條 symlink，連結檢查不會驗它們，`grep -R`／`du -L` 也會沿著走進去（待頂層裁示改成指標檔）。實際位置如下，用文字寫出：

- `mod-survey/esm-formid-access.md` → `projects/ModForge/workflows/investigation/esm-formid-access.md`
- `mod-survey/mod-survey-guide.md` → `projects/ModForge/workflows/investigation/mod-survey-guide.md`
- `mod-survey/game-data` → `projects/game-data/`
- `mod-survey/skyrim_mods`（本機未追蹤）→ `/home/lorkhan/skyrim_mods/`（約 125 GB，掃描時要排除）
