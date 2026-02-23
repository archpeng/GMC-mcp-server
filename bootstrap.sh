#!/usr/bin/env bash
# Bootstrap: create venv and install dependencies
set -e
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo ""
echo "✅ Done. Next steps:"
echo "  1. Copy .env.example to .env and fill in GMC_MERCHANT_ID"
echo "  2. Set up auth: export GOOGLE_APPLICATION_CREDENTIALS=/path/to/sa.json"
echo "  3. Run: source .venv/bin/activate && python server.py"
