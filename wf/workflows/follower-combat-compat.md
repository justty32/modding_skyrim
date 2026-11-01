# follower-combat-compat — 自訂隨從與戰鬥框架相容修補

[WORKFLOWS](../WORKFLOWS.md)｜[INDEX](../INDEX.md)

處理自訂隨從與成長／技能／裝備 AI 框架疊加後，反覆換手、收拔武器、不能劍法混用或原生戰鬥選擇遭覆蓋的問題。每位新隨從重新診斷，不把前一位的修補全隊套用。

**何時用**：已裝隨從有上述症狀；特定隨從要保留成長能力並恢復原生選擇；新隨從 intake 完成後與框架共用的唯讀相容盤點。
**何時不用**：中文 UI 破版 → [feature-dev](feature-dev/README.md)／[localization](localization/README.md)；CTD／凍結 → [crash-triage](crash-triage.md)；尚未完成取得安裝 → [nexus-intake](nexus-intake/README.md)。

## Done when

- 私有案件 REPORT 有本人與 winner 定位、版本來源、分層因果鏈、未驗缺口及已授權目標。
- 配置或 source patch、離線測試／review 結果、build provenance 與成品 hash 均有檔案可查。
- 部署 manifest／dry-run／備份／revert 路徑存在，profile 與檔案 winner 驗證命令通過。
- 開始前固定的驗收項逐條附 fresh-load 證據；未完成的實戰／人眼項已記 WAIT_USER，未冒稱通過。

## 流程

### 1. 先定目標與範圍

記錄使用者要原生混用、純近戰或施法，以及必須保留的成長、能力、對話、跟隨與裝備選擇。已有任務授權就繼續做必要的小型可逆細節，不反覆請准；新增目標、不可逆動作或缺少授權的 live 操作才確認。不得順手導入 NFF、刪光法術、重設角色或改全隊角色。

診斷走 [investigation](investigation/README.md)，已知修改走 [feature-dev](feature-dev/README.md)。跨 repo 或交冷啟動 agent 才另用 [patch](patch/README.md)，不為普通同 repo 修復多包一層。

### 2. 唯讀定位本人與真正勝出者

先查 [工具索引](../../agentctl/docs/tool-index.md)，使用現成 whichmod／profile query／ESP reader／houseCARL 工具。區分本人 persistent reference、NPC base 與臨時複本；記原 mod、NPC winner、Class／CombatStyle、已知法術、當前武器與背包候選、種族及裝備限制。

追 QUST／alias／NPC 的 VMAD 綁定，查腳本實際 winner 與會執行的裝備／施法／戰鬥事件呼叫。字串搜尋未命中只代表已查範圍，附帶 PSC 不自動等於現役 PEX；未綁定死腳本不能定罪。核對現役框架、角色、explicit pools／鎖定設定與重複 DLL，不能只看資料夾名或舊快照。

角色配置用穩定的 **plugin filename + local FormID**（如 `ExampleFollower.esp|005900`），禁止保存會隨 load order 改變的 runtime 前綴。核對工具要求的是 base 還是 reference，不混用；私有 runtime ID、save 與完整 load order 僅留案件證據。

### 3. 釘版本，分開三層歸因

對帳已裝 archive／DLL SHA-256、source commit、host／build flags、相依版本與可用 symbol／manifest。README 是設計敘述，仍須讀現役相符 source 的實際分支與 hook；同名版號或可編譯不代表重建了現役 DLL。無法建立對應時明列缺口，不拿舊 snapshot 整包降級替換。

分別追 **成長／點數**、**框架 ability 主動行為**、**普通武器／法術與 CombatStyle AI**。逐入口列出誰卸裝、誰挑候選、誰改 style、更新間隔與停止條件；存檔快照不等於當前記憶體。候選鏈、靜態證據與已復現原因分開寫，保留原生對話／跟隨腳本與衣服選擇。

### 4. 先設定，後最小 source 修補

已有經 source／實測證明符合目標的單角色設定，就用設定。不能把「Mage」「固定武器 pool」當成劍法混用已完成，也不能以全域關閉限制代替單角色方案。

需要 code 時在隔離 source/build 目錄改最小入口，review 跳過哪些 loadout／style 分支、是否清除舊 cache／battle lock，以及哪些 ability 仍保留。採多 NPC **明列白名單、逐角色 opt-in**，預設空集合，不自動加入新隨從或全隊；每個新增角色都重跑本流程。explicit pool、特殊硬裝備角色或不支援 host 的衝突須拒啟並記 log，不默默忽略玩家選擇。

配置的檔名、section、key、分隔符、重複／無效值處理及生效時機以交付 source／測試為準，寫進成品 SOURCE／用法；不得猜設定名稱。只支援 startup/fresh-load 的設定不做 runtime 熱切換。

Paths 1.2 本案修補的契約是獨立 `SKSE/Plugins/FightWithMePaths_NativeCombat.ini`，`[NativeCombat]` 下 `sActorBases=`，值為分號分隔的 `Plugin.esp|十六進位localID`，最多 16 個唯一 NPC base。空值停用；無效／找不到／非 NPC 項警告略過、重複去重、不支援 wildcard；整值超過 4094 UTF-16 code units 截斷時整值拒絕。於 DataLoaded 讀取，修改後須完整重啟，不支援舊單數 key。確切核准名單與凍結版本見私有交付證據，不把示例角色當成已授權對象。

離線驗證至少涵蓋：白名單命中／未命中、多角色／空集合／壞值、explicit pool 拒啟、原 host／特殊角色不變、成長與 ability 保留。檢查器餵壞輸入證明能紅；matching toolchain 產出真正 PE DLL，portable harness 不能冒充 DLL build。凍結 patch、review、命令／exit、source parent、依賴與 artifact hashes。

### 5. 停機部署與回退

改 live mods／profile 接 [profile-change](profile-change/README.md) 與 [safe-apply](safe-apply.md)：當下 envsnap、MO2／遊戲全關、先 desktop 後 game 鎖；已有 dirty 先審閱並保存，不 stash／revert 別人的寫回。

以獨立覆蓋層部署，不覆寫原版或既有 user 設定；manifest 只列本案 payload。先 dry-run 審變動與 hard anchors，備份到非 tmpfs 磁碟，寫後對 hash／winner／啟用集合／missing masters。新增 plugin 才加對應 gate；純 DLL／INI 不虛構 plugin 變更。MO2 循環後重驗，保留 profile 分支晉升規則。

REPORT 寫確切備份及 `layer_apply.py --revert` 所需 manifest；多輪反序退回，遇後續漂移先審不 force。回退後驗原 DLL／設定 winner、profile 與啟用集合，再重啟；不以刪存檔或重設角色作回退。

### 6. 固定驗收與版本追蹤

事前固定本案驗收條數，接 [runtime-qa](runtime-qa/README.md)。分開記：DLL／配置載入、fresh load 後目標 actor opt-in／拒啟 log、普通戰鬥選擇、成長／能力、對話與裝備選擇保留、非白名單對照。每組用新的 log window；主選單 smoke 不證明 actor 生效，actor enabled log 不證明劍法混用實戰正常。

讀玩家 save 或引戰必須在已授權範圍；保留原 save pair、hash 與備份，不把測試世界存回。未獲 runtime 授權先完成離線交付；反覆收拔是否消失、劍與法術是否正常使用等畫面／手感由使用者驗收，寫清場景、應見與不應見行為。

成品 SOURCE 記上游版本／commit、patch、toolchain、DLL/config hashes、適用 host、白名單與限制。上游／隨從／其他裝備 AI 更新時重新對帳，不盲搬 DLL；依 [mod-update](mod-update.md) 重驗衍生層。public 母 repo 只留通用流程，完整原檔、save、runtime ID、load order、log 與個案產物留 private repo。

## 交接

案件可參考 private 的 [Paths 歸因](../../agentctl/handoffs/home-2026-11-01/varinia-paths/PATHS.md)、[混用方案與版本核對](../../agentctl/handoffs/home-2026-11-01/varinia-paths/MIXED.md)、[原隨從腳本調查](../../agentctl/handoffs/home-2026-11-01/varinia-paths/VARINIA.md)、[部署與驗收界線](../../agentctl/handoffs/home-2026-11-01/varinia-native-combat/DEPLOY.md)；它們是個案證據，不是新角色的預設配置。

待人眼驗收記 [WAIT_USER](../../WAIT_USER.md)；Skyrim 跨場續行記 private agentctl 的現役交接入口。修補完成不自動擴至其他角色。
