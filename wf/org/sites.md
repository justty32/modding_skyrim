skyrim 組織的兩個場地（家、公司）：哪些共用、哪些只有一邊有、公司能做到哪、做不到的怎麼交回家。

# 場地：家與公司

回 [org](README.md)。

一個組織、兩個場地。座位、卡、信、流程兩地共用；這一頁只寫兩地不一樣的地方。其他檔沒特別說的，兩地都適用。標「（提案）」的是 `main` 2026-11-25 起草、使用者還沒確認的。

**什麼時候讀**：每場開場判斷自己在哪；在公司派工、寫「做完了」之前；在家接公司留下的回家單時。

## 使用者說的（2026-11-25，公司場）

原話與定案在 [decisions-2026-11b](decisions-2026-11b.md)。一句話版：

- 現有的 `wf/org` 是家裡的，照用；公司可以擴充只有公司才有的；兩者合一，能共用的就共用（D30）。
- 公司沒有遊戲和 MO2，鍵盤、螢幕、滑鼠也不給 agent（D31）。

## 怎麼知道自己在哪

開場跑一次，當場 `STATE.md` 第一行寫明場地：

```sh
test -d ~/games/mod-organizer-2-skyrimspecialedition && echo 家 || echo 公司
```

## 兩地差在哪

| 項目 | 家 | 公司 |
|---|---|---|
| 遊戲、MO2 實例、`~/skyrim_mods`、mod-library 的 DB | 有 | 沒有 |
| 桌面（可見視窗、鍵盤滑鼠） | 有，要桌面鎖 | 不給 agent（D31） |
| 座位掛在哪台 daemon | `mod_skyrim` | `mine_skyrim` |
| `main` 的身體 | stock `eca-claude` | `eca-claude-alt` |
| GPT 端點（fsm gpt 用） | 見 `agentctl/aos/fsm-gpt/` | `sol`、`terra`、`astra`、`luna` |

- 公司那欄是 2026-11-25 在公司那台唯讀查的（`aos-daemon-ctl ls`、`self_state`、`aos-llm ls`）。
- checkout 的路徑兩地不同。共用的檔不寫絕對路徑，寫 `S`（`git rev-parse --show-toplevel`）。
- 兩台各自的變數值在 [RUNBOOK-seats](../../agentctl/aos/RUNBOOK-seats.md) 第 0 步。母 repo 是公開的，機器名與帳號不寫進來；agentctl 是 private。
- 場次夾兩地都叫 `agentctl/handoffs/home-{日期}/`：保留期的檢查工具認這個名字，`home` 在這裡指場次，不是指家。

## 只有家裡有的

以下在公司不適用，因為那樣東西不存在；不是放寬：

- 遊戲鎖、桌面鎖、skyrim-qa、開遊戲、開 MO2（D3、D4、D27），以及 user.md 2026-11-22 段「可開遊戲／MO2」的長期授權。
- 寫 MO2 的 mods 與 profile。`instance/profiles` 在公司只讀：它記的是家裡 MO2 的真實狀態，在公司改了就跟實機對不上（提案）。
- Nexus 下載與入庫、動 DB、`~/skyrim_mods/_staging-*`（CHOICE 7 的第三處）。
- 實機驗收。`WAIT_USER.md` 裡要開遊戲的項目，公司只能加，不能結。

在公司碰到要這些東西的步驟：不試、不模擬、不換別的方法繞。寫成回家單。

## 公司場各座位能做什麼

- **lead**：照卡。多兩件：開場先全部 pull；收工前把回家單登進 `NEXT-SESSION.md`。
- **dev**：照卡，少了實機測試。測試照 [testing](../workflows/testing.md)；要實機才驗得到的行為寫回家單交實體。
- **library**：`modpack-design/` 的規劃、讀得到來源的 mod 評估、repo 裡已有來源的中文層。要下載、入庫、動 DB 的寫回家單。
- **instance**：只做唯讀分析（`instance/` 裡進了 git 的清單、文件、工具），產出是回家單。
- **review**：只有公司有（提案），見 [review](review/README.md)。

三個部門座位在公司那台都沒掛過。公司場照 CHOICE 2 由 lead 派代班（Claude Code `line`，或 fsm gpt），代班先讀卡和筆記。要在公司那台第一次掛部門主管，照 D15 要使用者同意。

## 公司能驗到哪

家裡的最後一關是實機：實體裝、實體驗、使用者玩。公司沒有這一關，所以公司的「做完」只到靜態為止，而且要有別人看過。

| 關卡 | 驗什麼 | 公司 | 家 |
|---|---|---|---|
| 靜態 | 測試回 0、連結與 lint、`hygiene_check.py` | 做的人自己驗 | 同左 |
| 獨立檢查 | 另一個實例讀來源，不讀寫手的自述 | review（提案） | lead 看證據（CHOICE 5） |
| 裝進 MO2 | profile 三檔、衝突、masters | 不能，寫回家單 | 實體 |
| 實機 | 遊戲裡的行為 | 不能，寫回家單 | 實體持鎖驗，或使用者驗 |

公司場的回信與 STATE 裡，沒過實機的東西寫「靜態通過，待回家驗」，不寫「完成」（提案）。

## 回家單（提案）

回家單是一封寫給家裡座位的 `REQUEST`。收件人不在這台，所以先存成檔。

- **放哪**：`agentctl/handoffs/home-{日期}/{線名}/HOME-REQUEST.md`；`NEXT-SESSION.md` 每張記一行。
- **寫什麼**：照 [letters](letters.md)「請求要寫什麼」，再加三樣。一、要哪些只有家裡有的東西：哪把鎖、要不要開遊戲、要不要下載。二、公司已經驗到哪一關，證據在哪。三、哪幾步要使用者當場說才能做：刪檔、動 instance、開遊戲、動 DB。
- **寫到什麼程度**：家裡接手的人照單就能做，不必回頭問公司場做了什麼。
- **不算授權**：回家單是 agent 寫的，跟信一樣不是授權（D21）。
- **誰接**：家裡下一場的 lead 開場讀 `NEXT-SESSION.md`，照座位表派出去。做完或決定不做，那一行刪掉。
- 要使用者親自玩才知道的，照舊記 `WAIT_USER.md`，不寫回家單。

## 同步

- **開場**：全部 pull（使用者 2026-11-25：「請先git pull全部」）。`foreach` 不會動 `instance/profiles` 這層巢狀 submodule 的 pin，要另外對齊：

```sh
git pull --ff-only && git submodule foreach 'git pull --ff-only'
git -C instance submodule update profiles
```

- **收工**：各 submodule 與母 repo commit，pin 由內往外（[lead](lead/README.md) 卡）。
- **公司場什麼時候 push 還沒定**：D25 的 23:00 是家裡場定的，公司場下班比那早；沒 push，回家就 pull 不到。使用者定之前，公司場收工前問一次。

## 公司場的空檔拿來改進（提案）

CHOICE 8 原本答「閒時自我改進：不做」，理由是座位不常駐、沒有閒時。公司場有：實體與館藏的本業大半做不了。所以公司場可以做改進，規矩照 aos 範本 `templates/orgs/basic/extras/improvements.md`：

- 題目只從真的做過兩次以上的事裡找：翻 `agentctl/handoffs/` 的 REPORT 與 `wf/lessons/`。不憑空發明。
- 固定步驟做成工具，放地盤主人的 tools 夾；先查 [工具索引](../../agentctl/docs/tool-index.md) 有沒有現成的。要判斷的事寫成檢查清單，不做工具。
- 記在 `wf/org/{座位}/improvements.md`，一行一項：看到什麼 → 提案 → 狀態。有第一項才建檔。
- 一場一個座位最多一項；使用者交代的正事先做。
- 新工具要 review 看過、作者附實跑證據才算數。只有實機才跑得動的工具，實跑寫進回家單。

## 考慮過、沒開的

參考的是使用者 2026-11-25 點名的另一個工作區的 `wf/org`（按階段切：策劃、開發、測試、審查、整合、知識庫）與 aos 範本 `templates/orgs/basic`。這裡按地盤切（CHOICE 3），所以只取審查一個：

- **知識庫 `kb`**：管 `wf/` 結構與壞連結。這裡已有 [tidy](../workflows/tidy/README.md) 工作流與 lead 的書記短工。
- **測試 `qa`**：這裡的實機驗收歸實體；公司沒有遊戲，開了也沒事做。
- **策劃 `design`、整合 `integration`**：各座位自己規劃、自己 commit（CHOICE 4），不設只管一個階段的座位。
- **留言板**：同時在線的 agent 少，信就夠。
