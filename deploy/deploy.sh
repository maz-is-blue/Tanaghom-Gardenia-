#!/bin/bash
# Run this every time you push changes and want to update the live site.
# Usage: bash deploy/deploy.sh

HOST="xbwywwwcvd@tanaghomgardenia.org"
REMOTE_DIR="/home/xbwywwwcvd/tanaghom"
PUBLIC_HTML="/home/xbwywwwcvd/public_html"

ssh "$HOST" bash << EOF
  set -e
  cd "$REMOTE_DIR"

  echo "--- Pulling latest changes ---"
  git pull origin master

  echo "--- Rebuilding static site ---"
  backend/venv/bin/python backend/build.py --domain

  echo "--- Deploying to public_html ---"
  cp -r dist/* "$PUBLIC_HTML/"

  echo ""
  echo "Done. Visit https://tanaghomgardenia.org"
EOF
