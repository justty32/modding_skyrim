# 臉與身體：裝備、身體與部署狀態排錯

[lessons 索引](README.md)

臉壞的第一輪分流與 facegen 沒生效（存檔快取、漏裝、自訂種族、資料夾路徑、Daegon 升級）在 [faces-facegen-paths-and-loading](faces-facegen-paths-and-loading.md)；頭部件對名規則在 [faces-facegen-consistency](faces-facegen-consistency.md)。

## outfit-hair-slot-hides-headparts

> 2026-09-11 Yoana 大媽臉真因：NPC 預設服裝的披風佔 biped slot 31（Hair）且 NIF 內縫假髮，引擎藏掉真頭髮；換頭部件／facegen／種族怎麼改都看不出來。臉壞先查裝備 slot 30/31/41/43/130 與 unequipall 對照

穿著佔 Hair slot 的裝備會隱藏頭髮 head part：Yoana the Wanderer 的預設 outfit「小紅帽 - 披風」ARMO 佔 **slot 31**、NIF 縫了假髮，換臉層寫的髮型永遠看不到；同一筆 NPC_ 的身高照樣有效，facegen 藏掉零變化，placeatme 複製體也壞（穿同一套 outfit）。

**How to apply（臉／髮壞的第一步）：**
1. 遊戲內先 `<ref>.unequipall` 再看；變好＝裝備問題，去查 outfit 的 ARMO/ARMA biped slots（30 頭、31 髮、41 長髮、43 耳、130 頭飾等）。
2. 離線：NPC_ DOFT（default outfit）→ OTFT → 每件 ARMO 的 BOD2 slots；佔 31／41 的都會蓋髮型。
3. 修法：outfit 層去掉那件，或改 ARMA 的 slot／NIF 切掉假髮。
4. 「複製體也壞」不代表不是 per-ref；判斷前先脫裝備。

頭髮也可能在 NPC 的 WornArmor 皮膚裡，見 [[npc-wornarmor-is-part-of-appearance]]；換種族後假髮 ARMA 種族不符見 [[look-transplant-wnam-and-skin-checks]]。相關：[[face-bugs-check-real-actor-and-upstream-fomod]]、[[look-layer-must-carry-hdpt-flst-clfm]]

## bodyslide-wine-preset-empty-nam7-weight

> 2026-09-11 私有身體層實測：NPC_ 的 NAM6 是身高、NAM7 才是體重；私有身體共用一套 ARMA/ARMO 就夠（三種族身體 TXST 同一張 dds＋FaceGenTextures）；當時 wine 下 BodySlide GUI 的 Preset 下拉空白是個案，烤身體走原生 `-p`

**BodySlide preset**：2026-09-11 Kurone 46560 私有身體（3BA）在當時 wine／Proton、從 staging 直接啟動，GUI preset 下拉空白（連 CBBE 官方預設也讀不到），改寫 `.osp` defaults 再 Batch Build。這不是 Wine 不支援 preset 的通則；現行走[原生 `-p` 路線](../workflows/bodyslide/headless.md#首選原生-preset-命令)，OSP fallback 的界線也在那份。

**NPC_ 欄位**：`NAM6`＝身高、`NAM7`＝體重。體重滑條（0-100）是兩個雕好形狀間的逐頂點內插，不是整體縮放（實測同 mod 兩體重檔深度差 17.94%、寬度 1.15%、高度 −0.11%）；要調整個人大小改 NAM6（2026-10-23，`agentctl/handoffs/done/2026-09/home-2026-09-09/body/REPORT.md:17-27`）。

**私有身體不必每人一套 ARMO**：原版 `SkinBodyFemale_1`／`DarkElf`／`WoodElf` 三個 TXST Diffuse 都是同一張 `FemaleBody_1.dds` 且帶 FaceGenTextures（膚色由 facegen tint 執行期給），共用一套 3 ARMA＋1 ARMO＋私有 nif 路徑即可，NPC_ 只改 WNAM。ARMA 第三人稱模型指向**全域** `FemaleBody_1.nif` 時不需重烤，做一支小 ESL 把該 ARMA 的 `WorldModel[1].File` 改指已烤好的私有 nif，0 筆 NPC_ 改動（2026-10-23，`agentctl/handoffs/done/2026-10/home-2026-10-10/batch4a-kurone/REPORT.md`）。

**素材包有沒有私有身體，看檔版本**：Kurone 76220 DEFAULT 1.12（37 MB 輕量版）把種族和 SkinNaked 改回原版、不附身體 nif；MAIN 1.1（661 MB）每人附 3BA `femalebody_0/1.nif`＋`.tri`、4K 頭身膚色與 `KF_<名字>Body3BA.osp`，兩版 plugin 同名不能並存，MAIN 只能當資產來源。判 donor 先看 Nexus 各檔的 content preview，不要拿現裝目錄推全系列（2026-10-26，`agentctl/handoffs/home-2026-10-26/bodyswap/REPORT.md` §2c）。

**交叉風險**：私有身體層的 NPC_ 覆寫會壓過換臉層；換臉層之後再改，必須把新贏家 forward 回身體層（或身體層載在前、換臉層帶 WNAM）。交接書寫死的單一欄位值可能依種族／型別而不同（「MorphRace 補回去用 013748」其實依種族有四個值），有疑慮用整筆 forward 自權威來源，不手改單一值（2026-10-23，`agentctl/handoffs/done/2026-09/home-2026-09-09/body/REPORT.md:69-78`）。

**OBody NG 4.4.3 preset 黑名單**（2026-10-23，`agentctl/handoffs/done/2026-10/home-2026-10-04/aniya/REPORT-fix.md`）：逐字串精確比對，不支援萬用字元／子字串（「Zeroed Sliders」擋不住「CT77 Zeroed Sliders - Zap Panties」）；只擋之後的新分配，已存進 cosave 的 preset 不會清（ORefit 換裝路徑只讀 cosave）。建黑名單前先掃出全部啟用中的實際 preset 名稱；加了之後對已中過的角色手動重置或清 skee morph cache。

**How to apply:** 實機看身材先 `<ref>.unequipall`，或用 Outfit Studio 開 nif 看形狀不用開遊戲；改體重動 NAM7、整體大小動 NAM6；多層覆寫同一個 NPC_ 時最後載入的那層要 forward 全部欄位。

相關：[[look-layer-must-carry-hdpt-flst-clfm]]、[[look-transplant-workflow-and-picker]]

## npc-wornarmor-is-part-of-appearance

> 原 NPC 的頭髮與身體不一定在 headParts，也不一定跟玩家種族皮膚相同。

- 現象：Soul Tomb preset 載入玩家後，沒有原 NPC 頭髮，也不是原私有身體。
- 真因：Chloe 的 WornArmor 皮膚包含 AAA_Hair_Chloe、AAANakedTorso；HDPT 髮 AAA_Dum_HL 是空殼。玩家走種族皮膚，不會因 jslot 自動繼承 NPC WornArmor。
- 驗法：沿 NPC WornArmor → ARMO → ARMA → 女性模型查 VFS 贏家，與 HDPT／FaceGen 分層盤點；髮肩碰撞也要用實際部署的身體與體重。
- 避法：玩家髮型用合適 HDPT；套回 NPC 時先複製共用皮膚，只在專屬複本替換髮，避免連帶改到 Recorder。靜態零穿越不代表走動或 SMP 過關。
- 出處：`agentctl/handoffs/home-2026-11-25/miku-face/support/REPORT.md:17`（agentctl `18953859`）；`REPORT.md:3`、`:22`（`44c11491`）。

## installed-state-before-install-plan

> 文件說缺外掛時，先查現役，不先再裝一份。

- 2026-11-25：文件說要裝 RaceMenu 身體滑桿，實際 RaceMenuMorphsCBBE 2.48 已啟用，來源包 11 檔和既有層 bytes 相同——文件沒跟上部署。
- 驗法：只讀交叉確認 modlist、plugins 星號、loadorder 與 VFS winner。裝了滑桿腳本不等於各身體 BODYTRI 支援全數 morph，仍需實機測試；OBody 重新指派預設會清掉其他 key 的手捏 morph。
- 避法：先核現役再申請安裝；測試副本只能替身，不重複啟用，收工不能拆掉原本已有的層。OBody 設定及修正方案另取授權，不能順手改。
- 出處：`agentctl/handoffs/home-2026-11-25/miku-face/gpt-bodymorph/INSTALL.md:5`、`:19`、`:39`（agentctl `2b02a23a`）；`REPORT.md:30`（`44c11491`）。
