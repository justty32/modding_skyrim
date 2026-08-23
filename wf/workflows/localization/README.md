# localization — 做一個中文層

專案裡做過最多次的事：34 個自製繁中層、11 支逐 mod 的建置工具。這條流水線的每一段都出過事。

```text
Done when: <同版閘門通過、層內確有中文、排序在本體之上、audit 綠、真人抽查已排入 WAIT_USER>
```

## 先決定要不要做

**成本規則**：難做就維持英文，順手能做就做。
見 [`modpack-design/sources/translation-layer-cost-policy.md`](../../../modpack-design/sources/translation-layer-cost-policy.md)。
**這是成本判斷，不是類別禁令**——不要因為某類 mod 難做就一律不做。

**繁簡都可接受。** 要的是有中文，不是正體。**有同版簡中就直接裝，不要開 CHS→CHT 轉換層。**

## 1. 找同版來源

見 [nexus-intake 的版本閘門](../nexus-intake/README.md#2-版本閘門)。
**API 的 `version` 欄位不是同版證明，二進位拓撲比對才是。** 沒有同版就停手。

## 2. 建層

工具在 [`mod-library/l10n/tools/`](../../../mod-library/l10n/tools/)：

| 工具 | 用途 |
|---|---|
| `inline_translation_overlay.py` | 行內覆蓋層產生器（核心） |
| `build_*_cht_layer.py` | 逐 mod 的建置腳本，各自 fail-closed |
| `match_translations.py` | 翻譯比對 |
| `project_adamant_translation.py` | 把既有譯文投射到新版 |

**fail closed**：筆數、record topology 與所有非目標 payload 都要鎖死。
VIGILANT `BOOK.DESC` 的例子是 45 筆一個不多一個不少，比數不對就中止。

## 2.5 補全既有中文層

**最常見的情況不是「沒有中文層」，而是「有，但不完整」。** 三種型態，處理方式不同：

| 型態 | 例子 | 做法 |
|---|---|---|
| 官方層漏了某批欄位 | VIGILANT 1.8.1／1.8.2 的正體包都原樣留下同一批 45 個召喚書／石之碎片的 `BOOK.DESC` 英文行 | 用**同一筆記錄既有的中文專名**當術語來源，只補那批欄位。`build_vigilant_book_desc_overlay.py` 是 exact-version、45-record fail-closed 的產生器 |
| 本體升版，舊層還停在舊版 | Adamant 從 5.9.2 升上去，舊層譯文還在 | `project_adamant_translation.py`：把既有譯文**投射**到新版結構，未命中的留英文並列出清單，不要自動猜 |
| 層存在但目標欄位根本沒翻 | Biggie Traits 層裝好、排序也對，但 trait 名稱 CJK 計數是 0 | `build_biggie_traits_cht_completion.py` 這類逐 mod 補全腳本，把缺的欄位補上 |

**補全的鐵律：**

- **只補目標欄位，其他 payload 一個 byte 都不能動。** 筆數對不上就中止，不要「盡量補」。
- **術語從同一個 mod 的既有中文取**，不要另外造詞——同一個專名在書名與描述裡必須一致。
- 產出要有**逐筆 ledger**，說明每一筆補了什麼、來源是哪一筆。
- 補完照樣要過第 3 步的 CJK 驗證與第 5 步的排序稽核。

## 3. 驗證層內真的有中文

**這一步不能用直覺寫。** 正確做法是**每種編碼都試、取最大值**：

```python
for enc in ('utf-8', 'utf-16-le', 'cp936', 'big5'):
    best = max(best, len(CJK.findall(b.decode(enc, errors='ignore'))))
```

**兩個踩過的坑**：

- `strings -a --encoding=s` 是單位元組的，對所有 AYOP 的 ESP 都回 0。
- `b.decode('utf-8', errors='ignore')` **永遠不會拋錯**，所以「依序試多種編碼、成功就 break」
  的迴圈第一輪就結束，根本沒試過 cp936——這讓 20 個層被誤報成「零中文」。
  四種編碼都試之後，68 個層**全部含中文**。

也要驗**目標欄位**真的被翻到。Biggie Traits 曾經層裝好了、排序也對，但 trait 名稱的
CJK 計數是 0——層本身是空的。

## 4. 排序

**`modlist.txt` 頂端 = 最高優先權。覆蓋層必須在本體之上。**
權威依據是 `projects/houseCARL/src/housecarl-core/Mo2LoadOrder.cs`。

```sh
mo2ctl install <archive> --priority "before:<本體 mod 名>"
```

裝在下面**完全失效而且沒有任何徵兆**：檔案在磁碟上、mod 也啟用著，英文原版照樣贏走每個衝突檔案。

## 5. 稽核

```sh
python3 mod-library/l10n/tools/audit_layer_priority.py
```

逐檔案路徑判勝出者。2026-08-23 用它抓出 4 個失效層、11 個被英文本體贏走的檔案。

## 6. 真人抽查

靜態全過**不等於**畫面上是對的。方框、mojibake、截斷、空白只有人眼看得出來。
把抽查項記到 [WAIT_USER.md](../../../WAIT_USER.md)，寫清楚要去哪裡、看哪幾個畫面。

## 產物落點

成品進 [`mod-library/l10n/mods/`](../../../mod-library/l10n/mods/)，附 `SOURCE.md`、
`MANIFEST.sha256`、`VERIFICATION.md`。

> **`mod-library` 必須永遠 private**：這些層**內含他人 mod 的完整原始 ESP 複本**
> （USSEP 那個是 20MB 的完整 plugin，不是差分），只能自用，不能公開散布。

## 何時不用

- 本體本身就有官方中文 → 直接裝，不要自己做層。
- 只是要查某 mod 有沒有中文層 → 走 [investigation](../investigation/README.md)。
- 已經有同版簡中 → 裝簡中，不要為了正體再做一層。
