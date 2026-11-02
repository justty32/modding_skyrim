# 我們已有什麼、最小能借什麼

[返回入口](../ai-world-context.md)｜[上下文語義](context-semantics.md)

對照 `agent-bridge@ab5f8a91e5c05e63608802701c79fda5237b90a8`。以下是來源研究後的設計判斷，
不是已排程功能。本輪沒有 C++、DLL build、部署或遊戲驗證。

此處是**給開發／QA agent 用的觀測路線**。agent-bridge 明定為可獨立移除的 test harness，
不得進玩家 load order；未來正式 NPC 玩法需要自己的 runtime 生命週期，不能以本 harness 在線為前提。
兩條路可共用事實與上下文契約，參見 [ModForge／Living 邊界](modforge-living-fit.md)。

## 已有觀測採集，不必重造附近 NPC 掃描器

`GET /state` 把一次 `State::Snapshot` 排到 game thread；預設等待 3 秒，未取得回應即 HTTP 503。
這提供同一次 game-thread 執行的玩家／世界讀值，沒有持續採樣、事件歷史或 LLM 摘要。
來源：[`Routes.cpp:129`](../../../../projects/agent-bridge/src/Routes.cpp)、
[`GameThread.h:24`](../../../../projects/agent-bridge/src/GameThread.h)、
[`State.cpp:328`](../../../../projects/agent-bridge/src/State.cpp)。

三個 actor 集合的觀測範圍不同。`nearby_actors` 掃 `highActorHandles`，按玩家位置計算距離，
只保留半徑內 actor；`cell_actors` 遍歷玩家 parent cell 的 references；`loaded_actors`
遍歷四類 process lists，按 runtime reference FormID 去重。三者排除玩家，按距離排序後截斷。
它們都不檢查 LOS、FOV、牆壁遮擋，也不把死者、disabled 或跨 cell actor 一律排除。
因此「附近／loaded」不可寫成「玩家看見」。來源：
[`StateActors.cpp:51`](../../../../projects/agent-bridge/src/StateActors.cpp)。

每個 actor 已有 `name, form_id, base_form_id, distance, position, level, dead, in_combat,
hostile_to_player, player_teammate, cell, cell_form_id, same_cell, loaded_3d, disabled`。
玩家另有 cell/worldspace ID、interior、角度、生命／魔力／耐力與旗標；遊戲區塊有 calendar、
`load_epoch`、menus、dialogue、MessageBox。`player.equipped` 只含左右手；護甲要從選讀
inventory 的 `worn` 看。來源：[`StateActors.cpp:16`](../../../../projects/agent-bridge/src/StateActors.cpp)、
[`State.cpp:144`](../../../../projects/agent-bridge/src/State.cpp)、
[`State.cpp:255`](../../../../projects/agent-bridge/src/State.cpp)。

## 現有 snapshot 還不能保證什麼

現在沒有採集 wall-clock 時間、snapshot sequence、請求 scope 的回聲或集合完整度標誌。
`limit` 預設 32，`radius` 預設 4096 game units；截斷後不附 total/truncated。
`ProcessLists` 或 cell 不存在也會回空陣列，與「成功掃描但沒有 actor」無法區別。
來源：[`State.h:22`](../../../../projects/agent-bridge/src/State.h)、
[`StateActors.cpp:39`](../../../../projects/agent-bridge/src/StateActors.cpp)。

因此外部 reader 可以記錄 request 開始／收到回覆時間、include/radius/limit 與原始 JSON，
但這只能給出觀測時間區間；不能偽造引擎內精確採集時間，也不能從 `len == limit` 證明一定截斷。
`load_epoch` 是本行程收到成功 load 通知的計數，不是跨行程 save identity，也不是每份 snapshot 的版本。
來源：[`State.h:12`](../../../../projects/agent-bridge/src/State.h)。

現有 `/state` 沒有 weather、Location hierarchy、家具／package 活動證據、NPC 關係與周邊 NPC 裝備。
這是範圍差距，不能直接解讀成必須一次補齊。尤其「正在打鐵」至少要先定義要讀家具使用、
package 還是 animation；三者不是同一種事實。

## actor-diagnostics 不能計入 live 能力

單一 NPC 的雙手物件、selected spells、base CSTY 與 reference override 已有 Python v1
協商／解析，但 DLL 沒有 capability 或 route，現役明確 `unsupported`。
其 `value / empty / unavailable`、指定 runtime reference 身分驗證，以及 query_failed 與
invalid_response 分離，可作新觀測欄位的語義範例；不必複製另一份矛盾契約。
來源：[`actor-diagnostics.md:5`](../../../../projects/agent-bridge/docs/actor-diagnostics.md)。

## 最小借鏡切片

若日後先做「把狀態整理給 AI 看」，第一片可以在遊戲外完成：讀現有 `/state`，保留 raw evidence、
scope／時間區間／load epoch，以 runtime reference ID 對齊 actor；只在已確認同一 runtime、
load epoch 與觀測範圍下比較快照，產生「新增列入此次觀測結果／不再列入本次結果／戰鬥旗標改變」
等有界差異。跨 bridge 重啟或身分未知時清除差分基線；沒列入結果不能寫成死亡或離場。

第二片才是可預算 renderer：固定保留玩家位置／世界時間、指定焦點 NPC、戰鬥或任務相關變更，
其餘按距離與字數預算裁切，附上 renderer 從已收資料裁掉的數量或「完整度未知」；
不宣稱知道 scanner 的總數。以原始數值產生文字，不把自然語言摘要
寫回唯一事實來源。這借的是三套系統的分層經驗，不是導入整套對話、TTS、長期記憶或 actions。

若任務真的需要 weather／活動／裝備，再逐項做 producer 契約與 runtime 驗證。
觀測 reader 不需要 console fallback、移動 NPC、選對話或執行 action；這些保留各自授權邊界。

最小離線驗收例：同一 runtime／epoch 下，第二包因 limit 只列較近角色，原 actor 掉出結果時
不得生成「離場／死亡」事件；下一次回 503 不得清空最後合法快照或將其改稱新觀測。
這只驗 consumer 語義，不代替家中對真實採集、效能與遊戲 thread 的驗證。

## 與 authoring 工具分工

ModForge 生成離線 records／scripts／packaged mods；scene-capture-bridge 以人的 hotkey／ImGui
操作採集 placed refs、transform、enable state，再輸出 scene.json 給 ModForge。
兩者可提供地點／角色的靜態 metadata，不能取代本場遊戲的即時 actor state。
不要把 localhost console listener 合併到隨內容交付的 authoring 工具。
來源：[`agent-bridge README`](../../../../projects/agent-bridge/README.md)、
[`scene-capture-bridge README`](../../../../projects/scene-capture-bridge/README.md)。

既有 [SkyPlace 研究](../../../tool-survey/findings/skyplace.md)談的是 reference 選取、操作和存檔持久化；
[Lilac 研究](../../../tool-survey/findings/lilac.md)談的是 Papyrus 測試結果。兩者與本題的對話上下文
觀測層相鄰，沒有必要在此再做一套同樣的工具盤點。
