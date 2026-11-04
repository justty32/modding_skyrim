# C 獨立玩法審核

逐讀16新行並對原CA3/CH1契約。C1多lot預付庫/FIFO支取與治療/自保轉換、C2守恆導流/固定有向序形成真玩法；C3原14不可改。

需修1項：共用compat把CA1/CA3一律定在原生載荷形成時計，C1H0無target準備時無法取得CA3實際敵prehitMP比例。拆owner輸出與recipient條件：CA3待合法實際交付時取得敵prehit快照、IH1存D前計一次，無targetlot保持未判，IH1釋放不得重判。原值與契約不變，source邊界未證就pending。

IA1 native_paid20%與IA4本人finalmaxMP5%不變；IA3/4只需IH0，不把庫/route當印。C2relay不產新nativehit，IH1攔root存D無即時relay，C1A5/D1次序與C2A2/IA3 canonical仍proposal，不能宣布ready。

覆核：已親讀主管送回修訂行，以上語義issue均消除；source/runtime/幾何仍分層待證。
