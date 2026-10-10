# 下次開玩前要做的事——E. 未解／下次派線（2026-09-26）

> 從 [2026-09-26-pre-play-checklist.md](../2026-09-26-pre-play-checklist.md) 拆出（2026-10-10 git-tidy，>8 KB 拆檔），內容未改。


<!-- wf-nav -->
- **profile 三檔漂移**：MO2 開遊戲後，modlist 自動多了一行 `-AssetTest-LightShaft-Dev-2026-09-25`，plugins／loadorder 也被重排了 5 行。dispatcher 已經派 mo2close 線去還原。開 MO2 前請先確認那條線已經收線。〔yvanni §5〕
- **vilja 需要重派**：實機顯示她已經在 nwsFF_ImportFac 裡，和報告「未匯入」的前提相反。要確認你看到的是哪一條選項（Import 還是 Export、在哪一層子選單），再決定要不要 Export。同時也影響 A 的 NFF 順序那項。
- **katana 待驗**：實機顯示兩人目前都不在隊上，報告推斷的「被 NFF 招募」這個前提沒有被坐實。也沒有查她們在不在 DismissedFollowerFaction，而 mod 自己的跟隨選項要求她們在這個 faction 裡。
- aniya：forcegreet 當初為什麼沒觸發，還沒查明。RT 第 8 步沒跑（要看米凱爾是不是被別的 mod 的場景佔住）。另外，上游「打架輸了任務目標不會完成」的缺陷沒修，要改 script 才能修。
- yvanni：她怎麼死的、怎麼跑到鬼海去的，都沒有定論。
- forget：種族被動用 `removespell` 移不掉的話，要派線做 SkyPatcher `spellsToRemove` 規則層（範本是 Nexus 159131）。
- farm：兩個 staging 層都還沒實機測過。
- RT 的限制：qa bridge 只抓得到 console 輸出的最後一行，所以 `sqv` 和 `help` 這類多行輸出都沒有拿到。各題 alias 有沒有填上，目前都還沒查到。
