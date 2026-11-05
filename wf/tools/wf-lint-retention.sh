#!/usr/bin/env bash
# wf-lint-retention.sh — 「過時即刪」與紀錄保留期的檢查（project-owned，四處同內容：母 repo、agentctl、
# modpack-design、mod-library 的 wf/tools/；由各自的 wf-lint-local.sh 呼叫）。規則出處：STRUCTURE.md local 段。
#
# 用法：bash wf-lint-retention.sh <dir>；印 finding 行，有 finding 結束碼 1。
#   ARCHIVE-DIR    受版控的 archive/、done/、superseded/、history/ 目錄（成品 l10n/mods/、plugins/ 豁免）
#   STALE-SESSION  handoffs/home-<日期>/ 超過 30 天且不在最近 5 場
#   HUB-OVERSIZE   SESSION-LOG.md > 2048、handoffs/NEXT-SESSION.md > 4096、2026-11-05（規則生效日）起的場次 STATE.md > 8192
set -u
dir=${1:-.}
dir=${dir%/}
n=0

if git -C "$dir" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  list() { git -C "$dir" -c core.quotepath=off ls-files; }
else
  list() { (cd "$dir" && find . -type f | sed 's|^\./||'); }
fi

while IFS= read -r d; do
  echo "ARCHIVE-DIR $dir/$d"; n=$((n + 1))
done < <(list | grep -Ev '^(l10n/mods|plugins)/' | awk -F/ '{
  for (i = 1; i < NF; i++) if ($i ~ /^(archive|done|superseded|history)$/) {
    out = $1; for (j = 2; j <= i; j++) out = out "/" $j; print out; break } }' | sort -u)

sessions=()
if [[ -d $dir/handoffs ]]; then
  while IFS= read -r s; do sessions+=("$s"); done < <(
    for p in "$dir"/handoffs/home-*/; do
      [[ -d $p ]] || continue
      b=$(basename "$p"); dt=$(grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' <<<"$b" | head -1)
      [[ -n $dt ]] && echo "$dt $b"
    done | sort)
fi
cutoff=$(date -d '30 days ago' +%F 2>/dev/null || echo 0000-00-00)
keep_from=$(( ${#sessions[@]} > 5 ? ${#sessions[@]} - 5 : 0 ))
for i in "${!sessions[@]}"; do
  dt=${sessions[$i]%% *}; b=${sessions[$i]#* }
  if (( i < keep_from )) && [[ $dt < $cutoff ]]; then
    echo "STALE-SESSION $dir/handoffs/$b ($dt)"; n=$((n + 1))
  elif [[ ! $dt < 2026-11-05 && -f $dir/handoffs/$b/STATE.md ]] && (( $(wc -c <"$dir/handoffs/$b/STATE.md") > 8192 )); then
    echo "HUB-OVERSIZE $dir/handoffs/$b/STATE.md ($(wc -c <"$dir/handoffs/$b/STATE.md") > 8192)"; n=$((n + 1))
  fi
done

for spec in "SESSION-LOG.md 2048" "handoffs/NEXT-SESSION.md 4096"; do
  f=$dir/${spec% *}; lim=${spec#* }
  [[ -f $f ]] && (( $(wc -c <"$f") > lim )) && { echo "HUB-OVERSIZE $f ($(wc -c <"$f") > $lim)"; n=$((n + 1)); }
done

echo "SUMMARY retention: findings=$n"
[[ $n -eq 0 ]]
