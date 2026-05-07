from __future__ import annotations
import json
import re
from pathlib import Path


# ---------------------------------------------------------------------------
# Dependency file parsers
# ---------------------------------------------------------------------------

def _req_packages(text: str) -> set[str]:
    """Return lowercase package names from requirements.txt content.

    Handles version specifiers, extras, environment markers, and VCS lines.
    """
    names: set[str] = set()
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith(("#", "-", "git+", "http://", "https://")):
            continue
        line = line.split(";")[0].strip()  # drop environment markers
        name = re.split(r"[\[><=!~@\s]", line)[0].strip().lower()
        if name:
            names.add(name)
    return names


def _toml_packages(text: str) -> set[str]:
    """Return lowercase package names from pyproject.toml dependency sections.

    Handles both PEP 621 list format and Poetry table format.
    """
    names: set[str] = set()

    # PEP 621: dependencies = ["fastapi>=0.100", ...]
    for block in re.findall(r'dependencies\s*=\s*\[(.*?)\]', text, re.DOTALL):
        for match in re.finditer(r'["\']([A-Za-z0-9][A-Za-z0-9._-]*)', block):
            name = re.split(r"[\[><=!~@\s]", match.group(1))[0].lower()
            if name:
                names.add(name)

    # Poetry: [tool.poetry.dependencies] / [tool.poetry.dev-dependencies]
    in_section = False
    for raw in text.splitlines():
        line = raw.strip()
        if re.match(r'\[tool\.poetry\.(?:dev-)?dependencies\]', line):
            in_section = True
            continue
        if line.startswith("["):
            in_section = False
        if in_section and "=" in line and not line.startswith("#"):
            name = re.split(r'[\s=\["\'<>!~\[]', line)[0].strip().lower()
            if name and name != "python":
                names.add(name)

    return names


# ---------------------------------------------------------------------------
# Import scanner
# ---------------------------------------------------------------------------

def _has_import(path: Path, package: str) -> bool:
    """Return True if any .py source file in the project imports the package."""
    pattern = re.compile(
        rf'^\s*(?:import\s+{re.escape(package)}|from\s+{re.escape(package)}\b)',
        re.MULTILINE,
    )
    for py_file in [*path.glob("*.py"), *path.glob("*/*.py")]:
        try:
            if pattern.search(py_file.read_text(errors="ignore")):
                return True
        except OSError:
            pass
    return False


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def detect_stack(path: Path) -> str | None:
    """Detect the project stack using multi-signal scoring.

    Signals checked (highest weight first):
      - Import statements in source files          (+10)
      - Definitive marker files (manage.py)        (+15)
      - Framework-specific files (alembic, artisan)(+4–5)
      - Properly parsed dependency declarations    (+6)
      - Supporting files (wsgi, settings, urls)    (+3 each)

    Returns one of: python-fastapi, python-django, php,
    react-web, react-native — or None if no signals found.
    """
    scores: dict[str, int] = {
        "python-fastapi": 0,
        "python-django": 0,
        "php": 0,
        "react-web": 0,
        "react-native": 0,
    }

    # --- React Native: app.json with expo key ---
    app_json = path / "app.json"
    if app_json.exists():
        try:
            data = json.loads(app_json.read_text())
            if "expo" in data:
                scores["react-native"] += 10
        except (json.JSONDecodeError, OSError):
            pass

    # --- React Web / Native: package.json ---
    pkg_json = path / "package.json"
    if pkg_json.exists():
        try:
            data = json.loads(pkg_json.read_text())
            deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            if "expo" in deps or "react-native" in deps:
                scores["react-native"] += 8
            elif "react" in deps:
                scores["react-web"] += 8
        except (json.JSONDecodeError, OSError):
            pass

    # --- PHP: composer.json (Laravel artisan gives bonus) ---
    if (path / "composer.json").exists():
        scores["php"] += 10
    if (path / "artisan").exists():
        scores["php"] += 5

    # --- Django: marker files ---
    if (path / "manage.py").exists():
        scores["python-django"] += 15  # definitive
    for marker in ("wsgi.py", "asgi.py", "urls.py"):
        if (path / marker).exists():
            scores["python-django"] += 3
    if (path / "settings.py").exists() or list(path.glob("*/settings.py")):
        scores["python-django"] += 3

    # --- FastAPI: alembic signals ---
    if (path / "alembic.ini").exists() or (path / "alembic").is_dir():
        scores["python-fastapi"] += 4

    # --- Import scanning (beats stale dependency files) ---
    if _has_import(path, "fastapi"):
        scores["python-fastapi"] += 10
    if _has_import(path, "django"):
        scores["python-django"] += 10

    # --- Dependency file parsing ---
    packages: set[str] = set()

    for dep_file in ("requirements.txt", "requirements-base.txt", "requirements/base.txt"):
        marker = path / dep_file
        if marker.exists():
            try:
                packages |= _req_packages(marker.read_text(errors="replace"))
            except OSError:
                pass

    pyproject = path / "pyproject.toml"
    if pyproject.exists():
        try:
            packages |= _toml_packages(pyproject.read_text(errors="replace"))
        except OSError:
            pass

    pipfile = path / "Pipfile"
    if pipfile.exists():
        try:
            packages |= _req_packages(pipfile.read_text(errors="replace"))
        except OSError:
            pass

    if "fastapi" in packages:
        scores["python-fastapi"] += 6
    if "django" in packages:
        scores["python-django"] += 6

    # --- Return stack with highest score ---
    best = max(scores, key=lambda k: scores[k])
    return best if scores[best] > 0 else None


def detect_framework(path: Path, lang: str) -> str | None:
    """Best-effort framework detection for a known language.

    Used as a fallback when detect_stack() finds no full-stack signals
    but detect_language() identified the language.
    Returns a framework key like 'fastapi', 'django', 'reactjs', 'react-native',
    or None if signals are ambiguous or absent.
    """
    if lang == "python":
        packages: set[str] = set()
        for dep_file in ("requirements.txt", "requirements-base.txt", "requirements/base.txt"):
            marker = path / dep_file
            if marker.exists():
                try:
                    packages |= _req_packages(marker.read_text(errors="replace"))
                except OSError:
                    pass
        pyproject = path / "pyproject.toml"
        if pyproject.exists():
            try:
                packages |= _toml_packages(pyproject.read_text(errors="replace"))
            except OSError:
                pass
        pipfile = path / "Pipfile"
        if pipfile.exists():
            try:
                packages |= _req_packages(pipfile.read_text(errors="replace"))
            except OSError:
                pass

        django_score = 0
        if (path / "manage.py").exists():
            django_score += 15
        for marker in ("wsgi.py", "asgi.py", "urls.py"):
            if (path / marker).exists():
                django_score += 3
        if (path / "settings.py").exists() or list(path.glob("*/settings.py")):
            django_score += 3
        if _has_import(path, "django"):
            django_score += 10
        if "django" in packages:
            django_score += 6

        fastapi_score = 0
        if (path / "alembic.ini").exists() or (path / "alembic").is_dir():
            fastapi_score += 4
        if _has_import(path, "fastapi"):
            fastapi_score += 10
        if "fastapi" in packages:
            fastapi_score += 6

        if django_score > 0 and django_score >= fastapi_score:
            return "django"
        if fastapi_score > 0 and fastapi_score > django_score:
            return "fastapi"
        return None

    if lang == "react":
        app_json = path / "app.json"
        if app_json.exists():
            try:
                data = json.loads(app_json.read_text())
                if "expo" in data:
                    return "react-native"
            except (json.JSONDecodeError, OSError):
                pass
        pkg_json = path / "package.json"
        if pkg_json.exists():
            try:
                data = json.loads(pkg_json.read_text())
                deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
                if "expo" in deps or "react-native" in deps:
                    return "react-native"
                if "react" in deps:
                    return "reactjs"
            except (json.JSONDecodeError, OSError):
                pass

    return None


def detect_language(path: Path) -> str | None:
    """Return the primary language when full stack detection fails.

    Checks file-system signals only — no parsing required.
    Returns 'python', 'php', or 'react', or None if ambiguous.
    """
    # PHP: composer.json or any .php file in root
    if (path / "composer.json").exists() or list(path.glob("*.php")):
        return "php"

    # React: package.json that lists react/expo as a dependency
    pkg_json = path / "package.json"
    if pkg_json.exists():
        try:
            data = json.loads(pkg_json.read_text())
            deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            if "react" in deps or "react-native" in deps or "expo" in deps:
                return "react"
        except (json.JSONDecodeError, OSError):
            pass

    # Python: any standard project descriptor or .py files in root
    python_markers = [
        path / "pyproject.toml",
        path / "requirements.txt",
        path / "setup.py",
        path / "setup.cfg",
        path / "Pipfile",
    ]
    if any(m.exists() for m in python_markers) or list(path.glob("*.py")):
        return "python"

    return None
