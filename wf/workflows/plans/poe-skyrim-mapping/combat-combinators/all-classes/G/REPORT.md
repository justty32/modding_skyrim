# 近衛三型設計交付

Done when: common單池4A2H、三型各6A2H合30條、每型至少3uniqueA/2uniqueH，原14條精確引用不改；新增規則含交易、狀態、互動及正負例，High真改操作，僅設計且compiled=false/runtime=0。

已完成30條：14 immutable legacy references加16新候選。G1浪潮鬥士維持每owner單focus及DBH1 accepted起手代付原費；G2浴血決鬥者以實傷來源帳→反打開自救→再擊交付，接受外援可結束本輪資格；G3藏鋒者由真交鋒→停手成熟→起手花勢，另一High改成一次攔截並禁重擊。

固定五項驗收：

1. 數量PASS：common4A2H只有一池；G1 6A2H中unique4A2H，G2/G3各unique6A2H。DBA4/G3與DBA5/G2/G3原共享宣告保留，仍以原DBH0前置混買引用，不複製新rule、不充兄弟六A。legacy SHA依ensure_ascii=False、sort_keys、compact JSON UTF8逐列重算核符。
2. 可審性PASS（設計）：新16條逐條有觸發、actor、target、owner、消耗、期限清理、混買及具體正負例；4個新High有選前後、收益、代價、非純數值理由。原14條欄位依來源dereference審查，未補寫payload。
3. 數值邊界PASS：普通atoms/per-share/1-3-5不動。所有新成本、強度、期限為符號pending_review，無新數字、職業鎖或選單。舊數字不重新裁示。
4. 共享邊界PASS：跨職canonical只在feasibility提案；GCA2/DCA1原合份一次不動，D1 portable多giver current不受model舊最早到期提案覆蓋。GCH2使G3雙端格擋來源無效；GCH1不能被新兄弟偷繞失衡禁制。
5. 交付PASS：四JSON皆wf-table/1並以tabledb API讀寫，獨立工作目錄五交付檔加一重建驗證script，合計低於150KB；無PoE新ID、幾何/keystone/原圖修改、source/runtime操作。

能力結論：全部design_candidate，非ready。主要缺口是attack identity/accepted及取消、來源明確的原生precommit與final HP/SP實付、外援正HP提交及來源、一次傷害撤銷、原生動作資格控制與互斥消耗；不能用補血或AttackCost query充已完成。詳見feasibility.json。

交付：rules.json、subtypes.json、parameters.json、feasibility.json及本報告。build.py可重建並檢查30 ID、legacy SHA、compiled/runtime與容量；未跑runtime。

獨立audit修正：G2A1/A5/H1統一single precommit，先界定可兌額B、HP容量份額P、A5分流D、H1餘額E=B-P，再一次提交HP=P-D及兩互斥來源的SP；不得事後撤HP。滿HP時P空仍可由H1處理E。只有共同提交正HP或正SP才消帳，雙零/失敗不消；外援實回正HP後清帳保留。參數全部pending_review。
