# 下次開玩前要做的事——D. 遊戲內要用對話／MCM 做的事（2026-09-26）

> 從 [2026-09-26-pre-play-checklist.md](../2026-09-26-pre-play-checklist.md) 拆出（2026-10-10 git-tidy，>8 KB 拆檔），內容未改。


<!-- wf-nav -->
- **D1 Katana／密格拉重招**：跟她們對話，選 **mod 自己的**跟隨選項，也就是回應是「我紧随在后。」的那條，**不要**選 NFF 的招募。兩人各做一次。報告原本寫要先用 NFF 讓她們離隊，但實機顯示她們目前不在隊上（C2 待驗），所以這一步可能可以省略。做完用 `GetGlobalValue AK69KatanaRecruited` 確認回 1。〔katana〕
- **D2 Vilja**（待驗）：可以用 MCM 關掉 `Import Enabled`，或什麼都不做、選項留著不按。C3 的矛盾釐清之前，**不要按** NFF 的 Import 或 Export 選項。〔vilja〕
- **D3 只是嫌 Active Effects 太雜**：用已經裝好的 Magic Organizer。打開魔法選單 → Active Effects → 選取效果 → 按 Hide 熱鍵。效果還在，只是看不到；要還原就開 F1 選單。〔forget〕
- **D4 金丘農園招總管**（沒裝 farm B 的情況）：帶一位語音合格的隨從，要在跟隨狀態、人在農園戶外，對話就會出現「我的農園需要一位總管。有興趣嗎？」。合格的例如 Uthgerd、Aela、Jordis、Iona、Brelyna、Marcurio、Kurone 系（Lili／Nina／Yumi／Coco）、Kiyomi、Rosalia、Charlotte、2B、Ryoko 等。完整名單在 `~/skyrim_mods/_staging-2026-09-26/farm/followers_eligibility.tsv`。〔farm〕
- **D5 Aniya 米凱爾**：C6 的 `set` 打完之後（或裝了 aniya 層之後），跟米凱爾對話，選「米凯尔，求你别再纠缠安妮亚了。」，然後選**威脅**（你 27 級，≥11 就一定成功）或**說服**（需要口才 ≥30）。**不要選打架**：上游有缺陷，打輸、對方逃跑或中途離開酒館，任務目標都不會完成。之後安妮亞會過來找你說話，任務收尾，好感 +3。〔aniya〕
- **D6 Yvanni**：救回之後跟她說「跟我来。我需要你的帮助。」，NFF 會自動接管（已實測）。確認 NFF 選單裡有她之後，存一個新檔。〔yvanni〕
