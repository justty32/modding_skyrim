# 動作 / 動畫系統框架（2026 完整堆疊）

← [mod-survey](README.md)｜[survey index](index.md)

中樞 [action-system/README.md](action-system/README.md) 有**五層堆疊地圖**（骨架→行為引擎→行為資料注入→動畫選擇→招式框架）+ 跨層「動畫驅動狀態」鐵三角 + ModForge 生成機會。原始 mod 頁文字存 `action-system/raws/`。

<!-- wf-nav -->

| 層 | 框架 | 文件 | ModForge 可生成性 |
| --- | --- | --- | --- |
| 0 骨架 | XPMSSE | [findings/xpmsse.md](action-system/findings/xpmsse.md) | 純前置 |
| 1 引擎 | Pandora | [action-system/pandora.md](action-system/pandora.md) | shell-out |
| 1 引擎 | Universal Behavior Runtime（A-Pose Fix + Auto Skeleton） | [findings/universal-behavior-runtime.md](action-system/findings/universal-behavior-runtime.md) | 前置（runtime 容錯/LE→SE 轉換） |
| 2 注入 | Behavior Data Injector（+Universal Support） | [findings/behavior-data-injector.md](action-system/findings/behavior-data-injector.md) | **config 可生成（roadmap）** |
| 2 注入 | Payload Interpreter | [findings/payload-interpreter.md](action-system/findings/payload-interpreter.md) | annotation 屬動畫管線 |
| 2 注入 | Animation Motion Revolution | [findings/animation-motion-revolution.md](action-system/findings/animation-motion-revolution.md) | annotation 屬動畫管線 |
| 3 選擇 | Open Animation Replacer | [action-system/oar-replacer-guide.md](action-system/oar-replacer-guide.md) | **結構可生成（roadmap，最高槓桿）** |
| 3 選擇 | Directional Movement Keys | [findings/directional-movement-keys.md](action-system/findings/directional-movement-keys.md) | 前置；其 graph var 供 OAR 條件 |
| 4 招式 | BFCO（攻擊框架，+Universal Support） | [findings/bfco.md](action-system/findings/bfco.md) | OAR 變體 config 可生成 |
| 4 招式 | SCAR（NPC 連段 AI） | [findings/scar.md](action-system/findings/scar.md) | AI 不可生成 |
| 4 招式 | moveset 實例庫（DAR/OAR/SCAR 真實檔案結構） | [findings/movesets-examples.md](action-system/findings/movesets-examples.md) | **OAR 生成器的輸出規格（已驗證）** |
