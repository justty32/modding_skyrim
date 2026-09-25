# Sofia Follower v2.51 — scene-anatomy

[返回入口](../sofia-follower.md)

### 2. Scene 解剖

Skyrim 的 scene = **phase 序列**，每個 phase 綁一個 action（Dialog / Package / Timer），actor 透過 alias 索引引用，並帶 behavior flags 控制中斷行為。

#### 範例（主貼）：`JJSofiaMainQuestDialogueScene` `[020468]`

來源：`/tmp/mfdump/sofia.txt:7702`–`7722`。**1 actor / 17 phase / 17 action**，是「一句台詞一個 phase」的線性獨白：

```
Scene JJSofiaMainQuestDialogueScene
  script: SF_JJSofiaMainQuestDialogueS_02020468 [1 prop(s)]
  scene: quest=JJSofiaMainQuestDialogue  flags=Interruptable  1 actor(s), 17 phase(s), 17 action(s)
    actor alias #0  behavior=DeathEnd, CombatEnd, DialoguePause
    action: Dialog alias #0 phase 0  -> topic 020469:SofiaFollower.esp (Neutral)
    action: Dialog alias #0 phase 1  -> topic 047839:SofiaFollower.esp (Neutral)
    action: Dialog alias #0 phase 2  -> topic 0500E1:SofiaFollower.esp (Neutral)
    ...（phase 3–15，每行 Dialog alias #0 -> 一個 topic）...
    action: Dialog alias #0 phase 16 -> topic 06B15B:SofiaFollower.esp (Neutral)
```

要點：
- **actor alias #0 的 behavior flags**：`DeathEnd`（actor 死則 scene 結束）、`CombatEnd`（進戰鬥則結束）、`DialoguePause`（玩家發起對話時暫停）——這是「演出中可被打斷、不卡死」的標準三旗標，全 mod 幾乎每個 scene 都用。
- 17 個 phase 都是同一個 actor（alias #0 = Sofia）對著玩家連說 17 句；scene 本身只負責**排序與節拍**，台詞內容在各 topic 的 INFO 裡。
- scene-level `flags=Interruptable`：整段可被中斷。

#### 範例（對比）：`SofiaWeddingScene` `[051BF6]` —— 多 actor 編排

來源：`:7805`–`7827`。**3 actor / 20 phase / 17 action**，flags=StopQuestOnEnd：

- actor alias #0（Sofia）、#2（Crooked Priest）、#1 交錯念誓詞（phase 1 Sofia → phase 4 Priest → phase 5 Sofia …），中間穿插 `Package alias #2 phase 2`、`Package alias #2 phase 17`（NPC 走位）。
- 證明 scene 能做**多角色對拍 + 走位**的完整演出，且 phase 數（20）> action 數（17）——有些 phase 是純等待節拍、不掛 action。

#### scene 的三種 action 類型（與 ModForge 對齊）
全 28 個 scene 只用到三種 action：
1. **Dialog**（最多）—— 綁一個 dialog topic 念一句。
2. **Package**—— NPC 做動作，如 `JJSofiaCastNudeBomb`（`:7750`，1 phase 1 action = Package alias #0）、`JJSofiaMountHorseScene`/`DismountHorseScene`（`:7797`/`7801`）。
3. **Timer**—— 停頓。見 `JJSofiaDrunkScene` `[07387F]`（`:7875`）：3 phase / 4 action，混用 `Package alias #0 phase 0` + `Timer alias #0 phase 0` + `Dialog phase 1` + `Timer phase 1`，flags=**RepeatConditionsWhileTrue**（醉態循環）。

comment scene 的共同模板（`JJSofia*SayComment`）：2 actor（Sofia + 目標 NPC）/ 2 phase，phase 0 Sofia 開口（情緒常為 Disgust/Anger）→ phase 1 目標 NPC 回嘴，flags=`BeginOnQuestStart, StopQuestOnEnd`（quest 一啟動就演、演完關 quest）。例 `JJSofiaNazeemSayComment`（`:7744`）。

