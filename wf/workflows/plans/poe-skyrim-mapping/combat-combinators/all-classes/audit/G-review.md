# G 獨立玩法審核

結論：需修同一自救 settlement 的兩處契約，未要求新能力或數值。30 行與 legacy SHA 已由主管 collect 驗證；本審核逐讀16新行與原G1契約。G2實傷帳/反打兌現與G3交鋒/停手/accepted起手消勢構成真玩法差異，非改名倍率。

1. G2A5：trigger 要求 A1 正HP已成功提交，effect 卻把該HP一部分改成SP。應改為同一次自救 precommit 分配，先固定可兌傷帳、HP可容容量與SP分流，最後原子提交；不得提交後回收HP。保留無H1且滿血不憑空給SP。
2. G2H1：轉SP收益僅 high_gain 有寫，trigger/effect 只有外援治療清帳。請加入與A1同次自救的 precommit 餘額轉SP分支，明列與A5不可重複用同一份帳。接受外援實回正HP後清帳、零實回不清仍保持。

可合併為一個 settlement 修正。參數維持 pending_review，compiled=false/runtime0；DBH1僅替換原生重擊SP、額外費仍支付，GCH2排真格擋來源；不要求新classlock/menu。G2A2消舊帳後同筆實傷如何交H0建新帳可沿既有交易次序明述，未列阻擋issue。

幾何獨立待單writer驗證；ordinary global_shared_connector 可保原ID/固定原payload且只買算一次，不算規則slot；H0>8ordinary只warning。

覆核：已親讀主管送回的上述修訂行，原issue均消除；設計語義通過，source/runtime/幾何仍待各自gate。
