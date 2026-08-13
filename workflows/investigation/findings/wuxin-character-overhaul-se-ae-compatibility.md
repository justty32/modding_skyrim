# 無心人物美化在 Skyrim SE/AE 1.6.1170 的適配路線

日期：2026-08-13

## Done when

無心人物線的原始來源、SE 替代方案、1.6.1170 相容邊界、現有 load order 衝突與下一個可執行步驟都已明確；未取得合法 archive 前不安裝未知鏡像。

## 使用者目標

- 主要目標：讓經典版「無心個人整合版」的**人物美化**在目前 Skyrim SE/AE 1.6.1170 工作。
- 不納入：環境、景觀、光影或材質包的整體移植。
- 次要／未來目標：日後可能把喜歡的角色外觀納入自製任務；這不屬於本次適配的完成條件。

## 已確認事實

1. 夜貓－無心的 Bilibili 作者頁仍提供「無心個人整合版 3.1.0」下載；頁面明載它只支援
   傳奇版，人物美化包含多種女性／男性臉部、皮膚、頭髮、眉毛等，另有獨立「頭模替換」修改
   1138 名 NPC。這是目前要精確保留無心角色時的首選來源：
   <https://www.bilibili.com/opus/839987838099390470>
2. 無心傳奇版的舊 MOD 原址清單把「女性 NPC 美化」指向 LE `Decent Women - improve female npcs face`（Nexus Skyrim id `14443`）：
   <https://www.uu-gg.one/forum.php?extra=&mobile=no&mod=viewthread&tid=32779>
3. `Decent Women` 目前頁面列出四個獨立檔案：Commoners、Followers、Enemies and Wanderers、Children；它不是一個現成的 SSE archive：
   <https://www.nexusmods.com/skyrim/mods/14443>
4. 同一份來源整理中的「重製版」段落使用 SSE `Women's faces`（Nexus SSE id `5630`），但該段落屬於**另一個重製版整合清單**，不能把它說成 `Decent Women` 的原樣移植。
5. houseCARL 於 2026-08-13 讀到 `Women's faces`：v1.7、323 名女性 NPC、英文主檔 `NPS_Female_SE_Eng`、290.7 MB、無列出的 Nexus requirements、BSA 自包含、不改 companions；作者已停用一般直接下載，須走 Nexus mod-manager（NXM）下載：
   <https://www.nexusmods.com/skyrimspecialedition/mods/5630>
6. `Women's faces` 沒有 SKSE DLL；就已知內容而言，Skyrim runtime `1.6.1170` 不是主要相容障礙。真正風險是它與其他 NPC record 修改的 winner／FaceGen 不一致，造成黑臉、髮型或 AI 改動被覆蓋。
7. 目前 `Modpack-KR-Dev` 可辨識但不是 selected profile；現役人物相關 mod 有 RaceMenu、
   XPMSSE／Skeleton Auto Patch、Face Discoloration Fix 與 AI Overhaul，尚無 body、skin 或 hair
   overhaul。Face Discoloration Fix 只能兜底，不能取代正確的 NPC winner patch。

## 結論

### A. 精確保留經典無心人物（目標路線）

需要取得使用者合法持有的下列其中一種來源，優先順序如下：

- 無心 3.1.0 下載資料夾中名稱含「人物美化」與「頭模替換」的 archive；或
- Nexus LE `Decent Women` 的所需原始檔案。

取得後才可實際驗證並轉換：

1. 解包、列出 plugin masters、NPC records、FaceGeom、FaceTint、head parts 與外部資產。
2. 用 Cathedral Assets Optimizer／等效工具把 LE mesh、texture、BSA 轉為 SSE 可讀格式；不要盲目只改 plugin header。
3. 以 Creation Kit resave 或可驗證的等效流程把 plugin 轉為 SSE Form 44。
4. 在 `Modpack-KR-Dev` 建獨立 MO2 mod，不覆寫 archive 原件。
5. 對目前 NPC winner 做衝突盤點。預期順序為 `AI Overhaul → 人物外觀 → 專用 conflict patch`；
   patch forward AI Overhaul 的 AI／package／faction 等非外觀欄位，同時保留目標外觀的 head
   parts、race、weight、tint 等欄位，並確保最後的 NPC record 與最後的 FaceGen 來自同一外觀來源。
6. 遊戲內抽查城鎮 NPC、followers、敵人與 DLC NPC：黑臉、頸縫、膚色、髮型、表情、AI 行為及對話。

### B. 先用可直接裝的 SSE 替代品（可選，不等同經典無心）

`Women's faces` 可作為不需 LE 轉換的廣覆蓋替代品，但它不改 companions，且外觀不是經典 `Decent Women` 的原樣。若使用者接受不同臉，下載後仍須做 AI Overhaul winner patch 與遊戲內抽查。

## 目前阻塞

本機在 `/home/lorkhan/skyrim_mods`、MO2 mods 與下載候選中尚未找到 `無心`、`Decent Women` 或 `Women's faces` archive。houseCARL 只能讀 Nexus metadata，不能下載；`Women's faces` 還要求經 Nexus mod-manager 下載。因此目前不能安全開始轉換或安裝。`Decent Women` 的 Nexus 權限另有限制轉換、修改與資產使用；私人本機技術試驗和可再發布的 SE port 必須分開看待，沒有作者許可不能製作可分發整包。

## 下一步

使用者若要**經典無心外觀**，從作者頁提供的百度網盤下載名稱含「人物美化」與「頭模替換」
的 archive，放到既有 Skyrim archive 目錄；不需要下載遊戲本體、環境美化或其他功能包。若接受
**近似的現成 SSE 替代品**，則用 MO2/Nexus 下載 `Women's faces` 英文檔。archive 出現後，安裝
agent 可繼續檔案級驗證、轉換、衝突 patch 與部署。
