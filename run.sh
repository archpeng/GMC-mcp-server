#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Load local .env if present
if [[ -f "$HERE/.env" ]]; then
  source "$HERE/.env"
fi

# Preflight: venv
if [[ ! -x "$HERE/.venv/bin/python" ]]; then
  echo "Python venv not found. Run: $HERE/bootstrap.sh" >&2
  exit 2
fi

# Preflight: Merchant ID
if [[ -z "${GMC_MERCHANT_ID:-}" ]]; then
  echo "GMC_MERCHANT_ID is not set. Create $HERE/.env (see .env.example)." >&2
  exit 3
fi

# Preflight: Google Auth (ADC or GOOGLE_APPLICATION_CREDENTIALS)
"$HERE/.venv/bin/python" - <<'PY'
import sys, google.auth
try:
    google.auth.default(scopes=["https://www.googleapis.com/auth/content"])
except Exception as e:
    print(
        "Google credentials not found.\n"
        "Fix by doing ONE of:\n"
        "  1) export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json\n"
        "  2) gcloud auth application-default login "
        "--scopes=https://www.googleapis.com/auth/content\n\n"
        f"Original error: {e}",
        file=sys.stderr,
    )
    raise SystemExit(4)
PY

exec "$HERE/.venv/bin/python" "$HERE/server.py"
