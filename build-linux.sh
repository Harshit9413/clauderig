#!/usr/bin/env bash
set -e

APP_NAME="clauderig"
VERSION="${APP_VERSION:-1.0.3}"
MAINTAINER="harshit jangid <harshitjangid99291@gmail.com>"
DESCRIPTION="Bootstrap a production-grade .claude/ setup into any project, instantly."
ARCH="amd64"

if [ -z "${SKIP_BUILD}" ]; then
    pip install pyinstaller --quiet
    pip install -r requirements.txt --quiet
    pyinstaller clauderig.spec --distpath dist/linux --workpath build/linux --clean
fi

DEB_ROOT="dist/${APP_NAME}_${VERSION}_${ARCH}"
mkdir -p "${DEB_ROOT}/DEBIAN" "${DEB_ROOT}/usr/local/bin" "${DEB_ROOT}/usr/share/doc/${APP_NAME}"

cp "dist/linux/${APP_NAME}" "${DEB_ROOT}/usr/local/bin/${APP_NAME}"
chmod 755 "${DEB_ROOT}/usr/local/bin/${APP_NAME}"

cat > "${DEB_ROOT}/usr/share/doc/${APP_NAME}/changelog" << LOG
${APP_NAME} (${VERSION}) stable; urgency=low
  * Release ${VERSION}
 -- ${MAINTAINER}  $(date -R)
LOG
gzip -9 "${DEB_ROOT}/usr/share/doc/${APP_NAME}/changelog"

cat > "${DEB_ROOT}/DEBIAN/control" << CTRL
Package: ${APP_NAME}
Version: ${VERSION}
Architecture: ${ARCH}
Maintainer: ${MAINTAINER}
Section: utils
Priority: optional
Description: ${DESCRIPTION}
CTRL

dpkg-deb --build "$DEB_ROOT" "dist/${APP_NAME}_${VERSION}_${ARCH}.deb"
echo "Done: dist/${APP_NAME}_${VERSION}_${ARCH}.deb"
