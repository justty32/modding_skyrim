# tools-lib-refactor — 設計：目標結構、每步通則、風險

[計畫入口](README.md)｜盤點 [inventory.json](data/inventory.json)｜分步 [steps.json](data/steps.json)

## 目標結構

`agentctl/tools/lib/` 是一個普通套件，放在 `tools/` 底下。各工具既有的開機碼已經把 `tools/` 插進 `sys.path` 第 0 位，所以不用新增 path 設定，主套件 discover 也掃得到 `lib/test_*.py`。

<!-- wf-nav -->
| 模組 | 來源 | 步 |
|---|---|---|
| `lib/nif.py` | `npc_face/nifio.py` 原封；加 `custom_race/verify.nif_shape_names`（改名 `shape_names_any_bs`） | B1 |
| `lib/nifgeom.py` | `head_render/geom.py` 原封；私有名加公開別名 | B2 |
| `lib/dds.py` | `npc_face/dds.py`＋`outfit/dds.py`＋`head_render` 的 `load_image`／`sampler_from_image`＋jslot 的 DXT1 嗅探 | B3 |
| `lib/espwrite.py` | `npc_face/espwrite.py` 原封；C1 再加相容參數 | B4、C1 |
| `lib/writeguard.py` | `outfit/paths.py` 的寫檔與白名單段，根清單改由呼叫端給 | B5 |
| `lib/layerapply.py` | 四家 `make_manifest` 的共同部分 | B6 |
| `lib/facegen.py` | FaceGen 路徑樣板、slot 6 字串、`vfs_key`、`texture_key` | B7 |
| `lib/esptree.py`（可選） | `esp_reforward_tree.py` | C2 |

不動 `esplib/`。它有跨 repo 的 `ESPLIB_PATH` 契約，instance、mod-library 都在用；它的 README 也寫明「不寫 esp」。

## 每步通則

**先鎖再搬。** 每一步動手前，先確認守它的測試在現行碼上是綠的；不夠就先補（A1–A3），而且補完要能證明它會抓錯：故意改一個位元組或一個判斷，測試要變紅（outfit-tools 線用過的 mutate 做法）。

**複製，不搬移。** 新模組是舊檔的原封複製，舊檔改成別名（見下節）。呼叫端先不改，別名讓它們照跑。之後一支呼叫端一個 commit，改成直接 import `lib.*`。

**一步一 commit，可以單獨 revert。** 搬家是一個 commit，每個呼叫端改 import 各一個 commit。commit 只加明確路徑，跑 `hygiene_check.py`。

**條數不能少。** 每步做完，主套件、`look_transplant/tests`、`facegen_sculpt`、`jslot_render` 的條數與 skip 數要等於 S0 的基線（新增的測試另計）。

**同步文件放最後一步。** 依 [refactor](../../refactor/README.md) 一次只動一個面向：程式步驟只改 `agentctl/tools/README.md` 那一列；CODE_MAP、tool-index、各工具 README 留到 D1 一起改。

## 舊路徑怎麼留

舊檔不寫 `from lib.nif import *`。星號匯入不帶底線名，而 facegen_sculpt、outfit、11-25 的 handoff 腳本都在用底線名；測試對舊模組做 monkeypatch 時，也改不到新模組的全域。舊檔改成整個模組的別名：

```python
"""舊路徑：實作在 lib/nif.py（tools-lib-refactor B1）。"""
import sys
import lib.nif as _impl
sys.modules[__name__] = _impl
```

這樣 `npc_face.nifio is lib.nif`，例外類別、私有名、monkeypatch 全部一致。B1 的公司驗收含一條測試鎖住這件事：`npc_face.nifio is lib.nif`，`NifError` 是同一個類別。

`npc_face/dds.py` 與 `outfit/dds.py` 都要併進同一個 `lib/dds.py`。兩邊的例外類別名不同（`DdsError`、`DDSError`），`lib/dds.py` 兩個名字都定義；舊檔照樣做別名。

## 驗證方法

**公司**：全靠合成 fixture。A3 的差異表測試有三組：同一組輸入餵三家白名單出准／拒矩陣，餵三份 DDS header 解析，餵四家 manifest。它們既是迴歸測試，也是行為差異的文件。搬之前矩陣是什麼，搬之後就要一模一樣。

**回家**：14 條黃金回歸在 [home-regress.json](data/home-regress.json)，分兩批。H1 在 B1–B4 之後，驗 NIF、DDS、espwrite；H2 在 B5–C1 之後，驗白名單、manifest、custom_race。每批開跑前先用現行 main 出一份 before，再 pull 新碼出 after，比 sha256。這樣不用靠 `/tmp` 的舊夾還在。兩次之間載入序若變了，先用 `instance/tools/whichmod.py <FormID> --chain` 查，不算重構的問題。回家單照 [sites](../../../org/sites.md) 的 D34 寫，每批一張。

## 風險

**別名漏網。** 舊路徑若有人用 `importlib.reload` 或比對 `__name__`，別名後行為會不同。現在 grep 不到這種用法；B1 加一條冒煙測試：import 11-25 handoff 腳本用到的每個舊名。

**私有名公開化。** B2 給 `_decode_vertices` 等函式取公開名，但舊名保留。只要不刪舊名，facegen_sculpt、outfit 與 handoff 腳本都不受影響。

**看似相同、其實不同的函式。** 收攏時最容易出事的地方，在 inventory 的 behavior 欄逐條寫了，例如：`describe` 與 `read_dds` 判格式的規則不同；`vfs_key` 與 `texture_key` 處理空字串不同；三份 `find_ci` 對歧義的處理不同；custom_race 的 HEDR 記錄數不含 GRUP。原則是：收的是程式碼，不是語意。語意不同就留兩個函式或加參數，各自的預設值等於現行行為。

**custom_race 位元組。** C1 若漏了一個相容參數，四輪黃金裡逐位元組一致的層數（r2 4/4 等）會掉。A2 先在公司用合成配對表鎖 ESP sha256，C1 不能讓它變。

**沒有黃金的工具。** transplant_lib 沒有直接測試，真流程要 houseCARL（Q6 推薦這輪不收）。esp_reforward 只有 6 條 CLI 測試，A2 補整檔 sha256。

**測試直接改模組全域。** face_loop 的測試改 `cli.OVERWRITE`，movesets 的測試改 `M.rec`、`M.run_scan`。拆檔後這些覆寫可能不再生效，測試卻照樣綠（假綠）。F1 先加「改了全域、行為跟著變」的測試；movecond 推薦不拆（[big-files.json](data/big-files.json)）。

**別的線同時在改。** outfit、custom_race、racetest、head_render 這幾天都有修正線（fix-tools、fix-outfit）。動工前查 [line-claims](../../../../agentctl/docs/line-claims.md)，同一檔一次只給一條線。

**既有不穩的測試。** `test_runtime_log_window` 的 `test_rotation_only_inspects_the_new_papyrus_zero` 在 11-26 公司場整套跑時紅了一次，單跑兩次都綠。S0 記基線時要標成已知不穩，不要算成重構弄壞的。

## 大檔

兩支超過 600 行：`face_loop/cli.py` 推薦拆（F1，按檔內既有分段切成四檔）；`movesets/movecond.py` 推薦不拆（import 時就有副作用、測試直接改全域、近期沒人改）。300–600 行的 20 多支多半不拆；有幾支在收攏後自然變小：racetest/build、custom_race/cli、facegen_install、custom_race/esp。逐檔見 [big-files.json](data/big-files.json)。
