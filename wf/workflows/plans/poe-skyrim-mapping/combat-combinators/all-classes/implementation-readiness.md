# 浪潮鬥士／守衛者實作前置核對（11-04）

Done when: current樣板、rule身份與共享canonical不混版；最多五個可行性gate逐一分清既有證據及缺證；下一次使用者review能作精確決策，沒有代批engine。

本輪只讀母repo660761e、agentctl c312537f、mod-library e07dd32內f510快照；不重建工程、不執行runtime、不改source/atoms/數值。下文S=`mod-library/plugins/Path-Of-The-Companions-IndependentSkills-1.2.4-dev-2026-11-04-NativeBridge/source`；D=`wf/workflows/plans/poe-skyrim-mapping/combat-combinators`；H=`agentctl/handoffs/home-2026-11-04`。

## current身份

G1浪潮鬥士（double-beat-sample）和D1守衛者（warden-sample）各19點、15 normal＋4 notable，各14條規則；兩份candidates/rules經tabledb實讀均compiled_runtime=false。浪潮H0=34009、變形H1=49538；守衛H0=58449、H1=61198。兩者A及變形H皆需本型H0；common獨立。守衛current是格擋授予可攜隊友buff、持盾延持，離授予半徑後保留至原expiry；舊圈版已被取代。來源：D/兩型README.md:11–15；H/warden-sample/README.md:5–9。

浪潮身份為GCA1–4、GCH1–2、DBH0–1、DBA1–6；守衛為DCA1–4、DCH1–2、WDH0–1、WDA1–6。GCA2與DCA1同canonical MELEE_BLOCK_HIGH_SP_DAMAGE_DIV：本人為target、存活非己敵Actor、可確認原生近戰WEAP且blocked，排bash/projectile/法術/環境/自傷；同交易開始SP/maxSP快照、有效份數合一次、只除一次。recipient護援WDA1是另一canonical，不能與DCA1混合。兩rules.json的shared_block_canonical本輪逐欄相同；未把這28個新ID套進術師typed14 registry。

## Gate 1：能否把原生近戰動作關聯到一次交易

已有的是觀測入口，不是可直接重用的attack交易。H/guard-double-beat/DBH1-observations.json三列釘住TESActionData::Process、ActorState/animation事件、AttackCost/SP寫入；S/src/Skald.cpp:886–905只見送graph攔截及power成本query。TESHitEvent無唯一attackID，sequenceIndex/attackCount/AttackData指標/tag不能充token。

缺的是player與NPC皆可證的accepted起手→命中/多target/揮空/取消/完成關聯；DBH0接拍、DBH1起手消耗與DBA排他分支不能用CD猜。下一次review應決定是否授權「只觀測、不改成本/效果」的隔離trace作第一步；尚未證明前保留設計pending，不批准DBH1零SP代付。具體否決矩陣已有H/guard-double-beat/DBH1-feasibility.md:7–9，不需再造規則。

## Gate 2：同一次原生防禦結算能否取得正確階段及控制資格

f510已提供HP寫入攔截及有限PlanDamage；但S/src/PoeHooks.cpp:148–156只傳actor ID、負HP量與MP，沒有attacker/weapon/blocked/原block費/transaction。TESHitEvent與HitData只是可用表面，未證最終正HP實扣階段。既有資料可表達typed policy，不等於runtime已有該policy。

缺的是native armor/block後、護援前正HP待扣的單一commit，以及stagger、本人不可被擋/不能擋、持盾期間禁止普重/bash的原生資格控制。這決定GCH1/2、DBA4、DCH1、WDH0/1和多giver護援順序是否可忠實實作。下一次review應確認「不能接到正確precommit/資格邊界就維持未ready」的驗收底線；不能批准after-hit補血/補傷替代。守衛規則的順序與消耗點已固定於D/warden-sample/README.md:21–23；浪潮DBA4是最終正HP才消，守衛普通lease則護援前正待扣即消，即使最終抵成零也消，兩者不可共用同一consume predicate。

## Gate 3：SP交易是否能分清實付、額外付款、退款與替代付款

f510 NativePayments有原生spell Request內MP實寫前後值、退款及nested synthetic排除，可借鑑不確定即拒絕的做法；S/src/PoeHooks.cpp:100–145限定Magicka與cast context。Skald AttackCost可改float，沒有證明accepted、SP付款或零SP能起手。因此不是把Resource改成Stamina就完成近戰collector。

缺的是原生block SP費與剩HP同txn、DBH1起手代付和取消、GCA4/DBA5退款、DBA6新增一次付款、DCH1先原費後剩SP轉HP的各自交易模式，並隔離同frame外來回/扣SP。下一次review應決定是否保留全部既定模式並接受分能力pending，而非把代付改事後退款；DBA6現有有理成本/n<=0停用只屬候選公式，付款精度及compiler支持仍待證。證據：H/guard-double-beat/primitive-gap.json resource_transaction_modes；D/double-beat-sample/README.md:23、:35。

## Gate 4：owner狀態及多giver lease能否獨立持有、清理與一次消耗

既有f510刻印有owner-target TTL、only-owned marker及先摘除後回呼形狀；FWM Rally Fire/Lift有授予TTL後離距保留形狀。直接看S/src/Abilities.cpp:1214–1225，舊Lift key是recipient/value/source，缺giver；1324–1334只按期限撤數值。能借生命週期模式，不能把舊Lift當新護援已接。

缺的是浪潮每owner單focus＋排他branch＋同txn不重建，和守衛giver+recipient+H0 lease、grant-time payload/原duration、只撤本人、不同giver同canonical合係數一次、死亡/離戰/Reset/load清理。隊友/受控召喚資格、視線/同戰鬥場景亦未全證。下一次review應確認現行portable contract及召喚物「歸屬未證即不合格」邊界，並核R_apply/T_aid/T_beat/T_guard等已留待調參數；本報告不補數值。不能Drop同perk清掉其他giver，也不能將臨時護援寫進recipient永久份數。來源：D/warden-sample/README.md:17–25、:31；H/warden-sample/references.md:5–7。

## Gate 5：新能力如何保持fail-closed且可獨立驗收

f510已具Graph::CanSpend的compiled-ready AND requires AND連通，以及所有start免費錨點；見S/src/PoeGraph.cpp:25–34、:72–79。既有整actor免費Reset、未知schema/tag隔離是可沿用的安全底座。現正常刻印ready仍空，experimental僅IH0/IA4；沒有兩新樣板POET4 export/registry，尚未跑守衛14規則完整Book購點順序。局部拓撲PASS並非可玩。

缺的是新IDs/schema/tag/capability分版、每能力的compiled拒絕資料/負例、同canonical混買與互斥分支處理、存讀/Reset/debug依存及可見提示，最後才是matching PE與隔離live。下一次review可精確裁示「選哪一樣板／哪些既有ID先做隔離可行性切片、其餘保持pending」，而不是一次批准28條handler或擴任意DSL。不能因前四gate未證便開ready，也不能以相容性文字宣稱UI已阻擋購點。來源：H/guard-double-beat/primitive-gap.md:9；H/warden-sample/README.md:7、:13；S/CODE_MAP.md:5–23。

## 三項驗收結論

current身份及共享canonical已核；五個gate各有現有source或具名觀測證據，也均明列缺證。下一次review已可圍繞首個樣板/ID範圍、先trace或施工、pending政策、portable/召喚物邊界及待調參數裁示；本報告沒有批准engine、給新數值、聲稱runtime通過或打開舊backlog。此輪無需新下載或恢復17GB研究樹。
