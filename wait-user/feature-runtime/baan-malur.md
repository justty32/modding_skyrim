# Baan Malur 渡船驗收（2026-11-07）

作者要求的 `bBorderRegionsEnabled=0` 已由頂層加入現役 `modpack-main/skyrim.ini` 的 `[General]`（profiles `6d703d0`）；原檔備份 `/home/lorkhan/skyrim_mods/skyrim.ini.bak-2026-11-07-border`。本次收尾未改 profile。

請**退出並重開遊戲，讀取搭船前的存檔**，向同一船夫選相同目的地，確認載入後抵達 Baan Malur、沒有被彈回，並記錄是否扣 30 金。若仍失敗，回報船夫／出發地、所選目的地、載入後實際落點與扣款狀況，再做單變量調查。

目前只「高度懷疑」遊戲邊界，尚未證實根因或修復成功；缺 CarriageScript 不在已核對的渡船呼叫鏈，不能據此補空腳本。調查見 [REPORT](../../agentctl/handoffs/home-2026-11-07/baan-malur/REPORT.md)。其他實機待驗不由此項結案。
