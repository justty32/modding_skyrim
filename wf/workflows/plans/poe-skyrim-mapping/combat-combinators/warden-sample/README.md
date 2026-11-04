# 重裝通用＋守衛者：可攜護援候選

[使用者頁](../../../../../user/2026-11-04-heavy-warden-sample.md)｜[真SVG](region.svg)｜[原節點](region.json)｜[19候選](candidates.json)｜[14規則](rules.json)

Done when: 真19點保ID/座標/全鄰接/type/weight，避術師17及浪潮19；H0有不被自身A擋住的普通入口、common不依H0；common4A2H/sub6A2H(3A/2H unique)，每A明列requires58449；可攜隊友buff與giver lease/消耗/撤除具體，資料及來源界線可審。compiled/runtime=false，不輸出到術師typed14。

使用者正式名『守衛者』，stable D1不變；本稿依使用者「Skyrim站位混亂、給隊友buff」修正為portable。舊固定圈/隨身錨只作歷史草案，不是current；19點幾何保留，沒有另造小樹。

## 真圖與份數

真MARAUDER start47175，raw classStartIndex=1、classes[1]=Marauder；19=15normal+4notable，38列僅selected/start/one-hop。19本身分兩支，透原起點47175才構成連通區；起點只作原圖connector，不填、不計19，沒有添加假橋。固定f510的Connected/CanSpend將所有七個原start都作每actor共用免費錨點；47175不購、不計19，兩支各從它的鄰點開購，並非穿越可購普通橋。這只證局部拓撲與既有起點語義，新14規則未註冊/未ready，也未實跑本候選完整Book購點順序。H0=58449，普通入口47175→31628→9511→23881→26523→58449；H1=61198。common可沿47175→50904→6981→36543→49412→24383→6718→65308，不依H0。所有WDA與WDH1需已買58449，圖連通AND前置；資料存在不表示engine可買。

normal五點按既定一份HP5/SP5/AR6/SPREGEN10%/HP5。四High仍原notable weight3，機制預算未核、不代表三次授援或三倍交換。進階n是本canonical效果實配份數，目前各normal1份；n<=0/未知不啟用。R_apply/T_aid、門檻與狀態份數不隨n自動放大。原raw57 keystone與policy48為不同集合，38/10政策不變，無保護型被填。

## 可攜狀態與結算

WDH0授予時才檢同戰鬥場景、R_apply、可見與合法存活友軍；優先最近尚無本人護援者，皆有才刷新本人最早到期一份，穩定key破平手。非敵對路人不算、不給自己fallback；受控召喚須可證歸屬才算。授予後離距不撤，沒有固定圈membership。

lease鍵giver+recipient+H0，持授予時n/payload/原期限/expiry；同giver重授只刷新，不添第二份。不同giver可並存，同canonical係數先合：WDA1只除一次、WDA2平扣一次、WDA3削敵SP先合量只扣一次；不把臨時份數寫成recipient永久星盤。giver失效/死/離戰/Reset/load只清自己的；recipient死非法清所收，期限各自到期。

事件前快照→原生/DCA2 block SP費→原生armor/block及已符合自持防護→護援同canonical合係數除一次→緩衝平扣一次→僅受擊者本人已購且符合DCH1時，用原生費後剩SP轉付→溢出HP。只有一筆HP結算，不先受傷再補。普通lease以『原生後/護援前有正HP待扣』為消耗門檻，即使護援抵成0仍消；WDH1 lease保留。新授/刷新不能回溯影響同生成交易。

WDH1必持續格擋，放下盾/解除格擋先撤本人全部lease才可普/重/bash，舉盾不延TTL。WDA4/5因而無進攻撤援收益；WDA4另受浪潮GCH1禁止bash失衡時整分支停用，不白撤援護，普通bash原傷照常。這是相容性語義，不宣稱UI已拒購。

WDA5撤的是本人有效lease，一次withdraw取remaining/originalDuration的平均比例，maxSP*.02*n*平均值只回一次；無有效lease不回，不按人頭翻倍，不退原生重擊實付。DCA1與GCA2是同canonical：相同敵活Actor/非己/原生近戰blocked selector與同SP快照，混買合份只判一次/除一次；recipient護援WDA1不是此canonical。

## 來源及未實作

已讀合併Illusion樹的Second Wind/Hold The Line/Arise描述只作隊友buff設計參考，不證完整SPEL/MGEF/script鏈或現役winning，也不把Courage當必學操作。真FWM Rally Fire→Abilities::Lift/UpdateBoosts與Skald Fervor的recipient.until有授TTL後離距保留的程式形狀；不是固定圈每次重算，也不表示新格擋授援已接。具體私有artifact/EDIDs與固定source行證保存在當日private交接，不把完整來源搬進public。

[固定CommonLib TESHitEvent](https://raw.githubusercontent.com/CharmedBaryon/CommonLibSSE-NG/7a60f4de794095d7b0f8928d1b930a52e9a7da83/include/RE/T/TESHitEvent.h)只有接觸/來源/旗標，不能單獨證剩HP、原生blockSP實付或禁止攻擊資格。舊Party範圍不含所有召喚；舊Lift key不是giver+recipient，不能Drop同perk抹掉其他giver。新的typed resolution、資源交易、giver lease/清理、姿態/前置攻擊資格及可見提示皆pending。沒有runtime、PE或live聲明。
