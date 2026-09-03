# investigation — 調查/解碼入口

用於研究外部專案、既有系統、bug 真因、可行性。目標是把不確定變成可行/不可行/待補缺口。

## 流程

開始前寫一句：

```text
Done when: <可行/不可行/缺口/下一步已明確，finding 已落檔>
```

```text
收集事實
  → 對照本專案現有能力
  → 分類：可直接做 / 有缺口 / 不值得做 / 需使用者驗證
  → 產出 finding
  → 缺口進 planning，踩坑進 common/gotchas
```

規則：

- 優先保留可驗證來源、命令、檔案路徑、版本。
- 不把未驗證猜測寫成結論。
- 調查結果若會導致功能開發，先進 [planning](../planning.md)／[plans](../plans/README.md)，不直接散落在聊天紀錄。

## 何時不用

- 已經知道要改哪裡且能直接實作，走 feature-dev。
- 是完整陌生 repo 初始分析，走 [analysis](../analysis.md)。

## 內容

| 路徑 | 內容 |
|------|------|
| `findings/` | 調查結果，按需建立 |
| `gotchas.md` | 調查踩坑，按需建立 |
| `session-log.md`（長出來才建）| 本工作流 open/in-flight 調查；目前一律記在根 [SESSION-LOG.md](../../../SESSION-LOG.md) |
| `archive/` | 過時調查文檔 |

### 現有 findings

<!-- wf-nav -->

- [dac0da-1.1.0b-cht-voice-matrix](findings/dac0da-1.1.0b-cht-voice-matrix.md) —— 可直接組成「繁中字幕＋英語 AI 語音」。
- [dialogue-translation-gaps-nff-gyh-ussep](findings/dialogue-translation-gaps-nff-gyh-ussep.md) —— Dev runtime acceptance 看到的英文對話不是 IFD Lydia 或 RDO Final 翻譯失敗，而是三個各自不完整的翻譯表面。
- [ifd-lydia-4.2.2-translation-audit](findings/ifd-lydia-4.2.2-translation-audit.md) —— 同版 CHS archive 可作翻譯語意種子，但不能未經驗證直接覆寫；主 ESP 與 loose PEX 都已證明為 text-only。
- [mo2ctl-static-gates-asset-scope](findings/mo2ctl-static-gates-asset-scope.md) —— `mo2ctl static-gates --asset <path>` 不是只執行 asset resolver，會固定先執行四項全局檢查。
- [mo2-moshortcut-steam-modal-2026-08-21](findings/mo2-moshortcut-steam-modal-2026-08-21.md) —— Skyrim 啟動失敗不是 DSPortP1 增加檔案使 MO2 掃描超時，實際停在 Steam 狀態檢查的 `Waiting` modal。
- [offline-correctness-batch-2026-08-12](findings/offline-correctness-batch-2026-08-12.md) —— 四項建議均已落地；保留為當時的缺口與驗收依據。
- [rdo-final-translation-audit](findings/rdo-final-translation-audit.md) —— 本機 RDO Final CHT archive 與現役官方 RDO Final 是精確結構相容的 text-only translation seed。
- [wuxin-character-overhaul-se-ae-compatibility](findings/wuxin-character-overhaul-se-ae-compatibility.md) —— 無心人物線的原始來源、SE 替代方案、1.6.1170 相容邊界、現有 load order 衝突與下一個可執行步驟都已明確；未取得合法 archive 前不安裝未知鏡像。
