#!/usr/bin/env bash
set -euo pipefail

usage='usage: log.sh [-f <logfile>] <decision> <why> <evidence> <result>'

logfile=''
if [[ ${1:-} == '-f' ]]; then
	[[ $# -ge 2 ]] || { printf '%s\n' "$usage" >&2; exit 1; }
	logfile=$2
	shift 2
fi
[[ $# -eq 4 ]] || { printf '%s\n' "$usage" >&2; exit 1; }

logfile=${logfile:-"$(git rev-parse --show-toplevel 2>/dev/null || pwd)/worklog.tsv"}
mkdir -p "$(dirname "$logfile")"

if top=$(git -C "$(dirname "$logfile")" rev-parse --show-toplevel 2>/dev/null); then
	top=$(realpath "$top")
	abs_log=$(realpath -m "$logfile")
	if [[ $abs_log == "$top"/* ]]; then
		rel=${abs_log#"$top"/}
		if ! git -C "$top" ls-files --error-unmatch -- "$rel" >/dev/null 2>&1; then
			exclude="$(git -C "$top" rev-parse --path-format=absolute --git-common-dir)/info/exclude"
			mkdir -p "$(dirname "$exclude")"
			if ! grep -qxF "/$rel" "$exclude" 2>/dev/null; then
				[[ ! -s $exclude || $(tail -c 1 "$exclude") == $'\n' ]] ||
					printf '\n' >> "$exclude"
				printf '/%s\n' "$rel" >> "$exclude"
			fi
		fi
	fi
fi

[[ -s $logfile ]] || printf 'ts\tdecision\twhy\tevidence\tresult\n' >> "$logfile"
ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)

clean() {
	local v=${1//$'\t'/ }
	v=${v//$'\n'/ }
	v=${v//$'\r'/ }
	[[ $v == [=+@-]* ]] && v="'$v"
	printf '%s' "$v"
}

printf '%s\t%s\t%s\t%s\t%s\n' \
	"$ts" "$(clean "$1")" "$(clean "$2")" "$(clean "$3")" "$(clean "$4")" \
	>> "$logfile"
