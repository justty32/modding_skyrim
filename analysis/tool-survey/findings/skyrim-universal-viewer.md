# Skyrim Universal Viewer（SUV）

← [tool-survey](../README.md)

**結論**：MO2 Python 插件，在 MO2 右側分頁瀏覽任一 mod 的 NIF／DDS／ESP／音效／HKX／Papyrus（loose 與 BSA 內）。沒有 CLI 或批次出圖；但 NIF 渲染器 `suv_nif_preview/` 不依賴 `mobase`，可由自寫驅動在 Linux（Python＋PyQt6＋Xvfb）離線出圖——**可當捏身形的形狀預覽元件；捏臉只到烘好的 FaceGen NIF，不會套 `.tri`／RaceMenu 滑桿**。未實測。

| 項目 | 值 |
|---|---|
| 版本／作者 | 1.4.62（2026-11-20）／AlhimikPh；Nexus SSE mod id 199895（由下載檔名推論，未查證） |
| 授權 | 未宣告（全樹無 license／copyright）→ 只自用，不搬程式碼進 repo |
| 規模 | Python 約 79k 行；選用 `_suv_native.pyd`（C++，cp312）；`tools/hkxc.exe`（serde-hkx）、`xWMAEncode.exe` |
| 需求 | Windows、MO2 2.5+（內建 Python 3.12＋PyQt6）、OpenGL 2.1；本機 MO2 2.5.2 符合，未安裝 |
| 網路 | 無（grep 無 urllib／socket／http） |
| 會改檔的功能 | 檔案複製／刪除、衝突「Hide Overriding」寫 `.mohidden`；首次啟動鎖 MO2 1-5 分鐘烘快取 |

## 渲染器可重用的介面（原始碼位置以 1.4.62 為準）

- `suv_nif_preview/nif_widget.py:81` `NifWidget(QOpenGLWidget)`：`set_nif_path()`（:306）、`frame_camera()`（:427）、`set_lighting_preset()`（:168）。
- `suv_nif_preview/texture_manager.py:100` `TextureManager(organizer=None, search_paths=[...])`：貼圖非同步（`QThreadPool`），擷取前要等載完。
- `suv_nif_preview/asset_resolver.py:60-113`：絕對路徑→MO2 VFS→search_paths→BSA；FaceGen 路徑 `.esp/.esm/.esl` 互換（:33-58）。
- 著色支援 FaceTint／SkinTint（`gl_scene_renderer.py:361,371`）、model-space 法線。
- 離屏範式：動畫 GIF 用 `grabFramebuffer()`（`suv_anim_preview/anim_player_widget.py:1589`、`gif_export.py`）。模型檢視器本身沒有存圖。
- 缺：`.tri` morph 解析、BodySlide preset／RaceMenu jslot 讀取。

## 下一步選項

1. 隔離原型（推薦）：`wf/temp` venv 裝 PyQt6、自寫驅動在 `xvfb-run` 渲染身體／FaceGen NIF 出圖——需授權安裝依賴與執行不可信程式碼。
2. 裝進 MO2 給人手動用——需授權動 MO2 安裝。
3. 僅留檔。

調查紀錄：2026-11-22 universal-viewer 線 REPORT（`agentctl/handoffs/home-2026-11-22/universal-viewer/REPORT.md`，到期即刪；本頁為留存結論）。
