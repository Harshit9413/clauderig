#!/usr/bin/env bash
set -e
APP_NAME="clauderig"
VERSION="${APP_VERSION:-1.0.9}"

echo "Installing dependencies..."
pip3 install pyinstaller --quiet
pip3 install -r requirements.txt --quiet
pip3 install -e . --quiet

ARCH=$(uname -m)

echo "Building binary..."
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null; true
pyinstaller clauderig.spec --distpath dist/macos --workpath build/macos --clean

echo "Creating zip..."
mkdir -p "dist/zip/${APP_NAME}-${VERSION}-macos"
cp "dist/macos/${APP_NAME}" "dist/zip/${APP_NAME}-${VERSION}-macos/"

cd dist/zip
zip -r "../${APP_NAME}_${VERSION}_macos_${ARCH}.zip" "${APP_NAME}-${VERSION}-macos/"
cd ../..
echo "Done: dist/${APP_NAME}_${VERSION}_macos_${ARCH}.zip"
