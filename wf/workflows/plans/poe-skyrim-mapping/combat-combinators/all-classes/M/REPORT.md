# 醫療 M 設計審稿

Done when: class-common 4A2H＋M1/M2/M3各6A2H共30條、每型至少3A/2H玩法unique，五項驗收可核；僅獨立工作目錄、無runtime。

交付 `rules.json` 30列、`subtypes.json` 3列、`parameters.json` 未定參數、`feasibility.json` 缺口與跨型仲裁。M沒有舊樣板legacy ID，故30列全新設計。warden current樣板僅對照欄位及portable護援邊界，不複製成醫療既有能力。

M1急救師以一筆主動恢復預算分流，H1改為保持原生channel才能送完的接力；M2戰地導血者先手選援者、攻敵、再主動治同人另付兌現，H1轉援改綁指定敵的交接；M3續療師先花施法與預付恢復額存印，印抵未來敵傷，H1危急時由再次主動施法解印。M3始終拒絕死亡Actor，印不夠抵的致死傷正常致死，沒有復活。

單筆B_native加合法已購候選加成及另付新增額成B_effective；舊queue/舊印先摘原帳後以prior_paid轉入，保留來源ID，只分一次，主目標原效果需被替換。來源逐row分登記、本人原生攻敵、主動恢復、敵傷消池及退款階段，合成輸出不再觸發；多giver不借狀態；M3存印先扣額，M1再分剩即時額；M2機會只由原生主目標兌現。M3A3對預付池的限定折耗為獨立待審強度函數，不是改normal atom。所有新成本、期限、門檻與強度均只保留符號及pending_review。

五項驗收：

1. 30=common6+子型24；common僅一池，subtype-shared=0。每型6A/2H皆聲明對另兩型unique，沒有拿common充數；High逐條列選前後、收益、代價及非純數值理由。
2. 30條皆有觸發、actor/target、state owner/刷新消耗、付款、失效、混買與正負例。所有H0無自身A前置，H1與子型A列stable requires；無PoE ID。
3. 不改normal/1-3-5份；全部參數null/pending_review。未新增選單或職業鎖。
4. 原生恢復帳canonical只提給主管，未寫全局。守衛current portable lease/合係數不被model舊最早到期覆蓋；醫療預付池多giver順序只為新提案。
5. 四份JSON皆wf-table/1並以tabledb讀寫。rules/subtypes/feasibility compiled=false、runtime=0；能力均缺證未ready，僅本M領地六檔。

能力缺口集中在原生主動恢復與channel預算collector、來源資格、原生付款替代/退款、正HP precommit預付池。readiness五gate只作缺證依據，不把現有hook宣稱ready。幾何待single owner，不阻礙設計審稿。
