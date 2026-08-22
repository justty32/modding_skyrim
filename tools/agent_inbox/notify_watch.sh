#!/usr/bin/env bash
set -uo pipefail

readonly DEFAULT_INBOX_ROOT="/home/lorkhan/skyrim_agent_out/_inbox"
readonly INBOX_ROOT="${AGENT_INBOX_ROOT:-$DEFAULT_INBOX_ROOT}"
readonly POLL_SECONDS="${AGENT_INBOX_POLL_SECONDS:-20}"
readonly NEW_DIR="$INBOX_ROOT/new"
readonly READ_DIR="$INBOX_ROOT/read"
readonly WATCH_LIST="$INBOX_ROOT/watch.list"
readonly ANNOUNCED_DIR="$INBOX_ROOT/.state/announced"
readonly SEEN_WORKING_DIR="$INBOX_ROOT/.state/seen-working"
readonly ORPHAN_ANNOUNCED_DIR="$INBOX_ROOT/.state/orphan-announced"
readonly ORPHAN_PENDING_DIR="$INBOX_ROOT/.state/orphan-pending"

message_from=''
message_status=''
message_headline=''

debug() {
    printf 'notify_watch: %s\n' "$1" >&2
}

ensure_directories() {
    mkdir -p "$NEW_DIR" "$READ_DIR" "$ANNOUNCED_DIR" "$SEEN_WORKING_DIR" \
        "$ORPHAN_ANNOUNCED_DIR" "$ORPHAN_PENDING_DIR" || true
}

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

announce_new_messages() {
    local message basename marker

    for message in "$NEW_DIR"/*.md; do
        [[ -f $message ]] || continue
        basename=${message##*/}
        marker="$ANNOUNCED_DIR/$basename"
        [[ ! -e $marker ]] || continue

        parse_message "$message"
        if [[ -z $message_from || -z $message_status || -z $message_headline ]]; then
            debug "malformed message skipped: $message"
            continue
        fi

        printf '[INBOX] %s %s — %s\n' "$message_from" "$message_status" "$message_headline"
        touch "$marker" || true
    done
}

state_key_for() {
    local value=$1
    value=${value//%/%25}
    value=${value//\//%2F}
    printf '%s' "$value"
}

session_has_message() {
    local wanted=$1 directory message

    for directory in "$NEW_DIR" "$READ_DIR"; do
        for message in "$directory"/*.md; do
            [[ -f $message ]] || continue
            parse_message "$message"
            [[ $message_from != "$wanted" ]] || return 0
        done
    done
    return 1
}

clear_pending() {
    local pending=$1
    [[ ! -e $pending ]] || rm -f -- "$pending" || true
}

check_session() {
    local session=$1 key capture capture_ok=1
    local seen_marker gone_marker orphan_marker pending_marker

    key=$(state_key_for "$session")
    seen_marker="$SEEN_WORKING_DIR/$key"
    gone_marker="$ORPHAN_ANNOUNCED_DIR/gone--$key"
    orphan_marker="$ORPHAN_ANNOUNCED_DIR/idle--$key"
    pending_marker="$ORPHAN_PENDING_DIR/$key"

    capture=$(tmux capture-pane -p -t "$session" -S -60 2>/dev/null) || { capture_ok=0; true; }
    if (( capture_ok == 0 )); then
        if [[ ! -e $gone_marker ]]; then
            printf '[GONE] %s tmux session 已消失\n' "$session"
            touch "$gone_marker" || true
        fi
        clear_pending "$pending_marker"
        return
    fi

    # 'Working (' 是明顯在跑；'Waiting for background terminal (' 是被自己開的背景
    # 指令擋住（例如五分鐘一次的輪詢 sleep、或 protontricks 拉起 MO2 GUI）。
    # 後者一樣是活著的，不算孤兒——2026-08-22 對 codex-pandora 誤報兩次才補上。
    if [[ $capture == *'Working ('* || $capture == *'Waiting for background terminal ('* ]]; then
        touch "$seen_marker" || true
        clear_pending "$pending_marker"
        return
    fi

    if [[ ! -e $seen_marker || -e $orphan_marker ]] || session_has_message "$session"; then
        clear_pending "$pending_marker"
        return
    fi

    if [[ -e $pending_marker ]]; then
        printf '[ORPHAN] %s 已閒置但沒有發 inbox 訊息，可能跑完忘了回報或中途死掉\n' "$session"
        touch "$orphan_marker" || true
        clear_pending "$pending_marker"
    else
        touch "$pending_marker" || true
    fi
}

check_watched_sessions() {
    local session

    [[ -r $WATCH_LIST ]] || return
    while IFS= read -r session || [[ -n $session ]]; do
        session=${session%$'\r'}
        [[ -n $session ]] || continue
        check_session "$session"
    done < "$WATCH_LIST"
}

while true; do
    ensure_directories
    announce_new_messages
    check_watched_sessions
    sleep "$POLL_SECONDS" || true
done
