## 1. DMK 1.5.0 人工校對版

**前置條件。** 手上要有 exact official ZIP、exact CHS 7z、7z、OpenCC，以及
`mod-library/l10n/tools/build_dmk_cht_layer.py`；兩個 exact archive 的既定 Linux 路徑在
`agentctl/handoffs/rtqa-2026-08-31/HANDOFF-cx-rq1-dmk.md:10`、`:11`、`:12`，builder 的五個必要參數在
`mod-library/l10n/tools/build_dmk_cht_layer.py:168`、`:169`、`:170`、`:171`、`:172`。目前可直接接續的
人工校對成品是 `agentctl/handoffs/rtqa-2026-08-31/dmk-build/DMK-1.5.0-Traditional-Chinese-Human-Reviewed.7z`；
它已離線重建 PASS，inventory 只有 `Data/Viny Mods/DMK/Language.json`
（`agentctl/handoffs/rtqa-2026-08-31/reports/dmk.md:46`；`:50`；`:52`）。

**實際動作。** 先完全關閉 Skyrim／MO2，再照 profile 工作流開 `feat/*`；入口指令是：

```bash
cd /home/lorkhan/repo/moddings/skyrim/instance/profiles
python3 -B tools/profile_workflow.py status
python3 -B tools/profile_workflow.py start feat/<主題>-<日期>
```

`<主題>` 的本次固定名稱 repo 內未記錄，回家現場確認；指令模板與「執行期間不得切 branch」的限制見
`instance/profiles/tools/README.md:17`、`:18`、`:19` 與 `instance/profiles/README.md:33`。用 MO2 安裝上述
人工校對 archive 成獨立層，停用現役 `Directional Movement Keys Traditional Chinese 1.5.0 Machine Private 2026-08-21`，
並讓新層位於 `Directional Movement Keys 1.5.0 Dev 2026-08-21` 之上；現役兩個名稱與優先關係見
`instance/profiles/manifest.json:3063`、`:3080`、`:3089`。`mo2ctl install <archive> --priority
"before:<本體 mod 名>"` 是 repo 記錄的覆蓋層安裝形式，但新層的 `--name` repo 內未記錄，回家現場確認
（`wf/workflows/nexus-intake/README.md:116`；`:121`；`:122`）。從 Steam 點 Skyrim SE、在 MO2 按 Run，
抽查一般設定、相機、PC／手把按鍵、OAR converter 警告，再做移動 smoke
（`wf/workflows/runtime-qa/README.md:24`；`wait-user/home-setup.md:42`；`:43`）。

**通過條件。** `human_reviewed_zh_tw`、66 reviewed、38 override、0 unresolved；不另加數字
（`wait-user/home-setup.md:40`；`:41`）。

**失敗退路。** 任一計數不合即停，不部署該重建物；若部署後 UI／移動異常，停用新層並恢復舊 DMK 本體／
machine CHT 的既定啟用組合，再維持原 `plugins.txt`／`loadorder.txt` 順序
（`agentctl/logs/mcm-helper-dmk-cht-install-2026-08-21.md:36`；`:37`；`:38`；`:39`）。

**預估時間。** 25–45 分鐘（本單估算）；依據是離線重建、token／JSON／archive gate 已經 PASS，剩餘工作集中在
部署與指定 smoke（`agentctl/handoffs/rtqa-2026-08-31/reports/dmk.md:58`；`:59`；`:60`）。

