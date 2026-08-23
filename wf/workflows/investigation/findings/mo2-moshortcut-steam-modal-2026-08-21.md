# MO2 `moshortcut` 啟動被 Steam 確認 modal 阻塞（2026-08-21）

## 結論

2026-08-21 01:04 後的 Skyrim 啟動失敗，不是 DSPortP1 增加 639 個檔案讓 MO2 掃描超過
600 秒。MO2 已完成 directory update 與 USVFS tree 建立，實際停在 Steam 狀態檢查的
`Waiting` modal：

> Please press OK once you're logged into steam.

`moshortcut://:SKSE` 冷啟動沒有顯示可操作的主視窗，因此這個 modal 對 headless runner
只表現為 `ModOrganizer.exe` 長期停在 futex wait、AgentBridge `/ping` 永遠不出現。
加長 wait 不會解除需要確認的 UI 狀態。

已驗證的恢復方式是先不帶 `moshortcut` 正常啟動可見 MO2，等待主視窗完成 refresh，
再按 Run。若出現上述視窗，先確認 Steam client 帳號頁已登入，再按 OK。本次按 OK 後
1 秒內出現 `SkyrimSE.exe`，AgentBridge 0.8.0 `/ping` 隨即成功。

## 成功與失敗的分岔

`/tmp/mo2ctl-launch.log` 是跨嘗試 append-only log；以下行號是調查當下 13,921 行版本：

| session | directory update 後的行為 | 結果 |
|---|---|---|
| 00:50 成功（line 12428） | progress 到 226（line 12719），接著建立 SKSE/Skyrim 子程序（line 12728 起） | `info: Game: SkyrimSE.exe`（line 12742） |
| 01:04 失敗（line 13017） | progress 到 227（line 13309），只到子程序終止訊息（line 13317） | 沒有 SKSE/Skyrim injection |
| 01:24、payload present 且 DSPortP1 停用（line 13319） | progress 回到 226，仍停在同一位置 | 沒有 fresh Papyrus、沒有 Skyrim |
| 01:27、DSPortP1 整個移出 `mods/`（line 13620） | 停點完全相同 | 沒有 fresh Papyrus、沒有 Skyrim |
| 01:29、已 warm instance 再送 shortcut（line 13921） | 又跑 directory-update UI 序列 | 仍沒有 Skyrim |

成功的 USVFS log `usvfs-2026-08-20_16-50-21.log` 有完整
`injecting to ... skse64_loader.exe`、`SkyrimSE.exe` 與 117,229-node tree attach；失敗的
`usvfs-2026-08-20_17-04-52.log`、`17-24-08.log` 都只到 67 MiB virtual tree 建立，沒有
任何 injection。失敗時 `mo_interface.log` 在啟動後約 2 秒已記錄完 directory update；
live thread 檢查顯示 main 與 `DirectoryRefresh` 都在 message/futex wait，沒有持續 CPU 或 I/O。

## 為什麼不是 DSPortP1 掃描變慢

- 舊 DSPortP1 在成功 session 前本來就已存在於 `mods/`（582 files）；新版是 639 files，
  只增加 57 files。
- 現有最大 mod 有 14,909 files；DSPortP1 的檔案量不是離群值。
- DSPortP1 停用後 progress 從 227 回到 226，但同樣卡住；這也說明該 progress 至少受啟用
  layer 數影響，不能直接當成 on-disk 掃描計時器。
- 把新版目錄完整移出 `mods/`，MO2 on-disk mods 從 246 降到 245，仍然重現同一停點。
- 兩個失敗 fresh windows 都是 0 fresh Papyrus、0 suspicious lines、0 new crash logs。

所以「更長 wait」與「測試前移出 DSPortP1」都不是修法；安裝發生在最後一次成功與第一次
失敗之間只是時間相關，不是因果證據。

## 實際恢復驗證

驗證時已把新版 DSPortP1 放回原位（639 files，ESP SHA-256
`d1462591cf0e27e08cc1beffe738dd80fdb66500e5156b64a157f997a8df48a2`），DSPortP1 停用，
AgentBridge 暫時啟用：

1. 以 plain `ModOrganizer.exe` 冷啟動，主視窗正常出現並完成 refresh。
2. UI 顯示 243 mods、220 enabled、246 on disk；執行項目為 `SKSE`。
3. 按 Run 後出現上述 Steam `Waiting` modal。Linux Steam client 同時顯示已登入
   `justty32` 的收藏庫；這次不是輸入帳密，而是 MO2 仍要求一次確認。
4. 按 OK 後 1 秒內 `pgrep -f '[S]kyrimSE.exe'` 命中 PID 626005。
5. `mo2ctl status --json` 回報 AgentBridge 0.8.0 `reachable: true`。
6. fresh window 產生 1 個 Papyrus log、0 new crash logs。8 條 missing-class warning 與
   00:41／00:46／00:51 三次成功啟動的 Papyrus baseline 逐條相同，因此是既有噪音，
   不是本次啟動 regression。

調查 artifacts 在
`/home/lorkhan/skyrim_agent_out/codex-g/launch-investigation/`，包含三個 runtime window
report 與 `mo2-steam-waiting-modal.png`。

## 操作與工具建議

- 短期：先 plain cold-start MO2；完成 refresh 後從 GUI Run，處理 Steam confirmation modal。
- `wait=600` 仍可保留給真正的 cold refresh，但不能取代 modal detection。
- `mo2ctl launch` 的最外層 `ok: true` 只代表 command handler 正常返回；仍須檢查
  `bridge.reachable` 與 `pgrep`，不能把它當成 Skyrim 已啟動。
- 後續工具化可在「MO2 存活、directory update 已靜止、長時間沒有
  `skse64_loader.exe`/`SkyrimSE.exe` injection」時，回報 `handoff_user: possible MO2 modal`
  並提示 plain GUI preflight。這是新 feature，這次調查沒有直接修改 `mo2ctl`。

本次只證明 Skyrim 啟動管線可恢復；DSPortP1 門洞尚未實走，仍為 inconclusive。
