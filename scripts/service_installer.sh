#!/usr/bin/env bash
set -euo pipefail

log() {
    echo "$(date +'%F %T') | $*"
}

detect_pkg_manager() {
    if command -v apt-get >/dev/null 2>&1; then
        echo "apt"
    elif command -v dnf >/dev/null 2>&1; then
        echo "dnf"
    elif command -v yum >/dev/null 2>&1; then
        echo "yum"
    else
        echo "unknown"
    fi
}

install_nginx() {
    local pkg_manager="$1"

    case "$pkg_manager" in
        apt)
            sudo apt-get update -y
            if ! dpkg -s nginx >/dev/null 2>&1; then
                log "Installing nginx via apt"
                sudo DEBIAN_FRONTEND=noninteractive apt-get install -y nginx
            else
                log "nginx already installed (apt)"
            fi
            ;;
        dnf)
            if ! rpm -q nginx >/dev/null 2>&1; then
                log "Installing nginx via dnf"
                sudo dnf install -y nginx
            else
                log "nginx already installed (dnf)"
            fi
            ;;
        yum)
            if ! rpm -q nginx >/dev/null 2>&1; then
                log "Installing nginx via yum"
                sudo yum install -y epel-release || true
                sudo yum install -y nginx
            else
                log "nginx already installed (yum)"
            fi
            ;;
        *)
            log "Unsupported package manager"
            exit 2
            ;;
    esac
}

start_nginx() {
    if command -v systemctl >/dev/null 2>&1; then
        sudo systemctl enable nginx || true
        sudo systemctl restart nginx
    else
        sudo service nginx restart || sudo service nginx start || true
    fi

    log "nginx is installed and running"
}

main() {
    local pkg_manager
    pkg_manager="$(detect_pkg_manager)"

    log "Detected package manager: $pkg_manager"
    install_nginx "$pkg_manager"
    start_nginx
}

main "$@"