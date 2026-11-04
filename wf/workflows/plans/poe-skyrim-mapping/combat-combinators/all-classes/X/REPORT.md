# 特種 X：三型設計候選

Done when: 通用4A2H與X1/X2/X3各6A2H共30條、每型至少3獨特A及2獨特H、五項驗收完成；僅交可review設計，不批准source或runtime。

已交 rules.json、subtypes.json、parameters.json、feasibility.json 四張 wf-table/1 與本報告。build.py 是可重現產生及結構核對的小script。全在本領地獨立工作目錄，沒有PoE ID/placement，沒有改原圖或legacy。

X1以切入返程錨為核心，第二High將返程權押在原生打斷與可取消起手上；X2從拉向自己改為向另一敵交接位置；X3先命中獵物再布專屬觸發陣，避免雜兵耗陣，但其餘敵可以通過；第二High則以既有原生重施入口犧牲原陣提前引爆。沒有新增選單或教新法術。X3H0須改原生trigger filter而非只做記帳，因此能力未證。

固定五驗收：

1. 結構核對PASS：30個唯一rule ID；class-common獨立4A2H，三型各6A2H，每型宣告6獨特A/2獨特H，subtype-shared=0。High逐條列選前後、收益、代價與非數值理由。unique以同職兄弟玩法核對，不表示底層primitive專用。
2. 各row有觸發、actor/target、owner、刷新消耗、成本時點、失效、混買、正負例；純本次快照XCA1/X2A6明列無狀態。狀態型附有死亡/離戰/Reset/load及expiry清理。幾何、免疫或事件歸因未知則不執行依賴能力。
3. 不改normal atoms/per-share/1-3-5。新增F/R/Q/C/T/P皆pending_review；無新強度、成本或期限數字。原生付款仍沿原交易；附加效果同快照足額提交，失敗不吞附加狀態。無職業鎖。
4. 本職僅一通用池。跨職canonical只在feasibility提出primitive對照，不合併狀態、不修改全局。D1 current portable lease及C3付費印不被XCH2移轉；model舊多giver最早到期提案不覆蓋守衛current。
5. 四張同質表以tabledb Python API寫入並讀回；30條均compiled=false、runtime=0。檔案均<1MB、全線<150KB。只寫獨立工作目錄，不改repo/DB/live/source。

最需主管仲裁：X2救援推離與H1交接若同筆衝突，暫拒附加方向而保留原生；X2搬獵物入X3陣可觸發但不領「自行誘入」回氣；XCH1扣留X1/X2/X3回流而不憑空增加本金。位移、碰撞、免疫、落點、取消及獵物陣trigger/引爆均缺能力證據，沒有任何ready宣稱。

依據：roster.json X1–X3原提案與boundary；template-requirements.md獨特/通用池及High分類；model.md事件快照/生命週期；inscription-sample/README.md H0與能力前置。已親讀共同brief及指定wf規矩；具體來源位於repo combat-combinators目錄，未複製既有payload。
