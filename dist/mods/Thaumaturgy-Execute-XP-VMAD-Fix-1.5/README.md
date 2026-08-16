# Thaumaturgy 1.5 Execute XP VMAD 修正

這是 `Thaumaturgy - An Enchanting Overhaul` 1.5 的單記錄修補：為
`MAG_EnchExecuteDamageFFContact` 的 `MAG_EnchantmentXP_Script` 補上缺失的 `PlayerRef`，
使處決附魔命中時能按官方腳本設計增加附魔經驗。

產物是 localized plugin，內含正體中文名稱與說明。重建與驗證：

```bash
python tools/build_translation.py \
  --source tools/source-ModpackKR_Thaumaturgy_ExecuteXP_VMADFixDev-unlocalized.esp
python tools/verify_translation.py \
  --source tools/source-ModpackKR_Thaumaturgy_ExecuteXP_VMADFixDev-unlocalized.esp
```
