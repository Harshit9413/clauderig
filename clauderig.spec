import os

block_cipher = None
APP_NAME = "clauderig"
ENTRY_POINT = "src/clauderig/cli.py"

# SPECPATH is set by PyInstaller to the directory containing this spec file.
# os.walk includes hidden dirs (.claude/) which datas=[] tuple silently skips.
_tmpl_src = os.path.join(SPECPATH, "src", "clauderig", "templates")
_tmpl_dst = "clauderig/templates"

_template_datas = []
for _root, _dirs, _files in os.walk(_tmpl_src):
    for _f in _files:
        _src = os.path.join(_root, _f)
        _rel = os.path.relpath(_root, _tmpl_src).replace(os.sep, "/")
        _dst = _tmpl_dst if _rel == "." else f"{_tmpl_dst}/{_rel}"
        _template_datas.append((_src, _dst))

a = Analysis([ENTRY_POINT], pathex=[], binaries=[],
    datas=_template_datas,
    hiddenimports=[], hookspath=[], hooksconfig={},
    runtime_hooks=[], excludes=[], cipher=block_cipher, noarchive=False)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(pyz, a.scripts, a.binaries, a.zipfiles, a.datas, [],
    name=APP_NAME, debug=False, bootloader_ignore_signals=False,
    strip=False, upx=True, console=True, disable_windowed_traceback=False,
    target_arch=None, codesign_identity=None, entitlements_file=None)
