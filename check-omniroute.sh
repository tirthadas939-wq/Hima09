#!/usr/bin/env bash
# Checks that a local OmniRoute gateway answers with a key and rejects requests without one.
# Usage: OMNIROUTE_API_KEY=your-endpoint-key ./check-omniroute.sh [base_url]

set -u

# Load OMNIROUTE_API_KEY from a .env file next to this script, if there is one.
ENV_FILE="$(dirname "$0")/.env"
if [ -f "$ENV_FILE" ]; then
  set -a
  # shellcheck disable=SC1090
  . "$ENV_FILE"
  set +a
fi

BASE_URL="${1:-http://127.0.0.1:20128/v1}"

if [ -z "${OMNIROUTE_API_KEY:-}" ]; then
  echo "Set OMNIROUTE_API_KEY to an endpoint key from the OmniRoute dashboard first." >&2
  exit 1
fi

echo "1) Listing models with the key at $BASE_URL ..."
if curl -fsS "$BASE_URL/models" -H "Authorization: Bearer $OMNIROUTE_API_KEY" >/dev/null; then
  echo "   OK: the gateway answered."
else
  echo "   FAILED: is OmniRoute running, and is the key correct?" >&2
  exit 1
fi

echo "2) Listing models without a key (expect 401) ..."
status=$(curl -s -o /dev/null -w '%{http_code}' "$BASE_URL/models")
if [ "$status" = "401" ]; then
  echo "   OK: requests without a key are rejected."
else
  echo "   WARNING: got HTTP $status. Make sure REQUIRE_API_KEY=true is set." >&2
  exit 2
fi
