# DAc0da 1.1.0b：繁中與英語語音版本矩陣

日期：2026-08-20

## Done when

最新版主體、繁中、語音、必要依賴與安全覆寫順序已有可驗證來源；缺語音時的本地生成邊界明確。

## 結論

可直接組成「繁中字幕＋英語 AI 語音」：

1. `DAc0da`（Nexus 134405）主體 `1.1.0b`；main file `Dac0da v110b`，2026-07-23，約 1.1 GB。
2. `DAC0DA - English Translation`（Nexus 135682）`1.1.0`，2026-07-01，8.1 MB。
3. `DAc0da - ElevenLabs Voiced`（Nexus 154663）`1.1-1`，2026-01-16，66.9 MB；已知 file id
   `710215`。`710216` 是無關的 3 KB patch，不可拿來當語音檔。
4. `DAc0da - Traditional Chinese (CHT)`（Nexus 158885）`1.1.0`，2026-08-13。一般安裝選
   `DAc0da (CHT)`；`DAc0da DSD (CHT)` 只供已使用 Dynamic String Distributor 的配置。

主體 `1.1.0b` 的變更只有 scripts，作者明示 ESM 沒變，因此 `1.1.0` 英文／繁中 replacer 與
`1.1.0b` 主體是同一份記錄版本。作者同時警告 ESM 與 BSA 版本不符可能 CTD，不得使用舊的
`1.0.5` 繁中或語音檔。

## 必要依賴

- Skyrim SE/AE/GOG 與 Dawnguard、Dragonborn
- SKSE
- Fuz Ro D-oh - Silent Voice（Nexus 15109；須選符合 Skyrim runtime 的版本）
- PapyrusUtil SE（Nexus 13048）

SSE Engine Fixes 與 Better Dialogue Controls 是作者推薦，不是硬依賴。

## MO2 安裝／覆寫順序

```text
DAc0da 1.1.0b 主體
  < English Translation 1.1.0
  < ElevenLabs Voiced 1.1-1
  < Traditional Chinese (CHT) 1.1.0
```

讓繁中層最後覆寫 `DAc0da.esm`，英語語音層的 `Sound/Voice/DAc0da.esm/` 保留。若語音包的
suppression plugin 與繁中包有同名 plugin／DSD 檔，安裝後須逐檔確認 winner，不能只看左欄順序。

## 語音完整度與本輪決策

主體本身無語音。ElevenLabs 包的歷史記錄顯示 `1.0.5-1` 已「Added all missing lines」，之後又補
intro、epilogue；`1.1-1` 取代 Vanus Galerion 聲線並加入 suppression plugin。這是目前最接近完整、
且明確對應 1.1 英文翻譯的現成方案，但 Nexus 描述沒有提供可機器驗證的 100% coverage 數字。

若日後需要精確量化，可用 `DAc0da.esm` 的所有 voiced INFO response 對照
`Sound/Voice/DAc0da.esm/<VoiceType>/<FormID>_*.fuz` 做 coverage audit；只有確定缺檔才生成。
本 repo 的路徑是：ModForge 解析 INFO／speaker→VoiceType 並生成 plan，逐行呼叫
`projects/skyrim-voicegen/voicegen-f5.sh` 產 WAV，再由 ModForge 打包 XWM/LIP/FUZ。F5 需要每個
VoiceType 的合法 reference clip；沒有可授權的參考嗓音時不得臆造／抓取第三方聲音。

2026-08-20 實際部署採用現成 ElevenLabs `1.1-1`，使用者其後明確決定「沒有語音就算了，不用
生成」。因此本輪不再把 coverage audit 或本地 TTS 視為安裝完成條件；只在未來使用者重新要求補
語音時才重開此工作。

授權邊界：ElevenLabs 包允許修改及再利用，但須 credit 原作者；主體素材標為不可修改／再利用，
繁中包也要求先取得作者許可才能修改或發布改良版。因此可優先補現有語音包的真正缺行，公開發布前
仍須確認所用 voice likeness、原台詞與翻譯的授權；不要修改或重發主體／繁中 archive。

## 可選補丁

- `DAC0DA - Delayed Start`（Nexus 136031）`1.1`：避免角色 15 級一到 Solitude 就立即出現
  Numidium；屬體驗補丁，非硬依賴。
- `Custom Skills - Skyshards`：主體 1.1.0b scripts 已加入事件支援，但作者明示非必要。
- Achievement Injector、Dragonborn's Bestiary、SkyValor、Animated Armoury 等補丁只在對應框架
  已啟用時加入，且其顯示文字需另外做繁中 winner audit。

## 來源

- https://www.nexusmods.com/skyrimspecialedition/mods/134405
- https://www.nexusmods.com/skyrimspecialedition/mods/135682
- https://www.nexusmods.com/skyrimspecialedition/mods/154663
- https://www.nexusmods.com/skyrimspecialedition/mods/158885
- https://www.nexusmods.com/skyrimspecialedition/mods/136031
- `projects/skyrim-voicegen/README.md`
- `projects/skyrim-voicegen/PROTOCOL.md`
