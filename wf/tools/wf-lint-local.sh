#!/usr/bin/env bash
# wf-lint-local.sh — 本 repo 的 wf-lint 外掛（project-owned，不是 kernel，升級 kernel 時不要覆蓋）。
# 契約：wf-lint 以 `bash wf/tools/wf-lint-local.sh <dir> <strict>` 呼叫；印 finding，exit 非 0＝有 finding
# （kernel 只在 --strict 算失敗）。目前只跑保留期檢查 wf-lint-retention.sh（規則見 STRUCTURE.md local 段）。
set -u
bash "$(dirname "${BASH_SOURCE[0]}")/wf-lint-retention.sh" "${1:-.}"
