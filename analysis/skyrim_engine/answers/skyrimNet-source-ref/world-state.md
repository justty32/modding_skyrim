# 1. 世界狀態總結相關原始碼

[返回入口](../skyrimNet-source-ref.md)

## 1. 世界狀態總結相關原始碼

### 1.1 Prompt 模板引擎 — Scene Context

| 檔案 | 內容 |
|------|------|
| `SKSE/Plugins/SkyrimNet/prompts/components/context/scene_context_full.prompt` | 場景上下文五大區塊結構（Scene Info / Weather / Nearby People / Recent Events / Scene Summary） |
| `SKSE/Plugins/SkyrimNet/prompts/components/context/scene_context.prompt` | 精簡版 scene context |
| `SKSE/Plugins/SkyrimNet/prompts/components/context/scene_context_target_selection.prompt` | 目標選擇專用 context |
| `SKSE/Plugins/SkyrimNet/prompts/components/context/component_npc_state_summary.prompt` | **核心：NPC 行為狀態推論**（~25 種家具關鍵字比對: bed→睡覺, forge→打鐵, shrine→祈禱...） |
| `SKSE/Plugins/SkyrimNet/prompts/components/context/component_recent_events.prompt` | 近期事件摘要 |

### 1.2 Prompt 模板引擎 — 事件歷史

| 檔案 | 內容 |
|------|------|
| `SKSE/Plugins/SkyrimNet/prompts/components/event_history.prompt` | **完整事件歷史**（含時間差標記: "[A while ago]", "[Yesterday]"；時間間隙: "Some time passes...", "The next day..."） |
| `SKSE/Plugins/SkyrimNet/prompts/components/event_history_compact.prompt` | 精簡版（action selector 用） |
| `SKSE/Plugins/SkyrimNet/prompts/components/event_history_verbose.prompt` | 詳細版 |

### 1.3 Prompt 模板引擎 — Character Bio Submodules

1.3 Prompt 模板引擎 — Character Bio Submodules的記錄已抽到 [world-state-character-bio-templates.json](world-state-character-bio-templates.json)（16 列）。

檔案：保留原表「檔案」欄內容。

內容：保留原表「內容」欄內容。

統計：共 16 筆記錄、2 欄。

### 1.4 Prompt 模板引擎 — System Head & Guidelines

| 檔案 | 內容 |
|------|------|
| `SKSE/Plugins/SkyrimNet/prompts/submodules/system_head/0010_instructions.prompt` | 系統指令 |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/system_head/0020_format_rules.prompt` | 格式規則 |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/system_head/0100_actor_bios.prompt` | Actor bio 聚合 |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/system_head/0150_telepathy_awareness.prompt` | Telepathy 感知 |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/system_head/0200_scene_context.prompt` | 場景 context 聚合 |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/system_head/0250_omnisight.prompt` | OmniSight vision |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/system_head/0400_speech_style_bio.prompt` | 說話風格 bio |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/guidelines/0500_roleplay_guidelines.prompt` | Roleplay 指南 |

### 1.5 Prompt 模板引擎 — User Final Instructions

1.5 Prompt 模板引擎 — User Final Instructions的記錄已抽到 [world-state-instruction-templates.json](world-state-instruction-templates.json)（9 列）。

檔案：保留原表「檔案」欄內容。

內容：保留原表「內容」欄內容。

統計：共 9 筆記錄、2 欄。

### 1.6 Decorator 測試（展示所有可用 decorator 的實例）

1.6 Decorator 測試（展示所有可用 decorator 的實例）的記錄已抽到 [world-state-decorator-examples.json](world-state-decorator-examples.json)（9 列）。

檔案：保留原表「檔案」欄內容。

內容：保留原表「內容」欄內容。

統計：共 9 筆記錄、2 欄。

### 1.7 API 文件

| 檔案 | 內容 |
|------|------|
| `docs/modding/prompts-and-decorators.md` | **Decorator 使用指南**、`decnpc()` 回傳結構、Inja 模板語法、render mode 說明 |
| `docs/modding/WORKFLOW_PROMPTS.md` | Prompt 建立 workflow（含 decorator category 列表、context variables） |
| `docs/modding/prompt-file-syntax.md` | Prompt 檔案語法 |

---

