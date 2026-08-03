# external —— 他人的 mod、框架、參考素材

第三方 Skyrim mod、框架、library 的存放區,供 `projects/` 下各專案(ModForge、houseCARL、my_skyrim_plugin_1,以後可能更多)與 `analysis/` 的分析文件統一引用。

## 結構

```text
external/
├── mods/         # 他人的 mod(已解壓;參考/拆解用,如 Sofia、RDO、SkyUI…)
└── frameworks/   # 框架與 library(如 CommonLibSSE-NG、Address Library、PapyrusUtil…)
```

## 慣例

- 每個項目一個子資料夾,盡量保留原始壓縮檔名資訊(Nexus mod id / 版本)在資料夾名或內附 `ORIGIN.md`。
- 這裡是**唯讀參考素材**:不修改內容;要改就複製進 `projects/` 相關 repo 再動。
- 對應的拆解分析寫在 `analysis/`(如 `analysis/skyrim_mods/` 分析的七個 mod)。

## 現況(2026-07-17)

既有素材**全部留在 `~/skyrim_mods/`,不遷入**(使用者決定):97G 下載庫——壓縮檔在根目錄、`hdd/`(83G)、`aa/`;已解壓素材在 `unzip/`(含分析用的七個參考 mod);`mine/` 是使用者**自製成品**(屬 dist 性質,同樣留原地);`.mo2-profile-backup-*` 是部署側備份,別動。`analysis/skyrim_mods/` 的文件以 `~/skyrim_mods/` 路徑為準。本目錄(`external/`)是**未來新進素材**的落點。
