#!/data/data/com.termux/files/usr/bin/bash
# Installs what JARVIS needs inside Termux and checks that Termux:API responds.
# Usage: bash setup-termux.sh

set -e

echo "Installing packages..."
pkg update -y
pkg install -y python termux-api git

if [ ! -f .env ] && [ -f .env.example ]; then
  cp .env.example .env
  echo "Created .env from .env.example"
fi

echo "Checking Termux:API (needs the Termux:API app installed) ..."
if timeout 10 termux-battery-status >/dev/null 2>&1; then
  echo "OK: Termux:API is working."
else
  echo "Termux:API did not answer. Install the Termux:API app from F-Droid" >&2
  echo "and grant its permissions in Android settings, then run this again." >&2
  exit 1
fi

echo "Done. Start JARVIS with: python -m jarvis.main"
