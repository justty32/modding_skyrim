# Dynamic Animation Casting（DAC / DAC NG Plus）

← [action-system 中樞](../README.md)

> **Layer：動畫驅動施法框架**。loki（loki_DynamicAnimationCasting.dll）的 SKSE plugin，靠**一張純文字 config 表**把「播到某 animation event → 在該 actor 身上釋放某些 spell」綁起來。對 ModForge 角度與 [BDI](behavior-data-injector.md)/[PIE](payload-interpreter.md) 同類：**DLL 不可生成，但它讀的 config 完全可生成**，且格式比 BDI/PIE 更貼近 ModForge 已有的 magic/perk record 與 OAR 的 `Plugin.esp|0xFormID` 字串。
>
> ⚠️ **命名陷阱**：本批次下載有三個都叫「DAC / DAc0da」的 mod，只有一個是這套框架。見最後「版本與同名混淆」。

<!-- wf-nav -->
- [DAC 功能、設定格式與執行依賴](dynamic-animation-casting/config-and-runtime.md)
- [DAC 版本辨識與 ModForge 生成規劃](dynamic-animation-casting/versions-and-generator.md)
