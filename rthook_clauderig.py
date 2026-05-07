import sys
import zipfile
from pathlib import Path

if getattr(sys, "frozen", False):
    _meipass = Path(sys._MEIPASS)
    _zip_file = _meipass / "templates_bundle.zip"
    if not _zip_file.exists():
        raise RuntimeError(
            f"clauderig bundle is corrupt: templates_bundle.zip not found in {_meipass}"
        )
    # Extract member by member so dotfiles/.claude dirs are created correctly
    _templates_dir = _meipass / "templates"
    _templates_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(str(_zip_file)) as _zf:
        for member in _zf.infolist():
            target = _templates_dir / member.filename
            if member.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                with _zf.open(member) as src, open(target, "wb") as dst:
                    dst.write(src.read())
