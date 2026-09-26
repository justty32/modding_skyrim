# 調度、模型分級與交接書（1/9）

[lessons 索引](README.md)｜同主題：[dispatch-and-agents-2](dispatch-and-agents-2.md)、[dispatch-and-agents-3](dispatch-and-agents-3.md)、[dispatch-and-agents-4](dispatch-and-agents-4.md)、[dispatch-and-agents-5](dispatch-and-agents-5.md)、[dispatch-and-agents-6](dispatch-and-agents-6.md)、[dispatch-and-agents-7](dispatch-and-agents-7.md)、[dispatch-and-agents-8](dispatch-and-agents-8.md)、[dispatch-and-agents-9](dispatch-and-agents-9.md)

## im-dispatcher-codex-implements

> 我是調度者，實作交給 codex gpt-sol；不要自己把整條線的查證與改碼做完（原 type: feedback）

2026-08-21 使用者明確更正：「記住，你只是調度者，實際事情由 codex gpt sol 去做。」
當時我已經自己做完兩個上游缺陷的完整根因分析、寫 BSA reader、反編譯、改 Papyrus、
編譯、位元組碼比對、寫報告、提交 —— 全部沒有開線。

**Why:** 主 context 是稀缺資源。深潛實作會把大量工具輸出灌進主對話，
一條線就吃掉三成 context；而 codex 線是獨立 context，跑完只回報結論。
調度者的價值在拆任務、寫死驗收、判斷回報可不可信，不在親手做。

**How to apply:** 拿到「去搞定 X」這種任務時，先想「這該開幾條線」，不是「我先查一下」。
探索性的前期查證可以自己做一點，但一旦確定要動手實作就開 codex 線交出去，
把已查明的事實寫進交接書讓它不必重查。這條**覆蓋** [[delegate-simple-work-to-sonnet]]
裡「判斷與改碼自己來」那句。交接書寫法見 [[codex-tmux-operational-notes]]、
信任程度見 [[trust-gpt-sol-more]]。

**2026-08-22 補充——這條比想像中更嚴格。** 使用者第三次糾正時，我正在做的是
「刪 5 個檔＋修斷鏈＋git commit」這種看起來很瑣碎的事。**瑣碎不是自己動手的理由。**

具體觸發：只要是**改檔案、跑 git、裝 mod、驗證檔案雜湊、寫報告**，一律開 codex 線。
我自己只做：讀狀態、判斷、寫交接書、轉述使用者回報、把關誠實界線。
唯一例外是**為了寫好交接書而做的最小查證**（例如確認路徑存在、確認鎖狀態）。

**2026-08-29 再收緊——「為了寫交接書的最小查證」被我撐太大。** 使用者只說了
「beyond reach 那些，與相關的，都要下載」，我卻先自己 grep 決策文件、翻庫存、
比對版本，才寫交接書；使用者當場糾正：「**你不要自己調查，你直接委託 agent 團隊**」。

**盤點本身就是線的工作。** 交接書只要寫清楚**範圍、判準、禁區、驗收**，
事實由線用 houseCARL 自己查——它有獨立 context，查得比我全，也不佔主對話。
我先查一輪不但重複，還會把不完整的事實寫死進交接書，反而框住線。

**修正後的界線**：交接書裡我只給「使用者要什麼、什麼算範圍內、遇到分歧怎麼選」，
連「庫裡已經有哪些版本」都交給線去比。真正的最小查證只剩：鎖狀態、現役線有沒有衝突、
路徑存不存在。
