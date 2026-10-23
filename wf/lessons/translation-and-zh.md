# 翻譯與中文層

[lessons 索引](README.md)

## zh-layer-gate-base-mod-must-be-enabled

> 中文層部署前要查本體 mod 在 modlist 是否啟用，不能只看 plugins.txt；Apocalypse 案例讓 242 個 Cannot open store 躺了三天（原 type: memory）

2026-09-03 post2 隊發現：Papyrus 323 個 `Cannot open store for class` 有 242 個來自 `Apocalypse - Magic of Skyrim.esp`——本體 `Apocalypse 10.2.3`（含 scripts BSA）早在 profiles 入版控（08-23）前就已停用（連 Ordinator／Vokriinator patch 一起，是刻意退役），但 08-31 22:45 的中文層部署把 `MAG-Apocalypse-Magic-of-Skyrim-CHS-MCM-7934` 啟用並在 plugins.txt 勾了同名 esp。`zh-gap-winners.csv` 把它標成 `ACTIVE-PARTIAL`，因為那張表只看 plugin 是否啟用，沒看本體 mod。

**Why:** 中文層只帶 esp（＋少量 MCM 腳本），本體 BSA 沒載入時 esp 的 VMAD 引用全部落空；`Cannot open store` 存量 318 從 lrinst 之前就在，四隊的「新增 0」驗收都沒發現存量本身就是病。
**How to apply:** 中文層／覆蓋層的部署 gate 要加一條「本體 mod 在 `modlist.txt` 是 `+`」，本體停用就不部署、也不勾 esp；`Cannot open store` 的存量要按 class 歸因到來源 mod（`post2/data/cannot-open-store-by-mod.csv` 的做法：掃 BSA 名稱表＋plugin 位元組搜尋），別只比新增數。zhmake 124 層裡也有 Apocalypse 簡中層，部署前先裁本體去留。相關：[[missing-master-scan-mast-not-housecarl]]、[[slanguage-english-chinese-in-english-slot]]。

## zhport-editorid-fallback-and-hdpt-untranslatable

> 中文層對種子時 FormID 對不上（作者改版重編）要改用 EditorID 比對；HDPT 頭部件 EDID／名稱絕不翻譯（原 type: project）

2026-09-12 want4 批（lead-want4）：`zhport.py` 用 FormID 對舊中文包種子，遇到作者改版整批重編 FormID 時 gaps 被嚴重高估（Runic Arts 少算 170 欄、Sacrifices 605/706）；改用 EditorID 比對就救回。另外 13 個 HDPT 頭部件代號留英文是對的：翻下去 facegen 對名失敗會整顆作廢（見 [[hdpt-edid-must-match-facegen-shape-names]]）。

**Why:** gaps 異常大時工人會急著整包重翻，白花翻譯量又降低一致性。

**How to apply:** 中文層任務 gate 前先看 gaps 比例，>50% 先換 EditorID 比對再決定翻不翻；翻譯範圍排除 HDPT／FLST／種族內部代號，只翻玩家讀得到的欄。
相關：[[translation-layer-cost-threshold]]、[[chinese-diff-ok-but-no-tofu]]

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

## zhport-whitelist-gap-before-1009

> 2026-10-09 前 zhport 白名單漏 INFO.RNAM／QUST.CNAM／QUST.NNAM／NPC_.SHRT，用它以本體重建的中文層這四類會退回英文

2026-10-09 vf3-zhfix 線（mod-library `357bf71`）發現並修好：zhport 原本不搬玩家對話選項（`INFO.RNAM`）、任務日誌（`QUST.CNAM`）、任務目標（`QUST.NNAM`）、NPC 短名（`NPC_.SHRT`），光 KWF 一層就 160+ 欄退回英文。同次加了 `--override`。

**Why:** 10-09 之前用 zhport 以新版本體重建過的中文層可能都有這個靜默退化。10-09 清查（agentctl `vf-text3/DONE-zhport-audit.md`）：178 層中 148 層 zhport 製，真退化 4 層 76 筆已修補部署；6 層種子中文包已刪無法判定（BLOCKED，要重下載）；另有 74 支 esp 2,791 欄是自譯時從沒翻過（非退化）。後兩項待使用者裁示。注意 09-11／09-12 的 zhport 層只存在 MO2 `mods/`，沒回寫 mod-library。

**How to apply:** 有人回報「中文層某些選項／日誌是英文」先懷疑這條；清查要使用者點頭才開線。相關：[[zhport-editorid-fallback-and-hdpt-untranslatable]]、[[voiced-follower-makeover-project]]、[[bsa-voice-index-false-negative]]。
