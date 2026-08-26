# profile-change — 改 MO2 profile

任何會動到「實際在玩的那個 Skyrim」的變更：裝／移除 mod、改啟用狀態、改排序、改設定。

```text
Done when: <check_profiles 通過、啟用集合差異已審、已晉升到 main、live checkout 回到 main>
```

實體在 `instance/profiles`（MO2 那邊是 symlink 指過來），唯一 profile 叫 **`modpack-main`**。
完整規則見 [`instance/profiles/README.md`](../../../instance/profiles/README.md)。

## 唯一流程

```text
main → feat/* → release/* → main
```

**不使用 `develop`、`feature/*`、`hotfix/*`，也不以額外 MO2 profile 模擬分支。**
狀態差異全部由 git 分支承載，磁碟上永遠只有一個 profile。

```sh
cd instance/profiles
python3 -B tools/profile_workflow.py status
python3 -B tools/profile_workflow.py start feat/<主題>-<日期>
#   …改 mod…
python3 -B tools/profile_workflow.py record -m "<一句話>" --kind feat
python3 -B tools/profile_workflow.py start release/<版本>
python3 -B tools/profile_workflow.py promote
```

`record` 只收 profile 目錄內的變更；同時動到工具或文檔就用一般 `git commit`。
`start` 在工作樹不乾淨時會拒絕——那是它該有的行為，用 `git stash` 讓路，不要繞過它。

## 不可違反

1. **Skyrim 或 MO2 執行期間，禁止切分支、合併、提交、還原。** 先關遊戲。
2. `selected_profile` 永遠是 `modpack-main`。該 ini 是 **CRLF**，用 sed 改要帶 `\r`。
3. `modpack-main/skyrim.ini` 的 `bAlwaysActive=1` 要維持。
4. baseline save pair `ModpackKRDev0A.{ess,skse}` 成對且 SHA-256 不變，是唯一進 git 的存檔。
5. **不 force-push、不自動 stash、不自動 push**；工作樹不乾淨就停。

## 晉升前必查

- Skyrim 與 MO2 已完全關閉
- `python3 tools/check_profiles.py` 通過——它現在**也會比對 `ModOrganizer.ini` 的
  `selected_profile`**。加這道之前，只要目錄結構對就 PASS，即使 MO2 指向一個不存在的
  profile（實際發生過：ini 停在 codex 線留下的 `PandoraRuntimeDefer-20260822`，每次都 PASS）
- `modlist.txt`／`plugins.txt`／`loadorder.txt`／`archives.txt` 的差異已審閱
- **比對啟用集合而不是行數**：MO2 的 rescan 會加一堆停用項、把檔案改成自己的 CRLF 格式，
  diff 看起來很大但實際載入的內容可能一個字都沒變

```sh
diff <(git show main:modpack-main/modlist.txt | grep '^+' | sort) \
     <(grep '^+' modpack-main/modlist.txt | sort)
```

- 裝了覆蓋層就跑 `mod-library/l10n/tools/` 的**層優先權稽核**（命令見該目錄 `README.md`）

## 排序

**`modlist.txt` 頂端 = 最高優先權。** 覆蓋層必須在本體之上，否則完全失效且無徵兆。
`mo2ctl --priority` 的 `bottom`（預設）與 `after:` 都會把它放到下面。

## 何時不用

- 只改開發側原始碼、不動實際遊戲 → 走 feature-dev。
- 只是要知道現在裝了什麼 → 讀 `instance/`，不用開分支。
- 改動需要跑遊戲才能確認 → 這條做完之後接 [runtime-qa](../runtime-qa/README.md)。
