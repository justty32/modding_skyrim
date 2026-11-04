# 術師三型可審稿

Done when: 一個術師common池4A2H＋三型各6A2H共30條；每型至少3獨特A/2獨特H；既有14條精確引用、其餘16條具完整交易與正負例，未定參數不填數值，全部compiled=false/runtime=0。

完成30條：14個immutable legacy reference＋C1/C2各8條新design candidate。common沿原CA1–4、CH1–2；刻印IA1–6、IH0–1只引用，不改payload、17候選或保護節點。C1蓄能、C2導流各6獨特A/2獨特H；C3刻印4獨特A＋IA3/4兩shared候選、2獨特H。IA3/4對兄弟是可選同ID承接引用，仍需IH0本人印，沒有複製或塞進common，也不重複算新兄弟6A。原C1_energy/C2_conduction alias只在摘要映射穩定C1/C2。

C1為owner自持的預付原生法術lot；雙施準備、單施命中交付，H1將整庫交付改為按準備序逐lot支取。額外投入、位移、異學派序、緊急恢復、傷害前燒庫防護與餘筆條件各有獨立交易邊界。C2不保存法傷本金，而在原生首擊precommit把同一有限載荷沿鄰敵傳遞；H1保存有向敵序，改以首靶選入口。六A分別處理根敵集中、relay牽制、當跳轉MP壓制、斷流成本回收、前次relay改選根與固定edge續壓。

最重要的混買順序仍是候選：C1準備無hit，不產印或導流；CH1只承接後續交付命令；實際命中若IH1先存D，就沒有同筆即時餘量讓C2分流。所有階段必須保存native-origin與付款身份，合成relay不得自造cast或重貼印。AoE、concentration、多命中未證單一完整載荷邊界即拒絕，不猜現有hook可做。

五項驗收：

1. 數量與分帳已由腳本/tabledb實讀斷言；High記前後打法、收益、代價與不能以倍率取代的交易/拓撲變化。legacy High亦原樣引用。
2. 每條新規則有觸發、actor來源、target、owner、刷新消耗、付款、失效、混買及具體正負例；既有資料以SHA dereference，未偷補寫原payload。
3. 新數值僅參數符號pending_review；normal atoms/per-share與1/3/5份不變，無新選單/職業鎖。IA1原生實付20%、IA4自身final maxMP5%與IH0 native-first不動。
4. common只有一池；C2A2與IA3輸出牽制合併、C1A5與守衛防護順序只提主管canonical proposal。model舊多giver最早到期不覆蓋current守衛portable lease合份。
5. 五份同質資料均wf-table/1、經tabledb讀寫；SHA採ensure_ascii=False/sort_keys/compact UTF-8。只有本獨立工作目錄，無source、runtime、DB、profile、幾何變更；總容量低於150KB。

關鍵能力缺口是accepted原生付款與未送達payload攔截、自持lot及typed防禦前commit、可證cast身份和有限導流/visited/視線。未證不得ready。詳細依存、參數、反例與拒絕條件見資料檔；build.py可重生與核對，不對repo施工。

獨立audit修正：C1無target lot只保存owner側CA1等既定快照，CA3留pending_target。合法實際交付敵prehit才讀敵MP/maxMP，依原CA3契約判一次，於IH1存D前完成並保存判定身份；IH1釋放不重讀/重乘，無敵prehit的治療/防禦改寫不預套CA3。缺該精確邊界仍pending不ready。14個legacy reference及原CA3數值/契約不動。
