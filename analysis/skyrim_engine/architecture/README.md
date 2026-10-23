# architecture — 引擎子系統深潛索引

← [skyrim_engine](../README.md)

每篇是一個引擎子系統「怎麼構成、怎麼運作」的深潛，依 `<分類>_<主題>.md` 檔名慣例分組。實作步驟走 [tutorial/](../tutorial/README.md)，單點問答走 [answers/](../answers/README.md)。

<!-- wf-nav -->

### 3D 圖形：模型／貼圖／著色器／特效

- [深度解析：Actor 骨骼系統](3D_Graphics_Actor_Skeleton_Deep_Dive.md)
- [深度解析：蒙皮與分組系統](3D_Graphics_Biped_Slots_and_Skinning_Deep_Dive.md)
- [Skyrim 模型與物理架構：NIF 構造、材質與 Havok 屬性](3D_Graphics_Model_and_Physics_Anatomy.md)
- [Skyrim 3D 模型深度解析：.nif 檔案格式與 Block 結構](3D_Graphics_NIF_File_Format_Deep_Dive.md)
- [深度解析：種族視覺系統](3D_Graphics_Race_Visual_System_Deep_Dive.md)
- [Skyrim 渲染架構：Shader、貼圖與動態覆蓋機制](3D_Graphics_Shader_and_Texture_Fundamentals.md)
- [Skyrim 貼圖「三位一體」架構：DDS 格式、資源路徑與動態操控](3D_Graphics_Texture_Trio_Anatomy.md)
- [Skyrim 特效架構：粒子系統、視覺效果與動態觸發](3D_Graphics_VFX_Architecture.md)

### 對話與任務

- [Skyrim 架構解析：對話與任務的定義與存儲機制](Dialogue_Quest_Dialogue_Quest_Storage_Architecture.md)
- [Skyrim 對話話題機制：DIAL 與 INFO 的深度運作邏輯](Dialogue_Quest_Dialogue_Topic_Mechanism.md)
- [深度解析：動態任務生成與別名填充](Dialogue_Quest_Dynamic_Quest_Generation_Deep_Dive.md)
- [Skyrim 劇情與任務系統架構](Dialogue_Quest_Quest_and_Storyline_Architecture.md)
- [深度解析：故事管理器](Dialogue_Quest_Story_Manager_Deep_Dive.md)

### 物品與裝備

- [Skyrim 容器系統架構：存儲、物品欄與動態內容管理](Items_Container_Architecture.md)
- [Skyrim 物品解剖學：物件的構造與屬性系統](Items_Item_Anatomy.md)

### 魔法與法術

- [Skyrim 法術系統架構：施法、數值計算與效果作用機制](Magic_Spell_System_Anatomy.md)
- [Skyrim 可投擲武器架構](Magic_Throwable_Weapon_Architecture.md)

### NPC／Actor／AI

- [Skyrim Actor 解剖學：角色的組成構造](NPC_Actor_Anatomy.md)
- [Skyrim Actor 動作與動畫架構：Havok Behavior 與動畫事件](NPC_Actor_Animation_Architecture.md)
- [Skyrim Actor 模型與物理架構：骨骼、種族與布娃娃系統](NPC_Actor_Model_and_Ragdoll_Anatomy.md)
- [Skyrim 深層 AI 架構：接管 NPC 的決策中樞](NPC_Deep_AI_Architecture.md)
- [MH 魔物引擎整合深度解析](NPC_Deep_Dive_MH_Creature_Engine_Integration.md)
- [Skyrim 動作邏輯核心：Havok Behavior (.hkx) 深度解析](NPC_Havok_Behavior_Deep_Dive.md)
- [Skyrim 新種族架構與開發指南](NPC_New_Race_Architecture_and_Creation.md)
- [Skyrim Radiant AI 架構：動態任務與自主行為系統](NPC_Radiant_AI_Architecture.md)
- [深度解析：Radiant AI 自主沙盒行為](NPC_Radiant_Sandboxing_Deep_Dive.md)

### 存檔

- [Skyrim 存檔深度解析：ESS 文件結構與 ChangeForms 機制](Save_Data_ESS_Save_Deep_Dive.md)
- [Skyrim 存檔系統架構：數據持久化與 ESS 結構](Save_Data_Save_System_Architecture.md)

### 引擎系統與資源格式

- [Skyrim 檔案封裝深度解析：BSA 格式與虛擬檔案系統運作流程](Systems_BSA_Format_and_Workflow.md)
- [Skyrim 碰撞系統架構：Havok 物理、碰撞層與射線偵測](Systems_Collision_System_Architecture.md)
- [Skyrim 數據文件架構：ESP, ESM 與二進制 Records](Systems_ESP_ESM_Architecture.md)
- [Skyrim 引擎核心架構：從數據到世界的演變](Systems_Engine_Workflow.md)
- [Skyrim 腳本綁定架構：C++ 與 Papyrus 的橋樑](Systems_Papyrus_Binding_Architecture.md)
- [Skyrim 天賦系統架構：BGSPerk, 星座介面與動態修改](Systems_Perk_System_Architecture.md)
- [Skyrim 資源檔案系統架構：NIF, DDS, HKX 與 BSA 封裝](Systems_Resource_Formats_Architecture.md)
- [TESForm - 深度解析與實戰指南](Systems_TESForm_Detailed.md)

### 世界與場景

- [Skyrim 建築物內部改造與室內空間設計](World_Interior_Renovation_Architecture.md)
- [Skyrim 開放世界架構：動態網格加載與單元管理](World_Open_World_Architecture.md)
- [Skyrim 世界運行機制：主循環、離線 AI 與事件驅動](World_World_Runtime.md)
