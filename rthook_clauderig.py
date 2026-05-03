import sys
import zipfile
from pathlib import Path

if getattr(sys, "frozen", False):
    _meipass = Path(sys._MEIPASS)  # type: ignore[attr-defined]
    _zip_file = _meipass / "clauderig" / "templates_bundle.zip"
    _templates_dir = _meipass / "clauderig" / "templates"

    if _zip_file.exists():
        _templates_dir.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(str(_zip_file)) as _zf:
            _zf.extractall(str(_templates_dir))
