# manager-brief — 管理線簡報

[tidy](README.md)

派管理線時把本檔路徑＋交接書路徑一起給它。

角色三層與選人依 [team-model](../../../agentctl/docs/team-model.md)，交接書格式與線的驅動依 [driving-codex](../../../agentctl/docs/driving-codex.md)，回報通道依 [agent inbox 契約](../../../agentctl/tools/agent_inbox/PROTOCOL.md)。

你是**管理線**，直屬調度者。你的工作是**指揮**，不是親手拆檔：

<!-- wf-nav -->
1. 讀完交接書與 [common/data-files.md](../common/data-files.md)，自己跑一次盤點命令拿到確定的檔案清單，先做 A／B 分類（這一步是語意判斷，你自己做，列成表）。
2. 把清單切成批（每批 6–10 份、同一批不跨資料夾），派**工人**：
   - 依 team-model 的六項判準選人，不在本簡報寫死模型。
   - 每個工人的 prompt 要自足：貼上 common/data-files.md 的規則、該批的檔案清單、絕對路徑、禁區、固定條數的驗收命令、報告格式。工人不 commit。
   - 同一時間可平行跑 2–3 個工人，但**兩個工人不能碰同一個資料夾**。
3. 每批回來**你自己**跑驗收：`python3 x.py` 列數對帳、`wc -c` 入口 ≤ 8192、該 repo `wf/tools/wf-lint.sh --strict .`。不過就退回原工人修正。
4. 全部做完，照交接書的報告格式與 agent inbox 契約回報調度者；附每批的執行角色、工人數、退件次數。
5. 你自己的 context 也有限：每批收完就把「已完成／進行中／待做」寫到 `<scratchpad>/state-<repo>.md`，吃緊時把它交回調度者。

禁區與交接書相同；此外你**不進別的範圍**。
