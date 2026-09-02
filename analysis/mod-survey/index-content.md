# 內容型

← [mod-survey](README.md)｜[survey index](index.md)

<!-- wf-nav -->

| Mod | Finding | Plugin | 敘事價值 | 重點 |
| --- | --- | --- | --- | --- |
| Follower Commentary Overhaul SE | [findings/follower-commentary-overhaul.md](findings/follower-commentary-overhaul.md) | `FCO - Follower Commentary Overhaul.esp` | 中 | generic follower ambient commentary；voice type + location/quest/player-state conditions |
| Improved Follower Dialogue - Lydia | [findings/improved-follower-dialogue-lydia.md](findings/improved-follower-dialogue-lydia.md) | `ImprovedCompanionsBoogaloo.esp` | 高 | unique follower arc；stage/global/VM quest variable；moral objection；scene quests |
| Inigo（unique follower 智能系統） | [findings/inigo.md](findings/inigo.md) | `Inigo.esp`（v2.4C，Skyrim+Update only，有 BSA） | 高（系統面極高） | standalone 語音隨從的**行為/追蹤/自治 AI 骨架**：alias-monitor→中央 status quest 假-AnimationEvent message bus；**faction-rank 當狀態機（GLOB=0）**驅動戰鬥風格/跟隨距離/心情；Radar cell-scan + 召喚 SPEL→marker + 哨聲 + 地圖定位 + NPCTalkedTo/PlayerJourney 記憶；依技能自動換裝 + 自主買酒/用祭壇；**零 DLL/PapyrusUtil/JContainers/MCM**，Sofia 系統面最佳對照 |
| Relationship Dialogue Overhaul | [findings/relationship-dialogue-overhaul.md](findings/relationship-dialogue-overhaul.md) | `Relationship Dialogue Overhaul.esp` | 高 | relationship/follower system overhaul；shared info；voice type matrix；generic recruit/command compatibility |
| I'm Glad You're Here | [findings/im-glad-youre-here.md](findings/im-glad-youre-here.md) | `ImGladYoureHere.esp` | 高（動作層） | follower/family hug action service；scene protection；camera/idle/package cleanup；Sofia compatibility hooks |
| Immersive Patrols SE/AE | [findings/immersive-patrols.md](findings/immersive-patrols.md) | `Immersive Patrols II.esp` | 低（系統高） | no quest/dialogue；static placed patrols + patrol/follow packages + custom aggro factions；M&B static patrol slice reference |
| Civil War Lines Expansion | [findings/civil-war-lines-expansion.md](findings/civil-war-lines-expansion.md) | `Civil War Lines Expansion.esp` | 中 | 415 combat/idle/hello bark lines；faction/voice/equipment/location/random condition matrix；voice + seq pipeline reference |
| Pirates of Skyrim - The Northern Cardinal | [findings/pirates-of-skyrim.md](findings/pirates-of-skyrim.md) | `NorthernCardinal.esp` | 中-高 | 雙海盜 quest 線 + 自訂 worldspace（Sea of Ghosts/Frostreef）；**船＝Enable/Disable 多實例靜態船的傳送樞紐**（非動畫船，FormList-of-FormList 定址）；XMarker 預置事件群 + RandomInt 重擲做輕量海戰/海域遭遇；crew=9-alias bank + morale global gate；SkyUI MCM，**無 DLL/BSA、附 .psc**；零件全已 landed，缺 `travelHub:` macro + MESG buttons[] |
