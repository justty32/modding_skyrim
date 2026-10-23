# 翻譯與中文層

[lessons 索引](README.md)

## zh-layer-gate-base-mod-must-be-enabled

> 中文層部署前要查本體 mod 在 modlist 是否啟用，不能只看 plugins.txt；Apocalypse 案例讓 242 個 Cannot open store 躺了三天（原 type: memory）

2026-09-03 post2 隊發現：Papyrus 323 個 `Cannot open store for class` 有 242 個來自 `Apocalypse - Magic of Skyrim.esp`——本體 `Apocalypse 10.2.3`（含 scripts BSA）早在 profiles 入版控（08-23）前就已停用（連 Ordinator／Vokriinator patch 一起，是刻意退役），但 08-31 22:45 的中文層部署把 `MAG-Apocalypse-Magic-of-Skyrim-CHS-MCM-7934` 啟用並在 plugins.txt 勾了同名 esp。`zh-gap-winners.csv` 把它標成 `ACTIVE-PARTIAL`，因為那張表只看 plugin 是否啟用，沒看本體 mod。

**Why:** 中文層只帶 esp（＋少量 MCM 腳本），本體 BSA 沒載入時 esp 的 VMAD 引用全部落空；`Cannot open store` 存量 318 從 lrinst 之前就在，四隊的「新增 0」驗收都沒發現存量本身就是病。
**How to apply:** 中文層／覆蓋層的部署 gate 要加一條「本體 mod 在 `modlist.txt` 是 `+`」，本體停用就不部署、也不勾 esp；`Cannot open store` 的存量要按 class 歸因到來源 mod（`post2/data/cannot-open-store-by-mod.csv` 的做法：掃 BSA 名稱表＋plugin 位元組搜尋），別只比新增數。zhmake 124 層裡也有 Apocalypse 簡中層，部署前先裁本體去留。相關：[[missing-master-scan-mast-not-housecarl]]、[[slanguage-english-chinese-in-english-slot]]。

2026-10-23 補：帳本標籤「READY-IN-LIBRARY」只代表中文層檔案已在庫、拓撲已驗，不代表本體已裝；曾有交接文件把兩件事併成一句話，誤判成「只差裝中文層」，實際本體都還沒裝進 MO2（Animated Armoury／Immersive Weapons 案例，`agentctl/handoffs/done/2026-08-28/opus-install-prep/PLAN.md:290-312`）。看到 READY 類標籤要額外雙向搜尋 MO2 mods/ 與 modlist 確認本體真的已裝且啟用。

## zhport-editorid-fallback-and-hdpt-untranslatable

> 中文層對種子時 FormID 對不上（作者改版重編）要改用 EditorID 比對；HDPT 頭部件 EDID／名稱絕不翻譯（原 type: project）

2026-09-12 want4 批（lead-want4）：`zhport.py` 用 FormID 對舊中文包種子，遇到作者改版整批重編 FormID 時 gaps 被嚴重高估（Runic Arts 少算 170 欄、Sacrifices 605/706）；改用 EditorID 比對就救回。另外 13 個 HDPT 頭部件代號留英文是對的：翻下去 facegen 對名失敗會整顆作廢（見 [[hdpt-edid-must-match-facegen-shape-names]]）。

**Why:** gaps 異常大時工人會急著整包重翻，白花翻譯量又降低一致性。

**How to apply:** 中文層任務 gate 前先看 gaps 比例，>50% 先換 EditorID 比對再決定翻不翻；翻譯範圍排除 HDPT／FLST／種族內部代號，只翻玩家讀得到的欄。
相關：[[translation-layer-cost-threshold]]、[[chinese-diff-ok-but-no-tofu]]

2026-10-23 補：本體大版本升級（8,000+ 行等級）不必全文重翻，用舊版翻譯當 corpus 建原文 exact-key map，相同行自動投射、只把變動行與新行放進人工隊列，工作量可降一個數量級（`agentctl/handoffs/done/2026-08-29/cx-serana/REPORT.md:192-199`）。

2026-10-23 補：本體整支替換式舊版翻譯遇大版升級，可用 `zhport.py port --seed-match both`（carrier=新版本體、seed=舊版中文、lexicon-pair=舊版英文對舊版中文）把譯文重新映射到新版 esp，gate 用 fontgate(缺字0)+esplib stats --cmp（跟新本體 record 集合比對 same）（`agentctl/handoffs/done/2026-10/home-2026-10-08/want/REPORT-build.md`）。

2026-10-23 補：排除範圍不只 HDPT/FLST/種族內部代號，pex 腳本裡靠字串比對的 3D 節點名（如 `MoveToNode(self,"FortSungard")`）翻了會讓對應功能失效（內戰地圖旗子插不到位），跑 zhport/pexstrings 前要先掃一輪這類呼叫參數（`agentctl/handoffs/done/2026-10/home-2026-10-10/m152315/REPORT.md`）。

2026-10-23 補：zhport 的種子同鍵規則會把載體裡「已經是中文、來自另一層」的欄位也換成種子譯文，不是單純補缺；只想補缺欄不想動既有翻譯時，carrier 與 seed 都用英文版本，缺口欄位改用 `--override` 指定（`agentctl/handoffs/done/2026-10/home-2026-10-10/tradingposts/REPORT.md`）。

2026-10-23 補（E2bs-10）：舊中文層當種子搬字時，種子與載體的 master index 可能不同（IDE Thalmor：種子 esp 該 master 前綴 05、載體 03），zhport.py 不做正規化會對不上 FormID 鍵；先核對兩邊 master 清單順序，不一致就把種子譯文轉成與 FormID 無關的 glossary（EditorID 或英文原文為鍵）再搬（`agentctl/handoffs/done/2026-09/home-2026-09-11/zhfix/REPORT.md:26-27`）。

## apocalypse-rebuild-waits-new-playthrough

> "2026-09-25 現役 Apocalypse 中文層其實是 7934 版記錄集（4,218 筆）整支換掉本體；10.2.3 英文底版重建層（staging apoc/）少 465 筆會動舊存檔，留到新周目才裝；同名覆蓋層部署要先比 record 集合"（原 type: memory）

2026-09-25 cx-deploy 前檢抓到：現役 `Apocalypse - Magic of Skyrim.esp` 的 winner 是 `Apocalypse-Magic-of-Skyrim-Simplified-Chinese-FULL-Completion-Combined-Dev-2026-09-03`，它把整支 esp 換成 CHS 7934 版的記錄集（4,218 筆），本體目錄雖是 10.2.3（3,945 筆）但實際跑的是舊結構。cx-apoc 以英文 10.2.3 重建的層（`~/skyrim_mods/_staging-2026-09-25/apoc/`、mod-library `Apocalypse-Magic-of-Skyrim-10.2.3-Chinese-Rebuilt-Dev-2026-09-25`）刪 465 筆／新增 192 筆，裝上去會讓舊存檔指到不存在的 FormID。

**Why**：同名覆蓋型中文層不是「翻譯」而是「整支替換」，版本不同就是換了本體。

**How to apply**：① 舊存檔在用時，Apocalypse 只能裝保留舊結構的 zhfix 層（已於 profiles `6dcb0fa` 部署）；10.2.3 重建層等**新周目**再裝。② 之後任何同名覆蓋層部署前，先用 record 型別＋raw FormID 集合比對現役 winner（cx-deploy 的 `deploy/work/preflight.py`），集合不同就不能在舊存檔上換。③ RDO 62500 Final 集合與現役相同（9,765 筆）可直接換。相關：[[zhport-editorid-fallback-and-hdpt-untranslatable]]、[[nexus-api-version-is-not-proof]]

## translation-layer-cost-threshold

> 2026-08-30 起翻譯層的主 gate 改成「是不是遊戲內容」;成本只決定做不做得到,不決定值不值得（原 type: feedback）

**2026-08-30 使用者裁示（現行）**——我問「無中文的要不要開自製翻譯輪，子線提議『可譯字串 < 300 條
且無語音字幕就做』，改這個數字即可」，他答：

> 要不要翻譯**就是看它是不是遊戲內容**。

**Why:** 他否掉的是**用數量當判準**。判斷點回到「玩家在遊玩過程中會不會讀到這段字」——
會讀到就翻，讀不到就不值得投成本。數量多不是不做的理由，反而正是該做的理由。

**How to apply:**
- **是遊戲內容 → 做**：對話、字幕、任務日誌／目標、書籍、物品與法術名稱／描述、
  遊戲內通知、NPC 名稱、地名。**不看字數。**
- **不是遊戲內容 → 不做**：工具 UI、MCM 設定頁、INI 顯示值、熱鍵名稱、框架／DLL 除錯訊息、
  安裝器文案。純動畫／純機制 tweak／SKSE DLL 通常根本沒有可翻文字，直接不列入。
- **成本只在「做不做得到」那一層**：文字硬編在 DLL、要換官方 executable、載體結構對不上
  → 標 `BLOCKED-載體`，那是做不到，不是不值得。OAR 換第三方 DLL 屬這類。
- 繁簡都可（[[no-cht-chs-preference]]）；方塊字是硬 gate（[[chinese-diff-ok-but-no-tofu]]）；
  版本對版真正的閘門是二進位拓撲比對（[[nexus-api-version-is-not-proof]]）。

**這條取代了 2026-08-21 的舊判準**（「依成本不依類別、非遊玩內容順手能做就做」）。
舊判準的實例標尺仍可參考：MCM Helper 容易、DMK 中等、OAR 做不到——但**現在 MCM 那類
本來就不該做**，因為它不是遊戲內容。正本文件：`modpack-design/sources/translation-layer-cost-policy.md`。

**仍然成立的教訓**：不要自己加限制。舊版我曾把「很難做就不用做」放大成「非遊玩內容一律英文」，
那是我加的；這次是使用者自己把 gate 改成類別，性質不同——[[dont-inflate-light-preferences]]。

2026-10-23 補：判斷「是不是遊戲內容」不能只看字串所在的函式/分組名稱猜，要實際追呼叫端；曾有一批英文字串被歸類為「MCM 主畫面英文」要修，實際追蹤後 MCM 根本不呼叫那個函式，玩家只會在跨區域時看到一則 Notify，另兩處只進 debug 日誌永遠看不到（`agentctl/handoffs/done/2026-08-28/opus-zh-summary/SUMMARY.md:539-567,742-744`）。

## no-cht-chs-preference

> 使用者繁簡都可接受，中文化不需要為了正體額外做 OpenCC 轉換層（原 type: user）

2026-08-22 使用者明說「繁簡我都沒差」。要的是**有中文**，不是**正體中文**。

**Why**：在此之前我把「同版正體層」當成硬需求，為此做過 CHS→CHT 的 OpenCC s2twp
轉換、還為此排過人工語言 QA 的成本。那整條成本其實不存在——直接裝同版簡中即可。

**How to apply**：
- 遇到只有簡中的 mod，**直接裝簡中**，不要開轉換層工作。
- 挑檔案時判準退回單一條：**版本要與本體完全相同**（見 [[translation-layer-cost-threshold]]）。
- 已存在的 CHT 層不用回頭改，但別再為新 mod 生成新的 CHT 層。
- 例外只在使用者針對**特定 mod** 另外指定時。這是偏好不是禁令，別放大成
  「中文化都不用做」——中文化本身仍然要做（見 [[dont-inflate-light-preferences]]）。

**2026-08-27 再放寬**：使用者原話「繁中簡中我都可以，各類漢化派別我也接受混用，隨意一點，
反正都是中文」。所以**不同 mod 用不同漢化派別（重光、清泉、各家民間層）混在同一個整合包裡是可接受的**，
不必為了統一派別而卡住某個 mod，也不必因為「基底漢化沒裝」就整個放棄某層。
判斷順序仍是 [[translation-layer-cost-threshold]]（該條 2026-08-30 已改成「看是不是遊戲內容」）——
但「派別不一致」**不再是**不做的理由。

**2026-08-30 擴到基底本身**：我提醒他「換和光 `139134` 等於**整個原版文本從繁體變簡體**，
加上我們自己 39 個繁中層，畫面會繁簡混雜」，他答「**簡體完全 OK**」。

所以這條偏好**涵蓋原版文本本身**，不只是個別 mod 層——**基底可以是簡中**。
以後不必再為「基底要不要保持繁體」停下來問。**唯一仍是硬 gate 的是缺字破版**
（方塊字、豆腐字、mojibake），見 [[chinese-diff-ok-but-no-tofu]]。

2026-10-23 補：簡中翻譯常綁定全域術語庫（如重光-湯鑊 `76474`、和光 `139134`、WOK Studios `10845`），彼此不通用；挑層時除了多查一輪有沒有不綁基底的 CHT 選項，也要確認新層基底跟整合包內其他層是否一致（`agentctl/handoffs/done/2026-08-28/opus-zh-summary/SUMMARY.md:736-738`）。

2026-10-23 補：少數情況仍需簡繁轉換時，opencc s2twp 會誤改音譯人名/地名裡剛好用到簡轉繁規則字的字（里→裡、托→託、重装→重灌，如「亨裡克」「阿卡託什」），同樣的字在一般詞彙裡轉換是對的；要先建反例清單才能用，不能無差別套規則（`agentctl/handoffs/done/2026-09/home-2026-09-03/zhmake/REPORT.md:107`）。

## chinese-diff-ok-but-no-tofu

> 中文層可以名詞不一致、繁簡混雜，但絕不可出現方塊字或缺字——差異可接受，壞掉不行（原 type: memory）

2026-08-29 裁示換中文基底（現役繁中 `Skyrim Traditional Chinese 8.20` → 和光 `139134` 簡中整包）時，
被告知 78 件現役中文層有 54 件會有名詞／字形衝突，回答是「**有差異也沒關係**」；
但隨即補一句「**字型要有，不能有方塊這種**」。

**Why:** 這兩句畫出的界線是「可讀但不一致」vs「不可讀」。名詞譯法不統一只是讀起來不順，
功能完好；缺字顯示成方塊是壞掉。把兩者一起歸進「差異」會做出錯誤的省事決定。

**How to apply:** 中文層相關的取捨，名詞體系不一致、繁簡混用一律不必為此加工；
但字型字集涵蓋、缺字、破版是硬 gate，必須有答案才能動工。
這條細化了 [[no-cht-chs-preference]] 的邊界，也跟 [[translation-layer-cost-threshold]] 一致
（差異不值得花成本，壞掉一定要修）。

## slanguage-english-chinese-in-english-slot

> 本包 skyrim.ini 是 sLanguage=ENGLISH，中文全塞在 *_English.STRINGS / *_english.txt 槽；只附 _chinese 檔的中文層會靜默失效（原 type: memory）

2026-08-27 opus-zh-active 稽核發現：`instance/profiles/modpack-main/skyrim.ini` 是 `sLanguage=ENGLISH`，
`Skyrim Traditional Chinese 8.20 Core and Fonts` 把 `*_Chinese.*` 與 `*_English.*` 兩份 STRINGS
都做成繁中內容。所以本包的硬規則：**引擎只讀 English 槽**——MCM 翻譯必須是 `*_english.txt`、
外部字串必須是 `*_English.STRINGS`；只給 `_chinese` 的層裝了看起來沒錯、實機全英文、零報錯。

**How to apply**：
- 評估中文層時先看實體型態：純 ESP 替換層與 sLanguage 無關（排本體下面即可）；
  translations txt 型要確認有 `_english.txt`（或改名）；DSD 型本機沒裝 DSD 不能用。
- 已知踩雷：Missives Settings Loader 只給 `Missives_chinese.txt`（改名即生效）。
- Modex 走自有 JSON 語言系統，要在 Modex 設定裡切語言，光裝中文層不生效。
- 「要不要改 sLanguage」是全域決定，使用者未裁示，不要順手改。

相關：[[no-cht-chs-preference]]、[[translation-layer-cost-threshold]]

2026-10-23 補：CC 官方簡中字串層初版用小寫 `strings/` 資料夾名——MO2 的 wine VFS 對路徑大小寫不敏感，但遊戲引擎讀 `Strings` 子目錄本身在 Proton 下對大小寫敏感，錯了會靜默失效；命名要逐字元比對現役已驗證生效的同類層（`agentctl/handoffs/done/2026-09/home-2026-09-03/cc/REPORT.md:47`）。

## zhport-whitelist-gap-before-1009

> 2026-10-09 前 zhport 白名單漏 INFO.RNAM／QUST.CNAM／QUST.NNAM／NPC_.SHRT，用它以本體重建的中文層這四類會退回英文

2026-10-09 vf3-zhfix 線（mod-library `357bf71`）發現並修好：zhport 原本不搬玩家對話選項（`INFO.RNAM`）、任務日誌（`QUST.CNAM`）、任務目標（`QUST.NNAM`）、NPC 短名（`NPC_.SHRT`），光 KWF 一層就 160+ 欄退回英文。同次加了 `--override`。

**Why:** 10-09 之前用 zhport 以新版本體重建過的中文層可能都有這個靜默退化。10-09 清查（agentctl `vf-text3/DONE-zhport-audit.md`）：178 層中 148 層 zhport 製，真退化 4 層 76 筆已修補部署；6 層種子中文包已刪無法判定（BLOCKED，要重下載）；另有 74 支 esp 2,791 欄是自譯時從沒翻過（非退化）。後兩項待使用者裁示。注意 09-11／09-12 的 zhport 層只存在 MO2 `mods/`，沒回寫 mod-library。

**How to apply:** 有人回報「中文層某些選項／日誌是英文」先懷疑這條；清查要使用者點頭才開線。相關：[[zhport-editorid-fallback-and-hdpt-untranslatable]]、[[voiced-follower-makeover-project]]、[[bsa-voice-index-false-negative]]。

2026-10-23 補：白名單遺漏不只 10-09 前那四類，後續重建 Masareria 1.4 時又發現漏了 `REGN.RDMP`（世界地圖區域名）；已補進白名單並加測試斷言（`agentctl/handoffs/done/2026-10/home-2026-10-10/m186441/REPORT.md`）。跑完 zhport 若仍有英文殘留，不要只假設是內部代號不翻，要逐條核對是不是玩家讀得到但白名單漏收的欄位類型。


## prefix-rename-rules-need-longest-first-ordering

> 批次改名規則若有前綴包含關係，短規則排在長規則前面會搶先命中、吃掉本該給長規則的字串

2026-08-27 cx-convert 把 `mco_*` 檔名轉 BFCO 命名時，短規則（`mco_powerattack`）排在長規則（`mco_powerattackloop`）前面會被短規則提前命中吃掉，產生錯誤改名；正式實作把三條長規則排到短規則前才修正，負向對照測試證實順序真的會咬到（`agentctl/handoffs/done/2026-08-27/cx-convert/RESULTS.md:11`）。

**Why:** 規則表的比對順序不會因為「語意上更精確」自動優先，程式只認第一個命中的規則。

**How to apply:** 寫批次改名/替換規則表時，只要規則之間存在字首包含關係，一律把較長（較精確）的規則排在前面；測試 fixture 要刻意把短規則排前做負向對照，證明順序真的會咬到而不是空焗試。

## non-localized-esp-overwrites-localized-vanilla-string

> non-localized 插件覆寫 vanilla localized 記錄時會把內嵌英文字串整個蓋掉中文，CELL/NPC 任何「為了改別的欄位整筆 forward」的記錄都會連帶英文化

2026-08-28～09-01 多線重複踩到同一機制：`Common Clothes and Armors` 覆蓋 24 筆 vanilla ARMO 把中文名變英文（`agentctl/handoffs/done/2026-08-27/opus-qa-triage/REPORT.md:279`）；換臉 mod `KuroneYsoldaReplacer.esp` 把 NPC 名字寫死英文字面繞過字串表（`agentctl/handoffs/done/2026-09/home-2026-09-11/misc/REPORT.md:42-47`）；hcell 全機掃描抓到 237 筆 CELL FULL 因為別的欄位（Music/WaterHeight）被順手 forward 而連帶回英文，集中在前五個 winner plugin（`agentctl/handoffs/done/2026-09-01/hcell-2026-09-01/REPORT.md:80-139`）。

**Why:** 問題出在 vanilla localized／覆寫插件 non-localized 的資料層級結構差異，不是排序錯誤，調序救不了，是反覆出現的通用迴歸成因。

**How to apply:** 回報「某物品/NPC/地名變回英文」先查 base record 是不是 vanilla localized、覆寫插件是否 non-localized 或整筆 forward 了別的欄位，修復只在 conflict patch 疊寫 FULL 一欄取回中文；接受「mod 贏過現役」建議前先查現役勝者本身是不是已經中文，避免誤判（`agentctl/handoffs/done/2026-09/home-2026-09-03/go19x/REPORT.md:71`）；決定第三方內容載入序位置前先算這個位置會讓多少欄位中文回退，照代價表選（`agentctl/handoffs/done/2026-09/home-2026-09-03/lrrev/REPORT.md:111`）。相關：[[zh-layer-gate-base-mod-must-be-enabled]]

## zh-layer-exact-match-protocol-topology-not-version-string

> 判斷中文層是否對版，要比對 masters／record 拓撲／FormID 集合是否完全相同，而不是看版本號或 bytes

七步協定在 hmih 八件 mod 稽核落地：身分記錄→分開解壓→二進位拓撲比對（masters/record 計數/FormID set/GRUP 與 subrecord 順序全同才算對齊，硬 gate）→CELL/placement 掃描→asset winner→records/gameplay 接觸面→回滾單位結論（`agentctl/handoffs/done/2026-09-01/hmih-2026-09-01/ANALYSIS-COMMON.md:33-121`；bgdl/ank 兩場次獨立採用同口徑亦判定成功）。版本不嚴格匹配時改用「字串ID集合覆蓋率」量化：100% 覆蓋且非文字欄位不動才可裝（`agentctl/handoffs/done/2026-10/home-2026-10-03/want-watch/rounds/20261003-1410/REPORT.md`）。

**Why:** 版號、header、bytes 都可能騙人——header 版號常落後於頁面最新檔案，唯一可信的是逐欄位拓撲比對。

**How to apply:** 搜中文層要廣搜本體全名＋常見後綴變體（CHS/CHT/zh_CN/譯者自訂名），不要只加 Chinese 關鍵字；選檔比對 Nexus files 分頁的精確 MAIN 版本，不信 header；判定「已有/已完整」前先查實際 load order winner（不要只憑有 CHT 資料夾就假設已中文化），翻譯層幾乎都在 Nexus、中文站只當補充；偵測是否已含中文要用 UTF-8 解碼＋連續漢字門檻＋濾假名；同一 plugin 若有多個兄弟 overlay 要先合併成單一 Combined 層才能裝，覆蓋率統計對每層各自 diff 再聯集，不能只看最上層；分母排除英文原本就空的欄位，BSA-only 字串算不出時要註明是下界。相關：[[zh-layer-gate-base-mod-must-be-enabled]]、[[zhport-editorid-fallback-and-hdpt-untranslatable]]

## zh-carrier-type-determines-deploy-risk

> 中文層的實作方式（純 Strings／整支 esp 替換／MCM txt／BSA 注入／DSD）決定它會不會被本體升版拖垮，體積與檔案型態就是訊號

Frozen Heart 只換 3 支 Strings 檔（ESM localized flag），本體升版腳本/模型/地形不受影響，只需比對字串編號集合；整支 esp 替換型（如 BnB）升版會把新版記錄整個蓋回舊版，須走拓撲 gate（`agentctl/handoffs/done/2026-10/home-2026-10-10/frozenheart-zh/REPORT.md`）。體積是另一訊號：KB 級通常純字串替換，百 MB 級是整包重打包，曾遇 210MB BSA 注入型層整包蓋掉本體資產需獨立驗收（`agentctl/handoffs/done/2026-09/home-2026-09-03/zhnex/REPORT.md:118`；`agentctl/handoffs/done/2026-08-28/opus-zh-summary/SUMMARY.md:730-732`）。DSD 是 runtime 字串替換,不參與 record 衝突、恆勝過 ESP 層且會遮蔽版本漂移（`agentctl/handoffs/done/2026-08-30/zh-2026-08-30/DSD-WINNER-CONTRACT.md:6-60`）；MCM 的 translations txt 只改介面文字，解決不了 ESP record 缺口。

**Why:** 不同載體的升版風險、覆蓋範圍、失效模式完全不同，用同一套 gate 驗收會漏判。

**How to apply:** 部署前先判定載體型態；純 Strings 型比對編號集合即可，整支替換型要走拓撲比對；補丁排在整支替換層之後又帶英文 FULL/DESC 要疊 forward 層把中文聯集加回去；覆蓋層 MO2 優先度用 `--priority before:`，`after:` 是排後面＝更低優先權，容易弄反；自帶 checksum/完整性檢查的 mod（如 OStim）覆寫前先讀原始碼找出被鎖定檔名，改完重算 checksum 附上；框架用「目錄列舉＋先讀先贏」載入翻譯檔的，只能同名覆蓋不能靠加新檔案。相關：[[slanguage-english-chinese-in-english-slot]]

2026-10-23 補（E2bs-07）：現成中文包版本落後本體時（Chatty NPCs 1.51 vs 1.6.1 少 4~5 條 QUST 條件、FLST 少 LNAM、少整筆 KYWD），直接拿中文包 esp 出貨等於把 mod 降級；一律改以本體 esp 當載體、用 zhport 類工具只搬中文字串，記錄結構一個位元不動，讓完整性由「結構沒改過」保證而不靠版本號（`agentctl/handoffs/done/2026-09/home-2026-09-11/zh/REPORT.md:46-49`）。

## zh-static-scan-misses-runtime-and-script-strings

> 靜態掃描 ESP record 不是可靠的完整度訊號——運行期注入、pex 內嵌通知、FOMOD toml 顯示字串都在它看不到的地方，而且空殼層能同時通過結構與完成度兩個 gate

Guard Dialogue Overhaul 的對話在 esp 靜態掃描看起來還有上百句英文，實際遊戲內由 DSD 注入覆蓋 97.75% 中文，2 份獨立記錄重複確認（`agentctl/handoffs/done/2026-09/home-2026-09-12/zhfix2/REPORT.md:119`）；反過來，Trade Routes 簡中層本體 32 個 .pex 只出 2 個，出的 2 個裡區域名稱與通知字串仍是英文硬編（`agentctl/handoffs/done/2026-08-27/opus-qa-triage/REPORT.md:199`）；Artisans of Skyrim 的附魔/藥水名稱寫在 FOMOD 產生的 preset toml 裡，DLL 直接讀 toml 顯示，不在 esp 裡（`agentctl/handoffs/done/2026-10/home-2026-10-10/artisans-guard/REPORT.md`）。另一面，一個 ESP 與 carrier 位元組完全相同的空殼層能同時通過結構 Gate A（判等）與完成度 Gate B（讀 ledger 不讀最終 esp）（`agentctl/handoffs/done/2026-09/home-2026-09-03/zhmake/REPORT.md:105`）；翻譯層建置引擎遇資料不符時有的靜默略過（continue）有的直接中止（SystemExit），選錯引擎拿到的失敗語意完全不同（`mod-library/l10n/tools/README.md:45-47,54-59`）。

**Why:** 「esp 沒有英文」「建置沒報錯」都不等於「玩家看到的是中文」，完整度要從多個通道實測才算數；診斷 MCM 問題時也不能只信中文標籤字面，可能譯得像另一個開關，要對照 DLL 實際變數名。

**How to apply:** 盤點覆蓋率把「運行期注入」「pex 通知字串」「ini/toml 設定檔字串」各自列一類分開查；gate 加 sha256(層esp)≠sha256(carrier) 硬檢查，完成度一律從最終產物實測不信 ledger；選建置引擎前先確認它遇不符資料是靜默跳過還是中止。相關：[[bsa-voice-index-false-negative]]

## zh-qa-checker-token-and-variant-false-positives

> 自動化翻譯 QA 檢查器（控制標記守恆／簡繁異體字偵測）本身會有系統性假陽性，命中清單要配例外表才能用

builder 安全 gate 會因控制標記不一致（來源缺 `<10>`、`<Alias=Item>` 大小寫寫成 `<Alias=item>`、尾端換行沒保留）整條跳過詞條，看起來像「沒對上」其實不是版本或 FormID 錯位（`agentctl/handoffs/done/2026-08-31/zh2-2026-08-31/REPORT.md:37-56`）；簡繁判別工具會把「秘/祕」「斗篷/鬥篷」這類正簡同形或異體字誤判成錯字（`agentctl/handoffs/done/2026-09-01/hperk-2026-09-01/REPORT.md`）；中文沒有空白分隔，用 `%[^%\s]+%` 查 token 守恆會把「50% more damage」裡兩個字面 `%` 誤判成佔位符。

**Why:** 這些是工具本身的邊界案例，不是翻譯真的錯，照單全收會逼出錯誤修正方向。

**How to apply:** 詞條「沒對上」先查 builder gate 日誌，核對控制標記大小寫/特殊符號/尾端換行是否一致；簡繁偵測前先核對命中是否落在已知異體字例外表；token 守恆檢查只用 `<…>`／`$Token`／`\n`／`{…}` 四類明確清單比對，不用泛用正則配空白邊界。

## official-chinese-name-is-community-convention

> Skyrim 沒有官方中文版，所謂「官方譯名」只是社群慣例；判準要看現役語料實際出現頻率，不是任何人的記憶

領導憑印象宣稱「官方中文是風盔城」要求全隊照辦，實際現役語料數出來是風舵城 944 次 vs 風盔城 27 次，已讓合併線做了 149 筆「正規化」，一大半還改到了授權範圍外、別人既有翻譯層的譯文，必須全部回滾（`agentctl/handoffs/done/2026-09/home-2026-09-03/zhmake/REPORT.md:122`）。自製翻譯層觸及官方 ESM 記錄的授權欄位中 913/1,592 筆譯法與現役原版中文不同（如「貝萊托爾雜貨店」vs「雜貨鋪」），須用 (master,FormID,tag) 精確比對官方 ESM 既有中文（`agentctl/handoffs/done/2026-09/home-2026-09-03/zhmake/REPORT.md:118`）；補譯地名時遊戲自己的 `*_English.STRINGS` 是唯一權威來源，憑印象寫譯名常跟整合包現有譯名對不上（`agentctl/handoffs/done/2026-08-28/opus-zh-summary/SUMMARY.md:591-594`）。

**Why:** 「標準譯名」的真正定義是整合包現役語料的既成事實，不是權威來源或個人記憶。

**How to apply:** 遇到「某名詞標準譯名是什麼」一律去現役語料數出現頻率判斷；自製翻譯層觸及 vanilla 記錄前先查對應 `*_English.STRINGS` 或現役原版中文翻譯，沿用既有譯法；任何「正規化譯名」指令波及別人既有翻譯層前先確認授權範圍。
