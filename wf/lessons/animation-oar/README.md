# 動畫取證：clip、替換與握持契約

[動畫與 OAR 教訓](../animation-oar.md)｜[lessons 索引](../README.md)

## static-winner-is-not-active-clip

> 靜態 winner 只給候選；症狀在同裝備條件下改變時，要分開比較實播 clip、replacement 與動作段。

2026-11-02 整理：OAR 的記錄能同時保存 animation name、clip、project、mod／submod 與替換路徑，見 [AnimationLog.cpp:10–85](https://github.com/ersh1/OpenAnimationReplacer/blob/f4e7688b065175aff70aa523073857911e15aca3/src/AnimationLog.cpp#L10)。這是釘版 source 的能力，不能未比對來源就宣稱任意已安裝 DLL 完全一致。

**Why:** 相同靜態條件仍可能走不同 graph 分支或動作段；資料夾缺格、預測 winner 或外觀印象，都不能單獨證明某次壞→好轉換的原因。日誌未啟用的時間窗也不能事後從初始化清單還原真 clip。

**How to apply:** 同條件問題／正常樣本分開比：clip 改變指向 graph 分支候選；clip 相同、replacement 不同指向選取候選；兩者相同則要另看動作段與連段序號，不能繼續叫作選招失效。讀 graph 變數還要確認存在性與型別；回傳零本身不提供這兩項證據，也不代表出錯時的值。

放寬武器／盾條件前，另驗原動畫的 handedness。原為雙手武器或雙持設計的 clip，即使條件模擬能命中持盾角色，也可能錯握盾手或揮不存在的第二把武器；沒有 block／bash 檔不等於它天然適盾。

方法來源：格擋調查 REPORT（已刪：`agentctl/handoffs/home-2026-11-01/block-recovery/REPORT.md`）、STANCES（已刪：`agentctl/handoffs/home-2026-11-01/block-recovery/STANCES.md`）、QA 邊界（已刪：`agentctl/handoffs/home-2026-11-01/block-recovery/QA.md`）。這些保留原始案例證據；本頁不改其未定因、候選凍結、觀察未執行的狀態，也不啟動新 runtime 工作。
