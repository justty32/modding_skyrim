# 可利用模式 + 對 ModForge 的參考價值

← [papyrusutil](papyrusutil.md)

## 三、ModForge 生成 Papyrus script 的可利用模式

以下 pattern 在 spec 層面可作為標準積木：

### Pattern 1：per-NPC 輕量記憶（StorageUtil）

```papyrus
; 記錄 NPC 上次對話時間（cooldown 防刷）
StorageUtil.SetFloatValue(akSpeaker, "mymod_lastGreet", Utility.GetCurrentRealTime())
float lastTime = StorageUtil.GetFloatValue(akSpeaker, "mymod_lastGreet", 0.0)
```

用途：follower 記憶、關係狀態、交互 cooldown、任務進度標記。

### Pattern 2：跨存檔外部設定（JsonUtil）

```papyrus
; 讀取外部 JSON 設定（可被玩家/其他 mod 在遊戲外編輯）
int cooldown = JsonUtil.GetIntValue("../MyMod/config", "greetCooldown", 300)
; 路徑 API：讀嵌套結構
float weight = JsonUtil.GetPathFloatValue("../MyMod/data", ".commentary.lydia.weight", 1.0)
```

### Pattern 3：動態 Package Override（ActorUtil）

```papyrus
; 讓 NPC 臨時站到指定位置
ActorUtil.AddPackageOverride(myFollower, myStandPackage, 50)
; 場景結束後清除
ActorUtil.RemovePackageOverride(myFollower, myStandPackage)
```

注意：priority 50 比普通 AI（30）高但不影響 combat（80+）。

### Pattern 4：Cell 掃描情境對話

```papyrus
; 附近有哪些 NPC 可以觸發情境 bark
Actor[] nearbyNPCs = MiscUtil.ScanCellNPCs(akSpeaker, 500.0)
if nearbyNPCs.Length > 2
  ; 觸發「人多」版本的 commentary
endif
```

### Pattern 5：FormList 型 cross-mod 協作（StorageUtil inter-mod）

```papyrus
; 其他 mod 把待處理的 Actor 加入我的 list
StorageUtil.FormListAdd(none, "mymod_processQueue", targetActor)
; 我的 mod 定期掃描並消費
int i = StorageUtil.FormListCount(none, "mymod_processQueue")
while i > 0
  i -= 1
  Actor a = StorageUtil.FormListGet(none, "mymod_processQueue", i) as Actor
  StorageUtil.FormListRemoveAt(none, "mymod_processQueue", i)
endwhile
```

### Pattern 6：prefix 批次清理

```papyrus
; 某 follower 離隊時，清除所有以 "mymod_follower_" 開頭的 key
StorageUtil.ClearAllObjPrefix(followerRef, "mymod_follower_")
```

---

## 四、對 ModForge 的參考價值

本表整理「四、對 ModForge 的參考價值」的逐項記錄。

已抽到 [papyrusutil-patterns-and-eval-modforge-capabilities.json](papyrusutil-patterns-and-eval-modforge-capabilities.json)（13 列）。

欄位「功能」：保留原表的功能。

欄位「評估」：保留原表的評估。

欄位「說明」：保留原表的說明。

統計：13 筆記錄，3 個欄位。


**對 ModForge 最高槓桿的生成點**：
- `StorageUtil.SetIntValue/GetIntValue` 搭配 Quest Script 的 per-NPC 狀態追蹤
- `JsonUtil.GetIntValue/GetPathFloatValue` 讀取外部 config（讓 mod 設定可在遊戲外調整）
- `ActorUtil.AddPackageOverride` + `RemovePackageOverride` 的 follower 動態行為包
- `MiscUtil.ScanCellNPCs` 驅動的情境 commentary 觸發

> ⚠️ 以上「可生成 / 純參考」是本 survey 推斷，**未查 ModForge src/**，可能有誤判。確認需另做 code pass。
