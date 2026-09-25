# API：ActorUtil / MiscUtil / 陣列操作

← [papyrusutil](papyrusutil.md)

### 2.4 ActorUtil — Actor Package Override

| Function | 簽名 | 說明 |
|---|---|---|
| `AddPackageOverride` | `(Actor targetActor, Package targetPackage, int priority=30, int flags=0)` | 加入 package，priority 0-100（100 最高），進 save |
| `RemovePackageOverride` | `(Actor targetActor, Package targetPackage) → bool` | 移除指定 package override |
| `CountPackageOverride` | `(Actor targetActor) → int` | 計算現有 override 數量（包含條件未滿足的） |
| `ClearPackageOverride` | `(Actor targetActor) → int` | 清除此 Actor 所有 override（包含其他 mod 的！） |
| `RemoveAllPackageOverride` | `(Package targetPackage) → int` | 從所有 Actor 移除此 package |

> **警告**：`ClearPackageOverride` 會清掉所有 mod 設的 override，使用需謹慎。

### 2.5 MiscUtil — 雜項 utility

本表整理「2.5 MiscUtil — 雜項 utility」的逐項記錄。

已抽到 [papyrusutil-api-actor-misc-array-misc-utilities.json](papyrusutil-api-actor-misc-array-misc-utilities.json)（14 列）。

欄位「Function」：保留原表的Function。

欄位「簽名」：保留原表的簽名。

欄位「說明」：保留原表的說明。

統計：14 筆記錄，3 個欄位。


### 2.6 PapyrusUtil — 陣列操作 utility

本表整理「2.6 PapyrusUtil — 陣列操作 utility」的逐項記錄。

已抽到 [papyrusutil-api-actor-misc-array-array-utilities.json](papyrusutil-api-actor-misc-array-array-utilities.json)（18 列）。

欄位「分類」：保留原表的分類。

欄位「Function（以 int 為例，同理 float/string/Form/Actor/ObjRef/Alias）」：保留原表的Function（以 int 為例，同理 float/string/Form/Actor/ObjRef/Alias）。

欄位「說明」：保留原表的說明。

統計：18 筆記錄，3 個欄位。


---

