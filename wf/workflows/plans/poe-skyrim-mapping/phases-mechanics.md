# 施工切片 S8–S14：機制與 keystone（第二波起）

[phases](phases.md)｜[mechanics](mechanics.md)｜[keystones](keystones.md)

每個機制上線時同步三件事：[family-rules.json](data/family-rules.json) 對應的暫代規則改指新 atom；[atoms.json](data/atoms.json) 加新 atom 列，每份數值照 50 份校準反推、請使用者確認；converter 的 golden 重產，diff 只出現在該規則命中的節點。下面每片的 Done when 都隱含這三項。

## S8 投射物關聯

依賴：S4、S7。派給：普通線。規模 M。

- 投射物 stat 關聯到弓箭矢、弩矢、法術投射物（火球、冰錐等）；投射物速度 stat 不做速度效果。
- 做法依 S7 結論：ESL perk 以條件區分投射型法術與箭矢／弩矢，讀新的 carrier AV。

Done when: ESL 有投射物 perk（`esplib header` 可見）；離線測試中同份數下弓、弩、投射型法術吃到加成，近戰與接觸型法術不吃。

## S9 能量護盾

依賴：S5。派給：普通線；規格先請使用者定。規模 L。

- 先出規格（池大小與份數的關係、充能延遲與速率、特效），寫進 [mechanics](mechanics.md)，登記 WAIT_USER 等使用者定。
- 實作：每個 actor 一個護盾池，存在 cosave；在 S5 的 handler 鏈上先扣護盾再扣 HP；受擊後延遲充能。

Done when: mechanics.md 有護盾規格與使用者裁示原話；離線測試：先扣護盾後扣 HP、延遲後回充、存讀 5 輪池值不漂移。

## S10 異常載具

依賴：S4、S5。派給：普通線。規模 L。

- 點燃、感電、冰緩／冰凍、流血、中毒、DoT 倍率，MGEF／SPEL 放 ESL，命中時依機率套用。

Done when: ESL 有各異常的 MGEF／SPEL；離線測試：機率 0 從不套用、機率 100 每次套用，DoT 倍率依份數放大。

## S11 charge

依賴：S5。派給：普通線。規模 M。

- 耐力球、狂怒球、暴擊球、Rage、其他：做成 buff（MGEF 放 ESL），依擊殺、暴擊、受擊等條件累積與衰減。不上 HUD，最多加特效。

Done when: 離線測試：累積、衰減、層數上限照 PoE 原文；新包 diff 沒有 HUD／Scaleform 檔的變更。

## S12 召喚物

依賴：S4。派給：普通線。規模 L。

- 召喚類 stat 落到 Skyrim 召喚物：召喚物的生命、傷害，以及召喚數。

Done when: 離線測試：召喚物依份數拿到生命、傷害加成；召喚數 +1 時不超過引擎允許的同時召喚上限。

## S13 藥瓶 buff

依賴：S4、S5。派給：普通線；門檻與冷卻先出提案。規模 M。

- 血量低於門檻時自動施放回復法術，有冷卻。

Done when: 離線測試：跌破門檻觸發一次、冷卻內不重複、門檻以上不觸發。

## S14 keystone 第一批（分 5 段）

派給：普通線。每段的 keystone 名單、方案與負面處理在 [keystones.json](data/keystones.json) 的 `施工批次`、`正面方案`、`負面與建議` 欄。

| 段 | 依賴 | 個數 |
|---|---|---:|
| K1 | S4、S5 | 18 |
| K2 | S9 | 8 |
| K3 | S10 | 8 |
| K4 | S11 | 2 |
| K5 | S12 | 2 |

- K1 同時做 6 組互斥（`exclusive_with`）：已擁有其中一方時，另一方不能購買。
- 施工前對照 CK wiki 核實 perk entry 與條件函式名稱。
- 段內 keystone 上線後，converter 不再讓它走通路規則。

Done when（每段）: 段內每個 keystone 有離線測試案例且通過；keystones.json 新增的 `施工狀態` 欄，該段的列都填上；K1 另有互斥測試：買了一方再買另一方會被拒且點數不變。
