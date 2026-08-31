# 日後素材／清理決定

## 夜貓－無心 3.1.0（可選精確替換）

目前 JH People 1.1.3＋NPC Plugin Chooser 2 的 536 NPC patch 已滿足方向，不阻塞整包。若仍要精確
3.1.0，只提供作者百度網盤中名稱含「人物美化」與「頭模替換」的 archive，放入既有
`/home/lorkhan/skyrim_mods/`；未取得完整資產許可不得公開重打包。見
[`相容性調查`](../wf/workflows/investigation/findings/wuxin-character-overhaul-se-ae-compatibility.md)。

## BG3 場景佈局實檔驗證

有合法遊戲資料時，以小型 `Levels/*.lsf` 做 `.lsf → .lsx`，記錄位置／旋轉／尺度／resource identity
能否無損對映 ModForge placements，再決定是否開 converter/spec；沒有實檔前不宣稱 pipeline 可行。
見 [`port-source-survey`](../analysis/port-source-survey/README.md)。

## 中文層五個裁示（2026-08-27 深夜起手清單第 5 條，仍未裁）

來源是 2026-08-28 的續行清單（已封存，只剩這條活著）；
逐項細節在 [`中文層覆蓋總表`](../modpack-design/content-plan/zh-layer/zh-layer-coverage-master-2026-08-28.md)的
「等使用者裁示」節：

1. **Bandolier NPC 層三選一**——注意覆寫陷阱不在 `BandolierForNPC.esp`，而在其後的
   `- No disenchant.esp`（70）與 `- Realistic Enchantements.esp`（23），forward patch 選項要照這個改設計。
2. **Reforging 綁 SkyPatcher** 要不要接受。
3. **AA（Armor Add-on）三個同版中文層選哪個流派**。
4. **`sLanguage` 要不要動**——現在是 `ENGLISH` 把中文塞英文槽；只附 `_chinese` 的層會靜默失效。
5. **Steam 2.5MB 補丁（TargetBuild 24914197）接不接受**——目前 acf 已搬出、exe 釘 1.6.1170。

## 2026-08-29 調查線留下的裁示

各線的完整結論在 [`agentctl DIGEST`](../agentctl/inbox/done/2026-08-29/DIGEST.md)，報告在 `agentctl/handoffs/done/2026-08-29/<線名>/REPORT.md`。

### 隨從凍結要不要維持（cx-fdlg）

Sofia／Recorder／Auri 的 dialogue 生態 GO 2／DEFER 5／NO-GO 13；Auri 技術與中文都可行，只因 follower 凍結判 NO-GO。
三問：是否維持凍結；是否採 Sofia Hub 的選配式 preflight；是否移除 Sofia bump dialogue。

### Mihail 生物要哪個方向（cx-mihail）

295 件 Creatures and Mounts 裡挑出 16 件低耦合 standalone，10 件有對版中文層（9 CHS／1 CHT）。
要定：自然環境／Morrowind／高奇幻哪個方向；hand-placed 還是 SkyPatcher topology；首批 4–6 件；接不接受 CHS。
