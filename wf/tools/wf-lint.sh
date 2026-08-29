#!/usr/bin/env bash
# wf-lint.sh — 工作流文檔的機械檢查（純 bash + grep/sed/awk/find）
#
#   wf-lint.sh [--strict] [--quiet] <dir>...   檢查一個（導入後的）專案目錄
#   wf-lint.sh --self                          在模板 repo 內：template/ + examples/ + 各 flavor 合併模擬
#
# 檢查項：① 相對連結（.md / 目錄 / 任何檔）是否存在  ② workflows/ 下單檔 > 8192 bytes
#         ③ {{ / 〔模板說明〕 / 〔導入判斷〕 殘留  ④ inbox/ 頂層未辦信數
# 結束碼：有 BROKEN → 1；--strict 時殘留 > 0 也 → 1。
set -u

strict=0 self=0 quiet=0
dirs=()
for a in "$@"; do
  case "$a" in
    --strict) strict=1 ;;
    --self) self=1 ;;
    --quiet|-q) quiet=1 ;;
    -h|--help) sed -n '2,10p' "$0"; exit 0 ;;
    *) dirs+=("$a") ;;
  esac
done

total_broken=0 total_residue=0

# 列出檔案裡的相對連結（去掉 fenced code block 與行內 code span 後取 ](…)）
extract_links() {
  awk '/^[[:space:]]*```/{c=!c; next} !c' "$1" \
    | sed -E 's/`[^`]*`//g' \
    | grep -oE '\]\([^)]+\)' \
    | sed -E 's/^\]\(//; s/\)$//; s/ "[^"]*"$//'
}

# 檢查一批檔案的連結；檔案清單由 stdin 提供，$1 = 顯示路徑時要去掉的前綴
check_links() {
  local prefix=${1%/} f d l broken=0
  while IFS= read -r f; do
    d=$(dirname "$f")
    while IFS= read -r l; do
      [[ -z $l ]] && continue
      case $l in http://*|https://*|mailto:*|'#'*|'<'*) continue ;; esac
      l=${l%%#*}
      [[ -z $l ]] && continue
      if [[ ! -e "$d/$l" ]]; then
        echo "BROKEN ${f#$prefix/} -> $l"
        broken=$((broken + 1))
      fi
    done < <(extract_links "$f")
  done
  return $broken
}

list_md() { find "$1" -name '*.md' -not -path '*/node_modules/*' -not -path '*/.git/*' | sort; }

# 檢查一個目錄
lint_dir() {
  local root=${1%/} label=${2:-$1}
  local broken=0 oversize=0 ph=0 note=0 judge=0 inbox=0

  [[ $quiet -eq 1 ]] || echo "== $label"
  list_md "$root" | check_links "$root"; broken=$?

  while IFS= read -r f; do
    echo "OVERSIZE ${f#$root/} ($(wc -c <"$f") bytes > 8192)"
    oversize=$((oversize + 1))
  done < <(find "$root" -path '*/workflows/*' -name '*.md' -not -path '*/archive/*' -size +8192c | sort)

  ph=$(grep -ro '{{' --include='*.md' "$root" 2>/dev/null | wc -l | tr -d ' ')
  note=$(grep -ro '〔模板說明〕' --include='*.md' "$root" 2>/dev/null | wc -l | tr -d ' ')
  judge=$(grep -ro '〔導入判斷〕' --include='*.md' "$root" 2>/dev/null | wc -l | tr -d ' ')
  if [[ -d "$root/inbox" ]]; then
    inbox=$(find "$root/inbox" -maxdepth 1 -name '*.md' | wc -l | tr -d ' ')
  fi
  local residue=$((ph + note + judge))

  if [[ $quiet -eq 0 || $broken -gt 0 ]]; then
    echo "SUMMARY $label: broken=$broken oversize=$oversize residue={{=$ph 模板說明=$note 導入判斷=$judge inbox_pending=$inbox"
  fi
  total_broken=$((total_broken + broken))
  [[ $strict -eq 1 ]] && total_residue=$((total_residue + residue))
  return 0
}

if [[ $self -eq 1 ]]; then
  repo=$(cd "$(dirname "$0")/.." && pwd)
  cd "$repo" || exit 2

  # 根文件（只檢連結）
  echo "== repo root files"
  printf '%s\n' README.md AGENTS.md CLAUDE.md IMPORT.md CHANGELOG.md docs/README.md docs/non-invasive-import.md \
    | while read -r f; do [[ -f $f ]] && echo "$repo/$f"; done | check_links "$repo"
  b=$?; total_broken=$((total_broken + b)); echo "SUMMARY root: broken=$b"

  # 本 repo 規矩：任何檔都不超過 8192 bytes
  while IFS= read -r f; do echo "OVERSIZE ${f#$repo/} ($(wc -c <"$f") bytes > 8192)"; total_broken=$((total_broken + 1)); done \
    < <(find "$repo" -type f -not -path '*/.git/*' -size +8192c | sort)

  lint_dir "$repo/template" template

  for ex in "$repo"/examples/*/; do
    [[ -d $ex ]] || continue
    saved=$strict; strict=1; before=$total_residue
    lint_dir "$ex" "examples/$(basename "$ex")"
    strict=$saved
    [[ $total_residue -gt $before ]] && { echo "RESIDUE examples/$(basename "$ex") must have 0 residue"; total_broken=$((total_broken + 1)); }
  done

  # 各 flavor 單獨 + 全部一起，標準與非侵入式各跑一次
  flavors=()
  for fl in "$repo"/flavors/*/; do flavors+=("$(basename "$fl")"); done
  all=$(IFS=,; echo "${flavors[*]}")
  for combo in "${flavors[@]}" "$all"; do
    for mode in std wf; do
      tmp=$(mktemp -d)
      if [[ $mode == std ]]; then
        "$repo/tools/wf-init.sh" --target "$tmp" --flavor "$combo" --quiet >/dev/null || echo "wf-init failed: $combo ($mode)"
      else
        "$repo/tools/wf-init.sh" --target "$tmp" --flavor "$combo" --non-invasive wf --quiet >/dev/null || echo "wf-init failed: $combo ($mode)"
      fi
      lint_dir "$tmp" "merged[$combo,$mode]"
      rm -rf "$tmp"
    done
  done
else
  [[ ${#dirs[@]} -eq 0 ]] && dirs=(.)
  for d in "${dirs[@]}"; do lint_dir "$d" "$d"; done
fi

echo "TOTAL broken=$total_broken$( [[ $strict -eq 1 ]] && echo " residue=$total_residue" )"
[[ $total_broken -gt 0 ]] && exit 1
[[ $strict -eq 1 && $total_residue -gt 0 ]] && exit 1
exit 0
