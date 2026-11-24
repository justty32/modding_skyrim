skyrim 組織的使用者原話與定案 D25 起：2026-11-24 第二批（push 時間、刪 `wf/archive/`、skyrim-qa、座位帶 MCP、sol 與 terra）。

# 定案（續）：使用者說的與 D25 起

回 [org](README.md)。D1–D24 在 [decisions](decisions.md)（該檔已近 8 KB，從這裡續寫）。原話照抄，不改字。D 編號在其他檔照這裡引用。

## 使用者說的

2026-11-24 約 19:30，頂層問五題（1 今天能不能 push；2 `wf/archive/` 要不要 `git rm`；3 實體座位帶著 `skyrim-qa`，要不要加規矩「拿到遊戲鎖、使用者不在玩才准用；動存檔的 console 指令先問」；4 館藏與開發座位要不要也帶 MCP；5 sol 該做什麼，`aos.md`「sol 只做蒐集與量大呆板」與 `user.md` 11-03「普通工作交給 sol」不一致），使用者答：

> push就是晚上十一點統一push。可以git rm。可以加上規矩。都可以帶mcp。這兩個sol的任務分配都可以，通常是建議普通工作，至於量大呆板的，則看難易度，簡單一點的可以交給terra。

### 已定案：push 與封存（使用者 2026-11-24）

- D25 push：每天晚上 23:00 由頂層統一 push；各線、各座位只 commit 不 push。取代「每場逐次授權」的做法；D14 原文保留在 [decisions](decisions.md)，當作 11-23 那場的紀錄。寫在 [user.md](../workflows/common/user.md) 2026-11-24 段。
- D26 `wf/archive/` 刪掉：`git rm`，封存改回 wf 既有的「過時即刪」（[STRUCTURE](../STRUCTURE.md) local 段）。舊 codex 派線工作流只剩 git 歷史可查。

### 已定案：遊戲與工具（使用者 2026-11-24）

- D27 skyrim-qa：只有實體座位可以操作跑著的遊戲；要先拿到遊戲鎖、使用者不在玩才准用；會動到存檔的 console 指令要先問使用者（座位經 lead 以 `NEEDS-USER` 問）。其他座位帶著也不准用。寫在 [instance 卡](instance/README.md)、[places](places.md)「跨部門資源」與三份 `seat-*` 的 `system.txt`。
- D28 館藏、開發座位也帶 MCP：`seat-library`、`seat-dev` 的 `claude_mcp` 改成跟 stock 一樣（D24 當時「另兩份先不帶」由此取代）。

### 已定案：模型（使用者 2026-11-24）

- D29 sol 與 terra：普通工作建議交 sol；量大呆板的看難易度，簡單一點的交 terra。兩處舊說法（`aos.md` 第 4 節的「sol 只做蒐集與量大呆板」、`user.md` 11-03 段）留作歷史；現行說法在 `user.md` 2026-11-24 段，`aos.md` 第 4 節與 fsm gpt 操作單的選型表照它寫。
