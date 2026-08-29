# mod-discovery — 上網找 mod

還不知道要哪個 mod 的階段。跟 [nexus-intake](../nexus-intake/README.md) 的差別是：
那條從「我要 mod X」開始，這條從「我想要某種內容」開始。

```text
Done when: <候選有結論(可追/暫放/不追)、連結存活狀態已查、結果回填 inbox>
```

## 分工：人挑頁面，AI 查頁面

**不做 AI 自動採集，也不維護 `skyrim.candidates` 隊列**：訊噪比太差，篩選成本高過人工翻頁。

```text
使用者人工翻來源索引 → 把有興趣的單頁 URL 貼進 inbox → AI 只處理 inbox 裡的 URL
```

## 來源索引

在 [`modpack-design/sources/`](../../../modpack-design/sources/)：

| 檔案 | 是什麼 |
|---|---|
| `global-source-index.md` | 全域來源索引：Nexus 以外的站點 |
| `korean-source-index.md` | 韓網來源（Tistory 等公開頁） |
| `mod-url-inbox.md` | **唯一入口**。有興趣的單頁貼這裡 |
| `candidate-review.md` | 候選審查的判準 |
| `mod-url-review-2026-08-12.md` | 一輪實際審查的結果 |

> 韓文也使用 `mod-url-inbox.md`，不要另開分流。

## AI 對 inbox URL 做什麼

**只做唯讀查證，不下載 mod 本體。** 每個 URL 回填五欄：

| 欄位 | 值域 |
|---|---|
| 頁面是否可讀 | live / blocked / gone |
| 下載是否可行 | Google Drive live / Drive dead / MEGA live / Yandex live / MediaFire live / 站內附件 / 需要登入 / 無下載 |
| 內容是否符合偏好 | 其他遊戲素材 porting／一次很多套裝備武器／地圖 porting／Nexus 不適合上架的敏感素材 |
| 風險 | 缺密碼、缺前置、LE/SE 不明、版權 port、成人內容 |
| 建議 | 可追 / 暫放 / 不追 |

**Nexus 頁面一律走 houseCARL MCP**（`housecarl_nexus_search`／`housecarl_nexus_mod`，無金鑰），
不要開瀏覽器代勞。只有非 Nexus 的站才需要實際抓頁面。
**codex 線沒有 houseCARL 也沒有瀏覽器**（2026-08-26 實測，見
[`agentctl/docs/dispatch-windows.md`](../../../agentctl/docs/dispatch-windows.md)），Nexus 查證由調度者親做，
派給 codex 的只能是「拿已寫死的 id／fileId 做離線收斂」。

## 狀態判定要寫死，不留臨場解讀空間

派給執行線時把判準寫成表，例如 Nexus v1 API：

```text
status="published" + available=true  → live
404                                   → gone
available=false 或 status ∈ {removed, wastebinned…} → hidden
其餘                                   → unknown
```

**`unknown` 不得觸發任何清理動作。** 判不出來就是判不出來，不要猜成 gone。

## 結果去哪

- 決定要裝 → 走 [nexus-intake](../nexus-intake/README.md)
- 決定納入整包規劃 → 走 [modpack-planning](../modpack-planning/README.md)
- 決定不追 → 記進 inbox 的「不要再看」表，附原因，避免下次重查

## 何時不用

- 已經知道要哪個 mod → 直接走 nexus-intake。
- 只是要知道某個框架怎麼運作（SPID、SkyPatcher…）→ 那是技術拆解，看
  [`analysis/mod-survey/`](../../../analysis/mod-survey/)。
