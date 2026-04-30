#!/usr/bin/env bash
set -e
APP="invoicer"
REPO="join/invoicer"
APT_REPO="john.github.io/apt-repo"

VERSION=$(curl -fsSL "https://api.github.com/repos/${REPO}/releases/latest" | grep '"tag_name"' | sed 's/.*"tag_name": *"\(.*\)".*/\1/')
echo "Installing ${APP} ${VERSION}..."

OS=$(uname -s)

if [ "$OS" = "Linux" ]; then
  if command -v apt-get &>/dev/null; then
    curl -fsSL https://${APT_REPO}/gpg.key | sudo apt-key add -
    echo "deb https://${APT_REPO} stable main" | sudo tee /etc/apt/sources.list.d/${APP}.list
    sudo apt-get update -qq && sudo apt-get install -y "$APP"
  fi
elif [ "$OS" = "Darwin" ]; then
  if command -v brew &>/dev/null; then
    brew tap ${REPO%/*}/${APP} 2>/dev/null || true
    brew install $APP
  fi
fi
echo "Done! Run: ${APP} --help"
