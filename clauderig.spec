import os

block_cipher = None
APP_NAME = "clauderig"
ENTRY_POINT = "src/clauderig/cli.py"


def collect_templates():
    """Walk templates dir manually so hidden dirs like .claude/ are included."""
    result = []
    src_base = os.path.join("src", "clauderig", "templates")
    dst_base = os.path.join("clauderig", "templates")
    for root, dirs, files in os.walk(src_base):
        for f in files:
            src_file = os.path.join(root, f)
            rel = os.path.relpath(root, src_base)
            dst_dir = dst_base if rel == "." else os.path.join(dst_base, rel)
            result.append((src_file, dst_dir))
    return result


a = Analysis([ENTRY_POINT], pathex=[], binaries=[],
    datas=collect_templates(),
    hiddenimports=[], hookspath=[], hooksconfig={},
    runtime_hooks=[], excludes=[], cipher=block_cipher, noarchive=False)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(pyz, a.scripts, a.binaries, a.zipfiles, a.datas, [],
    name=APP_NAME, debug=False, bootloader_ignore_signals=False,
    strip=False, upx=True, console=True, disable_windowed_traceback=False,
    target_arch=None, codesign_identity=None, entitlements_file=None)
