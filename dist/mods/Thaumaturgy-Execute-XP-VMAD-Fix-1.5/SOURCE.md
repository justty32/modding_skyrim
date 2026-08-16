# 來源與診斷

- 上游：[Thaumaturgy - An Enchanting Overhaul](https://www.nexusmods.com/skyrimspecialedition/mods/57138)
- 目標版本：1.5，Nexus file id `787801`。
- 目標記錄：`2EDE92:Thaumaturgy.esp`（`MAG_EnchExecuteDamageFFContact`）。

houseCARL 的 script-property gate 發現該記錄只綁定 `XP = 0.02`，卻沒有綁定腳本宣告的
`actor Property PlayerRef Auto`。官方 BSA 內的 `MAG_EnchantmentXP_Script.pex` 經原生 BSA
單檔讀取與 Papyrus 反編譯後，唯一事件為：

```papyrus
Event OnEffectStart(actor akTarget, actor akCaster)
    if akCaster == PlayerRef
        game.AdvanceSkill("Enchanting", XP)
    endif
EndEvent
```

未綁定時 `PlayerRef` 為 `None`，玩家命中不可能通過條件，因此這條官方 XP 路徑會靜默 no-op。
同一上游 plugin 的其他 `MAG_EnchantmentXP_Script` attachment 會把 `PlayerRef` 綁到
`000014:Skyrim.esm`。

`tools/source-ModpackKR_Thaumaturgy_ExecuteXP_VMADFixDev-unlocalized.esp` 由 houseCARL 新增一個
`ScriptObjectProperty`，內容為 `PlayerRef -> 000014:Skyrim.esm`；為避免上游 localized string
被 patch writer 內聯成亂碼，另把同記錄的 `FULL`／`DNAM` 精確正規化回 1.5 英文原句，再由
可重現的本地化流程生成正體中文 string tables。來源 patch SHA-256：
`5646e407ea3808ccd8e78678147f31e62c488f443ac4b46941fc2a65d5e46437`。
