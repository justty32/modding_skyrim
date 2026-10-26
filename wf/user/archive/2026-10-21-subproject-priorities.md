> 封存 2026-10-26：盤點已用完（使用者其後已選 DSP 與 houseCARL）

# 哪個子專案值得繼續

本頁保留開發前的盤點快照。使用者其後已選 DSP 與 houseCARL；最新離線成果與續接位置見 [修復與收尾記錄](../2026-10-21-offline-fixes.md)。

**先選 darksouls-port，把北方不死院現有場景打磨好。** 你曾明確表示不滿意；現在已有定位過的地板消失修正候選，但還沒完成實機驗收。下一輪只處理這個缺陷，確認多角度可見、碰撞與戰鬥／跟隨沒有退步，再決定是否擴內容。

想換方向時，有兩個次選：

- **想玩隨從劇情：Sofia。** Act1v2 已裝進主 profile，現在應驗女巫／Carene 分支、動作與嘴型；不是重寫四幕。v2 有一檔缺嘴型，後三幕也尚缺嘴型。
- **想先修日常工具：houseCARL。** 原版 Gold001 名稱查詢在 Linux 可重現失敗，小麥另有亂碼。可以做一輪範圍明確的修補，不必連帶升級整套上游。

其他專案先隨需求使用：ModForge、converter、agent-bridge 都已有可用能力；game-data、voicegen 等內容真的需要才補。Godot 改架構、scene 3D 預覽與 DaylightDungeon quest engine 暫時缺少值得現在投入的新需求。

11 個開發 repo 與四條主線都已查過，現役規矩亦已由 agents 親讀。離線測試有通過，但上述遊戲內結果尚未重新驗證。完整證據、測試範圍與過時待辦在 [盤點報告](../../workflows/investigation/findings/subproject-priorities-2026-10-21.md)。

建議下一步：選 DSP 的既有消失點，做一包來源版本固定、可對照驗收的修正候選；本輪尚未開工或部署。
