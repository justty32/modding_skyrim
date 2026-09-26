# 翻譯與中文層（1/2）

[lessons 索引](README.md)｜同主題：[translation-and-zh-2](translation-and-zh-2.md)

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
