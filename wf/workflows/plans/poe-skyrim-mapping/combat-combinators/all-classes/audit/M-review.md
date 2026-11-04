# M 獨立玩法審核

逐讀30行。M1單預算主/旁分流與channel延後、M2主動支援單援者→敵擊機會→主動另付兌現、M3預付印抵傷與主動解印，均形成玩法。

需修2項：
1. 共用actor_source只允許主動HP恢復法術，與M2原生武器/攻擊法術建機會及M3敵傷消池衝突；按row/階段明列合法source，合成仍不再觸發。
2. 共用守恆式B定義原生值，漏合法候選加成與舊queue/舊印轉入。明分B_native、候選調整後B_effective與prior-paid轉入ledger，再禁止重複分配。不要求刪加成/新增成本或新值。

M3抵傷在守衛current護援後，不把giver池排序套D1合係數lease；HP自付不算敵傷也不能由印免付；死亡不復活。能力待證、compiledfalse/runtime0。

覆核：已親讀逐phase actor_source與B_native/B_effective/prior_paid ledger修稿，兩issue消除；設計語義通過。
