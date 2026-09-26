# 調度、模型分級與交接書（4/9）

[lessons 索引](README.md)｜同主題：[dispatch-and-agents](dispatch-and-agents.md)、[dispatch-and-agents-2](dispatch-and-agents-2.md)、[dispatch-and-agents-3](dispatch-and-agents-3.md)、[dispatch-and-agents-5](dispatch-and-agents-5.md)、[dispatch-and-agents-6](dispatch-and-agents-6.md)、[dispatch-and-agents-7](dispatch-and-agents-7.md)、[dispatch-and-agents-8](dispatch-and-agents-8.md)、[dispatch-and-agents-9](dispatch-and-agents-9.md)

## model-tiers-and-headcount

> 使用者定的模型分級（S/A/B/C/D、GPT 消耗下移兩級）、角色三層、選人判準；2026-09-25 起 GPT 沒退，A 級是 Opus 5.5／gpt-6-astra／gpt-6-sol（原 type: user）

2026-08-30 使用者定調「依用途分配團隊與角色」的模型，正式文件在 agentctl/docs/（team-model）。

**角色三層**：頂層 agent（接指令、開團隊、傳達、協調使用者也會用的資源——HID／螢幕／CPU／硬碟／網路；資源使用權源頭是使用者）**通常 Opus 就夠**，且**可以有自己的輔助者 agent**（例如 Sonnet 查資料／盤點／事實查證），不經團隊領導、不算團隊 headcount；團隊領導＝計畫制定者，依難度用 **Fable 或 Opus**，**不建議 gpt-sol**（另一套體系、跟頂層溝通不便）；工人依難度、內容、**使用者給的 headcount** 開，便宜 AI（gpt-sol／terra／luna）在這層大量用，但要算溝通成本（inbox 協議也有摩擦）與**領導的管理上限**（開太多管不動）。

**聰明度（總分，之後會按用途細分）**：S＝Fable；A＝Opus（軟體工程）、gpt-sol（各方面，軟體工程算 B+）；B＝Opus（軟體工程之外）；C＝gpt-terra、Sonnet；D＝gpt-luna。
**消耗速度**：Claude 系列與聰明度成正比；GPT 系列整體下移兩級——gpt-sol A 級腦、C 級消耗，「性價比之神」。

**方案時間軸**：2026-08-30 Claude、GPT 各月付 $200；**約 2026-09 第一週退 GPT**——之後 gpt-sol／terra／luna 這層消失，工人回到 Sonnet（機械）／Opus（重要）。使用者說**不用上網查方案**。

**How to apply**：派線前先看今天 GPT 還在不在；在的話工人預設 gpt-sol、重要部分 Opus；不在就 Sonnet／Opus。領導永遠是 Claude 系。headcount 是使用者給的，不要自己膨脹。相關：[[fable-top-opus-middle-management]]、[[trust-gpt-sol-more]]、[[delegate-simple-work-to-sonnet]]

**2026-08-30 晚六條裁示**（已進 agentctl/docs/team-model.md）：① 頂層**下次 compact 或新 session 起降到 Opus**，某些情況 Sonnet 也行——頂層只轉達調度，比領導笨是正常的；② 領導負擔重（計畫＋指揮＋匯報）所以 Opus 是最低標準，但若「制定計畫」分給某個成員，領導 Sonnet 也可；③ 分級以 Claude 收費為基準，往下補 E/F 很正常（terra/luna 消耗 E/F；之後 DeepSeek 更低）；④ 退 GPT 後原本給 gpt-sol 的 A 級活應會改派 Opus，到時重新規劃團隊政策；⑤ gpt-sol 開多少 terra/luna 我們管不著，只告訴它可用資源、頂多建議兩三個；⑥ 頂層輔助者數量使用者指定，沒指定默認兩個。

**context 管理（同日）**：每個 agent 管自己下級的 context，一大段任務結束就 compact；計畫制定者要在計畫裡預定大段任務間的 compact 間隙；頂層的 compact 與使用者商量；gpt-sol 的 `/compact` 從 stdin（tmux）送；Claude subagent 沒外部 compact 入口就一段一條線接力。目的是清雜訊、提升決策品質。

**信箱分層（2026-08-30 晚補）**：頂層平常不盯 inbox，但**若團隊裡有外部 agent（codex／別台機器）要直接跟頂層交流，頂層也要盯自己的信箱**——所以 inbox 要做得更好：方向是**大家都可以有自己的信箱，團隊內部信箱與 agent 個人信箱都算**。個人 `mail/<session>/` 與 `topics/` 已有；缺「團隊信箱成一級概念（開團隊配一格、成員預設訂閱）」與「頂層自己那格的位址＋醒鐘策略」。已寫進 team-model.md 第七節與 agentctl backlog，未實作。同日頂層已從 Fable 切到 Opus（`/model`）。

**執行速度與時程（2026-08-30 晚補）**：使用者有時要求「幾小時內完成」，**計畫制定者要依各模型執行速度排時程**。速度三因素：① token 產出速度——通常越聰明越慢但不一概而論、廠商也有影響；體感上分兩檔：**B 級以上比以下慢 1.5 倍**；② 聰明度——笨的要多繞幾圈，聰明的一次搞定（所以慢模型未必總時間長）；③ **模型癖好**——gpt-sol 每做一小事就驗證，硬把時間拉長 1–2 倍（交接書要寫死驗收條數壓這個）。已寫進 agentctl/docs/team-model/speed-and-driving.md（2026-08-30）。

**2026-09-08 使用者 /goal 更新（取代上面的分級表當作預設路由）：** 普通任務交 Opus，簡單任務交 Sonnet，量大且呆板的任務開 codex gpt-sol（gpt-sol 可自行呼叫更便宜的 gpt-terra／luna 處理）；對使用者說話與給他看的東西一律大白話。頂層仍只做調度、裁示轉達、artifact 發布。

**2026-09-25 使用者更新（覆蓋方案那段）**：Opus 5.5、gpt-6-astra、gpt-6-sol 都出了，三者與 Sonnet 都可用。**headcount 仍逐次由使用者給**——當天說的「隊伍無上限」只限那一輪，使用者明說不要記成規則。GPT **沒有退**：codex 模型代號 `-m gpt-6-astra`（09-20 起 config 預設）／`-m gpt-6-sol`／`-m gpt-6-luna`；astra 與 sol 的用途細分待實測，暫定 astra 給需要判斷的線、sol 給量大呆板的。Claude 端 Opus 已是 5.5。剩下的唯一上限是「領導監看得過來」。已寫進 agentctl/docs/team-model.md 第二／五節與 team-model/plans.md。

## prefer-gpt-sol-for-all-tasks

> 2026-09-11 使用者原話「可以的話，之後的任務都盡量用 codex gpt-sol」；Opus 領隊只切工、合併、覆核，實作／掃描／翻譯／腳本一律交 gpt-sol（可自開 terra/luna），領隊自己動手＝違反（原 type: feedback）

2026-09-11 22:5x 使用者：「可以的話，之後的任務都盡量用 codex gpt-sol」。

**Why：** 省 Claude token；gpt-sol 便宜且可自開 terra/luna 做呆板量大的事。

**How to apply：**
1. 交接書寫死「領隊只分派／合併／覆核，不自己跑掃描或寫產物」；量小的事也丟一條 gpt-sol（`cx-<隊>-a`）。
2. 頂層（我）也一樣：查資料／整理表／產頁腳本能交就交，不自己寫。
3. 例外：拿遊戲鎖的實機段、需要 MCP（houseCARL／qa）的步驟，gpt-sol 沒有 MCP 時由領隊代跑，但只跑那一步。
相關：[[im-dispatcher-codex-implements]]、[[trust-gpt-sol-more]]、[[model-tiers-and-headcount]]

**2026-09-12 補充（使用者原話）：**「盡量讓所有agent都指揮gpt-sol去做事。至於漢化這塊，則可以讓gpt-sol去指揮更低階更便宜的gpt-terra/luna」。→ Opus 領隊的實作工人一律 codex gpt-sol；中文層交接書明寫 gpt-sol 可自開 terra／luna 做量大翻譯搬字串，gpt-sol 只做切工與 gate。額度用盡時暫改 Sonnet，重置後換回。

**2026-09-16 再申：** 使用者原話「你盡量不要自己做事。要麼gpt-sol，要麼opus, sonnet」——當晚我親手改 profile 裝 patch、關 MO2、開遊戲之後被糾正。頂層連「一行 profile 編輯」「裝一支 esp」「開遊戲煙霧」都要派線；自己只留：寫交接書、驗收、鎖仲裁、對使用者說話。crash log 初判可以自己看，但修法要派線。
