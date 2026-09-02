# tool-survey — Skyrim 模組工具調查

← [sub_projs/README.md](../../projects/ModForge/sub_projs/README.md)

調查 Skyrim 模組製作生態中的**工具**（非 mod content，而是製作工具、SKSE plugin 框架、編輯器、patcher 等），評估其與 ModForge 的關係與潛在用途。

**性質**：agent 工作區 — 原始 findings 放 `findings/`，Gemini 原始輸出放 `../gemini-research/tool-survey/`，確認過的結論才往上搬（roadmap / WAIT_USER 等）。

Repo 本體 clone 至 `repos/`（gitignored，shallow clone）：

```
repos/
  SkyrimIngameEditor/   (Jonahex)
  TES5Edit/             (TES5Edit team)
  F4RefToBlender/       (6ooflames)
  BodySlide-and-Outfit-Studio/ (ousnius)
  OBody/                (Aietos, 舊版 Papyrus)
  OBody-NG/             (Aietos, 新版 SKSE C++)
```

---

## Findings

| 工具 | 類型 | 狀態 | 摘要 |
|------|------|------|------|
| [skyrim-ingame-editor](findings/skyrim-ingame-editor.md) | SKSE plugin + EspGenerator | ✅ 完整調查 | 遊戲內即時 Weather/Cell/ImageSpace/LGTM 編輯；EspGenerator 已支援 Reference（IPlacedGetter）匯出；**擴展路徑清楚**（見 roadmap generation.md #3） |
| [SkyPlace](findings/skyplace.md) | SKSE runtime object manipulator | ✅ 原始碼調查 | 準星 raycast + runtime reference 群組／搬動／縮放；結果綁定 save 與 `_Place.bin`，**無 ESP 匯出**；source repo 未宣告授權 |
| [Lilac](findings/lilac.md) | Papyrus in-game test framework | ✅ 原始碼調查 | `startquest` 驅動 Jasmine 風格 `describe`／`it`／`expect*`，結果進 Papyrus log；可接 AgentBridge console，但需先做 1.6.1170 重編譯 smoke 與 summary parser |
| [CKPE](findings/ckpe.md) | CK GUI stability/performance extension | ✅ 文件／設定調查 | **可直接用於穩定／加速 facegen 的 CK GUI 工作流，SSE 預設已設 1024 tint mask；但 CKPE 不提供無頭批次層，且 AE 1.6.1170 對應 CK 版本仍須驗證。** |
| [nexus-autodl](findings/nexus-autodl.md) | Python screenshot autoclicker | ✅ 原始碼調查 | 可借概念：以可調模板與隨機掃描簡化隨手慢速點擊，但缺 file_id、檔名、進度與 MD5 驗證，不能直接接 LoreRim 465 件批次隊列。 |
| TES5Edit | Delphi GUI 編輯器 | 📄 Gemini raw | xEdit：record 查看/清理/衝突解決/Pascal 腳本；`wbDefinitions.pas` 定義 record binary 佈局 |
| F4RefToBlender | Python Blender 腳本 | 📄 Gemini raw | CK reference data + PyNifly → Blender 3D 場景重建；了解 reference 資料流用 |
| BodySlide-and-Outfit-Studio | C++ wxWidgets GUI | 📄 Gemini raw | NIF 服裝/身體 mesh 編輯器；BodySlide 滑桿自訂 + Batch Build；Outfit Studio mesh 編輯 + skinning |
| OBody-NG | SKSE C++ plugin | 🔍 原始碼讀取 | JSON config 按 NPC FormID/plugin/faction/race 分配 BodySlide preset；ORefit 自動貼合服裝 |
| OBody | Papyrus + ESP | — | 舊版（Papyrus-based）；已被 OBody-NG 取代 |
| [SkyrimSE-Linux-Modding](findings/linux-modding-guide.md) | 指南 | ✅ 快照調查 | 過時的 Proton 3.16-4／SKSE／FAudio 指南；與現行 Manjaro＋MO2 的可借接點與缺口 |
| [Mundusform](findings/mundusform.md) | SKSE worldbuilding toolkit | ✅ 原始碼調查 | 可借概念，不可直接用：玩家走位粗鋪 navmesh 與 connector/bounding-box block grammar 有研究價值，但現成 DLL／export 鏈停在 1.5.97-era 且缺完整 NAVM/NAVI、跨 cell 與 1.6.1170 證據。 |
| [Mundusform 三片段借用評估](findings/mundusform-borrow-assessment.md) | 遊戲內編輯器移植評估 | ✅ 原始碼對照 | navmesh 鋪 quad＝PORT；cell 快照＝SKIP；block 生成＝CONCEPT。 |
| [wrye-bash](findings/wrye-bash.md) | Python mod manager + Bashed Patch generator | ✅ 原始碼調查 | 可借概念：LeveledListsPatcher 的 master-delta＋Delev/Relev 合併可補我方缺口，但現成 Bashed Patch 沒有無頭 CLI/API，且 GPL-3.0 不宜直接嵌入。 |

---

## 調查方法

1. git clone --depth=1 → `repos/`（直接讀原始碼，比 Gemini 準確）
2. Gemini CLI（聯網）補充 README / release 資訊
3. 重點：工具做什麼、架構怎麼運作、與 ModForge 的交集／差異
