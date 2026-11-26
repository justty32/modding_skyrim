# CTD：crash log 讀法與歸因陷阱

[lessons 索引](README.md)

DLL 與腳本的個案在 [crash-dll-and-scripts](crash-dll-and-scripts.md)，資料層與素材在 [crash-data-and-assets](crash-data-and-assets.md)。

## spid-outfit-manager-live-inventory-reset-ctd

> `SkyrimSE.exe+02B789A` 背景載入 CTD：真兇未明，SPID 不是兇手（2026-10-03）

簽章 `SkyrimSE.exe+02B789A  mov rcx,[rcx+0x130]`、rcx=0，崩在背景載入執行緒（frame 10-11 是 kernel32/ntdll 進入點），現場 `QueuedCharacter`／`IOManager`／`BSFadeNode "skeleton.nif"`，受害 actor 不固定。SPID 上游源碼的 `Resetting inventory` log 記的是原版引擎自己的 reset；空檔覆寫層 `SPID-NoElderOutfit-2026-09-24`（壓在 CT77 `ElderOutfit_DISTR.ini` 之上）無害但沒修到，同簽章照樣復發。`agentctl/handoffs/home-2026-10-03/crash/c0927/REPORT.md`。

**Why:** call stack 全是原版碼、沒有 SKSE DLL，不等於 DLL 無關（trampoline hook 跳回原版碼就不留名），但「log 裡出現同 FormID」也只是相關不是因果；`Resetting inventory`／`Resurrecting` 總次數會被遊玩時長汙染，不能當 A/B 指標。

**How to apply:** 再崩先打包 SKSE log 目錄再開 MO2；DLL 嫌疑可從「崩潰前數秒 DLL log 裡有沒有同一個 ACHR/FormID」找線索，定罪要機制證據。crash log 讀法（2026-10-23）：

（1）frame 標 [P]（precise）或 [S]（stack scan），多數是 [S]，只能定位功能路徑、不是嚴格因果鏈；排除「今天新裝的 mod 是兇手」要查同簽章崩潰在裝之前是否已發生，不能只看名字沒出現（`agentctl/handoffs/done/2026-09/home-2026-09-20/crash/REPORT.md:17`）。

（2）RIP=0 時 frame[0] 是浮點殘值，改讀 `[RSP+偏移]` 的真返回位址起算，`triage_crash.py` 已有這段（`agentctl/handoffs/done/2026-10/home-2026-10-03/crash/c0928/REPORT.md`）。

（3）暫存器裡的插件名／FormList 字串只是「當下還留著的值」，要對照崩潰那行指令實際讀寫哪個暫存器（`agentctl/handoffs/done/2026-10/home-2026-10-10/crash-1/REPORT.md`）。

（4）.exe 被 SteamStub 加密反組譯不了時，用 alandtse/skyrim_vr_address_library 的 offsets CSV（AE ID→1.6.318→se_ae_offsets→SE→1.5.97→1.5.97_comments）鏈式對照，把匿名函式 ID 推回公開名稱（`agentctl/handoffs/done/2026-10/crossbow-ctd-2026-10-09/REPORT.md`）。

相關：[[doomperk-advanceobject-block-ctd]]、[[verify-waituser-against-logs]]。

## papyrus-line-count-is-not-missing-file-count-or-causation

> Papyrus 警告行數、去重 signature、缺 PEX、型別契約錯誤與執行期因果必須分開。

2026-11-02。同一缺 store 可連鎖產生多次 binding 失敗；property 初始化失敗不能算成同數量缺 PEX。腳本在當前 loose／BSA 而歷史 log 綁定失敗時，查 alias／base 型別與 PEX 契約，不直接補同名檔。VMAD 名稱命中可支持引用證據，未完整解析 alias／fragment 就不擴稱已解出所有掛接語義。當前 provider 不是歷史 VFS 快照，BSA 有成員也不證當時已掛載；沒有同條件前後對照不能歸咎最近一次部署，沒有影響驗證也不能宣稱無害。

**How to apply:** 先固定歷史 log 的 hash／時窗，按明確規則分類去重，再核對當前 PEX provider 與相關 plugin VMAD。沒有 provider 而 VMAD 有引用只能列部署缺件候選，仍須比對原 archive／版本／FOMOD；只有 log、沒有現役引用時，不直接判成 save 殘留或清理存檔。

來源：private `agentctl/handoffs/home-2026-11-02/papyrus-attribution/REPORT.md:13–41`；既有工具 `instance/tools/papyrus_missing_stores.py`、`agentctl/tools/runtime_log_window.py:inspect_papyrus`。

## background-cell-load-use-after-free-crash-diagnosis

> 背景載入 cell 崩潰時 CrashLogger 標的 FormID=0／ParentCell=None 是假歸屬；BOS 把 STAT 換動畫 MSTT 是常見候選

物件讀出 `FormID=0`、`ParentCell=None`＝ref 已釋放或未建構，CrashLogger 掛到 Skyrim.esm 只是預設值；掃 cell children GRUP 找唯一符合型別的來源才找得到（2026-10-09：Animated Ice Floes 用 BOS 把 `IceFloes01` 換成動畫 MSTT）。BOS swap 執行期換 base，存檔不留痕跡，停用安全。`agentctl/handoffs/done/2026-10/home-2026-10-09/crash/REPORT-crash2.md`

**How to apply:** FormID=0 別信 CrashLogger 的 plugin/cell，改掃 GRUP 消去法；背景載入＋MovableStatic 優先查 BOS 換 MSTT 的 mod。
