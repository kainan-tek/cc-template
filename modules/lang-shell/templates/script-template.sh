#!/usr/bin/env bash
set -euo pipefail

# {{PROJECT_NAME}} - {{PROJECT_DESCRIPTION}}

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

log() {
    local level="$1"; shift
    printf "[%s] %s\n" "$level" "$*" >&2
}

main() {
    log "INFO" "Starting {{PROJECT_NAME}}"
    # TODO: implement
}

main "$@"
