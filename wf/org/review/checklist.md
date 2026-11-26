審查座位 `review` 的檢查清單：同一類問題出現第二次才收；只列項目與出處，規矩本身看連結。

# 檢查清單：`review`

回 [卡](README.md)。收錄條件見卡「職責」：同一類問題第二次出現。

## 會寫檔的工具

- **每個實際寫出的檔都判白名單**，不只判根：先解析 realpath，再判在不在白名單裡；根底下的 symlink、硬連結（`st_nlink > 1`）都要擋；寫檔走同目錄暫存檔＋`os.replace`，不寫進既有 inode。白名單寫成「准哪裡」，不寫「擋哪裡」；MO2 mods／overwrite／profiles、遊戲 Data、`_layer-apply`、`_testlayer` 都不在裡面。出處：2026-11-26 custom_race（review-tools B 意見 4、review-outfit、fix-outfit）、outfit（review-outfit 意見 2、rereview-outfit N1）、racetest（review-tools A 意見 9）。
- **測試不得指向真的實機路徑**：拒寫測試要把 MO2、Data 等常數 patch 到 tempdir，守門退化時測試才不會自己寫進實機。出處：review-tools A 意見 10。

## 閘門與驗證

- **輸入缺、空集合、打錯 key 不得安靜 PASS**：路徑不存在、零筆、`--only` 對不到、基線是 null、選區零變色，都要報錯或 FAIL。逐一找「兩邊都是空所以相等」的比較。出處：2026-11-26 testlayer closeout（review-tools A 意見 1、6）、custom_race 零層與 G1 不核 NPC_（review-tools B 意見 2、3）、f5gate `forbid` 型別（A 意見 7）、outfit 帶內零變色與 P6 零筆（review-outfit、rereview-outfit N2）。
- **逐項判，不要合計後判一次**：合計的比例會被不相干的大項目稀釋。出處：outfit 溢色 R2／R3（review-outfit 意見 1）。只出現一次，先列著觀察。

## 回家單

- **預期結果要跟工具的新行為對得上**：修正改了預設（例如新的 FAIL 條件）時，回家單的「預期 rc」要跟著改；會被新條件擋的步驟寫明停下來交誰定。出處：2026-11-26 fix-tools C 的 J2 警告（rereview-tools C N1）、outfit 袖套 R3（rereview-outfit N3）。
- **預期不能在指令失敗時也成立**：「兩邊 rc 相同」「兩邊 diff 無差」在兩邊同樣失敗時也成立，要附「rc 不是 2」或「產物存在」。出處：2026-11-26 tools-lib 回家單 11(b) 漏必填參數、兩邊 rc 2 被判相同（rereview-tools-lib N1）；outfit R3「帶內 0%」同類。

上面 handoff 名稱都在 `agentctl/handoffs/home-2026-11-26/` 底下。
