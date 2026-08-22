#!/usr/bin/env bash
set -uo pipefail

readonly DEFAULT_INBOX_ROOT="/home/lorkhan/skyrim_agent_out/_inbox"
readonly INBOX_ROOT="${AGENT_INBOX_ROOT:-$DEFAULT_INBOX_ROOT}"
readonly NEW_DIR="$INBOX_ROOT/new"

usage() {
    printf 'Usage: %s <session> <STATUS> <headline> [body_file]\n' "${0##*/}" >&2
}

fail() {
    printf 'inbox_send: %s\n' "$1" >&2
    exit 1
}

if (( $# < 3 || $# > 4 )); then
    usage
    exit 2
fi

session=$1
status=$2
headline=$3
body_file=${4-}

case "$session" in
    ''|*[!A-Za-z0-9._-]*)
        fail 'session must contain only letters, digits, dot, underscore, or hyphen'
        ;;
esac

case "$status" in
    DONE|BLOCKED|NEEDS-USER|FAILED|PROGRESS) ;;
    *) fail "invalid STATUS '$status' (allowed: DONE, BLOCKED, NEEDS-USER, FAILED, PROGRESS)" ;;
esac

if [[ -z $headline || $headline == *$'\n'* || $headline == *$'\r'* ]]; then
    fail 'headline must be one non-empty line'
fi

if [[ -n $body_file && ! -r $body_file ]]; then
    fail "body file is not readable: $body_file"
fi

mkdir_ok=1
mkdir -p "$NEW_DIR" || { mkdir_ok=0; true; }
(( mkdir_ok == 1 )) || fail "cannot create inbox directory: $NEW_DIR"

clock=''
clock_ok=1
clock=$(date '+%Y%m%dT%H%M|%Y-%m-%dT%H:%M:%S%:z') || { clock_ok=0; true; }
(( clock_ok == 1 )) || fail 'cannot read the current time'
stamp=${clock%%|*}
at=${clock#*|}

filename="${stamp}-${session}-${status}.md"
destination="$NEW_DIR/$filename"
[[ ! -e $destination ]] || fail "message already exists for this session, status, and minute: $destination"

tmp=''
cleanup() {
    if [[ -n $tmp && -e $tmp ]]; then
        rm -f -- "$tmp" || true
    fi
}
trap cleanup EXIT
trap 'exit 130' HUP INT TERM

tmp_ok=1
tmp=$(mktemp "$INBOX_ROOT/.inbox-send.XXXXXX") || { tmp_ok=0; true; }
(( tmp_ok == 1 )) || fail "cannot create temporary file in: $INBOX_ROOT"

if ! {
    printf '%s\n' '---'
    printf 'from: %s\n' "$session"
    printf 'status: %s\n' "$status"
    printf 'at: %s\n' "$at"
    printf '%s\n' '---'
    printf '# %s\n\n' "$headline"

    if [[ -n $body_file ]]; then
        while IFS= read -r line || [[ -n $line ]]; do
            printf '%s\n' "$line"
        done < "$body_file"
    else
        while IFS= read -r line || [[ -n $line ]]; do
            printf '%s\n' "$line"
        done
    fi
} > "$tmp"; then
    fail 'could not write the message body'
fi

move_ok=1
mv -- "$tmp" "$destination" || { move_ok=0; true; }
(( move_ok == 1 )) || fail "cannot publish message to: $destination"
tmp=''

printf '%s\n' "$destination"
