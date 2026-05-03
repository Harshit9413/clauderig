import sys
import shutil
from pathlib import Path

if getattr(sys, "frozen", False):
    _meipass = Path(sys._MEIPASS)  # type: ignore[attr-defined]
    _templates = _meipass / "clauderig" / "templates"
    if _templates.is_dir():
        for _stack in _templates.iterdir():
            if not _stack.is_dir():
                continue
            _dot_claude = _stack / ".claude"
            if _dot_claude.is_dir():
                continue
            _dot_claude.mkdir()
            for _item in _stack.iterdir():
                if _item.name == ".claude":
                    continue
                _dst = _dot_claude / _item.name
                if _item.is_dir():
                    shutil.copytree(str(_item), str(_dst))
                else:
                    shutil.copy2(str(_item), str(_dst))
