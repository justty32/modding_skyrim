# answers — 具體問題的分析解答索引

← [skyrim_engine](../README.md)

每篇回答一個具體問題（「X 怎麼做到」「Y 的資料怎麼存」），比 [architecture/](../architecture/README.md) 窄、比 [tutorial/](../tutorial/README.md) 少步驟。帶同名資料夾的項目（如 `mantella-analysis.md`）是入口檔，細節在同名子資料夾。

<!-- wf-nav -->

### 3D 圖形：模型／貼圖／著色器／特效

- [Skyrim 自製特效與粒子系統](3D_Graphics_Custom_VFX_and_Particle_Systems.md)
- [MMD 模型導入 Skyrim 技術解答](3D_Graphics_MMD_to_Skyrim_Model_Conversion.md)
- [Skyrim 架構解析：NIF 加載時機與資源管理系統](3D_Graphics_NIF_Loading_and_Resource_Management.md)
- [運行時網格與材質動態修改架構](3D_Graphics_Runtime_Mesh_and_Material_Modification.md)

### 對話與任務

- [Skyrim 對話系統實作指南](Dialogue_Quest_Dialogue_System_Implementation.md)
- [Skyrim 任務與對話交互架構：生命週期、行為觸發與獎勵](Dialogue_Quest_Quest_Dialogue_Interactions.md)

### 物品與裝備

- [Skyrim 高階模組化鍛造系統架構](Items_Advanced_Modular_Crafting_System.md)
- [Skyrim 自製武器模型整合指南](Items_Custom_Weapon_Model_Integration.md)
- [Skyrim 槍械系統實作架構](Items_Firearm_System_Implementation.md)
- [Skyrim 架構解析：物品的定義、實例化與存儲機制](Items_Item_Definition_and_Storage.md)
- [Skyrim 物品文本與介紹架構：名稱、描述與書籍內容](Items_Item_Text_and_Description.md)

### 魔法與法術

- [Skyrim 高階大鍋釀造與法術加工系統](Magic_Advanced_Cauldron_Brewing_System.md)
- [Skyrim 法術與自定義動畫整合：以「街舞法術」為例](Magic_Dance_Spell_Animation_Integration.md)
- [Skyrim 架構解析：投射物碰撞、撞擊數據與效果執行流](Magic_Projectile_Impact_and_Effect_Flow.md)
- [Skyrim 投射物與效果架構：火球、火焰與物理負載](Magic_Projectiles_and_Effects.md)
- [Skyrim 法術定義與資源架構：SPEL, MGEF 與視覺載體](Magic_Spell_Definition_and_Resources.md)

### NPC／Actor／AI

- [進階 MH AI 與物理邏輯實作](NPC_Advanced_MH_AI_and_Physics_Implementation.md)
- [Skyrim 自製特殊角色開發指南](NPC_Custom_NPC_Creation_Guide.md)
- [Monster Hunter 魔物導入技術架構](NPC_Monster_Hunter_Creature_Integration.md)
- [Skyrim NPC 行為架構：AI 進程與行為邏輯](NPC_NPC_Behavior.md)
- [NPC 動態工作行為擴充架構](NPC_NPC_Dynamic_Work_Behavior_Architecture.md)
- [Skyrim NPC 生命週期與類別解析：獨特 NPC vs 隨機路人](NPC_NPC_Lifecycle_and_Types.md)
- [Skyrim NPC 反應機制：觀察、過濾與自動對話](NPC_NPC_Reaction_Mechanics.md)
- [Skyrim 架構解析：NPC 的定義、實例化與存檔序列化](NPC_NPC_Storage_and_Serialization.md)

### 引擎系統與資源格式

- [AI 助手回覆協議](Systems_AI_Assistant_Protocol.md)
- [Skyrim 自定義 UI 與 Flash (Scaleform) 整合指南](Systems_Custom_UI_and_Flash_Integration.md)
- [Skyrim 地圖載入、過場畫面與世界轉場邏輯](Systems_Loading_Screens_and_Transitions.md)
- [Skyrim Lua 腳本系統整合架構](Systems_Lua_Scripting_Integration.md)
- [Monster Hunter 風格戰鬥系統技術架構](Systems_Monster_Hunter_Combat_Overhaul.md)
- [Skyrim 商店經營系統架構](Systems_Shop_Management_System_Implementation.md)

### 世界與場景

- [Skyrim 3D 自由飛行系統技術架構](World_3D_Flight_System_Architecture.md)
- [Skyrim 自定義房屋與家具製作系統](World_Custom_Housing_and_Furniture_System.md)
- [Skyrim 龍騎士系統技術架構](World_Dragon_Riding_System_Architecture.md)
- [Skyrim 引擎解析：室外 (Exteriors) vs 室內](World_Exteriors_vs_Interiors.md)
- [Skyrim 農作物與種植系統實作架構](World_Farming_Crop_System_Implementation.md)
- [Skyrim 可互動家具與樣式更換系統](World_Interactive_Furniture_and_Styles.md)
- [Skyrim 新大地圖架構與開發指南](World_New_Worldspace_Creation_Guide.md)
- [Skyrim 載具系統實作架構](World_Vehicle_System_Implementation.md)
- [Skyrim 世界交互與觸發機制：陷阱、區域、門與鎖](World_World_Interactions_and_Triggers.md)

### AI 框架拆解（SkyrimNet／Mantella／MinAI／IntelEngine）

- [綜合：四個 AI 框架（SkyrimNet / Mantella / MinAI / IntelEngine）能給 ModForge 什麼](ai-frameworks-modforge-relevance.md)
- [IntelEngine-GamePlugin 分析：世界狀態、NPC 指令、對話控制](intelEngine-gameplugin-analysis.md)
- [IntelEngine-GamePlugin — 原始碼出處索引](intelEngine-source-ref.md)
- [Mantella 分析：世界狀態、NPC 指令、對話控制](mantella-analysis.md)
- [Mantella — 原始碼出處索引](mantella-source-ref.md)
- [MinAI 分析：世界狀態、NPC 指令、對話控制](minAI-analysis.md)
- [MinAI — 原始碼出處索引](minAI-source-ref.md)
- [SkyrimNet-GamePlugin 分析：世界狀態、NPC 指令、對話控制](skyrimNet-gameplugin-analysis.md)
- [SkyrimNet-GamePlugin — 原始碼出處索引](skyrimNet-source-ref.md)
