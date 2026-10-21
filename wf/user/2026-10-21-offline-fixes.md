# DSP 與 houseCARL 離線修復

授權來源：使用者選擇「1,3。不要碰熒幕遊戲滑鼠鍵盤」。本輪在隔離工作樹修復 DSP 的面序候選、houseCARL 名稱解析，以及一處必要的 agentctl 名稱 consumer；沒有碰螢幕、遊戲、MO2、鍵鼠、現役部署或 profile。

## DSP 候選包

`projects/darksouls-port` 的隔離分支 `dsp-winding-20261021`，本機 commit `fcad6f5d739280f423372b41b25adb8ede837c38`。修掉舊候選在不同 accessor 共用 buffer 時反轉兩次的漏洞，加入範圍／重疊／重複處理檢查，並禁止沿用未修 NIF 假通過。

69 個 render NIF 的 621,534 個三角形各反轉一次，位置、法線、UV、tangent、材質及其他位元組保持不變。完整 367 項測試與獨立 review 通過；reviewer 另測 identity／mirror transform 的真 converter 輸出，並重驗全部 794 個基準檔案。

候選包在該隔離工作樹 `out/DSPortP3-Winding-20261021.zip`，11,714,396 bytes，SHA-256：
`79910aff6c4f727671cae90ed6e8d5ba92ad20feb32de1a2615c0a1e87b7f47f`。

`out/winding-manifest.json` 記來源 commit、工具 pin、前後檔案雜湊及 ESP 引用，SHA-256：
`552f0a7e9cf1d7a588143177b064f8b31c854b6a43ae700bbb5315bdf63f24f9`。

固定 converter `cf12ae9`；沿用 ModForge `0af3188` 產生的基準 ESP，沒有重建 ESP。覆蓋包沒有碰撞、貼圖或腳本。少量原始異常面保留，沒有猜測性重繪；**遊戲可見性仍未驗證**。下一階段驗收條件見 [DSP 待驗項](../../wait-user/feature-runtime/dsport-p3.md)。

## houseCARL 名稱解析

隔離分支 `fix/linux-record-names-20261021`，本機 commit `b4a1865509b38f11abb0067df56f21f1d2d718e2`，修正兩條通路：Linux 的 BSA 字串讀取不再依賴 Windows LocalAppData；UTF-8 中文名稱使用正確的顯示與查詢語義，原始寫回 Token 保留。`read_record`、`resolve`、`resolve_names` 和 Name predicate 都有覆蓋。

Mutagen 0.53.1 沒有公開 ArchiveListing／PluginListings override；新 Linux 通路使用限定版本且遇不相容就明確失敗的單一相容入口。Windows 保留原公開 factory。合法 CP1252 與 UTF-8 雙解時，顯示／predicate 優先 UTF-8；原始 Token 仍可無損寫回。archive 內同表有多個來源時明報歧義，不猜贏家。

使用**同一 probe、同一組六個真實 plugin、同一檔案雜湊與贏家**，基底 product DLL 有 5 項失敗，修正版 6 項全過：Gold001、CHS 贏家「小麦」、指定原版 HearthFires 的 Wheat、連結名稱、中文 predicate，以及不偷偷轉成繁體「小麥」。這是固定六插件 subset 的驗證，並非完整現役 profile 驗收。

32 項新 guards 通過，包含 localized BSA、CP1252／UTF-8、predicate、原始 Token 重播、複製寫回與檔案生命週期；既有 strings、case-insensitive assets、dialogue encoding、bulk、predicate、snapshot 六組 guards 亦通過。隔離 Release build／self-contained publish 成功，使用既有 NuGet cache，沒有下載或安裝依賴。來源選擇與 baseline／fixed／deployed DLL 雜湊保存在該工作樹 `generated/record-name-evidence/`；deployed 與 fixed 不同。**現役 MCP 沒有更新或重啟，不能把隔離 harness 成功當作已部署成功。**

## 相容修補與後續界線

`agentctl` 隔離分支 `fix/2026-10-21-candidate-display`，本機 commit `32ed60a5`：換臉候選標籤優先讀既有 `Name.display`，舊回覆退回 `Name.value`，原寫回 helper 不變。修前有 2 項回歸失敗，修後與 reviewer 都 8 項通過；未執行換臉工具。

consumer 修補可相容舊 houseCARL 回覆；未來整合時可先準備 consumer，再更新 houseCARL。三處程式變更都留在隔離分支，已依後續授權 push，沒有 merge；部署與遊戲驗收須另獲允許，本輪不執行。

## 收尾與下次續接

收尾授權來源：使用者要求「按照 wf/規矩，整理收尾」。Done when: 成果有持久續接位置、母記錄完成本機提交、明確區分已驗與待驗，且保留既存變更與來源副本。

下表是正式續接位置，路徑相對母 repo 根目錄；原本的三個主工作樹與 gitlink 均保持原版本。

| 專案 | 分支 | 持久工作樹 |
|---|---|---|
| DSP | `dsp-winding-20261021` | `../skyrim-worktrees/dsp-20261021/darksouls-port` |
| houseCARL | `fix/linux-record-names-20261021` | `../housecarl-name-fix-20261021` |
| agentctl | `fix/2026-10-21-candidate-display` | `../skyrim-worktrees/agentctl-name-display-20261021` |

agentctl 已建立持久工作樹，10,998 個 tracked 檔逐檔、symlink 與 executable 位元皆與原副本一致，新位置 8 項測試通過。系統暫存目錄的 `skyrim-agentctl-candidate-display-20261021` 保留為同 commit 的 detached 歷史副本，後續不要在該副本開新工作；沒有新增重複分支。

DSP 的 `extracted`／`venv` 是仍需使用的本機依賴連結，target 有效；以該 repo 本機 `info/exclude` 的精確規則處理，沒有刪除、加入 commit 或改 tracked `.gitignore`。候選包及 manifest 的雜湊維持不變。

母 repo 盤點、修復、閱讀偏好與 WAIT 記錄一併做本機提交，僅收明確文件路徑。三個主專案保持乾淨；instance／profiles 的既存變更原樣保留。DSP 實機待驗仍在 WAIT_USER；houseCARL 未 reload 是後續可由 agent 處理的部署事項，不列為使用者必須親做。

2026-10-21 使用者後續明確授權「隨意 push」。本次推送 Done when: 母 repo 的收尾與狀態文件、上述三個修復分支已普通推送，逐一核對遠端 SHA 與本機相同，不留下本輪新增的未推送 commit。母 repo 推至 `origin/main`（包含 `59f90a0` 及本段狀態更新）；DSP 與 agentctl 推至各自 `origin` 同名分支；houseCARL 推至使用者 `fork` 同名分支，未推原作者 `origin`。三個修復分支的 commit 如上，均已設定對應 upstream。

這是本次成果的明確授權，沒有修改 [使用者偏好](../workflows/common/user.md) 的一般確認邊界。未 force、merge、部署或刪除；暫存快照保留，沒有因推送順便清除。後續整合與部署另行處理，遊戲可見性仍待驗。
