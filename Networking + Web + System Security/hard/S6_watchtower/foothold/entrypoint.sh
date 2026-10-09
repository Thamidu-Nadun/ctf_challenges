#!/bin/sh
set -e

: "${SSH_USER:=player}"
: "${SSH_PASS:=player}"


if ! id "$SSH_USER" >/dev/null 2>&1; then
    adduser -D -s /bin/sh "$SSH_USER"
fi

echo "${SSH_USER}:${SSH_PASS}" | chpasswd

ssh-keygen -A

echo "[entrypoint] sshd starting — user='${SSH_USER}'"

exec /usr/sbin/sshd -D -e
