# 動畫取證：clip、替換與握持契約

[動畫與 OAR 教訓](../animation-oar.md)｜[lessons 索引](../README.md)

## static-winner-is-not-active-clip

> 靜態 winner 只給候選；症狀在同裝備條件下改變時，要分開比較實播 clip、replacement 與動作段。

2026-11-02：OAR 記錄可同時存 animation name、clip、project、mod／submod 與替換路徑（[AnimationLog.cpp:10–85](https://github.com/ersh1/OpenAnimationReplacer/blob/f4e7688b065175aff70aa523073857911e15aca3/src/AnimationLog.cpp#L10)，釘版 source，未比對不能宣稱與已裝 DLL 一致）。同靜態條件仍可能走不同 graph 分支或動作段；缺格、預測 winner、外觀印象都不能單獨證明壞→好的原因；日誌沒開的時間窗不能從初始化清單還原真 clip。

**How to apply:** 問題／正常樣本分開比：clip 改變→graph 分支候選；clip 相同、replacement 不同→選取候選；兩者相同→看動作段與連段序號，不能再叫選招失效。讀 graph 變數要確認存在性與型別，回傳零不提供這兩項證據。放寬武器／盾條件前另驗原動畫 handedness：雙手或雙持設計的 clip 即使條件能命中持盾角色，也可能錯握盾手或揮不存在的第二把武器；沒有 block／bash 檔不等於適盾。

OAR/DAR 條件都正常卻外觀異常（如雙持握持）時，比對實際生效 hkx 跟原版同名檔的骨骼動畫差異，尤其疊加層：「同名但骨骼改動範圍不同」的 hkx 可能動到左手武器節點（`agentctl/handoffs/done/2026-10/home-2026-10-03/revgrip/REPORT-log.md`）。禁用主控台時，可用 AnimationMotionRevolution.log 的微秒時間戳量「clip 標註時間／實測間隔」反推播放倍率，配不受嫌疑影響的對照組（如 NPC）判全域或局部（`agentctl/handoffs/done/2026-10/home-2026-10-07/meleeslow/REPORT-skse.md`）。

方法來源（已刪）：`agentctl/handoffs/home-2026-11-01/block-recovery/REPORT.md`、`STANCES.md`、`QA.md`。
