# 重新發佈、限制與最小驗證

[返回入口](../linux-manjaro-mo2-runbook.md)

## 什麼時候該重新 publish

沒有自動偵測，所以定成三條**明確觸發條件**，符合任一條就重跑「建議安裝步驟 1」：

1. **例行**：每次要開始一條會用到 houseCARL 的工作線之前，先對現役 exe 問一次版本，
   跟 `plugin/.claude-plugin/plugin.json` 的 `version` 比。不同就重 publish。
2. **事件**：`projects/houseCARL` 的 gitlink 一有推進（fork 合了新 commit、換 checkout），
   當次就重 publish，不要留到「下次需要時再說」。
3. **症狀**：出現「工具不存在」「找不到 loose asset／INI」「回報的 `.seq`／檔名大小寫對不上磁碟」
   這類徵狀時，先查版本再查別的——這些正是 Linux 修正所在的區域。

查詢工具（不需要 MO2 在跑，也不會動到任何檔案）：

```sh
python3 "$HOME/repo/moddings/skyrim/agentctl/tools/check_housecarl_deployed.py"
```

三態退出：`0` 現役即最新、`1` 過期（含未戳版本的 `0.0.0-dev`）、`2` 判不出來
（exe 不在、server 不回應、`plugin.json` 讀不到、或 `corpus.json` 不在 exe 旁邊）。
`2` 刻意不併進 `1`——「安裝壞了」與「你欠一次 publish」要採取的行動不同。

**別想用 shell 一行版做這件事。**顯而易見的
`printf '…initialize…' | housecarl-mcp | grep version` **完全沒有輸出**（2026-08-26 實測）：
stdin 一到 EOF server 就關掉，來不及寫回應。stdin 必須在整個交握期間保持開著，
所以這件事需要一支真的程式，不是一條管線。

### 2026-08-26 的實測基準

發現部署中的是 **1.6.0／35 tools**（2026-07-10 build），source 已在 `efe28f8`＝**1.8.1／44 tools**。
差 9 個工具、0 個移除：`housecarl_diff_record`、`housecarl_nexus_check_updates`、
`housecarl_nexus_graphql`、`housecarl_nexus_identify`、`housecarl_resolve`、
`housecarl_skse_config_audit`、`housecarl_skypatcher_layer`、`housecarl_skypatcher_read`、
`housecarl_update_status`。重新產生的 `corpus.json` 與舊的 **byte-identical**
（`6b965f16…`），所以 corpus 不是這次落差的來源，Mutagen 版本沒動。

## 風險與限制

<!-- wf-nav -->
1. **目前 Codex 需重開 session 才能直接用工具**：已註冊 `housecarl` MCP，但本次已啟動的 Codex session 不會自動熱載新 MCP。
2. **寫入 patch 前要先小規模讀取測試**：先問 active load order/status，再讀一個 vanilla record；確認解析正常後再要求它產 patch。
3. **in-place lane 暫時不要用**：houseCARL 支援直接改現有 plugin，但預設新 patch lane 才適合 Linux 首次驗證。
4. **Papyrus compiler / BSArch 外部工具另算**：資料層讀寫和 patch 產生可先跑；Papyrus 編譯、BSA repack 會牽涉 Wine/CK/工具路徑，應另做一次工具路徑設定。
5. **`corpus.json` 必須在 exe 旁邊**：只做 publish 會漏掉它，寫入工具與 type 查詢會全部失效（見「建議安裝步驟 1」）。
6. **大小寫敏感修正尚未進 upstream**：本機 clone 已修並 publish；換 source 或重裝後要重新確認（見「必要 Linux 修正 → 第二層」）。
7. **publish 出來的 exe 不會自己告訴你它過期了**：`housecarl-mcp` 沒有任何自我版本檢查，
   跑得動不代表是新的。判斷方式只有上面「什麼時候該重新 publish」那一節。

## 最小驗證順序

1. 註冊 MCP 後，先問 houseCARL load order status。
2. 確認它看到 `Modpack-KR` profile、active plugin 數與 MO2 大致一致。
3. 讀 `Skyrim.esm` 裡一個穩定 vanilla record。
4. 查一個已裝 SKSE plugin inventory，確認 VFS/mod winner 能解析。
5. 建立一個無害測試 patch mod，例如新增/修改容易回復的 dummy override；產物應出現在 `~/games/mod-organizer-2-skyrimspecialedition/modorganizer2/mods/houseCARL - <name>/`。
6. 在 MO2 refresh，啟用該 mod，再用 xEdit 或 MO2 檢查，不直接進遊戲測大型變更。
