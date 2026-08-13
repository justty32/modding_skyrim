# ideas — 想法入口

放不確定要不要做、還沒承諾的想法。這裡可以粗糙，但要能回頭理解。

## 規則

- 開始前寫 `Done when: <想法被保存到可回頭理解的程度>`；brainstorm 不需要完整驗證。
- 一個想法成熟後，若確定會做但不知何時，移到 [roadmap](../roadmap/README.md)。
- 需要認真討論架構時，升到 [specs](../specs/README.md)。
- 已放棄的想法可以移到 `archive/` 或標記為 dropped。

## Ideas

- **「無心人物風格」任務角色群**（2026-08-13）：使用者喜歡經典版「無心個人整合版」
  的人物風格，未來可能把這種角色外觀做成一個任務中的**全新具名 NPC 群**，而不是只替換
  vanilla NPC。已核對該整合的 LE 人物線以 `Decent Women`、Fair Skin、ECE、UNPB/CBBE、
  KS/SG hair 等為主；本機目前沒有無心包或 `Decent Women` archive。

  - 私人原型：可研究 LE FaceGen／head parts，轉成 SE 格式後建立新的 `NPC_` record、FaceGeom、
    FaceTint、voice type、outfit、AI package 與 quest alias；任務／對話由 ModForge spec 生成。
  - 公開發布：`Decent Women` Nexus 權限明示修改／再發布需作者許可，髮型、皮膚、眉毛等又有
    各自作者權利。沒有完整許可鏈時只能重做「相近審美」的原創 preset／FaceGen，不能把無心包
    或其第三方資產重新打包。
  - 升級成 spec 前先決定：角色數量與身份、是否只做女性、任務題材、私人自用或公開發布，並
    取得合法來源檔。技術驗證先挑一名角色做 LE→SE 外觀轉換與新 NPC 小樣，確認頸縫、膚色、
    表情、眨眼、Lip Sync、裝備 body 與存檔持久性，再批量化。

## 何時不用

- 已確定要做，走 roadmap/spec/plan。
- 是外部資料整理，走 research。
- 是立即可做的小修，直接做。
