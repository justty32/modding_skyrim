# agent-dispatch — 指揮 codex 或其他 coding agent

把整條工作線外包給同機的其他 CLI agent（`codex`／`pi`），自己當調度者。

```text
Done when: <該線發了終局狀態、逐條對過驗收、commit 已推、鎖已釋放、交接書移到 done/>
```

**完整流程在 [`agentctl/docs/driving-codex.md`](../../../agentctl/docs/driving-codex.md)。**
本檔只做路由與四條最容易錯的。

| 要什麼 | 去哪 |
|---|---|
| 派線的完整流程（切線、交接書契約、tmux、監看、收線七步） | [`agentctl/docs/driving-codex.md`](../../../agentctl/docs/driving-codex.md) |
| 資源鎖與限流 | [`agentctl/docs/resource-locks.md`](../../../agentctl/docs/resource-locks.md) |
| 通訊契約與五種 STATUS 語意 | [`agentctl/tools/agent_inbox/PROTOCOL.md`](../../../agentctl/tools/agent_inbox/PROTOCOL.md) |
| 交接書範本與已完成的範例 | [`agentctl/handoffs/`](../../../agentctl/handoffs/) |

## 四條最容易錯的

1. **我是調度者，不是實作者。** 自己深潛實作會吃掉主 context，後面就沒有餘裕做判斷。
   這條優先於「改碼自己來」。
2. **按獨立 repo 切線，不按功能切。** 兩條線碰同一個 repo 會互相覆寫 commit，git 不會擋。
   碰 profiles repo 的線同一時間只能有一條。
3. **驗收條數寫死。** 寫「以及其他你認為必要的驗證」＝ gpt-sol 會為了保險亂跑，
   燒光 token 還交不出東西。寫「回報只要這 5 條」。
4. **禁區要明寫，沒寫就等於允許。** 至少決定：能不能開遊戲／MO2 GUI／瀏覽器、
   能不能拿遊戲鎖、能不能改 `modlist.txt`／load order、能不能下載、能不能碰別的 repo。
   **使用者在電腦前時，一律禁止搶焦點、送按鍵、截圖。**

## 多信任它

給整條線的大任務，不要重算它的 hash、不要幫它決定每一步、讓它自己 push。
**微管理會燒光 token**，而且它的自查通常比逐步驗收更有效。

## 但收線時要對證據

**「跑完了」不等於「通過了」。** 一次實例：回報全 PASS，實際 log 只有 2 個 commit、
需要 ≥13 個，三條驗收項的關鍵字出現 0 次。**逐條對證據，不要對自我宣告。**

## 何時不用

- 一兩個檔案的小改 → 自己做，開線的交接成本大過收益。
- 需要跟使用者來回確認方向的 → 自己做，agent 線不適合承載未定的需求。
- 會刪檔的工作 → 可以派，但**要先確認目標目錄已 commit 且已 push**，或另架看門狗。
