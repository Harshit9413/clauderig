from __future__ import annotations
import json
from pathlib import Path


def detect_stack(path: Path) -> str | None:
    """Return one of five stack keys or None, based on marker files.

    Priority order:
      1. python-django  (manage.py present — definitive)
      2. react-native   (app.json with expo key)
      3. react-web      (package.json with react dependency)
      4. php            (composer.json present)
      5. python-fastapi (requirements.txt or pyproject.toml contains 'fastapi')
      6. python-django  (requirements.txt or pyproject.toml contains 'django')

    Note: php takes priority over requirements-based Django detection.
    A project with both composer.json and a requirements.txt mentioning django
    is treated as PHP.
    """
    # Django: manage.py is definitive
    if (path / "manage.py").exists():
        return "python-django"

    # React Native: app.json with expo key
    app_json = path / "app.json"
    if app_json.exists():
        try:
            data = json.loads(app_json.read_text())
            if "expo" in data:
                return "react-native"
        except (json.JSONDecodeError, OSError):
            pass

    # React Web: package.json with react dependency
    pkg_json = path / "package.json"
    if pkg_json.exists():
        try:
            data = json.loads(pkg_json.read_text())
            deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            if "react" in deps:  # exact key match — "react" not "react-router" etc.
                return "react-web"
        except (json.JSONDecodeError, OSError):
            pass

    # PHP: composer.json
    if (path / "composer.json").exists():
        return "php"

    # Python: requirements.txt or pyproject.toml
    for filename in ("requirements.txt", "pyproject.toml"):
        marker = path / filename
        if marker.exists():
            try:
                content = marker.read_text().lower()
                if "fastapi" in content:
                    return "python-fastapi"
                if "django" in content:
                    return "python-django"
            except OSError:
                pass

    return None
