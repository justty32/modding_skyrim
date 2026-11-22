# Baan Malur 渡船驗收（2026-11-07）

作者要求的 `bBorderRegionsEnabled=0` 已由頂層加入現役 `modpack-main/skyrim.ini` 的 `[General]`（profiles `6d703d0`）；原檔備份 `/home/lorkhan/skyrim_mods/skyrim.ini.bak-2026-11-07-border`。本次收尾未改 profile。

請**退出並重開遊戲，讀取搭船前的存檔**，向同一船夫選相同目的地，確認載入後抵達 Baan Malur、沒有被彈回，並記錄是否扣 30 金。若仍失敗，回報船夫／出發地、所選目的地、載入後實際落點與扣款狀況，再做單變量調查。

目前只「高度懷疑」遊戲邊界，尚未證實根因或修復成功；缺 CarriageScript 不在已核對的渡船呼叫鏈，不能據此補空腳本。調查見 [REPORT](../../agentctl/handoffs/home-2026-11-07/baan-malur/REPORT.md)。其他實機待驗不由此項結案。

agent 2026-11-22 下午（runtime-3）代驗：Save342 → 傳送到鴉石鎮碼頭船夫雷米里斯隊長 → 真按鍵選「我想雇用你的船」→「班馬魯（30 金幣）」→ 落在 `BaanMalur15`（目的地座標），金幣 20256→20226（扣 30），沒被彈回。**但抵達約 1.5 分鐘後遊戲崩潰**（`EngineFixes.dll` 的 tbbmalloc 大物件快取存取違規，log 存在 `agentctl/handoffs/home-2026-11-22/runtime-3/B3/`），所以本項先不結案：請你自己搭一次，看抵達後待幾分鐘會不會崩。沒存檔，你的存檔沒變。

2026-11-22 crash-ferry 唯讀分析結果：渡船抵達後那次崩潰，不是記憶體不夠，也不是 EngineFixes 的錯。原因是某段程式在主執行緒用「沒對齊的堆疊」呼叫記憶體配置，EngineFixes 剛好第一個踩到；log 只寫了 1 KB 就卡死，所以查不出是哪段程式。它跟今天上的身體 morph 層不能排除關係（那些層讓這類配置變多），跟 11-14～11-19 的舊崩潰不是同一種。你自己搭船時，如果抵達後遊戲卡住，請先按 `Ctrl+Shift+F12` 再關遊戲。詳見 `agentctl/handoffs/home-2026-11-22/crash-ferry/REPORT.md`。

agent 2026-11-22 傍晚（ferry-repro）重走 3 次：同存檔 Save342、同船夫、同樣用 AgentBridge 截圖，抵達後各停 5.6～7.5 分鐘（B3 是 1.5 分鐘就崩），**3 次都沒崩**，抵達、扣 30 金都正常。所以目前是「今天部署後 18 場只崩 1 次、重走 3 次未重現」，算偶發。對照實驗（不截圖、不搭船直接傳送）因為沒重現所以沒做；男女身體滑桿實測因為你回來、鍵鼠交還，沒做，要再跑需要你同意讓 agent 用遊戲。你自己玩時若在渡船或任何地方卡死：先按 `Ctrl+Shift+F12`（CrashLogger 的執行緒堆疊熱鍵），等 30 秒再關遊戲，然後告訴 agent。你的存檔沒變。詳見 `agentctl/handoffs/home-2026-11-22/ferry-repro/REPORT.md`。
