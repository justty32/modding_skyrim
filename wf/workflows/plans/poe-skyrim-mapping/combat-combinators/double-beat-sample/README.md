# 近衛通用＋浪潮鬥士單型真圖候選

[給使用者看](../../../../../user/2026-11-04-guard-double-beat-sample.md)｜[原生SVG](region.svg)｜[原節點](region.json)｜[19點填充](candidates.json)｜[14條規則](rules.json)

使用者正式命名「浪潮鬥士」，表示一浪接一浪；G1／DB* IDs與double-beat-sample路徑保留。

Done when: 19個真連通候選保留ID／座標／連線／類型與原weight；近衛common4A2H與浪潮6A2H分開計數、後者4A/2H有本型辨識度；H0先可達且6A/變形H都需它；普通照已定atom每份；一場原生操作情境與互動代價可審，資料／拓撲／前置精確核符。狀態prototype_pending_user_review_not_runtime，使用者看過再決定，不接新engine。

## 真區域與前置

固定來源為GGG3.29.1、SHA `7e9f755e33152129ebf36c2ebdad639c527e4ad70d274b1fefb860f30ca01122`。19selected＝15 normal＋4 notable，另外只保start與one-hop context共36資料列；不搬整個原dump。原有48 keystone政策38/10不變，raw source的57 keystone是另一集合；本區未填任何keystone/mastery/socket/ascendancy。

H0=34009，入口50986→47389→42911→40867→476→34009；四個必經normal都不gate。49538是變形High。近衛common H放48807／48438，可經50986→39725→63649→49806→6580→48807→25933→48438，不依接拍。

18302與28265可從common繞達，正好證明『只靠圖鎖』不成立：6個DBA與DBH1都要AND已購34009；common無接拍依賴。這是候選資料前置，不表示現有程式已認識新rule ID。

## 數值與狀態契約

五ordinary：47389 HP+5、42911 SP+5、40867 HP+5、476 SPREGEN+10%、39725 AR+6，皆原normal一份；沒有自造普通尺度。10個A也都原normal，n1示例可直接看。四High保原notable weight3，整包mechanic份額尚待審，不留原GGG數值再免費附加能力。

DBH0是每owner一個focus_target／expires／首擊來源的狀態，不是每敵一份印。需要可歸因且不同的原生攻擊實例，不把同一揮擊多target／多hit當多拍；不以固定CD猜次序。普通換敵消舊、不自動給新拍；普通揮空無收益／不刷新。第二普通被同敵擋時，只有DBA6足額新付款才保原期限。DBA1＋DBA5同路一次consume；重擊／換敵／轉守不兼拿普通收益。

DBH1在accepted重擊啟動消機會代原生SP，並保本次context供DBA2判同敵；揮空／取消亦花。原生SP啟動門檻、一次付款與取消生命周期未證，不在AttackCost query中花狀態，也不把先扣再退當替代付款。

GCH1使GCA3無stagger可增；GCH2只改本人近戰不可被擋與本人不能擋，不影響敵擋其他隊友，並使GCA2／GCA4／DBA4／DBA6失去觸發。所有新增A倍率／資源比例／期限皆試案；原術師MP20%／maxMP5%裁示不自動批准近衛SP數字。

## 原生依據與未驗

[固定CommonLib TESHitEvent](https://raw.githubusercontent.com/CharmedBaryon/CommonLibSSE-NG/7a60f4de794095d7b0f8928d1b930a52e9a7da83/include/RE/T/TESHitEvent.h)提供cause／target／weapon base與power／bash／blocked旗標，沒有attack transaction、實傷或左右手實例。[TESObjectWEAP](https://raw.githubusercontent.com/CharmedBaryon/CommonLibSSE-NG/7a60f4de794095d7b0f8928d1b930a52e9a7da83/include/RE/T/TESObjectWEAP.h)可辨近戰類型；null不直接當徒手。[HitData](https://raw.githubusercontent.com/CharmedBaryon/CommonLibSSE-NG/7a60f4de794095d7b0f8928d1b930a52e9a7da83/include/RE/H/HitData.h)雖有attacker／weapon／傷害等欄位，需新hook與階段驗證，不等於已知最終HP實扣。

因此GCA/DBA傷害、stagger、真格擋SP退款、額外SP付款、重擊接受／揮空消耗皆未ready。候選沒有POET4 runtime export，不進術師14條typed registry；術師source通過不能轉成近衛可玩聲明。將來接線須另定capability/tag與存讀／退款政策，保留既有整actor免費Reset、不靜默剝依存點。

DBA3按owner+原敵重得刷新/替換，不乘疊、不作用全隊。DBA4每owner一份守步，重得替換強度/刷新有限T_guard，秒數待調；只下一筆敵向原生近戰武器正HP傷，排法術/箭矢/DoT/環境/自傷，同生成交易與零HP傷不消；成功一次/到期/owner死離戰/Reset/load清。這些是設計語義與相容性提示，UI尚未實作，不聲稱已阻擋不相容購點。

n是分配給這條進階效果的份數；本19點每A原normal一份，故目前n=1，不是unlock rank或High weight3。門檻、期限、狀態份數不隨n自動成長。High只解鎖/改規則，不給三份焦點/三次免SP。DBA6成本採本人maxSP×0.05/n，n為這條規則有效份數；n<=0/未知不啟用。n1仍5%，更多份數只降同一次續拍成本，不增次數/期限。這是可審有理成本函數，不改27atom或宣稱compiler已支持，付款精度仍待實作。

focus建立與後續分支只接受存活、非本人、相對owner敵對的Actor，weapon型別/旗標不代替敵我關係。非Actor/自傷/友方誤擊不建、不刷、不兌現，不擅加誤擊清舊拍；原focus自身死/失效/到期仍按既定清理。
