# 先鋒設計候選

Done when: common 4A2H＋三型各6A2H共30規則，完整交易／狀態／正負例與高階打法；只用獨立工作目錄，compiled=false、runtime=0。

已交 [rules.json](rules.json)、[subtypes.json](subtypes.json)、[parameters.json](parameters.json)、[feasibility.json](feasibility.json)。本職沒有既有legacy rows需要重包；守衛／刻印只作對照，未修改。

固定五驗收：分帳30=common6＋三型24；各型6A2H全為兄弟對照unique，shared0，common不充unique。每列明列actor、target、owner、刷新／消耗、失效、混買、正負例；八個High均有選前後、收益、代價與非純倍率理由。強度／期限／新付款只留pending_review符號，既定atoms、per-share與1/3/5份不動。common只一池；跨職canonical只有proposal；portable守衛不被舊model最早到期假設覆蓋。四JSON皆wf-table/1經tabledb寫讀，獨立工作目錄且無PoE ID、source、runtime或DB修改。

V1是單一獵物的戰果續戰，助攻須真貢獻receipt。V2以原生持續支援施法的MP實付換隊友SP／MP，排本人payer與支援施法回流，和S2的HP／防護不同。V3是指定召援→本人近戰→同召援的實際命中鏈；和S3本人法術消契印／召喚護援不同，不下AI命令。

重要缺口是原生accepted攻擊與付款／揮空歸因、持續支援施法receipt與攻擊資格控制、召援owner-instance與助攻／失援分類。尚未證據充分；資料欄完整不等於引擎已支援。VCH1提前解除本人原生恢復期需獨立資格primitive，缺證維持拒購，不以送攻速替代。

依據：母repo combat-combinators/template-requirements.md「每型unique／common」、model.md「事件快照與來源」，roster.json V1/V2/V3/S2/S3；warden-sample/README.md「可攜狀態與結算」；inscription-sample/README.md「H0不是免費附送的付費庫」；wf/workflows/plans/poe-skyrim-mapping/combat-combinators/all-classes/implementation-readiness.md五gate。幾何由主管單一owner處理，不擅配PoE ID。
