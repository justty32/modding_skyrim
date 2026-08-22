#!/usr/bin/env bash
set -uo pipefail

readonly DEFAULT_INBOX_ROOT="/home/lorkhan/skyrim_agent_out/_inbox"
readonly INBOX_ROOT="${AGENT_INBOX_ROOT:-$DEFAULT_INBOX_ROOT}"
readonly NEW_DIR="$INBOX_ROOT/new"

message_from=''
message_status=''
message_headline=''

parse_message() {
    local path=$1
    local line in_frontmatter=0 after_frontmatter=0

    message_from=''
    message_status=''
    message_headline=''

    while IFS= read -r line || [[ -n $line ]]; do
        if (( after_frontmatter == 0 )); then
            if [[ $line == '---' ]]; then
                if (( in_frontmatter == 0 )); then
                    in_frontmatter=1
                else
                    after_frontmatter=1
                fi
            elif (( in_frontmatter == 1 )); then
                case "$line" in
                    'from: '*) message_from=${line#'from: '} ;;
                    'status: '*) message_status=${line#'status: '} ;;
                esac
            fi
        elif [[ -n $line ]]; then
            message_headline=${line#\# }
            break
        fi
    done < "$path"
}

[[ -d $NEW_DIR ]] || exit 0

for message in "$NEW_DIR"/*.md; do
    [[ -f $message ]] || continue
    parse_message "$message"
    printf '[INBOX] %s %s — %s — %s\n' \
        "${message_from:-UNKNOWN}" "${message_status:-UNKNOWN}" \
        "${message_headline:-（缺少標題）}" "$message"
done
