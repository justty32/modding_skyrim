# 10-10 檢查清單：野外與地點——野外活動：露營、狩獵、灌木叢

[回野外入口](../2026-10-10-play-checklist-wild.md)｜[回總頁](../2026-10-10-play-checklist.md)｜〔〕是 `agentctl/handoffs/done/2026-10/home-2026-10-10/` 下的報告目錄。崩潰的處理方式一律照總頁 1e。

## 露營：Dovah 馬車與營地

- [ ] **第一次上車、啟用馬車前先存檔**。上游有一則 2.1.5 啟用馬車時 `XAudio2_7.dll` 崩潰的回報，Proton 下會不會發生不確定。崩了照總頁 1e 處理。〔camp-hunt-install〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕
- [ ] **MCM**：`Dovah Rider` 頁有出現；自動拾取、自動採集預設是關的，確認一下就好。紮營時跳「也要清理树木吗？」選**否**。〔camp-hunt-install〕
  - **agent 10-10 實機**：agent 驗不了，留給你（要開 MCM）。〔ingame-test〕
- [ ] **中文**：馬車、營地、料理、手冊是簡中；待售告示名、車廂內部地名和多數通知列提示是英文（已知、翻不到）。〔camp-hunt-install〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕

## 露營：吃東西與烤火（生存模式開著時）

- [ ] **Dovah 料理會回飽食**：有點餓時吃一份烤肉（大份）或一杯茶（極小份），飢餓值要回升；同一份食物只回一次，不會回兩次。戴著娜米拉戒指時一般食物不回飽（Taste of Death 的設計）。〔smi〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕
- [ ] **營火取暖**：在雪地紮 Dovah 營地、生火，站在火旁約 8 公尺內，寒冷值要回升。〔smi〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕
- [ ] **快速旅行**：生存模式開著時，從地圖快速旅行仍然可用。〔smi〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕

## 狩獵：SHO 與 DAK

- [ ] **剝皮**：殺一隻鹿或狼，一般「搜刮」就能剝皮並推進時間（提示「…过去了…」）；`Shift＋E` 可以扛屍體；把獵物賣給商人要有對白。〔camp-hunt-install〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕
- [ ] **Deepborn 的 Shift 互動照常**（DAK 換成 DLL 版的連帶影響）。〔camp-hunt-install〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕

## 灌木叢（Hide in Bushes）

- [ ] **站進大片灌木叢**（例如河木一帶的松灌木），主動效果欄出現「藏身灌木叢」／「強化潛行」，蹲下時眼睛指示要比在空地上更晚張開；走出去 1～2 秒內效果消失。〔hide-in-bushes、artisans-guard〕
  - **agent 10-10 實機**：agent 驗不了，留給你（log 正常：OIF 規則 7 條、FLM 讀了 HideInBushes_FLM.ini）。〔ingame-test〕
- [ ] **蹲著貼矮灌木**（雪莓、薰衣草、薊）會有效果，站起來就消失；貼著松樹幹或樹樁也有小幅效果。完全沒反應的話，看 SKSE 目錄下的 `ObjectImpactFramework.log` 與 `FormListManipulator.log`。〔hide-in-bushes〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕
