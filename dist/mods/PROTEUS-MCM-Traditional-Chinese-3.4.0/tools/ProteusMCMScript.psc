ScriptName ProteusMCMScript extends SKI_ConfigBase

int castK5
int spawnSpellsLoadOID
int castK8
int castK11
int backupAppearanceSaveOID
bool presetGameStartOnVal
int castK10
int alternativeDeathSystemOID
int castK2
int castK12
bool alternativeDeathSystemVal
int castK1
int castK7
bool spawnPerksOnVal
bool spawnSpellsOnVal
bool backupAppearanceSaveVal
int castK6
bool explosionsOnVal
int presetGameStartOID
bool disableVal
int castK3
int spawnPerksLoadOID
int castK13
int disableOID
int explosionsOnOID
int castK9
int castK14

globalvariable Property ZZEnableSpawnPerkLoad Auto

globalvariable Property disableHotkeys Auto

globalvariable Property k7 Auto

globalvariable Property ZZBackupAppearanceSave Auto

globalvariable Property k11 Auto

globalvariable Property explosionsOn Auto

globalvariable Property k13 Auto

quest Property ZZProteusRecurringQuest Auto

globalvariable Property k5 Auto

globalvariable Property k2 Auto

globalvariable Property k14 Auto

globalvariable Property k6 Auto

globalvariable Property k10 Auto

globalvariable Property ZZEnableSpawnSpellLoad Auto

globalvariable Property ZZLoadPlayerPreset Auto

globalvariable Property k12 Auto

globalvariable Property ZZAlternativeDeathSystem Auto

globalvariable Property k8 Auto

globalvariable Property k3 Auto

globalvariable Property k9 Auto

globalvariable Property k1 Auto

Event OnConfigOpen()
    ; Pages is a saved Papyrus property. Existing saves can retain the original
    ; English values even when the plugin VMAD changes, so refresh it every time
    ; the MCM opens before SkyUI reads the page-name array.
    Pages = new String[2]
    Pages[0] = "$PROTEUS_MCM_PageGeneral"
    Pages[1] = "$PROTEUS_MCM_PageHotkeys"
EndEvent

Event OnPageReset(string page)
    if page == "$PROTEUS_MCM_PageGeneral"
        SetCursorFillMode(Self.TOP_TO_BOTTOM)
        AddHeaderOption("$PROTEUS_MCM_HeaderPlayerOptions", 0)
        explosionsOnOID = AddToggleOption("$PROTEUS_MCM_GreenExplosion", explosionsOn.getValue(), 0)
        spawnPerksLoadOID = AddToggleOption("$PROTEUS_MCM_SpawnPerks", ZZEnableSpawnPerkLoad.getValue(), 0)
        spawnSpellsLoadOID = AddToggleOption("$PROTEUS_MCM_SpawnSpells", ZZEnableSpawnSpellLoad.getValue(), 0)
        presetGameStartOID = AddToggleOption("$PROTEUS_MCM_LoadPresetAtStart", ZZLoadPlayerPreset.getValue(), 0)
        backupAppearanceSaveOID = AddToggleOption("$PROTEUS_MCM_RaceMenuBackups", ZZBackupAppearanceSave.getValue(), 0)
        alternativeDeathSystemOID = AddToggleOption("$PROTEUS_MCM_AlternativeDeath", ZZAlternativeDeathSystem.getValue(), 0)
        SetCursorPosition(1)
        AddHeaderOption("$PROTEUS_MCM_HeaderNPCOptions", 0)
    endif
    if page == "$PROTEUS_MCM_PageHotkeys"
        SetCursorFillMode(Self.TOP_TO_BOTTOM)
        AddHeaderOption("$PROTEUS_MCM_HeaderHotkeyOptions", 0)
        disableOID = AddToggleOption("$PROTEUS_MCM_DisableHotkeys", disableHotkeys.getValue(), 0)
        AddHeaderOption("$PROTEUS_MCM_HeaderPlayerHotkeys", 0)
        castK9 = AddKeyMapOption("$PROTEUS_MCM_PlayerMenu", (k9.getValue() as int), 0)
        castK1 = AddKeyMapOption("$PROTEUS_MCM_SaveCharacter", (k1.getValue() as int), 0)
        castK3 = AddKeyMapOption("$PROTEUS_MCM_SwitchCharacter", (k3.getValue() as int), 0)
        castK6 = AddKeyMapOption("$PROTEUS_MCM_SummonCharacter", (k6.getValue() as int), 0)
        castK7 = AddKeyMapOption("$PROTEUS_MCM_LoadAppearance", (k7.getValue() as int), 0)
        castK10 = AddKeyMapOption("$PROTEUS_MCM_LoadAppearanceItems", (k10.getValue() as int), 0)
        castK11 = AddKeyMapOption("$PROTEUS_MCM_PlayerCheatMenu", (k11.getValue() as int), 0)
        AddHeaderOption("$PROTEUS_MCM_HeaderNPCHotkeys", 0)
        castK8 = AddKeyMapOption("$PROTEUS_MCM_NPCMenu", (k8.getValue() as int), 0)
        castK5 = AddKeyMapOption("$PROTEUS_MCM_ControlNPC", (k5.getValue() as int), 0)
        SetCursorPosition(1)
        AddHeaderOption("$PROTEUS_MCM_HeaderOtherHotkeys", 0)
        castK12 = AddKeyMapOption("$PROTEUS_MCM_ProteusWheel", (k12.getValue() as int), 0)
        castK13 = AddKeyMapOption("$PROTEUS_MCM_Spawner", (k13.getValue() as int), 0)
        castK14 = AddKeyMapOption("$PROTEUS_MCM_Weather", (k14.getValue() as int), 0)
    endif
EndEvent

Event OnOptionKeyMapChange(int option, int keyCode, string a_conflictControl, string a_conflictName)
    if option == castK1
        SetKeyMapOptionValueST(keyCode, false, "")
        k1.setValue(keyCode)
    elseif option == castK3
        SetKeyMapOptionValueST(keyCode, false, "")
        k3.setValue(keyCode)
    elseif option == castK5
        SetKeyMapOptionValueST(keyCode, false, "")
        k5.setValue(keyCode)
    elseif option == castK6
        SetKeyMapOptionValueST(keyCode, false, "")
        k6.setValue(keyCode)
    elseif option == castK7
        SetKeyMapOptionValueST(keyCode, false, "")
        k7.setValue(keyCode)
    elseif option == castK8
        SetKeyMapOptionValueST(keyCode, false, "")
        k8.setValue(keyCode)
    elseif option == castK9
        SetKeyMapOptionValueST(keyCode, false, "")
        k9.setValue(keyCode)
    elseif option == castK10
        SetKeyMapOptionValueST(keyCode, false, "")
        k10.setValue(keyCode)
    elseif option == castK11
        SetKeyMapOptionValueST(keyCode, false, "")
        k11.setValue(keyCode)
    elseif option == castK12
        SetKeyMapOptionValueST(keyCode, false, "")
        k12.setValue(keyCode)
    elseif option == castK13
        SetKeyMapOptionValueST(keyCode, false, "")
        k13.setValue(keyCode)
    elseif option == castK14
        SetKeyMapOptionValueST(keyCode, false, "")
        k14.setValue(keyCode)
    endif
    ForcePageReset()
EndEvent

Event OnOptionHighlight(int option)
    if option == disableOID
        SetInfoText("$PROTEUS_MCM_InfoDisableHotkeys")
    elseif option == explosionsOnOID
        SetInfoText("$PROTEUS_MCM_InfoGreenExplosion")
    elseif option == spawnPerksLoadOID
        SetInfoText("$PROTEUS_MCM_InfoSpawnPerks")
    elseif option == spawnSpellsLoadOID
        SetInfoText("$PROTEUS_MCM_InfoSpawnSpells")
    elseif option == presetGameStartOID
        SetInfoText("$PROTEUS_MCM_InfoLoadPreset")
    elseif option == backupAppearanceSaveOID
        SetInfoText("$PROTEUS_MCM_InfoRaceMenuBackups")
    elseif option == alternativeDeathSystemOID
        SetInfoText("$PROTEUS_MCM_InfoAlternativeDeath")
    endif
EndEvent

Event OnOptionDefault(int option)
    if option == disableOID
        disableVal = false
        SetToggleOptionValue(disableOID, disableVal, false)
        if disableVal == false
            disableHotkeys.setValue(0)
        elseif disableVal == true
            disableHotkeys.setValue(1)
        endif
    endif
    if option == explosionsOnOID
        explosionsOnVal = true
        SetToggleOptionValue(explosionsOnOID, explosionsOnVal, false)
        if explosionsOnVal == false
            explosionsOn.setValue(0)
        elseif explosionsOnVal == true
            explosionsOn.setValue(1)
        endif
    endif
    if option == spawnPerksLoadOID
        spawnPerksOnVal = true
        SetToggleOptionValue(spawnPerksLoadOID, spawnPerksOnVal, false)
        if spawnPerksOnVal == false
            ZZEnableSpawnPerkLoad.setValue(0)
        elseif spawnPerksOnVal == true
            ZZEnableSpawnPerkLoad.setValue(1)
        endif
    endif
    if option == spawnSpellsLoadOID
        spawnSpellsOnVal = true
        SetToggleOptionValue(spawnSpellsLoadOID, spawnSpellsOnVal, false)
        if spawnSpellsOnVal == false
            ZZEnableSpawnSpellLoad.setValue(0)
        elseif spawnSpellsOnVal == true
            ZZEnableSpawnSpellLoad.setValue(1)
        endif
    endif
    if option == presetGameStartOID
        presetGameStartOnVal = true
        SetToggleOptionValue(presetGameStartOID, presetGameStartOnVal, false)
        if presetGameStartOnVal == false
            ZZLoadPlayerPreset.setValue(0)
        elseif presetGameStartOnVal == true
            ZZLoadPlayerPreset.setValue(1)
        endif
    endif
    if option == backupAppearanceSaveOID
        backupAppearanceSaveVal = false
        SetToggleOptionValue(backupAppearanceSaveOID, backupAppearanceSaveVal, false)
        if backupAppearanceSaveVal == false
            ZZBackupAppearanceSave.setValue(0)
        elseif backupAppearanceSaveVal == true
            ZZBackupAppearanceSave.setValue(1)
        endif
    endif
    if option == alternativeDeathSystemOID
        alternativeDeathSystemVal = false
        SetToggleOptionValue(alternativeDeathSystemOID, alternativeDeathSystemVal, false)
        if alternativeDeathSystemVal == false
            ZZAlternativeDeathSystem.setValue(0)
            (ZZProteusRecurringQuest.GetNthAlias(0) as referencealias).Clear()
        elseif alternativeDeathSystemVal == true
            ZZAlternativeDeathSystem.setValue(1)
            (ZZProteusRecurringQuest.GetNthAlias(0) as referencealias).ForceRefTo(game.GetPlayer())
            int targetModIndex = game.GetModByName("Sacrosanct - Vampires of Skyrim.esp")
            if !(targetModIndex == 255)
                (game.GetFormFromFile(1311193, "Sacrosanct - Vampires of Skyrim.esp") as globalvariable).setValue(1)
            endif
        endif
    endif
EndEvent

int Function GetVersion()
    return 1
EndFunction

Event OnOptionSelect(int option)
    if option == disableOID
        disableVal = !disableVal
        SetToggleOptionValue(disableOID, disableVal, false)
        if disableVal == false
            disableHotkeys.setValue(0)
        elseif disableVal == true
            disableHotkeys.setValue(1)
        endif
    endif
    if option == explosionsOnOID
        explosionsOnVal = !explosionsOnVal
        SetToggleOptionValue(explosionsOnOID, explosionsOnVal, false)
        if explosionsOnVal == false
            explosionsOn.setValue(0)
        elseif explosionsOnVal == true
            explosionsOn.setValue(1)
        endif
    endif
    if option == spawnPerksLoadOID
        spawnPerksOnVal = !spawnPerksOnVal
        SetToggleOptionValue(spawnPerksLoadOID, spawnPerksOnVal, false)
        if spawnPerksOnVal == false
            ZZEnableSpawnPerkLoad.setValue(0)
        elseif spawnPerksOnVal == true
            ZZEnableSpawnPerkLoad.setValue(1)
        endif
    endif
    if option == spawnSpellsLoadOID
        spawnSpellsOnVal = !spawnSpellsOnVal
        SetToggleOptionValue(spawnSpellsLoadOID, spawnSpellsOnVal, false)
        if spawnSpellsOnVal == false
            ZZEnableSpawnSpellLoad.setValue(0)
        elseif spawnSpellsOnVal == true
            ZZEnableSpawnSpellLoad.setValue(1)
        endif
    endif
    if option == presetGameStartOID
        presetGameStartOnVal = !presetGameStartOnVal
        SetToggleOptionValue(presetGameStartOID, presetGameStartOnVal, false)
        if presetGameStartOnVal == false
            ZZLoadPlayerPreset.setValue(0)
        elseif presetGameStartOnVal == true
            ZZLoadPlayerPreset.setValue(1)
        endif
    endif
    if option == backupAppearanceSaveOID
        backupAppearanceSaveVal = !backupAppearanceSaveVal
        SetToggleOptionValue(backupAppearanceSaveOID, backupAppearanceSaveVal, false)
        if backupAppearanceSaveVal == false
            ZZBackupAppearanceSave.setValue(0)
        elseif backupAppearanceSaveVal == true
            ZZBackupAppearanceSave.setValue(1)
        endif
    endif
    if option == alternativeDeathSystemOID
        alternativeDeathSystemVal = !alternativeDeathSystemVal
        SetToggleOptionValue(alternativeDeathSystemOID, alternativeDeathSystemVal, false)
        if alternativeDeathSystemVal == false
            ZZAlternativeDeathSystem.setValue(0)
            (ZZProteusRecurringQuest.GetNthAlias(0) as referencealias).Clear()
        elseif alternativeDeathSystemVal == true
            ZZAlternativeDeathSystem.setValue(1)
            (ZZProteusRecurringQuest.GetNthAlias(0) as referencealias).ForceRefTo(game.GetPlayer())
            int targetModIndex = game.GetModByName("Sacrosanct - Vampires of Skyrim.esp")
            if !(targetModIndex == 255)
                (game.GetFormFromFile(1311193, "Sacrosanct - Vampires of Skyrim.esp") as globalvariable).setValue(1)
            endif
        endif
    endif
EndEvent

Event OnOptionSliderAccept(int option, float value)
    {Called when a new slider value has been accepted}
EndEvent

Event OnOptionSliderOpen(int option)
    {Called when a slider option has been selected}
EndEvent
