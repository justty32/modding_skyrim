# 一整套系列／生態的取得與安裝

動作系統、perk 系統、任務框架這類**互相咬合**的一整套。跟單件的差別不是數量，
是**它們會彼此覆寫檔案、共用生成式 output、而且一次全裝就再也分不清是誰壞的**。

現役動作系統已改走 MCO；階段與隊列見
[`mco-migration-plan-2026-09-02.md`](../../../modpack-design/content-plan/gameplay/mco-migration-plan-2026-09-02.md)。
下方 BFCO 內容只保留為「系列分層與生成式 output」的歷史實例，不代表現役選型。

```text
Done when: <每層各自成批且各自驗過、生成式 output 已重跑且 hash 有記錄、DLL winner 唯一、真人矩陣已排>
```

## 鐵律：每一層各自成批（BFCO 歷史實例）

BFCO 線的實際順序：

```text
1 框架更新（BFCO 本體）
2 命中核心（Precision）
3 閃避（IFrame 系統）
4 第三人稱方向與鎖定（TDM ＋ 對版繁中）
5 進階節奏（可選，Wait Your Turn Redux）
```

**一層裝完驗完才動下一層。** 混批的代價不是麻煩，是**壞掉時無法歸因**——
動作系統的症狀（不出招、卡動畫、攻速不對）長得都一樣。

## 升版時要停用被取代的元件

BFCO `3.100.3` → `3.100.5` 時，新版**自帶單一 `BFCO.dll`**，
所以同批要停用舊的 `BFCO Universal Support`，讓新版的 DLL 成為唯一 winner。

**升版不是只換本體。** 每次升版都要問：新版吸收了哪些原本要另外裝的東西？

## FOMOD：先重播舊版驗一致，再套同規則到新版

安裝器不會替你判斷條件式補丁。做法是：

1. 用**舊版 archive** 重播當初的 FOMOD 選項
2. 跟**現役安裝**逐檔比對——BFCO 那次是 **1,358／1,358 檔完全一致**
3. 一致之後，才用**同一組規則** materialize 新版

不一致就代表你對「當初裝了什麼」的理解是錯的，這時候升版等於在錯誤基礎上疊錯誤。

選項要記進 [`agentctl/qa/fomod-choices/`](../../../agentctl/qa/fomod-choices/)
（`mo2ctl-fomod-choices-v1` 格式），例如 Precision 選 `Compatibility=None`——
**不提前混入 TK Dodge patch**，那是下一層的事。

## 生成式 output 是獨立 mod，而且要重跑

Pandora／Nemesis／FNIS 的產物放在專屬的 `Pandora Output` mod，**不是 shared `overwrite`**。
每次動到 behavior 相關的 mod 都要重跑，並且：

- **升版前先備份舊 output**：`pandora-output-backups/<日期>-<用途>/`
- 重跑後記錄檔數與 `Engine.log` 的 ERROR／FATAL／WARN 數
  （BFCO 3.100.5 那次是 224 檔／186 HKX、0 ERROR／0 FATAL／7 WARN）
- 確認 **input tree 與 shared `overwrite` 的 hash 沒變**——生成物不該寫回來源 mod

**踩過**：Pandora 4.x 的 CLI 改用 `--output:"..."`／`--tesv:"..."`，
沿用舊參數會把 **212 個 output 寫錯地方**，還有 **11 個檔被寫回 BFCO 來源 mod**。
錯置的那批保留在 `pandora-output-backups/20260813-2149-misdirected-bfco-3.100.5/`，
被污染的 11 個檔用 archive 復原。

Nemesis／Pandora 的 patch 有 **active／inactive** 之分：Precision 的 `colis` patch
首次 auto-run 被 cache 發現但**預設 inactive**，要明確啟用後重跑。

## 第三方常自帶框架副本

動作／腳本類 mod **極常**自帶 PapyrusUtil／JContainers 的副本。若它在 VFS 贏了，
**整個 load order 的腳本會散彈式失效，極難反推**。

```sh
# 安裝前後各跑一次，做 diff
housecarl_skse_inventory   # contested 清單
```

**只看一次不算**——要的是「這次安裝有沒有改變 contested 的勝出者」。

## 每批的靜態閘門

- archive `7z t` 通過，SHA-256 記進批次紀錄
- ESP 無 missing master／dangling ref
- **DLL winner 唯一**
- validator 標出的未綁定屬性要逐個判讀——MCM quest 的未綁定屬性常是正常的，
  但要 runtime 確認，不能因為「看起來像既有問題」就跳過

## 真人驗收

動作矩陣只有人眼／手感能判：玩家與 NPC 各武器類、連段結束、處決／互動後狀態恢復、
moveset 沒有 `mco_` event 殘留、hitbox、多人命中、ragdoll／flinch、cancel window。
記進 [WAIT_USER.md](../../../WAIT_USER.md)，寫清楚要驗哪幾項。

## 何時不用

- 只是本體加一兩個 patch → 走 [README 的「衛星件」](README.md#衛星件擴充patch漢化)。
- 系列裡只換其中一個元件，其他不動 → 當單件處理，但**仍要重跑生成式 output**。
