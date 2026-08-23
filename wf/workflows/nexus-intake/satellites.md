# nexus-intake — 衛星件：擴充／patch／漢化

[nexus-intake 主線](README.md) 的形態 B。**一個 mod 的衛星件常常散在好幾個 Nexus 頁面**，
而且各自有各自的版本節奏。整套互相咬合的生態走 [series.md](series.md)。

實例：Apothecary 本體 1.3.9 ＋ Fishing Patch 1.4.1 ＋ Rare Curios Patch 1.4.0 ＋
Saints and Seducers Patch 1.4.0，**四個版本號全不一樣**，各自還有各自的繁中層。

## 抓之前先列全

用 `housecarl_nexus_mod` 把本體頁的 requirements 與「相關檔案」列出來，做成一張表：

| 欄位 | 為什麼要 |
|---|---|
| 元件名 | —— |
| **各自的版本** | 元件版本幾乎不會跟本體一致 |
| 是否必需 | 分「requirement」與「optional」；optional 的先不抓 |
| 有沒有同版中文層 | 沒有就照成本規則決定，不要為了湊齊硬做 |
| 對應的本體版本 | **patch 要同時對上兩邊** |

## patch 的版本要對兩邊

`Apocalypse - Ordinator Compatibility Patch 10.0.2` 同時綁 Apocalypse 與 Ordinator 兩個版本。
只對上其中一邊就裝，等於裝了一個對另一邊無效甚至有害的 patch。

## 翻譯層可能只涵蓋部分元件

At Your Own Pace 有 9 個元件（版本 `2.1.0`／`2.1.0MG`／`3.0.4CP`／`1.1.1DB`／`1.1.0MS`／
`2.1.1TG`／`1.0.1DB`／`1.0.1DG`／`1.0.4TO`），中文層只覆蓋 8 個 ESP——
Dragonborn 元件本身就沒有 ESP。**覆蓋數少於元件數不一定是缺漏**，要逐個對，不要憑數字下結論。

## 排序：衛星件在本體之上，翻譯層在最上

```text
<X> 繁中層          ← 最高
<X> patch / 修正
<X> 本體            ← 最低
```

裝的時候一律 `--priority "before:<下一層的 mod 名>"`，裝完跑 `audit_layer_priority.py`。
