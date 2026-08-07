# 交接書 — deepseek（pi）· A4a：漢化包配對草稿

上位計畫：`~/repo/moddings/skyrim/workflows/plans/round-2026-08-07-catalog-and-korean.md`
你的角色：**執行者**。codex 是本輪領導，它出治具與判準；你負責量大的活。

## 最重要的三條護欄（先讀完再動手）

1. **你不刪任何東西。** 不 `rm`、不 `mv`、不清空任何目錄。**特別是 `~/skyrim_mods/.quarantine/`——隔離區本身也不准刪。**
   > 背景：2026-08-06 有一次外包作業把檔案照規矩移進隔離區之後，把整個隔離區刪掉了，107 筆記錄沒經 restore 就永久消失（ext4 無快照）。實質損失為零純屬運氣好。所以這條是硬規則，不是建議。
2. **你不寫 git。** 不 `git add`、不 `git commit`、不 `git checkout`。你的產出全部落在 `/home/lorkhan/skyrim_agent_out/deepseek/`（**在任何 git repo 之外**）。
3. **你不寫 MongoDB。** 本階段只讀。配對結果產成 TSV 交給 codex 審，審過才由 codex 的治具正式寫回。

另外：**不改 `~/notes/projects/modding/skyrim/tools/` 下的任何腳本**。那是 codex 的地盤。你發現 bug 就回報，不要自己修。

## 環境

mongod 是手動啟動的，不是 systemd 那個（系統的 `mongodb.service` 指向空的 `/var/lib/mongodb`，**不要動它**）：

```
mongod --dbpath ~/data/mongodb --bind_ip 127.0.0.1 --port 27018 --logpath /tmp/mongod-manual.log --fork
```

連線：`SKYRIM_MONGO_URI=mongodb://127.0.0.1:27018`，資料庫 `skyrim`。
schema 文件（唯讀參考）：`~/notes/projects/modding/skyrim/docs/mongodb-schema.md`。

## 任務

`skyrim.archives` 裡有一批 `is_translation: true` 的漢化包（估 ~286 筆）。要把每一個連回它翻譯的**本體 mod**。

### 做法（三段，逐段降級）

1. **檔名正規化比對**：把檔名裡的衍生標記去掉——`- CHS`、`- CHT`、`(Chinese Translation)`、`漢化`、`汉化`、`繁中`、`簡中` 等（實際有哪些標記你自己從資料裡掃出來，別只用我列的這幾個）——然後拿剩下的名字去比對 `skyrim.mods` 的 `name` 與 `nexus_mod_id`。
2. **對不上的，看內容表**：`archives` 文件裡有目錄列表。看裡面的 plugin basename（`.esp`/`.esm`/`.esl`）是否命中某個本體 mod 的 plugin。
3. **還是對不上就留空。不要猜。** 一個錯誤的配對比一個空值傷害大得多——它會讓後續的清理判準拿錯的本體去比版本。

### 產出

`/home/lorkhan/skyrim_agent_out/deepseek/translation-pairs-draft.tsv`，欄位：

```
archive_sha256 · archive_filename · normalized_name · matched_mod_id · matched_mod_name · match_method · confidence · note
```

- `match_method`：`filename` / `plugin_basename` / `none`
- `confidence`：`high` / `low` / `none`。**只要你有一絲不確定就寫 `low`**——codex 會把 `low` 的挑出來人工看，這正是它存在的意義
- `note`：對不上的原因、或配到多個候選時的候選清單

同時產一份 `/home/lorkhan/skyrim_agent_out/deepseek/translation-pairs-summary.md`：總數、三種 match_method 各多少、confidence 分布、以及你在資料裡實際觀察到的衍生標記有哪些（這份會回饋進計畫文件）。

## Done when

- [ ] TSV 產出，每一筆 `is_translation: true` 的 archive 都有一列（包含配不上的）
- [ ] summary.md 產出
- [ ] Mongo 完全沒被寫入（你可以自己驗：跑前跑後比對一個 archives 文件的內容）
- [ ] 在 tmux 印一行 `A4a DONE`

## 之後

codex 審過 TSV 之後，你會接 **A2**：跑 codex 寫的 `fetch_nexus_status.py` 對 ~1,400 個 mod 補 Nexus 在架狀態。那是長跑任務，一樣是「你跑、你回報，不改腳本」。
