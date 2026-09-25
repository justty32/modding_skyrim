# powerofthree's Tweaks (v1.15.1)

## 定位

SKSE plugin，本質是一包**引擎層級的修補與微調集合**。它幾乎沒有 Papyrus 內容——主體是一顆 native DLL（`po3_Tweaks.dll`），直接在 runtime hook/patch 遊戲引擎，修掉一票 crash 與 bug，順帶做一些行為調整與效能優化。

對外的 Papyrus 面**極小**：整個 `po3_Tweaks.psc`（來源 `Required/source/scripts/po3_Tweaks.psc`，共 47 行）只暴露**一個**公開函式：

```papyrus
;returns whether the following tweak is enabled
bool Function IsTweakInstalled(String asTweak) global native
```
（`Required/source/scripts/po3_Tweaks.psc:46`）

也就是說：它不是給 mod 作者拿來「呼叫功能」的 library，而是一個**背景修補器**。`IsTweakInstalled()` 唯一的用途是讓別的 mod 在 runtime 詢問「某項 tweak 有沒有開」，以便決定要不要自己再補一次。所有實際邏輯都在 DLL 裡，`.psc` 開頭那段大註解（`Required/source/scripts/po3_Tweaks.psc:2`–`44`）就是這顆 DLL 完整的 tweak 清單。

Nexus #51073（`fomod/info.xml`）。它與 JContainers 那種「補資料結構給別人用」的 library 不同——JContainers 是被別人 `import` 的依賴，而 po3 Tweaks 是裝了就生效、別人通常不感知的隱形修補層。

<!-- wf-nav -->
- [檔案結構](powerofthree-tweaks/files-and-tweaks.md)
- [FOMOD 安裝流程](powerofthree-tweaks/installation-and-modforge.md)
