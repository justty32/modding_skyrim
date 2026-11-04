# 輔助 S 設計交付

Done when: 通用4A2H與S1/S2/S3各6A2H共30條，獨特性、High打法轉構、事件/owner/消耗/失效/混買/正負例完整，五項驗收可review；全部僅設計。

30條已落於 rules.json；subtypes.json 3列記計數與stable slot requires；parameters.json 30列將新強度/成本/期限全部保留 pending_review；feasibility.json 10列記能力缺口、否決、互動及canonical提案。沒有legacy S樣板可引用，未新建或修改任何legacy payload。刻印README/rules/candidates已親讀對照，不借用其P/B/D或固定付款裁示。

S1以原生法術縛印建立控制窗口；H1將集中強控制轉成換敵移交、舊敵殘留弱化。控制免疫與衰減owner尚未證，未知就不提交，不默認永久停機或新全局cap。S2是HP恢復及防護跟身域；H1犧牲額外域HP持續恢復，改有效原生實補後停唱發一次可攜HP救援，不能產SP/MP推進。S3是召喚落印→本人原生法術削弱；H1反轉成本人法術落印→召喚兌現本人防護，不涉及本人近戰或新AI命令。

三個重要混買界線：SCH1本人合成副本不可再被SCH2轉贈；S2H1最終正HP實扣後才消，普通防護護援前正HP待扣即消，不能共用consume predicate；S3H1反向印令A1/A2/A4原方向收益不適用，買點不加職業鎖，但轉構本身有真代價。S2H1停止額外域HP tick後，不虛構其A1/A2/A5/A6收益。各rule都標owner、recipient及來源隔離。

五項驗收：

1. 計數PASS：共通6條獨立一池；三型各6A2H，所有6A/2H皆對兄弟型有不同觸發/歸屬/消費語義；subtype-shared=0。High皆有選前/選後/收益/代價/非數值理由，H0載具及H1轉構沒有只靠倍率湊數。
2. 完整性PASS：30條明列trigger、actor、target、owner、刷新消耗、生命週期、成本、混買及正負例；High requires鎖到核心stable slot。來源與參數未證不宣稱ready。
3. 數值邊界PASS：不改27 atoms/per-share及1/3/5份；新K/C/T與範圍/自用/衰減均pending_review，沒有填新百分比、秒數、付款或global cap；不增法術、命令或選單。
4. 共享邊界PASS：common單池，不拿來充unique；跨職防護合併只向主管proposal，保留giver+recipient/授予payload/原expiry，不用model最早到期舊案蓋current D1。V2/V3/C3辨識見feasibility。
5. 交付邊界PASS：四JSON皆wf-table/1並經tabledb寫入、重載；compiled=false/runtime=0。只寫獨立工作目錄；未改repo、圖、source、DB、live或保護ID。

驗證是資料結構與設計自核；不是可玩性、engine capability、付款/控制/召喚/channel或runtime驗收。最優先缺口是control衰減owner、原生channel交易與實補/阻傷、召喚實例owner及多target cast識別。幾何配置待single owner，本線沒有猜PoE ID。

獨立audit後修正S3A5 recipient用語：印target是該敵，額外防護recipient僅本次命中並兌現的合法summon_instance；owner僅作購點及歸屬。同步build與rules，不新增收益或數值。
