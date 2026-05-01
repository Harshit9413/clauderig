#!/usr/bin/env bash
set -e
APP="clauderig"
REPO="harshit9413/clauderig"
APT_REPO="harshit9413.github.io/apt-repo"

VERSION=$(curl -fsSL "https://api.github.com/repos/${REPO}/releases/latest" | grep '"tag_name"' | sed 's/.*"tag_name": *"\(.*\)".*/\1/')
echo "Installing ${APP} ${VERSION}..."

OS=$(uname -s)

if [ "$OS" = "Linux" ]; then
  curl -fsSL https://${APT_REPO}/gpg.key | sudo apt-key add -
  echo "deb https://${APT_REPO} stable main" | sudo tee /etc/apt/sources.list.d/${APP}.list
  sudo apt-get update -qq && sudo apt-get install -y "$APP"
elif [ "$OS" = "Darwin" ]; then
  brew tap ${REPO%/*}/${APP} 2>/dev/null || true
  brew install $APP
fi
echo "Done! Run: ${APP} --help"
