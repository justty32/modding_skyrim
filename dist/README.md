# dist —— 自製產物區

`projects/` 下各 repo 產出的**可對外使用產物**統一放這裡,等待被使用/發佈。這裡只放產物,不放原始碼(原始碼在 `projects/`)。

## 結構

```text
dist/
├── mods/      # 完整 mod 包(esp/esm/esl + 資產,可直接丟給 MO2 安裝)
├── plugins/   # SKSE plugin(DLL + 必要設定檔)
├── libs/      # 可被其他專案引用的 library 產物
└── docs/      # 對外的手冊、文檔、想法(非 repo 內部分析——那些在 analysis/)
```

## 慣例

- 每個成品一個子資料夾,名字含版本:`<名稱>-<版本>/`(例:`DaylightDungeon-0.1.0/`)。
- 子資料夾內附 `SOURCE.md`:記錄由哪個 `projects/` repo 的哪個 commit 建出、建置指令、日期。
- `docs/` 的判準:寫給**外部讀者**(發佈、分享、給其他 mod 作者看)的才放這裡;給 agent/自己用的內部分析放 `analysis/`。
- 部署到實機(MO2 instance)的狀態**不在這裡記**——歸 `~/notes/projects/modding/skyrim/` 管(職責劃分 2026-07-17);這裡只是成品倉庫。
- 舊版本要不要留由使用者決定;預設保留最近一版,更舊的問過再刪。
- **歷史自製成品在 `~/skyrim_mods/mine/`**(DSPort*/ModForge*/MF* 系列 zip;使用者決定留原地,2026-07-17)——找舊成品去那裡;新成品從進 dist/ 開始管理。
