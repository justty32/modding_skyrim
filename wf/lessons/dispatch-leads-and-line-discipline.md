# 調度：領隊與線的運作紀律

[lessons 索引](README.md)

## rush-mode-parallel-opus-agent-lines

> 急件模式：一份 COMMON.md 交接＋Agent 工具一次開多條 Opus 平行線；只有一條線持遊戲鎖代跑 RT-QUEUE；最後整理線出清單

2026-09-26 使用者有硬時限，說「想開多少線都可以、儘快」，也明說「用啥模型都行」；8 條線 15 分鐘收完八題存檔調查。

**Why:** Agent 工具的線起線零成本、完成有通知、可多條平行，急件時最快。

**How to apply:** 使用者有硬時限或說「儘快」時：先寫 `handoffs/home-<日期>/COMMON.md`（硬停時刻、報告格式、路徑、鎖規則）→ 一次開多條 Opus 調查線（每線一個交接段）→ 只有一條線准取 game.lock，代跑其他線排進 `RT-QUEUE.md` 的 console 查詢 → 整理線把各份 REPORT 濃縮成 `PRE-PLAY-CHECKLIST.md`。平常仍依 [[prefer-gpt-sol-for-all-tasks]]。REPORT 落檔見 [[subagent-report-write-authorized]]；MO2 開過後 profile 三檔會漂移，收線派小線 `git checkout` 還原（[[mo2-first-launch-drops-new-plugin-star]]、[[mo2-auto-adds-stray-mods-dirs]]）。

平行分工規則（凍結契約再切工、一個 repo 只一條線有 commit 權、寫別隊權威檔交 merge-request、共用 scratchpad 只動自己命名的子目錄、別對頂層 `rm -f`）現行全文在 [team-model/roles.md](../../agentctl/docs/team-model/roles.md)（出處：`agentctl/handoffs/done/2026-09-02/spike-2026-09-02/REPORT.md:114-124`、`agentctl/handoffs/done/2026-09-05/dsport4-2026-09-05/STATE.md:118-126`、`agentctl/handoffs/done/2026-08-31/content-2026-08-31/SPEC.md:56-71`、`agentctl/handoffs/done/2026-10/home-2026-10-10/batch2/REPORT.md`）。另一條：兩條線要同時寫 MO2 `mods/` 這類共享目錄時，後動的線要先從對方回報或畫面證實對方批次已結束，才能建自己的新資料夾（`agentctl/handoffs/done/2026-08-31/bgdl-2026-08-31/HANDOFF.md:14`）。

## leads-manage-subordinate-context

> Claude 系 agent 的 context 由其上級管理（頂層管 Opus、Opus 管 Sonnet）；建議開 auto compact

2026-09-18 使用者原話：「你轄下的claude系agent如opus, sonnet，要記得管理他們的context。opus作為隊伍領導，也要管理其轄下的sonnet的context。我建議是設定auto compact會比較舒服。」頂層的 context 由使用者管（他會抓斷點叫 compact）。fsm gpt 工人做完就換新的，不必管（[context.md](../../agentctl/docs/team-model/context.md)）。

**Why:** 領隊吃大輸出（log、截圖、目錄列表）後 context 爆掉會卡線，沒人替它抓斷點。

**How to apply:** 開隊時交接書（COMMON.md）寫死：大輸出由工人落檔、Sonnet 任務單一做完就收、領隊每完成一項先寫 REPORT 再接下一項、Sonnet 回報 ≤10 行只回結論與路徑。本機 auto-compact 預設開（settings 沒設 `autoCompactEnabled=false`），但不要依賴它。與 [[fable-top-opus-middle-management]]、[[leads-must-not-end-turn-to-wait]] 並用。

## leads-must-not-end-turn-to-wait

> 領隊用「結束回合＋背景 watcher」當等待會卡死；交接書要寫死「前景 until 迴圈（timeout 540 分段）」，卡住超過 20 分鐘就 TaskStop 換人接手

2026-09-06：結束回合等待的領隊卡了兩小時；TaskStop 後新領隊用現成 plan 十分鐘做完。

**Why:** 子代理結束回合後，佇列裡的 SendMessage 只在「下一個 tool round」送達；沒有 tool round 就永遠收不到。背景 Bash 完成的通知也不保證把它叫醒。

**How to apply:**
- 交接書與 spawn prompt 明寫「等待一律用前景 Bash `until` 迴圈，每輪 `timeout 540`，沒到再跑一輪；別把結束回合當等待」。
- dispatcher 看到 STATE.md 超過 20 分鐘沒動、鎖空、沒 commit → 直接 TaskStop，開小隊接手（料通常都在 staging＋plan json）。
- 等「另一條平行線先完成」時，BRIEF 寫死可驗證的完成判準（不猜對方進度）、前景等待方式、逾時上限與逾時後怎麼回報，並寫明哪些步驟不受阻塞可先做（`agentctl/handoffs/done/2026-10/home-2026-10-03/want-watch/rounds/20261003-1410/INSTALL-BRIEF.md`）。
- 收到「先暫停」裁示時，即使條件已滿足也不硬做完：把已完成部分、成果位置、下一步確切指令寫成任何人都能接手的清單（`agentctl/handoffs/done/2026-10/home-2026-10-03/want-watch/rounds/20261003-1455-zh/REPORT.md`）。

相關：[[im-dispatcher-codex-implements]]、[[tmux-working-text-is-not-liveness]]

## silencer-changes-need-user-signoff

> 會讓既有報告的壞數字變好的變更（豁免清單、排除路徑、閾值放寬、口徑改寫），線只能提案不能自核——它的效果是讓問題從報告裡消失

2026-10-24 訂（`classify_unreached.py` 兩組豁免經使用者逐件拍板時定下；全文在該檔豁免區塊註解）。

**判準：這個變更會讓既有報告裡的壞數字變好嗎？** 會，就是提案不是施工。典型：分類器／lint 的豁免清單、掃描的排除路徑、warning 降級成 info、閾值放寬、「這批不算在內」的口徑改寫。修一個會讓壞數字變多或不變的 bug 不受此限（例：`reachability.py` 的 symlink bug，[[doc-restructure-safety-checklist]]）。

**沒有「顯而易見所以不用問」的例外**：同一組六個檔，使用者上午裁「補索引」、同日改裁「寫豁免」。**裁示反轉要在 REPORT 留軌跡**（記「先裁 A、同日改裁 B」，不只記 B），否則下一場看到 B 覺得理所當然，就在類似題目上自核。

**提案格式**（寫進 REPORT）：逐件兩句——①判準是什麼（為什麼該豁免，不是「它很煩」）；②它取代了什麼（不豁免的正確做法與成本）。使用者逐件裁示，通過才動檔，理由寫進程式碼註解。

**唯一有效的強制手段是測試**：把豁免集合逐條釘死在測試裡，新增一組就得同時改測試。`classify_unreached.py` 目前沒有這種測試，只靠註解與人工 review 擋——這是已知弱點。相關：[[handoff-must-split-no-evidence-from-negative-evidence]]（證據不足是 BLOCKED，不是把它從報告拿掉）。

## subagent-report-write-authorized

> 使用者授權子代理直接寫 REPORT.md；擋住它的不是權限設定而是子代理預設指示——派線用 line 型別，Write 被擋就改用 shell 寫

2026-10-03 使用者說「放寬權限」：子代理可以直接把 REPORT.md／data／tools 寫進 `agentctl/handoffs/<日期>/<代號>/`。

**Why:** settings／hooks 沒有擋寫檔的規則；擋下的是子代理內建的「不要主動建立報告檔」指示，交接書明寫授權也擋不住（2026-11-21 仍會發生）。

**How to apply:** 派線用 `.claude/agents/line.md`（subagent_type: line）；每份交接書／prompt 明寫「使用者已授權：REPORT.md 是交付物，直接寫檔，不要把全文塞回覆」；Write 被擋時線改用 shell（heredoc／python）寫 REPORT，不要放棄落檔；真的沒寫，頂層從輸出代落摘錄版即可，不必逐字。相關：[[leads-manage-subordinate-context]]。

## checkpoint-line-silent-stall

> 存檔線（STATE／commit／push）可能無聲停住：外部指令一律帶 `timeout`、每階段寫 PROGRESS、push 放最後且逾時不重試；頂層要主動看落檔時間，不要只等完成通知

2026-11-22（[checkpoint-2 REPORT](../../agentctl/handoffs/home-2026-11-22/checkpoint-2/REPORT.md)「checkpoint-1 停在哪」）。

**Why:** 存檔線串很多外部指令（lint、git、push、hook），任一個卡住（hook 等輸入、網路、鎖）整條線就靜止，而它自己不會發訊息。

**How to apply:**
- BRIEF 寫：每個外部指令帶 `timeout`（push `timeout 120`＋`GIT_TERMINAL_PROMPT=0`）、每完成一階段在 `PROGRESS.md` 追加一行時間戳、push 放最後一步且逾時不重試。
- 頂層定期看線夾的最新 mtime 與 PROGRESS；超過預期一倍沒有新行就去查，不要等通知。
