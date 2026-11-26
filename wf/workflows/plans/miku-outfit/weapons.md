# 階段 W 武器：蔥與麥克風架

[計畫入口](README.md)

初音的標誌道具裡最常被當武器的是蔥：2007 年 Ievan Polkka 的甩蔥影片讓它變成固定配件。另一個是演唱用的麥克風架。這兩樣做成 Skyrim 武器，都要決定形狀從哪來、用哪種動作。選項列給使用者挑（D9–D11）。

## 查了什麼

2026-11-26 在公司只讀查公開資料，沒下載任何 mod 檔。Nexus 網頁被 Cloudflare 擋（403），所以內容來自 Nexus 公開的 GraphQL API（`api.nexusmods.com/v2/graphql`，不需 key）。**這也代表所有候選的 Permissions 段都沒看到**，授權一律標「未查到」，回家在瀏覽器看過頁面才算數。原版 Leek 的 FormID 來自 UESP 的 Skyrim:Food 頁。

查無結果的關鍵字：SE 站名稱含 negi、vocaloid、microphone、mic stand、ievan、spring onion、green onion、necktie、headset 的都是 0 筆，名稱含 miku 的全站只有 5 筆。API 的名稱查詢只比對名稱，不搜內文，名稱沒寫關鍵字的 mod 會漏。

## 候選

已抽到 [weapons.json](data/weapons.json)（6 列：蔥 3、麥克風架 2、初音主題劍 1）。欄位：

- `id`／`prop`／`route`：代號、道具、做法。
- `source`、`url`、`license`、`requires`：素材從哪來、連結、授權、前置。
- `anim_type`：動作類型。
- `new_mesh`、`download`：要不要新網格、要不要下載。
- `effort`、`notes`、`recommend`：工作量、注意、推薦程度。

統計：零下載的有 3 列（WP1、WP3、WP4 用原版法杖時），要下載的 3 列，要新建模的 1 列（WP5，等 D2）。推薦 WP1 為主、WP3 保底。

另外看到但不列候選的：Cursed Skyrim - Food Hair Ornaments（79581）把原版食物網格做成頭飾，有成人標記；Kanjs - Sexy Leek（77001）也有成人標記；Ballistic Shield and Police Baton（96534）只是短棍，跟 WP3 重疊。

## 武器記錄要做的事

WEAP 跟 ARMO 一樣用 outfit-tools 複製並換貼圖。另外要注意四件事：

1. **動作類型**：DNAM 的 animation type 決定用哪組動作，現役 MCO／ADXP 動作是照武器類型與關鍵字選的。蔥建議單手錘（D10），要配 `WeapTypeMace` 關鍵字，perk 才算得對。
2. **握點**：武器 NIF 的原點就是手握的位置。原版 Leek 是桌上的食物，原點不在一端，所以要平移。houseCARL `nif_set` 現在只能縮放（`set_scale`），不能平移，要先擴（W2）。
3. **碰撞**：丟在地上要有碰撞。食物 NIF 本來有沒有 collision block，回家用 `nif_inspect` 看（W1）。放大後碰撞跟不跟著縮放，只能實機驗。
4. **第一人稱與收刀**：單手錘沒有劍鞘。第一人稱模型照原武器的做法處理，實機一起看（W5）。

## 家裡與公司

| 步驟 | 公司 | 家 |
|---|---|---|
| W2 NIF 平移工具 | 能，合成 NIF 測試 | — |
| W1 讀原版 Leek NIF | 不能，沒有 Skyrim.esm | 能 |
| W3、W4 做 NIF 與 WEAP | 不能，沒有素材 | 能，只到 staging |
| W5 實機 | 不能 | 使用者當場說才開 |
| WP2、WP4、WP6 下載 | 不下載 | 使用者授權才下載 |

## 閘門與驗收

1. **離線**：`nif_inspect` 讀回縮放、平移、貼圖路徑；`head_render` 出一張側視圖看比例。WEAP 讀回動作類型、MODL、關鍵字。
2. **對照圖**：使用者看比例與顏色。
3. **實機**：握點在手心，揮砍時 MCO 動作正常；丟在地上不穿地、不彈飛；不 CTD。

工作量約 2–3 天，加一次實機，可以跟階段 A 的實機一起做。task 是 W1–W6，在 [tasks-near.json](data/tasks-near.json)。

## 跟特效的關係

蔥做好後可以加青綠附魔光效（E4），走記錄層，不用動網格。見 [effects.md](effects.md)。
