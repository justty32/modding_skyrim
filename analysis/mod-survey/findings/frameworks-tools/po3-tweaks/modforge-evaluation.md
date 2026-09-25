# 三、對 ModForge 的參考價值

← [原文入口](../po3-tweaks.md)

## 三、對 ModForge 的參考價值

**定位**：純前置 + 行為環境標記。ModForge 不生成 po3_Tweaks 的任何 record（它沒有 esp record）。

### 直接影響 ModForge 生成物的 tweak

<!-- wf-nav -->
1. **`CombatToNormal Dialogue Fix`（Fixes）**  
   - 修引擎 bug：NPC 戰鬥結束回 normal 狀態時誤用 LostToNormal 分支。  
   - **影響**：ModForge 生成的 NPC dialogue 若有 CombatToNormal topic，只有在 po3's Tweaks 安裝後才能正確觸發。若不假設安裝，需用額外的 LostToNormal INFO 做 fallback，或將 CombatToNormal 設計成和 LostToNormal 相同（最保險）。

2. **`Use Furniture In Combat`（Fixes）**  
   - **影響**：ModForge SceneSpec 若設計 NPC 戰鬥中坐椅/使用家具，此 tweak 決定能否成立。不安裝時家具 action 在戰鬥中會失效。

3. **`Cast Added Spells on Load`（Fixes）**  
   - **影響**：ModForge 若為 NPC 生成永久 ability SPEL（例如特殊被動）並用 AddSpell 添加，此修正確保存檔載入後效果不丟失。不安裝時可能需要在 OnInit/OnPlayerLoadGame 重新 AddSpell。

4. **`IsFurnitureAnimType Fix`（Fixes）**  
   - **影響**：ModForge 生成的 dialogue/condition 若用 IsFurnitureAnimType，需此 fix 才能在家具 reference 上正確求值。

5. **`No Conjuration Spell Absorb` / `No Hostile Spell Absorb`（Fixes/Tweaks）**  
   - **影響**：ModForge 生成召喚或 buff 法術時，若有安裝 po3's Tweaks 則不需手動設 NoAbsorb flag（自動補上）；若沒安裝則需在 SPEL record 手動指定。

6. **`Offensive Spell AI`（Tweaks）**  
   - **影響**：ModForge 生成的 NPC 若裝備攻擊法術 AI package，此 tweak 決定 NPC 是否預先驗證法術條件。可讓法術 AI 行為更符合設計意圖。

7. **`Clean Orphaned ActiveEffects`（Experimental）**  
   - **影響**：ModForge 更新 NPC perk/ability 後，若舊的 active effect 未清理，此 tweak 自動清除。對 ModForge 的版本迭代 mod 有用。

8. **`Update GameHour Timers`（Experimental）**  
   - **影響**：若 ModForge 生成的 Quest/Script 依賴 GameHour 推進做計時觸發，需此 tweak 確保 timer 同步更新。

### Papyrus API

```papyrus
; 任何 psc 可查詢某 tweak 是否啟用
bool bFix = po3_Tweaks.IsTweakInstalled("CombatToNormal Dialogue Fix")
```

可用於 ModForge 生成的 script 做條件分支（有 po3 時用 A 路徑，沒有時用 B 路徑）。

### 結論

- **ModForge 立場**：po3's Tweaks 是「建議安裝前置」層級，不是必須。ModForge spec 可加一個 `optional_dependencies` 欄位說明「若安裝 po3's Tweaks，下列 tweak 會改善行為」。
- **生成物設計原則**：不應以 po3's Tweaks 存在為假設前提；若依賴某 fix，應在 spec 文件備注「需要 po3's Tweaks」。
- **立即可用的 API**：`IsTweakInstalled()` 可在 generated script 裡做 graceful fallback。

> ⚠️ 以上「ModForge 缺什麼」欄位為推斷，未查 ModForge src/，可能有誤判。
