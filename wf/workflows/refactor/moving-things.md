# 搬移與改名

檔案換位置、目錄改名、專案拆 repo。2026-08-23 一天做了三次（工作區統整、profile 改名、
骨架收進 `wf/`），**每一次都以同一批方式壞掉**。這份是那批坑的清單與偵測程序。

```text
Done when: <逐檔比對已落地、六類斷裂已掃、工具冒煙測試過、連結歸零、CI 實測過>
```

## 鐵律：複製，不要搬移，直到驗證完

`cp -a` 進新位置 → 驗證 → 最後才清掉舊的。這樣不需要靠 tar 當救命繩，
而且中途出錯不會兩邊都沒有。清舊的之前先確認**來源已 commit 且已 push**。

## 六類會斷的東西

**只 grep 連結是不夠的。** 依實際踩到的頻率排序：

### 1. 硬編碼絕對路徑

```sh
grep -rn '/home/lorkhan/<舊路徑>' --include='*.py' --include='*.sh' --include='*.json'
```

踩過：`build_biggie_traits_cht_completion.py` 的 evidence root、13 個 QA spec 的
`manifest` 欄位、inbox 三支腳本的 `DEFAULT_INBOX_ROOT`。

### 2. `__file__` 相對推導——**語意會變**

```sh
grep -rn '__file__' --include='*.py'
```

最陰的一類：程式碼沒變、路徑也「還是相對的」，但**基準點變了**。
`scan_mod_library.py` 的 `BACKUP_DIR = Path(__file__).parent.parent / "backups"`
搬進 git repo 之後，每次 `backup` 會把 3MB 的 DB dump 提交進版控。

判準：`parents[n]` 指向**跟著一起搬的東西**就安全，指向**沒跟著搬的東西**就要改。

### 3. package import

```sh
grep -rn '^from \|^import ' --include='test_*.py'
```

`from scripts import x` 在 `scripts/` 消失後死掉。**兩次都是測試檔**——
因為主程式通常自己跑得起來，只有測試靠 package 佈局。改成從自身位置推導。

### 4. 相對 markdown 連結

跨 repo 拆分後**原本的兄弟變成別的 repo**。`git ls-files` **到 gitlink 就停**，
所以檢查器預設看不到 submodule——四條線曾累積 87 個壞連結而沒人知道。

修法：拿目標的 basename 去整個工作區找實體，再算相對路徑。
2026-08-23 兩輪共 134 個壞連結，自動解掉 79 個，其餘是同名多候選要手工指定。

### 5. CI 與外部設定

```sh
grep -rn '<舊路徑>' .github/ *.yml *.json ~/.claude/settings*.json
```

踩過：`.github/workflows/docs.yml` 跑的兩條指令、`hook-settings-snippet.json`。

### 6. 執行期資料目錄

不進版控的東西（鎖、inbox 投遞區、DB 快照）**不能跟著搬進 repo**，
但它們的路徑常寫在跟著搬的程式裡。

**最陰的變體**：路徑指向一個**已經不存在**的目錄，於是「已釋放／不存在」的檢查
**恆真通過**。遊戲鎖指著被刪掉的 `~/skyrim_agent_out/_lock/`，
每次 teardown 檢查都在檢查一個不可能存在的路徑。

## 驗證程序

```sh
# 1. 逐檔比對有沒有東西掉在半路（size + basename）
#    刻意不搬的要明確列出來，不要靠「應該沒漏」
# 2. 六類掃描（上面）
# 3. 每支搬過的工具冒煙測試
for f in <moved>/*.py; do python3 -c "import ast;ast.parse(open('$f').read())"; done
python3 <tool>.py --help
python3 -m unittest discover -s <dir> -p 'test_*.py'
# 4. 連結檢查，並確認檢查器涵蓋新位置
python3 tools/check_markdown_links.py
# 5. CI 指令實跑一次
```

## 改名時額外注意

- **名字會不會跟別的東西撞。** MO2 profile 一度改叫 `main`，結果它同時是分支名和目錄名，
  `git log main` 直接報 ambiguous。加前綴解掉（`modpack-main`）。
- **所有分支都要改。** 只改現役分支的話，切回其他分支時目錄名就對不上了。
  用 worktree 在別的分支上做，現役 checkout 全程不動。
- **區分「同一個東西的路徑」與「當時的紀錄」。** QA 報告、VERIFICATION.md、
  歷史 log 裡的舊路徑**不要改**——那些記的是當時實際用的路徑，改了就是竄改紀錄。
  只改「還會再跑」的東西：活工具、spec、CI、現役文件。

## 推母 repo 前檢查 submodule 指標

首次啟用：

```sh
git config core.hooksPath tools/hooks
```

`tools/hooks/pre-push` 只檢查本次 push 中相對 remote tip 新增或改變的 gitlink；既有、未隨本次
push 改變的壞指標不會鎖死閘門。若新指標的 commit 本機存在、fetch 後仍無法由 submodule 的
remote-tracking refs 走到，先照錯誤訊息列出的 `git -C <sub> push <remote> <branch>` 推送
submodule，再重試母 repo push。未初始化或本機不存在的 commit 只警告；緊急時可用
`git push --no-verify` 繞過。
