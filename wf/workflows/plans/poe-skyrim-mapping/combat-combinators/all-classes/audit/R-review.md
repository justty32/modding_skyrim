# R 獨立玩法審核

逐讀30行。R1單focus危險窗口、R2位置錨守恆派生集合/線廊、R3真裝填待射與命中後延遲攔截券，皆有實際玩法差異。

需修2項：
1. RCH2效果保換裝後已射projectile，但其lifecycle仍寫卸遠程清全部暫態。無H基線已由其他行卸遠程清狀態確立，不需重設High；只明訂H例外保已射固定snapshot，focus/錨/待射照清，Reset/死亡/離戰仍清，不可借換裝新值。
2. R3H1原生弩bash stagger受GCH1既有WEAP/bash禁令。混買須先停該附加分支，不得先消待射再請求必禁stagger；原生bash照常。R3A2箭矢stagger不受GCH1此禁令，不能擴禁。

RCH1離瞄/移動即退出，不隨待射攜帶抗中斷；R2派生不冒native建R1/R3，R3bash非preparedprojectile。能力仍待證，參數pending/compiledfalse/runtime0。

覆核：已親讀主管送回修訂行，以上語義issue均消除；source/runtime/幾何仍分層待證。
