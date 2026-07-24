#!/bin/bash
# Run this ONCE to set up the server for the first time.
# Usage: bash deploy/setup.sh

HOST="xbwywwwcvd@tanaghomgardenia.org"
REPO="https://github.com/maz-is-blue/Tanaghom-Gardenia-"
REMOTE_DIR="/home/xbwywwwcvd/tanaghom"
PUBLIC_HTML="/home/xbwywwwcvd/public_html"

ssh "$HOST" bash << EOF
  set -e

  echo "--- Cloning repository ---"
  git clone "$REPO" "$REMOTE_DIR"

  echo "--- Creating Python virtual environment ---"
  cd "$REMOTE_DIR"
  python3 -m venv backend/venv

  echo "--- Installing dependencies ---"
  backend/venv/bin/pip install --upgrade pip
  backend/venv/bin/pip install -r backend/requirements.txt

  echo "--- Building static site ---"
  backend/venv/bin/python backend/build.py --domain

  echo "--- Copying to public_html ---"
  cp -r dist/* "$PUBLIC_HTML/"

  echo ""
  echo "Setup complete. Visit https://tanaghomgardenia.org"
EOF
