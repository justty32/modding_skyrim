# 狙擊 R 設計交付

Done when: 單一common4A2H，加R1弱點獵手／R2破群射手／R3蓄彈弩手各6A2H，共30條；unique、原生來源、owner生命週期、混買與High前後玩法可review。僅本獨立工作目錄，compiled=false、runtime=0。

已交付rules.json、subtypes.json、parameters.json、feasibility.json，另有可重產的build.py。R無凍結legacy需接入；未引用或改寫G1/D1/C3 payload。讀過共同brief、根AGENTS、wf派發／user／data-files／planning／investigation、roster的R1–3、model、template-requirements及刻印README/rules/candidates對照。原圖ID／座標／受保護點與normal atoms/per-share/1-3-5份均未動。

R1以owner單focus追可驗原生危險起手，H1轉標只搬剩餘期限，不能同箭轉標又吃新標。R2先打固定位置錨、下一箭才兌現次要敵區域傷；H1改線廊與友軍遮線，不偽裝爆炸箭或貫穿箭。R3真裝填後站定蓄待射，移位可攜；發射accepted即耗且射空照耗，命中才給針對該敵下一次朝本人可中斷近戰起手的撤退攔截券。H1可把待射改花在原生弩bash應急，放棄下箭與撤退券；不是原生彈匣，也不產生多發箭。

RCH1以站定瞄準抗一般受擊中斷交換格擋／近戰／bash資格；硬控仍中斷。RCH2已明訂無H時卸遠程裝備清已射箭R交付資格；有H只保已射projectile固定包及交付資格，owner focus/錨/待射照清，Reset/死亡/離戰/存讀仍清包。發射快照守恆不是High收益，新增的是卸裝資格例外。R3H1在GCH1下先停整附加分支，不消待射、不申請stagger，原native bash照常；R3A2箭stagger不受此近戰禁令。

五項驗收：

1. 結構核對：common獨立6條；R1/R2/R3各8條，全部6 unique A／2 unique H，subtype-shared=0；不以common充unique。High皆有動作資格、狀態出口、目標轉移或幾何集合差別，非換倍率。
2. 每rule含trigger、target、actor來源、owner、刷新消耗、失效、混買、正負例；High具before/after/gain/cost/not-numeric。R3H0單獨已有延遲攔截收益，不是要再買A才有效的空載具。
3. 全部新距離/期限/強度/成本符號在parameters.json列pending_review，不填新數字。所有能力design_candidate；未採用新數值，未加選單/職業鎖。
4. common只一池；跨職canonical只提主管；R2派生傷不觸發R1標記或R3退款，R3 bash不是遠程交易。model舊多giver建議不覆蓋D1 current portable lease。
5. JSON皆wf-table/1，經tabledb建立/重讀；各檔小於1MB，本領地總小於150KB。compiled=false/runtime=0；僅寫獨立工作目錄，未動repo/source/runtime/DB。

主要缺口是原生遠程accepted／reload／彈體交易歸因、敵方起手成功取消與硬控分類、SP真實付款及射空完整性、R2空間/友軍遮線。RCA4與R3回氣類沒有原生實付就不生資源；R3H0起手取消未證就保持pending，不偷換成after-hit減傷。
