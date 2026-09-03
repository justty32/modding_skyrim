# agent-dispatch — 指揮 codex 或其他 coding agent

把整條工作線外包給同機的其他 CLI agent（`codex`／`pi`），自己當調度者。

```text
Done when: <該線發了終局狀態、逐條對過驗收、工作樹／commit 已核（push 需使用者確認，不代按）、鎖已釋放、交接書移到 done/>
```

**完整流程在 [`agentctl/docs/driving-codex.md`](../../../agentctl/docs/driving-codex.md)。**
本檔只做路由與六條最容易錯的。

| 要什麼 | 去哪 |
|---|---|
| 三層角色、模型分級與選人判準 | [`agentctl/docs/team-model.md`](../../../agentctl/docs/team-model.md) |
| 派線完整流程（交接書、tmux、送兩次 Enter、`/bin/ls`、監看與收線） | [`agentctl/docs/driving-codex.md`](../../../agentctl/docs/driving-codex.md) |
| 現役成員、身份聲明格式、各自領地與能答什麼 | [`agentctl/inbox/ROSTER.md`](../../../agentctl/inbox/ROSTER.md) |
| 資源鎖與限流 | [`agentctl/docs/resource-locks.md`](../../../agentctl/docs/resource-locks.md) |
| 通訊契約：五通道、teams、自動上游路由與醒鐘策略 | [`agentctl/tools/agent_inbox/PROTOCOL.md`](../../../agentctl/tools/agent_inbox/PROTOCOL.md) |
| 交接書範本與已完成的範例 | [`agentctl/handoffs/`](../../../agentctl/handoffs/) |

## 三層派線結構

現行的「頂層 agent → 團隊領導 → 工人」角色、模型與資源權責只以
[`agentctl/docs/team-model.md`](../../../agentctl/docs/team-model.md) 為準。

## 六條最容易錯的

1. **我是調度者，不是實作者。** 自己深潛實作會吃掉主 context，後面就沒有餘裕做判斷。
   這條優先於「改碼自己來」。
2. **按獨立 repo 切線，不按功能切。** 兩條線碰同一個 repo 會互相覆寫 commit，git 不會擋。
   碰 profiles repo 的線同一時間只能有一條。
3. **驗收條數寫死。** 寫「以及其他你認為必要的驗證」＝ gpt-sol 會為了保險亂跑，
   燒光 token 還交不出東西。寫「回報只要這 5 條」。
4. **禁區要明寫，沒寫就等於允許。** 至少決定：能不能開遊戲／MO2 GUI／瀏覽器、
   能不能拿遊戲鎖、能不能改 `modlist.txt`／load order、能不能下載、能不能碰別的 repo。
   **使用者在電腦前不是禁區**（2026-08-30 裁示）：線仍可取鎖、開 MO2／Skyrim，不必先問。
   要禁的是**搶他的輸入**（送按鍵、注入他正在用的視窗、搶回焦點）；硬禁區只有
   「他正在玩不能暫停的遊戲」（見 [`agentctl/docs/resource-locks.md`](../../../agentctl/docs/resource-locks.md)）。
5. **Nexus 查證要指定走 houseCARL MCP，不能讓線自己 curl。** 純 HTTP 打 Nexus 回 403
   （2026-08-26 實測）；codex 端已在 `~/.codex/config.toml` 的 `[mcp_servers.housecarl]`
   掛上 houseCARL MCP，`housecarl_nexus_*` 查得到。2026-08-29 的 `cx-lands`／`cx-quest`／
   `cx-font` 三線已自行查完逐件 fileId、bytes 與翻譯層 requirements。
   （本條曾寫成「不能派給 codex 線」，2026-08-29 更正：403 是 curl 的限制，不是 codex 的限制。）
   交接書要明寫「Nexus 事實一律走 `housecarl_nexus_*`，不 curl 網頁」。下載是另一回事：
   調度者先用 houseCARL 把 id／fileId／版本／bytes 寫死，線只做離線收斂；下載由調度者跑 Claude in Chrome，
   或指定**唯一一條**瀏覽器線走 CDP，見 [nexus-intake 第 3 段](../nexus-intake/README.md#3-下載)。
6. **範圍詞會被線遞移展開。** 「相關的」若只寫包含條件，線會沿依賴圖忠實展開成遞移閉包，
   每多一跳都可能讓件數升一個數量級。交接書要用排除法界定邊界，並把容量 gate 與件數 gate 並列；
   任一觸發就停下來問。可直接抄用的三條排除規則與雙 gate 格式見
   [nexus-intake 的範圍樣板](../nexus-intake/README.md#派下載線前範圍樣板與雙-gate)。

## 通訊：五通道與輪詢義務

`new`／`mail`／`teams`／`orders`／`topics` 的選擇、自動上游路由與各層醒鐘只以
[`agentctl/tools/agent_inbox/PROTOCOL.md`](../../../agentctl/tools/agent_inbox/PROTOCOL.md) 為準。

## 多信任它

給整條線的大任務，不要重算它的 hash、不要幫它決定每一步。
**微管理會燒光 token**，而且它的自查通常比逐步驗收更有效。

**「讓它自己 push」已作廢：未經使用者確認不 push**（見母 repo
[`AGENTS.md`](../../../AGENTS.md)「Always-on 鐵律」）；commit 可由執行線或調度者完成。細節見
[`agentctl/docs/driving-codex.md`](../../../agentctl/docs/driving-codex.md)「多信任 gpt-sol」。

## 但收線時要對證據

**「跑完了」不等於「通過了」：曾有回報全 PASS，但 log 只有 2 個 commit、需要 ≥13 個，
三條驗收項的關鍵字出現 0 次。逐條對證據，不要對自我宣告。**

## 何時不用

- 一兩個檔案的小改 → 自己做，開線的交接成本大過收益。
- 需要跟使用者來回確認方向的 → 自己做，agent 線不適合承載未定的需求。
- 會刪檔的工作 → 可以派，但**要先確認目標目錄已 commit 且已 push**，或另架看門狗。
