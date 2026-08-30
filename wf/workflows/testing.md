# testing — 測試入口

把本專案所有常用驗證指令放這裡。agent 能跑的測試應自己跑；不能跑的記到 [../WAIT_USER.md](../../WAIT_USER.md)。

開始前寫 `Done when: <指定測試/驗證命令跑完，結果已回報>`。

## 母 repo 驗證

母 repo 主要是 Markdown、索引、submodule gitlink 與 Python stdlib 文件驗證器，沒有統一 build。
改文件時至少跑：

```bash
python -m unittest discover -s tools -p "test_*.py" -v
python tools/check_markdown_links.py
git diff --check
git status --short --branch
git submodule status
```

GitHub 的 `Documentation checks` 跑同一組 unittest，link checker 則加 `--skip-symlinks`。

`git submodule status` 行首空白代表 checkout 與母 repo gitlink 一致；`+` 代表不一致，`-` 代表
尚未初始化。fresh clone 或母 repo gitlink 更新後再跑：

```bash
git submodule update --init --recursive
```

## 常用離線測試

各子 repo 的命令、本機通過數基線與各自的坑，見
[testing/offline-matrix.md](testing/offline-matrix.md)；那份也收 `agent-bridge` 的 Windows DLL
clang-cl+xwin 驗證，以及「不在母 repo 複製命令」的 repo 清單。

判讀結果前先看 [testing/environment.md](testing/environment.md) 的已知環境條件（無 Godot、
`darksouls-port` 必須用自帶 venv、ModForge 的既有 warnings）。

## 測試分類

- `fast`：目標 repo 自己的 unit/source-gate；每次小改都跑。
- `contract`：跨 sibling repo 的真實 CLI/process boundary；改 producer、consumer 或 protocol 時跑。
- `full`：目標 repo README 指定的完整離線 suite；commit 前或大改後跑。
- `external`：需要 Skyrim、MO2、Godot GUI、遊戲素材、模型、帳號或人工感官驗收；不能由
  agent 代跑的項目記到 [../WAIT_USER.md](../../WAIT_USER.md)。

## 何時不用

- 只是查測試指令，直接讀本檔回答。
- 測試是 feature/refactor 的一部分，不需要另開測試工作流；在原工作流內執行即可。

## 綠燈不等於有檢查

**一道檢查通過，可能是因為它根本沒在檢查。** 這不是假設，2026-08-23 一天抓到四個
（profile 結構稽核、teardown 的「遊戲鎖已釋放」、`check_markdown_links.py`、自製 CJK 偵測），
四個實例與由此得到的兩個推論見 [testing/green-light-evidence.md](testing/green-light-evidence.md)。

### 規則：新增或修改一道檢查時，要證明它能變紅

```sh
# 餵一個「應該被擋」的輸入，確認 exit != 0
SKYRIM_MO2_INSTANCE="$fake" python3 <你剛改的那道檢查>; echo $?   # 應為 1
# 再餵正確的，確認 exit == 0
```

沒做過這個雙向驗證的檢查，不要拿它的綠燈當證據。
