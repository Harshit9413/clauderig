block_cipher = None
APP_NAME = "mytool"
ENTRY_POINT = "src/clauderig/cli.py"

a = Analysis([ENTRY_POINT], pathex=[], binaries=[], datas=[],
    hiddenimports=[], hookspath=[], hooksconfig={},
    runtime_hooks=[], excludes=[], cipher=block_cipher, noarchive=False)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(pyz, a.scripts, a.binaries, a.zipfiles, a.datas, [],
    name=APP_NAME, debug=False, bootloader_ignore_signals=False,
    strip=False, upx=True, console=True, disable_windowed_traceback=False,
    target_arch=None, codesign_identity=None, entitlements_file=None)
