# testing — 測試入口

把本專案所有常用驗證指令放這裡。agent 能跑的測試應自己跑；不能跑的記到 [../WAIT_USER.md](../WAIT_USER.md)。

開始前寫 `Done when: <指定測試/驗證命令跑完，結果已回報>`。

## 常用指令

```bash
# TODO: unit tests

# TODO: integration tests

# TODO: lint / format check

# TODO: build
```

## 測試分類

- `fast`: 每次小改都能跑。
- `full`: commit 前或大改後跑。
- `external`: 需要本機服務、實機、帳號、授權、下載資料。

## 已知環境性失敗

- 無。若有，寫清楚「失敗條件」「預期通過數」「為何不是 regression」。

## 何時不用

- 只是查測試指令，直接讀本檔回答。
- 測試是 feature/refactor 的一部分，不需要另開測試工作流；在原工作流內執行即可。
