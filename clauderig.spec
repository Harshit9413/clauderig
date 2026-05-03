import os
import sys
import zipfile

block_cipher = None
APP_NAME = "clauderig"
ENTRY_POINT = "src/clauderig/cli.py"

sys.path.insert(0, os.path.join(SPECPATH, "src"))

_tmpl_src = os.path.join(SPECPATH, "src", "clauderig", "templates")
_zip_path = os.path.join(SPECPATH, "templates_bundle.zip")

with zipfile.ZipFile(_zip_path, "w", zipfile.ZIP_DEFLATED) as _zf:
    for _root, _dirs, _files in os.walk(_tmpl_src):
        for _f in _files:
            _src_file = os.path.join(_root, _f)
            _arc_name = os.path.relpath(_src_file, _tmpl_src).replace(os.sep, "/")
            _zf.write(_src_file, _arc_name)

a = Analysis([ENTRY_POINT], pathex=["src"], binaries=[],
    datas=[(_zip_path, ".")],
    hiddenimports=[], hookspath=[], hooksconfig={},
    runtime_hooks=["rthook_clauderig.py"], excludes=[], cipher=block_cipher, noarchive=False)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(pyz, a.scripts, a.binaries, a.zipfiles, a.datas, [],
    name=APP_NAME, debug=False, bootloader_ignore_signals=False,
    strip=False, upx=True, console=True, disable_windowed_traceback=False,
    target_arch=None, codesign_identity=None, entitlements_file=None)
