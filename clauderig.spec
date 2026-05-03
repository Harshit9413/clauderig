import os
import sys

block_cipher = None
APP_NAME = "clauderig"
ENTRY_POINT = "src/clauderig/cli.py"

sys.path.insert(0, os.path.join(SPECPATH, "src"))

_tmpl_src = os.path.join(SPECPATH, "src", "clauderig", "templates")
_tmpl_dst = "clauderig/templates"

_template_datas = []
for _root, _dirs, _files in os.walk(_tmpl_src):
    _rel_root = os.path.relpath(_root, _tmpl_src).replace(os.sep, "/")
    if ".claude" not in _rel_root:
        continue
    _rel_clean = _rel_root.replace("/.claude", "").replace(".claude/", "").replace(".claude", "")
    _dst = _tmpl_dst if not _rel_clean else f"{_tmpl_dst}/{_rel_clean}"
    for _f in _files:
        _template_datas.append((os.path.join(_root, _f), _dst))

a = Analysis([ENTRY_POINT], pathex=["src"], binaries=[],
    datas=_template_datas,
    hiddenimports=[], hookspath=[], hooksconfig={},
    runtime_hooks=["rthook_clauderig.py"], excludes=[], cipher=block_cipher, noarchive=False)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(pyz, a.scripts, a.binaries, a.zipfiles, a.datas, [],
    name=APP_NAME, debug=False, bootloader_ignore_signals=False,
    strip=False, upx=True, console=True, disable_windowed_traceback=False,
    target_arch=None, codesign_identity=None, entitlements_file=None)
