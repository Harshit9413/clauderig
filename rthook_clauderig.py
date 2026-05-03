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
    _templates_dir = _meipass / "clauderig" / "templates"
    _templates_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(str(_zip_file)) as _zf:
        _zf.extractall(str(_templates_dir))
