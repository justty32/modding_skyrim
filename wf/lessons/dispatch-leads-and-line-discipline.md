# 調度：領隊與線的運作紀律

[lessons 索引](README.md)

## rush-mode-parallel-opus-agent-lines

> 2026-09-26 急件模式：一份 COMMON.md 交接＋Agent 工具開 8 條 Opus 平行線，15 分鐘收完八題存檔調查；一條線持遊戲鎖代跑 RT-QUEUE（原 type: memory）

2026-09-26 早使用者 09:07 開場、10:20 關機，說「想開多少線都可以、儘快」。做法：先寫一份 `handoffs/home-<日期>/COMMON.md`（硬停時刻、報告格式、路徑、鎖規則），再用 Agent 工具一次開 8 條 Opus 調查線（每線一個交接段），只有一條線准取 game.lock 並在 09:45 代跑其他線排進 `RT-QUEUE.md` 的 console 查詢；最後開一條整理線把八份 REPORT 濃縮成 `PRE-PLAY-CHECKLIST.md`。09:25 全部收線並 commit。

**Why:** codex tmux 線要送鍵、驗 Enter、盯 Working，起線成本高；Agent 工具的 Opus 線起線零成本、完成有通知、可平行八條，急件時快得多。使用者當天也明說「用啥模型都行」。

**How to apply:** 使用者有硬時限或說「儘快」時，走這條：COMMON.md → 平行 Agent(Opus) → 單線持鎖代跑 RT-QUEUE → 整理線出清單。平常仍依 [[prefer-gpt-sol-for-all-tasks]]。注意子 agent 偶爾寫 REPORT 被 harness 擋，頂層要從完成通知代落檔；MO2 開過後 profile 三檔會漂移，收線派小線 `git checkout` 還原（見 [[mo2-first-launch-drops-new-plugin-star]]、[[mo2-auto-adds-stray-mods-dirs]]）。

2026-10-23 補：要開平行線寫程式，領導先凍結可執行契約（型別/介面/schema）再切工，契約本身列進驗收，四條線才能真平行一次成功（`agentctl/handoffs/done/2026-09-02/spike-2026-09-02/REPORT.md:114-124`）。多線平行施工同一批 repo 時，每個 repo 只由一條線獨佔 commit 權，其餘線唯讀或只寫非版控輸出目錄（`agentctl/handoffs/done/2026-09-05/dsport4-2026-09-05/STATE.md:118-126`）；要同時寫 MO2 `mods/` 這類共享目錄時，後動線要先從對方 inbox 或 tmux 畫面證實對方批次已結束才能建自己的新資料夾（`agentctl/handoffs/done/2026-08-31/bgdl-2026-08-31/HANDOFF.md:14`）；兩隊各自領地但有共用權威檔時，要寫入的一隊寫成 `merge-requests-<x>.tsv` 交擁有領地那隊按信心分級併入，不直接跨領地寫（`agentctl/handoffs/done/2026-08-31/content-2026-08-31/SPEC.md:56-71`）；共用 scratchpad 清理只能動自己命名的子目錄，別對頂層跑 `rm -f`（`agentctl/handoffs/done/2026-10/home-2026-10-10/batch2/REPORT.md`）。

## leads-manage-subordinate-context

> 2026-09-18 使用者定：Claude 系 agent 的 context 由其上級管理（頂層管 Opus、Opus 管 Sonnet）；gpt-sol 自帶 auto-compact 不用管；建議開 auto compact（原 type: feedback）

2026-09-18 使用者原話：「你轄下的claude系agent如opus, sonnet，要記得管理他們的context。opus作為隊伍領導，也要管理其轄下的sonnet的context。我建議是設定auto compact會比較舒服。」頂層的 context 由使用者管（他會抓斷點叫 compact）。

**Why:** Opus／Sonnet 領隊吃大輸出（log、截圖、目錄列表）後 context 爆掉會卡線，而且沒人替它們抓斷點；gpt-sol 會自己 auto-compact 所以只有 Claude 系要管。

**How to apply:** 開隊時交接書（COMMON.md）寫死：大輸出交 gpt-sol 落檔、Sonnet 任務單一做完就收、領隊每完成一項先寫 REPORT 再接下一項、Sonnet 回報 ≤10 行只回結論與路徑。本機 auto-compact 是預設開（settings 沒設 autoCompactEnabled=false），但不要依賴它。與 [[fable-top-opus-middle-management]]、[[leads-must-not-end-turn-to-wait]] 並用。

## leads-must-not-end-turn-to-wait

> Opus 領隊用「結束回合＋背景 watcher」當等待會卡死；交接書要寫死「前景 until 迴圈（timeout 540 分段）」，卡住超過 20 分鐘就 TaskStop 換人接手（原 type: memory）

2026-09-06 三個領隊（upd／new10／mcoi）都在等工人或等鎖時「結束回合、掛背景 watcher」；watcher 觸發後領隊有時會醒、有時不會。lead-upd 從 16:52 卡到 18:59 沒套最後一批，最後 `TaskStop` 停掉、開 lead-upd2 用現成的 plan 十分鐘做完。

**Why:** 子代理結束回合後，佇列裡的 SendMessage 只在「下一個 tool round」送達；沒有 tool round 就永遠收不到。背景 Bash 完成的通知也不保證把它叫醒。
**How to apply:** 交接書與 spawn prompt 明寫「等待一律用前景 Bash `until` 迴圈，每輪 `timeout 540`，沒到再跑一輪；別把結束回合當等待」。dispatcher 看到 STATE.md 超過 20 分鐘沒動、鎖空、沒 commit → 直接 TaskStop，開一個小隊接手（料通常都在 staging＋plan json）。相關：[[im-dispatcher-codex-implements]]、[[tmux-working-text-is-not-liveness]]。

2026-10-23 補：等待「另一條平行線先完成」時，BRIEF 要寫死具體可驗證的完成判準（不是猜對方進度）、前景等待方式、逾時上限與逾時後回報方式，哪些步驟不受阻塞可先做也要寫清楚（`agentctl/handoffs/done/2026-10/home-2026-10-03/want-watch/rounds/20261003-1410/INSTALL-BRIEF.md`）。收到「先暫停」裁示時，即使條件已滿足也不硬做完，把已完成部分、成果位置、下一步確切指令寫成任何人都能接手的清單（`agentctl/handoffs/done/2026-10/home-2026-10-03/want-watch/rounds/20261003-1455-zh/REPORT.md`）。

## silencer-changes-need-user-signoff

> 會讓既有報告的壞數字變好的變更（豁免清單、排除路徑、閾值放寬、口徑改寫），線只能提案不能自核——它的效果是讓問題從報告裡消失

2026-10-24 訂。當天 `classify_unreached.py` 要加兩組豁免（`agentctl/docs/<主題>/README.md` 六份、`instance/profiles/.repo/workflows/profile/` 三份），使用者逐件拍板後順手定下這條門檻；全文在該檔的豁免區塊註解，不另開文件。

**判準，一句話：這個變更會讓既有報告裡的壞數字變好嗎？** 會，就是提案不是施工。典型品項：分類器／lint 的豁免清單、掃描的排除路徑、warning 降級成 info、閾值放寬、「這批不算在內」的統計口徑改寫。**反過來，修一個會讓壞數字變多或不變的 bug 不受此限**——2026-10-24 同一天修 `reachability.py` 的 symlink bug 就沒走這道門（見 [[doc-restructure-safety-checklist]] 的 2026-10-24 補）。

**沒有「顯而易見所以不用問」這個例外。** 同一組六個檔，使用者上午裁「補索引」、同日改裁「寫豁免」——同一個人對同一件事在一天內反轉過一次，線更不可能自己推得出來。**裁示反轉要在 REPORT 留軌跡**（記「先裁 A、同日改裁 B」而不是只記最終的 B）：只記 B 的話，下一場看到 B 會覺得理所當然，於是在類似題目上自核。

**提案格式**（寫進 REPORT，不要只給結論）：逐件兩句——①判準是什麼（為什麼這件該豁免，而不是「它很煩」）；②它取代了什麼（不豁免的話正確做法是什麼、成本多少）。使用者逐件裁示，通過才動檔，理由寫進程式碼註解。

**唯一有效的強制手段是測試，不是註解。** 把豁免集合逐條釘死在測試裡，新增一組就必須同時改測試，變成藏不住的動作。2026-10-24 當天被容量 gate 卡住沒做（`test_classify_unreached.py` 仍缺），所以這條門檻目前只靠註解與人工 review 擋——**這就是它目前的已知弱點**。相關：[[handoff-must-split-no-evidence-from-negative-evidence]]（證據不足是 BLOCKED，不是把它從報告拿掉）。

## subagent-report-write-authorized

> 10-03 使用者授權子代理直接寫 REPORT.md；擋住它的不是權限設定而是子代理預設指示，交接書要明寫「REPORT 是交付物、必須寫檔」，或用 .claude/agents/line.md 型別

2026-10-03 使用者說「放寬權限」：子代理可以直接把 REPORT.md／data／tools 寫進 `agentctl/handoffs/<日期>/<代號>/`。

**Why:** 10-03 前有 5+ 次子代理回「系統擋下寫 REPORT（子代理不寫報告檔）」，頂層只好代寫，浪費 context。查過 settings/hooks 都沒有擋寫檔的規則——真因是子代理內建的「不要主動建立報告檔」預設指示，跟交接書衝突時有些線選擇不寫。

**更正（同日 kitA）**：交接書明寫授權後仍被擋，子代理回報是 harness 層擋寫報告檔，不是模型自選；部分線（c0925／c0927／c0928、retro r*）寫得進去，條件不明。交接書授權無效，只剩 line 型別待新 session 驗證；驗證前頂層照舊代存。

**10-03 下午再觀察**：general-purpose 線 12 條中只有 mc-1003 寫進 REPORT.md，其餘全被擋、全文塞回覆，頂層代存成本高（每份數 k token）。代存時寫摘錄版即可，不必逐字。

**How to apply:** 派線用 `.claude/agents/line.md`（subagent_type: line，新 session 才載入）；在那之前，每份交接書／prompt 明寫「使用者已授權：REPORT.md 是交付物，直接寫檔，不要把全文塞回覆」。相關：[[leads-manage-subordinate-context]]。
