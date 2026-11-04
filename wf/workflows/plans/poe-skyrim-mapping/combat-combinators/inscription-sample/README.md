# 術師通用與刻印 NativeBridge候選

[使用者頁](../../../../../user/2026-11-04-inscription-sample.md)｜[共同範本要求](../template-requirements.md)｜[原生法術技術附錄](../../../../../user/2026-11-04-native-spell-templates.md)

使用者新裁示：擊中附印本身是高階能力，先點亮後才有後續印規則資格。本輪已獲授權隔離source與公司離線驗證，刻印回主線；蝕魔暫緩。狀態native_bridge_candidate_in_progress，不是live或整套已核可範本。16:50前收尾進度在private交接，不以中途切片結束active goal。

Done when: 真17候選點保ID/邊/座標/type/weight；H0先解鎖、圖連通AND規則前置ANDcompiled capability；整actor免費Reset保高水位且清debug快照，不靜默丟點；source/patch從固定parent可重套，離線邊界具證，家中未驗明列。

## 真圖與兩層

[region.json](region.json)保存20原點：17候選與3保護（Mastery40439、Runebinder42343、DivineFervour30693）；[SVG](region.svg)另畫7個真一跳外接。原來源為授權[GGG3.29.1](https://raw.githubusercontent.com/grindinggear/skilltree-export/3.29.1/data.json)，SHA7e9f755e33152129ebf36c2ebdad639c527e4ad70d274b1fefb860f30ca01122；不搬整份dump進public。

H0=原notable61308 Amplify，58402→59728兩普通點可直接抵達，不會先買進階才到H0。21389留爆破transform候選；活印傳承移[未落變體](unplaced-variants.json)，不充第三個High。不改原48keystone／38先做10延後裁示。

只有IH0/IA4可測的probe切片中，原IA4位59070被其他pending規則擋住，故只交換IA4／IA5綁定：40927為斷咒、59070為回流。原type/weight/位置/邊不改。全ready設計closure與排除pending的真start路徑分開驗證，不能從58402假設已得點或開pending繞路。普通外接路仍合法，通用區可經58402→10575→21262而不被刻印核心鎖住。

## 單一資料契約

- [candidates.json](candidates.json)：17點原型／新名／rule refs／requires／待審預算。
- [rules.json](rules.json)：14規則，共通4A2H與刻印6A2H，scope/unique/High前後打法及代價分開。
- [native-bridge-bindings.json](native-bridge-bindings.json)：wf-table/1＋poe-native-bindings/1，14 typed bindings。rank1是一次解鎖，不是原node.weight或已校準n；原1/3份仍保留。
- [比例輸入](proportional-values.json)：IA1本次原生實付MP20%、IA4自身final maxMP5%，actor/recipient/快照明確。
- [實作難點](feasibility.md)：現有底座／新增交易與原生事件限制；[native-first對照](native-first-review.md)是此前待修原因與未採替代，不再推蝕魔。

Bindings不准自稱engine ready；未知schema/rule或非法前置須拒絕。14rule-node的原GGG numeric payload由候選取代／清空，不偷偷附送原數值。三普通由numericOverrides明確輸出：58402 MP1份+5、40776 DMG_DESTR1份+2%、59728 MPREGEN1份+10%，不改27atom/per_share或node.weight。無overlay時仍應輸出byte-identical原POET3，有overlay才POET4/share-rule-v1並把機械資料納hash與compiled identity。

## H0不是免費附送的付費庫

IH0只讓買點者的正常既有傷害SpellItem命中後，被動加owner-target限時狀態；不教新法術、不加隱含10MP、P/B/D或爆傷。六A全需61308；IA2/IA5/IA6另需53018的IA1付費印。IA3/IA4只讀免費H0狀態，不加假IA1依賴。

IA1未來須自己包含付款→基本兌現，不能變成花錢但必須再買IA2才有效的空點。原生實付20%裁示保留；舊固定10只移A1顯式待審，不藏回H0。本輪首slice不做完整P/B/D，因此IA1及相關未接線能力不可購。進階rule＋數值與High多純規則的分類、刻印至少3獨特A／2獨特H、class-common另計，依共同範本要求保留；不能用接口就緒充遊戲性已驗。

## 購點與退款

購買與載入／debug恢復都要驗依賴。Debug只繞點數，不繞連通／核心／capability。已買高階不等於未實作進階可先花點；編譯adapter未ready必須顯示原因並拒買。

既有只有免費整actor Reset，沒有單點refund，本輪沿用：清allocation、debug.beforeDebug，保highestGrantedLevel，所有點回池，並清該actor附印等暫態。不能只移除H0保住依存、不能退出debug又復活舊依存；未知舊tag記錄須明確隔離或遷移，不把原同ID舊效果無聲升級成新High。

## 公司證據與未驗

公司可證fixed-parent來源／逐snapshot SHA、POET3回歸與POET4 effective payload、真start可達＋順序Spend、requires／capability／save-debug-reset、owner印交易及callback重入、A4 max100→5／300→15。source core曾抓到清理callback重貼的P1及TTL同型，修後由獨立固定blob復核；這不提升native ready。

原生命中歸因、marker ActiveEffect存活／可見、真MP debit、Windows ABI與家中實際操作仍待驗。靜態501-byte Script/noVMAD MGEF/SPEL只是candidate carrier，無visual；normal ready不可因檔存在就自動打開。明確opt-in hidden probe若有，需與正常tag/readiness分流並標needs-live，不能稱一般功能已完成。未改凍結1.2.3、r3部署、DB/profile或安依賴。
