# clauderig — Complete Project Explanation

Everything from the very first line of code to what happens when a user types `brew install clauderig`.
Written in simple, plain English. No shortcuts.

---

## Table of Contents

1. [What Are We Building?](#1-what-are-we-building)
2. [Why Does This Tool Exist?](#2-why-does-this-tool-exist)
3. [The Three Repositories — Why Three?](#3-the-three-repositories--why-three)
4. [Project Folder Structure](#4-project-folder-structure)
5. [Every Source File Explained](#5-every-source-file-explained)
6. [The Template Files Inside the Tool](#6-the-template-files-inside-the-tool)
7. [What is PyInstaller and Why We Use It](#7-what-is-pyinstaller-and-why-we-use-it)
8. [How the Binary is Built — Step by Step](#8-how-the-binary-is-built--step-by-step)
9. [The Build Scripts](#9-the-build-scripts)
10. [GitHub Releases — What and Why](#10-github-releases--what-and-why)
11. [GitHub Actions — Automation Explained](#11-github-actions--automation-explained)
12. [The Workflow File — Every Job and Command Explained](#12-the-workflow-file--every-job-and-command-explained)
13. [GitHub Secrets — What Are They?](#13-github-secrets--what-are-they)
14. [Package Managers — Homebrew, APT, Winget](#14-package-managers--homebrew-apt-winget)
15. [End User Journey — How Someone Installs and Uses clauderig](#15-end-user-journey--how-someone-installs-and-uses-clauderig)
16. [How to Release a New Version — Step by Step](#16-how-to-release-a-new-version--step-by-step)
17. [The Tricky PyInstaller Bug We Solved](#17-the-tricky-pyinstaller-bug-we-solved)

---

## 1. What Are We Building?

**clauderig** is a command-line tool (a CLI) that sets up a `.claude/` folder inside any software project.

The `.claude/` folder contains special configuration files that make Claude AI (Anthropic's AI coding assistant) much smarter about your specific project. Instead of Claude knowing nothing about your codebase, it learns:

- What language and framework you use (Python/FastAPI, Django, PHP/Laravel, React, React Native)
- What coding standards to follow
- What shortcuts (called "commands" or "slash commands") to give you
- How to connect to useful tools like databases, GitHub, Playwright testing

**Simple example:**

You have a new Python/FastAPI project. Without `clauderig`:

- Claude knows nothing about your project structure
- You have to explain everything from scratch

After running `clauderig init`:

```
myproject/
  .claude/
    CLAUDE.md              ← tells Claude about your project
    commands/              ← slash commands like /add-endpoint, /review
    skills/                ← deep knowledge about FastAPI patterns
    hooks/                 ← scripts that run when Claude edits files
    rules/                 ← coding standards to always follow
    settings.json          ← which tools (MCP servers) Claude can use
```

Now when you open Claude Code in that project folder, Claude already knows everything.

---

## 2. Why Does This Tool Exist?

Every developer who uses Claude Code has to manually create `.claude/` folders. This takes time, and most people don't know the best practices.

clauderig solves this by giving you a **production-grade** `.claude/` setup in one command:

```bash
clauderig init
```

That's it. One command. Done.

---

## 3. The Three Repositories — Why Three?

We use **three separate GitHub repositories** for this project. This is a common pattern for distributing software. Here's why:

### Repository 1: `harshit9413/clauderig` (Main Code Repo)

**What it is:** The actual Python source code of the tool.

**What it contains:**

- All the Python code
- Templates (the `.claude/` folder blueprints)
- Build scripts
- GitHub Actions workflow

**Why it exists:** This is where development happens. Developers write code here, fix bugs here, add features here.

---

### Repository 2: `harshit9413/homebrew-clauderig` (Homebrew Formula Repo)

**What it is:** A recipe that tells Homebrew (the macOS package manager) how to install clauderig.

**What it contains:** A single file called `Formula/clauderig.rb` that says:

```ruby
class Clauderig < Formula
  version "1.0.10"
  url "https://github.com/.../clauderig_1.0.10_macos_arm64.zip"
  sha256 "abc123..."    # checksum to verify the download
  
  def install
    bin.install "clauderig"  # puts the binary in /opt/homebrew/bin/
  end
end
```

**Why it is SEPARATE from the main repo:** Homebrew requires formula files to be in a repository that follows its naming convention (`homebrew-<name>`). When you run `brew tap harshit9413/clauderig`, Homebrew looks for a repo named `homebrew-clauderig` under that GitHub user. It cannot be in the main code repo.

**Example:** When a user runs:

```bash
brew install harshit9413/clauderig/clauderig
```

Homebrew:

1. Looks up `harshit9413/homebrew-clauderig` on GitHub
2. Reads `Formula/clauderig.rb`
3. Downloads the zip file from the URL in the formula
4. Extracts it and puts `clauderig` binary in `/opt/homebrew/bin/`

---

### Repository 3: `harshit9413/apt-repo` (Linux APT Repository)

**What it is:** A Debian/Ubuntu package repository hosted on GitHub Pages.

**What it contains:** The `.deb` package files plus metadata files that APT (Ubuntu/Debian's package manager) reads.

**Why it is SEPARATE:** APT repositories have a very specific folder structure with cryptographic signatures. GitHub Pages serves these files over HTTPS. APT on the user's computer reads the metadata to know what packages are available, their versions, and their checksums.

**Why it cannot be in the main repo:** The APT repository needs to be on GitHub Pages (a static website). GitHub Pages serves content from a specific branch (`gh-pages`). The main code repo uses the `main` branch for development. Mixing them would be messy and confusing.

**Example:** When a user runs:

```bash
echo "deb [trusted=yes] https://harshit9413.github.io/apt-repo stable main" | sudo tee /etc/apt/sources.list.d/clauderig.list
sudo apt update
sudo apt install clauderig
```

APT:

1. Downloads the metadata from `harshit9413.github.io/apt-repo`
2. Finds the `clauderig` package
3. Downloads the `.deb` file
4. Installs the binary to `/usr/local/bin/clauderig`

---

## 3b. GitHub Pages — How It Powers Our APT Repository

This section deserves its own detailed explanation because it is the invisible backbone of the Linux distribution system.

### What is GitHub Pages?

GitHub Pages is a **free static website hosting service** built into GitHub. For any repository, you can turn on GitHub Pages and GitHub will host the files in that repository as a website available at:

```
https://<username>.github.io/<repository-name>/
```

**Example:** The `harshit9413/apt-repo` repository is served at:
```
https://harshit9413.github.io/apt-repo/
```

### What is a "Static Website"?

A static website just means the files are served as-is, with no server-side code running. GitHub reads files from the repository and sends them to anyone who requests them over HTTP.

This is perfect for an APT repository because APT just needs to download files — it doesn't need any server logic. The files are:
- `dists/stable/Release` — metadata file listing what's in the repo
- `dists/stable/main/binary-amd64/Packages` — index of all packages
- `pool/main/c/clauderig/clauderig_1.0.10_amd64.deb` — the actual package

### How We Set It Up

The `harshit9413/apt-repo` repository has a special branch called `gh-pages`. GitHub Pages is configured to serve files from this branch.

```
harshit9413/apt-repo (repository)
  └── gh-pages (branch)             ← GitHub Pages serves from here
       ├── dists/
       │   └── stable/
       │       ├── Release           ← signed metadata
       │       ├── Release.gpg       ← GPG signature
       │       └── main/
       │           └── binary-amd64/
       │               └── Packages  ← package index
       └── pool/
           └── main/
               └── c/
                   └── clauderig/
                       └── clauderig_1.0.10_amd64.deb
```

### How `reprepro` Creates This Structure

`reprepro` is a tool that manages Debian repositories. When our GitHub Actions job runs:

```bash
reprepro includedeb stable clauderig_1.0.10_amd64.deb
```

`reprepro` automatically:
1. Copies the `.deb` file to `pool/main/c/clauderig/`
2. Updates `dists/stable/main/binary-amd64/Packages` with the new package info
3. Updates `dists/stable/Release` with new checksums
4. Signs `Release` with the GPG key to create `Release.gpg`

Without `reprepro`, you'd have to maintain all this manually.

### How GitHub Pages Serves the Repository

After `reprepro` updates the files and we push to `gh-pages`:

```
GitHub Pages serves:
  https://harshit9413.github.io/apt-repo/dists/stable/Release
  https://harshit9413.github.io/apt-repo/pool/main/c/clauderig/clauderig_1.0.10_amd64.deb
  ... all other files
```

These URLs are permanent and never change (only the content changes with each release).

### How APT on a User's Machine Reads This

When the user runs `sudo apt update`, APT:

1. Reads `/etc/apt/sources.list.d/clauderig.list` which contains:
   ```
   deb [trusted=yes] https://harshit9413.github.io/apt-repo stable main
   ```
   
2. Goes to `https://harshit9413.github.io/apt-repo/dists/stable/Release`
3. Downloads the `Release` file to check what packages are available
4. Downloads `Packages` index to get package names, versions, and download URLs
5. Caches this locally at `/var/lib/apt/lists/`

When the user runs `sudo apt install clauderig`:

1. APT looks up `clauderig` in its local cache
2. Finds the download URL: `https://harshit9413.github.io/apt-repo/pool/main/c/clauderig/clauderig_1.0.10_amd64.deb`
3. Downloads the `.deb` file
4. Verifies the SHA256 checksum matches what's in `Packages`
5. Extracts and installs

### What Happens During a New Release

When we release version 1.0.11:

```
GitHub Actions Job 5 runs:
    ↓
Downloads clauderig_1.0.11_amd64.deb
    ↓
Checks out harshit9413/apt-repo at gh-pages branch
    ↓
reprepro includedeb stable clauderig_1.0.11_amd64.deb
    (adds new .deb, updates metadata, signs everything)
    ↓
git push → GitHub Pages now serves updated files
    ↓
User runs: sudo apt update
    (APT downloads fresh metadata, sees 1.0.11 is available)
    ↓
User runs: sudo apt upgrade clauderig
    (APT downloads 1.0.11 and installs it)
```

### Why GitHub Pages Instead of a Real Server?

| GitHub Pages | Paid Server |
|---|---|
| Free forever | Costs money monthly |
| Maintained by GitHub | You maintain it |
| 99.9% uptime guaranteed | You handle downtime |
| Automatic HTTPS | You configure SSL |
| Works perfectly for static files | Needed only if you run code |

For serving static files (which is all an APT repository needs), GitHub Pages is perfect and free.

### The `[trusted=yes]` Part — Why We Use It

In the full APT setup, you'd have:
```bash
# Proper GPG key import (more secure):
curl -fsSL https://harshit9413.github.io/apt-repo/clauderig.gpg | sudo gpg --dearmor -o /usr/share/keyrings/clauderig.gpg
echo "deb [signed-by=/usr/share/keyrings/clauderig.gpg] https://harshit9413.github.io/apt-repo stable main" | sudo tee /etc/apt/sources.list.d/clauderig.list
```

We currently use `[trusted=yes]` which tells APT to trust the repository without checking the GPG signature. This is simpler for users but slightly less secure. For a full production setup, the GPG key import approach is preferred.

---

## 4. Project Folder Structure

```
clauderig/                          ← main repository root
│
├── src/
│   └── clauderig/                  ← Python package (the actual code)
│       ├── __init__.py             ← package version
│       ├── __main__.py             ← lets you run `python -m clauderig`
│       ├── cli.py                  ← command-line interface (what user types)
│       ├── analyzer.py             ← auto-detects what kind of project it is
│       ├── installer.py            ← copies template files into user's project
│       └── templates/              ← the .claude/ folder blueprints
│           ├── python-fastapi/
│           ├── python-django/
│           ├── php/
│           ├── react-web/
│           └── react-native/
│
├── .github/
│   └── workflows/
│       └── release.yml             ← GitHub Actions: automatic build + publish
│
├── clauderig.spec                  ← PyInstaller build recipe
├── rthook_clauderig.py             ← PyInstaller runtime hook (runs at startup)
├── build-macos.sh                  ← script to build macOS binary
├── build-linux.sh                  ← script to build Linux binary + .deb package
├── pyproject.toml                  ← Python package definition + metadata
├── requirements.txt                ← Python library dependencies
├── .gitignore                      ← files git should not track
└── README.md                       ← documentation for GitHub
```

---

## 5. Every Source File Explained

### `pyproject.toml` — The Package ID Card

This is the **official definition** of the Python package. Every Python package needs this file.

```toml
[project]
name = "clauderig"          # the package name on PyPI and in pip
version = "1.0.10"          # current version number
description = "..."         # one-line description
requires-python = ">=3.10"  # minimum Python version required

dependencies = [
    "typer>=0.12",          # library that makes CLI apps easy to build
    "rich>=13.0",           # library for pretty colored terminal output
]

[project.scripts]
claude-setup = "clauderig.cli:app"  # creates the `claude-setup` command
```

The `[project.scripts]` section is very important. It tells Python: "When this package is installed, create a command called `claude-setup` that runs `clauderig.cli:app`."

**Wait, isn't the command called `clauderig`?** Yes! The PyInstaller binary is named `clauderig`. The `claude-setup` script is for users who install via `pip install clauderig` instead of downloading the binary.

```toml
[tool.setuptools.package-data]
clauderig = [
    "templates/**/.claude/*",
    "templates/**/.claude/**/*",
]
```

This tells Python to include the `.claude/` template folders when packaging. Without this, pip install would NOT include the template files, and the tool would have nothing to copy.

---

### `requirements.txt` — Library Dependencies

```
typer>=0.12
rich>=13.0
```

Very simple. Just two external libraries:

- **typer**: Makes building CLI tools easy. You define Python functions and typer automatically creates the command-line interface with `--help`, options, arguments, etc.
- **rich**: Makes terminal output beautiful. Gives us colored text, tables, progress bars.

---

### `src/clauderig/__init__.py` — Package Version

```python
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("clauderig")
except PackageNotFoundError:
    __version__ = "0.1.0"
```

This file does one thing: reads the version number from the installed package metadata. When you run `clauderig version`, this is where that number comes from.

**Why `try/except`?** If the package isn't installed (you're running it directly from source during development), `PackageNotFoundError` would crash. The fallback `"0.1.0"` prevents that crash.

---

### `src/clauderig/__main__.py` — Direct Execution

```python
from clauderig.cli import app

if __name__ == "__main__":
    app()
```

This tiny file lets developers run the tool without installing it:

```bash
python -m clauderig init
```

The `-m clauderig` part tells Python to look for `__main__.py` inside the `clauderig` package and run it.

---

### `src/clauderig/cli.py` — The Command-Line Interface

This is the **front door** of the application. It defines every command the user can type.

**Commands defined:**

- `clauderig init` — main command, sets up `.claude/` in a project
- `clauderig list` — shows all supported stacks in a table
- `clauderig version` — prints the version number

**The `init` command flow:**

```
User runs: clauderig init
    ↓
No --lang flag given? → Auto-detect the project type (calls analyzer.py)
    ↓
Detected "Python → FastAPI"? Ask: "Use detected stack? [Y/n]"
    ↓
User says Y → Resolve to internal stack name "python-fastapi"
    ↓
Call installer.py to copy the template files
    ↓
Print success message
```

**Simple example of what `_resolve_stack` does:**

```python
_resolve_stack("python", "fastapi")   → returns "python-fastapi"
_resolve_stack("react", "reactjs")    → returns "react-web"
_resolve_stack("php", None)           → returns "php"
_resolve_stack("php", "laravel")      → ERROR: php doesn't take a framework
```

---

### `src/clauderig/analyzer.py` — Auto-Detection

When you run `clauderig init` without specifying `--lang`, the tool looks at your project files to guess what kind of project it is.

**How it works — the scoring system:**

The analyzer gives "points" to each possible stack based on what files it finds:

| File Found                              | Points Given To    |
| --------------------------------------- | ------------------ |
| `manage.py` exists                    | +15 to Django      |
| `import fastapi` in any `.py` file  | +10 to FastAPI     |
| `import django` in any `.py` file   | +10 to Django      |
| `package.json` has `"react-native"` | +8 to React Native |
| `package.json` has `"react"`        | +8 to React Web    |
| `composer.json` exists                | +10 to PHP         |
| `artisan` file exists                 | +5 to PHP          |
| `fastapi` in `requirements.txt`     | +6 to FastAPI      |
| `alembic.ini` exists                  | +4 to FastAPI      |

The stack with the **most points wins** and gets suggested to the user.

**Example:**

```
Your project has: manage.py, wsgi.py, requirements.txt with "django"
Scores: Django=15+3+6=24, FastAPI=0, PHP=0, React=0
Winner: Django ✓
```

---

### `src/clauderig/installer.py` — File Copier

This file does the actual work: copies template files into the user's project.

**The main function is `install()`:**

```python
install(stack="python-fastapi", target=Path("/my/project"), force=False, dry_run=False)
```

Step by step:

1. Validate the stack name is one we support
2. Check if `.claude/` already exists — if yes and `force=False`, raise an error
3. Find the template source folder (`_template_src()`)
4. Copy everything from the template to the user's project using `shutil.copytree()`
5. Make `.sh` files executable (they'd be read-only otherwise)
6. Count what was installed and return a summary

**The `_template_src()` function — most important function:**

```python
def _template_src(stack: str) -> Path:
    if getattr(sys, "frozen", False):
        # We're running as a PyInstaller binary (installed from Homebrew)
        templates_dir = _ensure_templates(Path(sys._MEIPASS))
        base = templates_dir / stack
        with_dot_claude = base / ".claude"
        return with_dot_claude if with_dot_claude.is_dir() else base
    # We're running as a regular Python script (pip install or development)
    return Path(__file__).parent / "templates" / stack / ".claude"
```

This is the most important function in the whole project. It answers: **"Where are the template files right now?"**

There are two completely different answers depending on how the tool is running:

**Case 1: Running as a PyInstaller binary (Homebrew install)**
When you download the binary from Homebrew, there's no `src/clauderig/templates/` folder sitting on your disk. The templates were packed into the binary file. PyInstaller extracts them to a temporary directory (`sys._MEIPASS`) at runtime. This function finds them there.

**Case 2: Running as a Python script (pip install or development)**
Templates are right next to `installer.py` on disk. So `Path(__file__).parent / "templates" / stack / ".claude"` is just the templates folder next to the Python file.

**The `_ensure_templates()` function — safety net:**

```python
def _ensure_templates(meipass: Path) -> Path:
    templates_dir = meipass / "clauderig" / "templates"
    if not templates_dir.exists():
        zip_file = meipass / "templates_bundle.zip"
        if not zip_file.exists():
            raise RuntimeError("bundle is corrupt: templates_bundle.zip not found")
        templates_dir.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(str(zip_file)) as zf:
            zf.extractall(str(templates_dir))
    return templates_dir
```

When running as a PyInstaller binary, the templates are stored as a zip file (`templates_bundle.zip`) inside the binary. This function unzips them to the temp directory if they haven't been unzipped already.

**Why is this needed?** See section 17 for the full story, but the short version: PyInstaller has a bug where it silently drops folders that start with a dot (`.`), like `.claude/`. Storing everything in a zip file first, then unzipping at runtime, bypasses this bug.

---

### `rthook_clauderig.py` — Runtime Hook

This file runs **automatically at binary startup**, before any user code.

```python
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
```

**Think of it like this:** When the user runs `clauderig init`, the first thing that happens is this runtime hook. Before the tool even says hello to the user, this hook:

1. Checks if we're inside a PyInstaller binary (`sys.frozen == True`)
2. Finds `templates_bundle.zip` in the temp folder (`sys._MEIPASS`)
3. Unzips it to `_MEIPASS/clauderig/templates/`
4. Now the templates exist as real files on disk and `installer.py` can copy them

If the zip file is missing (which would mean the binary was built wrong), it raises a `RuntimeError` immediately with a clear message instead of crashing later with a confusing error.

---

### `clauderig.spec` — PyInstaller Recipe

This is the **build recipe** that tells PyInstaller exactly how to package our Python tool into a single binary file.

```python
import os
import sys
import zipfile

# Tell PyInstaller where our source code is
sys.path.insert(0, os.path.join(SPECPATH, "src"))

# Step 1: Create a zip of all template files
_tmpl_src = os.path.join(SPECPATH, "src", "clauderig", "templates")
_zip_path = os.path.join(SPECPATH, "templates_bundle.zip")

with zipfile.ZipFile(_zip_path, "w", zipfile.ZIP_DEFLATED) as _zf:
    for _root, _dirs, _files in os.walk(_tmpl_src):
        for _f in _files:
            _src_file = os.path.join(_root, _f)
            _arc_name = os.path.relpath(_src_file, _tmpl_src).replace(os.sep, "/")
            _zf.write(_src_file, _arc_name)

# Step 2: Tell PyInstaller to bundle the zip file at the root level
a = Analysis(
    ["src/clauderig/cli.py"],       # entry point
    pathex=["src"],                  # where to find our Python code
    datas=[(_zip_path, ".")],        # include the zip at the root of _MEIPASS
    runtime_hooks=["rthook_clauderig.py"],  # run this before user code
)
```

**What each part does:**

- `sys.path.insert(0, "src")` — Tells PyInstaller "when you import `clauderig`, look in the `src/` folder first". This ensures we bundle our LOCAL code, not an outdated version from PyPI.
- **Zip creation loop** — Walks through ALL files in the templates folder (including those in `.claude/` subdirectories) and zips them into `templates_bundle.zip`. This is the workaround for the PyInstaller hidden-folder bug (explained in section 17).
- `datas=[(_zip_path, ".")]` — Tells PyInstaller: "include `templates_bundle.zip` and put it at the root of the temp folder (`_MEIPASS`)". The `"."` means "root".
- `runtime_hooks=["rthook_clauderig.py"]` — Tells PyInstaller to run this file first when the binary starts.

---

### `build-macos.sh` — macOS Build Script

```bash
#!/usr/bin/env bash
set -e                                    # exit on any error
APP_NAME="clauderig"
VERSION="${APP_VERSION:-1.0.10}"          # use env variable or default to 1.0.10

pip3 install pyinstaller --quiet          # install the build tool
pip3 install -r requirements.txt --quiet  # install typer and rich
pip3 install -e . --quiet                 # install our local code (editable)

find . -name "*.pyc" -delete              # remove old compiled Python files
pyinstaller clauderig.spec \
    --distpath dist/macos \               # output folder
    --workpath build/macos \              # temp folder during build
    --clean                               # start fresh

# Package as a zip
mkdir -p "dist/zip/${APP_NAME}-${VERSION}-macos"
cp "dist/macos/${APP_NAME}" "dist/zip/${APP_NAME}-${VERSION}-macos/"
cd dist/zip
zip -r "../${APP_NAME}_${VERSION}_macos_${ARCH}.zip" "${APP_NAME}-${VERSION}-macos/"
```

**What `pip3 install -e .` does:**
The `-e` flag means "editable". It installs the LOCAL code from `src/` so PyInstaller bundles OUR code, not any old version from the internet. Without this, PyInstaller might find an outdated `clauderig` version cached on the system and bundle that instead.

---

### `build-linux.sh` — Linux Build Script

Similar to the macOS script but also creates a `.deb` package:

```bash
# Build with PyInstaller inside a Docker container (see below)
# Then package as .deb:

DEB_ROOT="dist/clauderig_1.0.10_amd64"
mkdir -p "${DEB_ROOT}/usr/local/bin"
cp dist/linux/clauderig "${DEB_ROOT}/usr/local/bin/clauderig"

dpkg-deb --build "$DEB_ROOT" "dist/clauderig_1.0.10_amd64.deb"
```

**Why Docker for Linux?** Linux binaries depend on system libraries. If you build on Ubuntu 22.04, the binary might not work on Ubuntu 18.04 because the system library `glibc` might be a different version. By building inside a `python:3.11-slim-bullseye` Docker container (Debian Bullseye, an older stable version), we produce a binary that works on ALL modern Linux systems.

---

### `.gitignore` — Files Git Ignores

```
__pycache__/        ← compiled Python files (auto-generated, not needed in git)
dist/               ← build output (the compiled binaries)
build/              ← build temp files
*.egg-info/         ← Python package metadata (auto-generated)
templates_bundle.zip ← build artifact (generated by clauderig.spec at build time)
```

`templates_bundle.zip` is listed here because it's created fresh every time we build. We don't want to commit it to git — it would change with every build and pollute the git history.

---

## 6. The Template Files Inside the Tool

Each supported stack has its own folder under `src/clauderig/templates/`:

```
templates/
├── python-fastapi/
│   └── .claude/
│       ├── CLAUDE.md                    ← main project description for Claude
│       ├── commands/
│       │   ├── add-endpoint.md          ← /add-endpoint slash command
│       │   ├── add-test.md              ← /add-test slash command
│       │   ├── db-migration.md          ← /db-migration slash command
│       │   ├── claude-fit.md            ← /claude-fit slash command
│       │   └── review.md               ← /review slash command
│       ├── skills/
│       │   ├── async-db/SKILL.md        ← how to work with async databases
│       │   ├── fastapi-patterns/SKILL.md ← FastAPI best practices
│       │   └── pydantic-models/SKILL.md  ← Pydantic data validation
│       ├── hooks/
│       │   ├── post-edit-lint.sh        ← runs linter after Claude edits a file
│       │   └── setup-mcps.sh           ← installs MCP prerequisites
│       ├── rules/
│       │   └── coding-standards.md     ← always-on coding rules
│       └── settings.json               ← MCP server configuration
```

**What each folder does:**

- **`commands/`** — Each `.md` file becomes a slash command in Claude Code. For example, `add-endpoint.md` creates `/add-endpoint` which tells Claude exactly how to add a new API endpoint in your FastAPI project.
- **`skills/`** — These are guides Claude reads to deeply understand patterns used in your project. `fastapi-patterns/SKILL.md` might explain how routes are structured, how dependencies are injected, etc.
- **`hooks/`** — Shell scripts that run automatically at certain events. `post-edit-lint.sh` runs `ruff` or `flake8` every time Claude modifies a Python file.
- **`rules/`** — Coding standards that Claude always follows (e.g., "always use type hints", "always write docstrings").
- **`settings.json`** — Which MCP (Model Context Protocol) servers to use. Example:

  ```json
  {
    "mcpServers": {
      "github": {...},
      "filesystem": {...},
      "postgres": {...}
    }
  }
  ```

  This gives Claude the ability to read GitHub issues, access files, and query your database.

---

## 7. What is PyInstaller and Why We Use It

**The problem:**

clauderig is written in Python. To run it, users would normally need Python installed, then run `pip install clauderig`, then run `python -m clauderig`. This is 3 steps and requires Python knowledge.

**The solution — PyInstaller:**

PyInstaller packages your Python program + Python itself + all libraries into a **single executable file**.

```
Before PyInstaller:
  clauderig source code → needs Python installed → user runs: pip install clauderig

After PyInstaller:
  clauderig source code → PyInstaller → clauderig (one binary file, 12 MB)
  Users just run: ./clauderig or brew install clauderig
```

**Simple analogy:**

Imagine your program is a recipe (the Python code), and cooking it requires a specific kitchen (Python + libraries). PyInstaller takes the recipe, the kitchen, all the ingredients, packs them into a sealed container, and gives you a ready-made meal. The user just opens and eats — no cooking required.

**How PyInstaller creates the binary:**

1. Analyzes your Python code to find all imports
2. Bundles Python itself + all imported libraries
3. Packs your code (as compiled `.pyc` files)
4. Packs any data files you specify (`templates_bundle.zip` in our case)
5. Creates a single executable that extracts itself to a temp folder at runtime

**What happens when the user runs `clauderig`:**

```
User runs: clauderig init
    ↓
Binary extracts itself to temp folder: /tmp/_MEIxxx/
    /tmp/_MEIxxx/
        python3.11             ← embedded Python interpreter
        libpython3.11.dylib    ← Python library
        typer/                 ← the typer package
        rich/                  ← the rich package
        clauderig/             ← our code
        templates_bundle.zip   ← templates (zip file)
    ↓
Runtime hook (rthook_clauderig.py) runs FIRST:
    Extracts templates_bundle.zip → _MEIxxx/clauderig/templates/
    ↓
Our main code (cli.py) runs
    ↓
User sees the output
    ↓
When done, /tmp/_MEIxxx/ is deleted
```

---

## 8. How the Binary is Built — Step by Step

Here is exactly what happens when we build the binary:

### On macOS:

```
Step 1: pip3 install pyinstaller
    → Installs the PyInstaller tool itself

Step 2: pip3 install -r requirements.txt
    → Installs typer and rich (the libraries our tool needs)

Step 3: pip3 install -e .
    → Installs OUR LOCAL clauderig code so PyInstaller finds it
    → Critical: without this, PyInstaller might bundle an old version from the internet

Step 4: pyinstaller clauderig.spec
    → The spec file runs, which first creates templates_bundle.zip
    → PyInstaller analyzes cli.py and finds all its imports
    → PyInstaller bundles Python + typer + rich + our code + templates_bundle.zip
    → Output: dist/macos/clauderig  (a single file, ~12 MB)

Step 5: zip -r clauderig_1.0.10_macos_arm64.zip clauderig
    → Package the binary into a zip file for distribution
    → Output: dist/clauderig_1.0.10_macos_arm64.zip
```

### On Linux (inside Docker):

```
Same steps as macOS, but runs inside:
  docker run python:3.11-slim-bullseye
    → Debian Bullseye (old, stable Linux)
    → Guarantees the binary uses old glibc (works on all Linux systems)

Output: dist/linux/clauderig  (Linux binary)
Then packaged as: dist/clauderig_1.0.10_amd64.deb
```

### On Windows:

```
Same steps, output is:
  dist/windows/clauderig.exe
Then packaged as: dist/clauderig_1.0.10_windows_amd64.zip
```

---

## 9. The Build Scripts

### `build-macos.sh` in detail:

```bash
set -e
```

`set -e` means "exit immediately if any command fails". If `pip3 install` fails, the script stops instead of continuing with a broken state.

```bash
VERSION="${APP_VERSION:-1.0.10}"
```

`${APP_VERSION:-1.0.10}` means: "use the `APP_VERSION` environment variable if it's set, otherwise use `1.0.10`". GitHub Actions sets `APP_VERSION` to the release tag (like `1.0.10`).

```bash
find . -name "*.pyc" -delete
```

Deletes compiled Python files (`.pyc`). This is a cleanup step. Stale `.pyc` files can confuse PyInstaller into bundling old code.

```bash
pyinstaller clauderig.spec --distpath dist/macos --workpath build/macos --clean
```

- `--distpath dist/macos` — put the final binary here
- `--workpath build/macos` — put temp files here during build
- `--clean` — delete any previous build artifacts and start fresh

---

## 10. GitHub Releases — What and Why

**What is a GitHub Release?**

A GitHub Release is a snapshot of your code at a specific point in time, plus attached files (like binary downloads).

Think of it like shipping a product. Every time you ship a new version (1.0.10), you:

1. Take a snapshot of the code (this is called a "tag" — like `v1.0.10`)
2. Attach the compiled files (the `.zip` and `.deb` binaries)
3. Write release notes

**Why do we use releases instead of just pushing code?**

- Users need a stable version to download. They shouldn't have to compile code themselves.
- Each release has a specific download URL that never changes. Homebrew formulas and APT repos can point to these permanent URLs.
- Users can always download an older version if the new one has a bug.

**How releases trigger everything:**

```
Developer pushes tag v1.0.10
    ↓
GitHub automatically creates a release
    ↓
GitHub Actions workflow triggers (the release.yml file)
    ↓
5 jobs run automatically:
    1. build-linux → creates .deb file
    2. build-macos-arm → creates macOS binary + zip
    3. build-windows → creates .exe + zip
    4. update-homebrew → updates the Homebrew formula
    5. publish-apt → publishes .deb to the APT repository
```

---

## 11. GitHub Actions — Automation Explained

**What is GitHub Actions?**

GitHub Actions is GitHub's built-in automation system. You write a YAML file that says "when X happens, run these commands on a computer that GitHub provides for free".

**Why do we use it?**

Without GitHub Actions, releasing a new version would require:

1. Manually running the build script on macOS
2. Manually running the build script on Linux (need Linux machine or VM)
3. Manually running the build script on Windows
4. Manually uploading files to GitHub release
5. Manually editing the Homebrew formula file
6. Manually updating the APT repository

That's 6 manual steps, each error-prone. GitHub Actions does all of this automatically when you push a tag.

**How it works:**

1. You write instructions in `.github/workflows/release.yml`
2. When an event happens (like creating a release), GitHub spins up virtual machines
3. These VMs run your instructions automatically
4. You sit back and the binaries appear on the release page

---

## 12. The Workflow File — Every Job and Command Explained

File: `.github/workflows/release.yml`

```yaml
name: Build and Release

on:
  release:
    types: [created]    # Run when a GitHub Release is created
  workflow_dispatch:    # Also allow manual triggering from GitHub UI
```

**`workflow_dispatch`** means you can press a "Run workflow" button on GitHub without creating a release. Useful for testing.

---

### Job 1: `build-linux`

```yaml
build-linux:
  name: Build Linux .deb
  runs-on: ubuntu-latest      # GitHub gives us an Ubuntu machine
  steps:
    - uses: actions/checkout@v4    # downloads our code onto the VM
  
    - name: Build binary in Debian Bullseye
      run: |
        docker run --rm \
          -v "$GITHUB_WORKSPACE:/work" \
          -w /work \
          python:3.11-slim-bullseye \
          bash -c "apt-get update -q && apt-get install -y -q binutils && \
                   pip install pyinstaller -r requirements.txt -q && \
                   pip install -e . -q && \
                   find . -name '*.pyc' -delete && \
                   pyinstaller clauderig.spec --distpath dist/linux --workpath build/linux --clean"
        sudo chown -R "$USER:$USER" dist/ build/
```

**What this does:**

1. Downloads our code onto the Ubuntu VM
2. Runs a Docker container with Debian Bullseye (older Linux)
3. Inside Docker: installs dependencies, builds the binary
4. `sudo chown` — fixes file ownership (Docker creates files owned by root, CI needs to access them)

**Why Docker?**
If we built on Ubuntu 22.04, the binary would require a newer version of `glibc` (Linux's C library). Older systems (Ubuntu 18.04, Debian 10) have an older `glibc` and would refuse to run the binary. Bullseye has `glibc 2.31` which is old enough to work on all modern Linux systems.

```yaml
    - name: Package as .deb
      run: |
        VERSION="${{ github.ref_name }}"    # get "v1.0.10" from the release tag
        VERSION="${VERSION#v}"              # strip the "v" → "1.0.10"
        APP_VERSION="$VERSION" SKIP_BUILD=1 ./build-linux.sh
```

`SKIP_BUILD=1` tells `build-linux.sh` to skip the PyInstaller step (already done in Docker) and only do the `.deb` packaging step.

```yaml
    - uses: softprops/action-gh-release@v2
      with:
        files: dist/*.deb    # attach the .deb file to the GitHub Release
```

This uploads the `.deb` file to the GitHub Release page so users can download it.

```yaml
    - uses: actions/upload-artifact@v4
      with:
        name: linux-deb
        path: dist/*.deb
```

"Artifacts" are files shared between jobs. Job 5 (`publish-apt`) needs the `.deb` file, and it runs on a different virtual machine. Artifacts are how GitHub Actions passes files between jobs.

---

### Job 2: `build-macos-arm`

```yaml
build-macos-arm:
  name: Build macOS Apple Silicon
  runs-on: macos-latest    # GitHub gives us an Apple Silicon Mac
  steps:
    - uses: actions/checkout@v4

    - uses: actions/setup-python@v5
      with:
        python-version: "3.11"    # Install Python 3.11 specifically
```

**Why specify Python 3.11?** macOS comes with Python 3.13 from Homebrew. If we used that, we'd be building with a different Python than intended, and there could be version inconsistencies. `actions/setup-python` installs a clean, controlled Python 3.11 and makes `python`, `python3`, `pip`, and `pip3` all point to it.

```yaml
    - run: |
        pip install pyinstaller
        pip install -r requirements.txt
        pip install -e .           # installs OUR local code
        APP_VERSION="$VERSION" ./build-macos.sh
```

The `pip install -e .` ensures that when PyInstaller runs, it finds our LOCAL version of clauderig (with all our fixes), not an old version from PyPI.

```yaml
    - uses: softprops/action-gh-release@v2
      with:
        files: dist/*.zip    # attach the macOS zip to the GitHub Release
```

---

### Job 3: `build-windows`

```yaml
build-windows:
  name: Build Windows
  runs-on: windows-latest    # GitHub gives us a Windows machine
  steps:
    - uses: actions/setup-python@v5
      with:
        python-version: "3.11"

    - shell: pwsh    # PowerShell (Windows doesn't have bash by default)
      run: |
        pip install pyinstaller
        pip install -r requirements.txt
        pip install -e .
        Get-ChildItem -Recurse -Filter "*.pyc" | Remove-Item -Force  # delete .pyc files
        pyinstaller clauderig.spec --distpath dist/windows --workpath build/windows --clean
        Compress-Archive -Path dist/windows/clauderig.exe -DestinationPath "dist/clauderig_${VERSION}_windows_amd64.zip"
```

`Compress-Archive` is PowerShell's equivalent of `zip`. It creates the Windows zip package.

---

### Job 4: `update-homebrew`

This job runs AFTER `build-macos-arm` finishes (indicated by `needs: [build-macos-arm]`).

```yaml
update-homebrew:
  needs: [build-macos-arm]    # wait for macOS build to finish first
  steps:
    - uses: actions/download-artifact@v4
      with:
        name: macos-arm-zip    # get the zip file that Job 2 saved as artifact
        path: zips/

    - id: sha
      run: echo "arm64=$(sha256sum zips/*.zip | awk '{print $1}')" >> $GITHUB_OUTPUT
```

**SHA256 checksum:** This calculates a unique fingerprint of the zip file. Homebrew uses this to verify the download hasn't been corrupted or tampered with. If even one byte changes, the SHA256 changes, and Homebrew rejects the download.

```yaml
    - uses: actions/checkout@v4
      with:
        repository: harshit9413/homebrew-clauderig    # check out the FORMULA repo
        token: ${{ secrets.HOMEBREW_TAP_TOKEN }}      # use secret token for auth
        path: homebrew-tap
```

This checks out the **separate Homebrew repository** (not the main clauderig repo). We need to edit the formula file in that repo.

```yaml
    - run: |
        sed -i "s/version \".*\"/version \"${VERSION}\"/" homebrew-tap/Formula/clauderig.rb
        sed -i "s/sha256 \"[^\"]*\"/sha256 \"...\"/\" homebrew-tap/Formula/clauderig.rb
        cd homebrew-tap
        git commit -m "Update to v1.0.10"
        git push
```

`sed -i "s/old/new/"` — find and replace in a file. This updates the version number and SHA256 checksum in the Homebrew formula. Then commits and pushes to the Homebrew formula repo.

**After this runs:** When anyone does `brew upgrade clauderig`, Homebrew reads the updated formula, sees the new version, downloads the new zip, verifies the SHA256, and installs.

---

### Job 5: `publish-apt`

```yaml
publish-apt:
  needs: [build-linux]    # wait for Linux build to finish

  steps:
    - uses: actions/download-artifact@v4
      with:
        name: linux-deb
        path: debs/

    - uses: actions/checkout@v4
      with:
        repository: harshit9413/apt-repo    # the SEPARATE APT repo
        token: ${{ secrets.APT_REPO_TOKEN }}
        ref: gh-pages                        # the gh-pages branch
        path: apt-repo

    - run: |
        sudo apt-get install -y reprepro    # tool for managing APT repos
        echo "${{ secrets.GPG_PRIVATE_KEY }}" | gpg --import    # import signing key
        reprepro includedeb stable "$DEB"   # add the .deb to the APT repo
        git commit -m "Release v1.0.10"
        git push
```

**`reprepro`** — a tool that manages Debian package repositories. It takes a `.deb` file, adds it to the repository, and updates the metadata files that APT reads.

**GPG signing** — every APT repository must be cryptographically signed. When a user does `apt update`, APT verifies the signature to ensure the packages haven't been tampered with. The `GPG_PRIVATE_KEY` secret contains the signing key.

---

## 13. GitHub Secrets — What Are They?

GitHub Secrets are **encrypted environment variables** stored in your GitHub repository settings. They're used to store sensitive information like passwords, API tokens, and private keys.

**Our secrets:**

### `HOMEBREW_TAP_TOKEN`

A GitHub Personal Access Token with write permission to the `harshit9413/homebrew-clauderig` repository.

**Why needed:** The workflow runs on GitHub's computers, not yours. When it tries to push changes to the Homebrew formula repo, it needs credentials. Your password can't be stored in the workflow file (that's public). A token stored as a secret is safe.

**How to create:** GitHub Settings → Developer Settings → Personal Access Tokens → New token with "repo" scope for the homebrew-clauderig repo.

### `APT_REPO_TOKEN`

A GitHub Personal Access Token with write permission to the `harshit9413/apt-repo` repository.

Same reason as above — needed to push the updated APT repo to GitHub.

### `GPG_PRIVATE_KEY`

The private cryptographic key used to sign the APT repository.

**Why needed:** APT repositories must be signed so users' systems can verify authenticity. The private key signs each release. Only the holder of this key can publish legitimate packages.

**How to create:**

```bash
gpg --gen-key              # create a new key pair
gpg --export-secret-keys   # export the private key
# paste the exported key into GitHub Secrets
```

**Important:** If this key is lost, you can never update the APT repo. If it's stolen, someone could publish fake packages. Keep it safe.

---

## 14. Package Managers — Homebrew, APT, Winget

Package managers are tools that install, update, and remove software automatically. Instead of "go to website, download file, run installer", you just type one command.

### Homebrew (macOS)

Homebrew is the most popular package manager for macOS. It was created because macOS doesn't come with a built-in package manager like Linux does.

**How it works:**
1. Homebrew reads a "formula" (Ruby script) that describes how to install software
2. The formula says where to download the binary, how to verify it, where to put it

**Our setup:**
- Formula repo: `harshit9413/homebrew-clauderig`
- Formula file: `Formula/clauderig.rb`

---

#### Command 1: `brew tap harshit9413/clauderig`

```bash
brew tap harshit9413/clauderig
```

**Word by word:**

- `brew` — the Homebrew program itself
- `tap` — Homebrew's word for "add a third-party repository of formulas". Like tapping into a new water source.
- `harshit9413/clauderig` — this is `<github-username>/<short-name>`. Homebrew automatically converts this to the full repo name `harshit9413/homebrew-clauderig` by adding the `homebrew-` prefix.

**What actually happens when you run this:**
1. Homebrew converts `harshit9413/clauderig` → `harshit9413/homebrew-clauderig`
2. Runs: `git clone https://github.com/harshit9413/homebrew-clauderig ~/.homebrew/Library/Taps/harshit9413/homebrew-clauderig`
3. The formula file is now on your machine at: `/opt/homebrew/Library/Taps/harshit9413/homebrew-clauderig/Formula/clauderig.rb`
4. Homebrew now knows the `clauderig` package exists

**Why you only do this ONCE:**
After tapping, the formula stays on your Mac. Homebrew knows about our package forever. You only tap again if you completely uninstall Homebrew.

**What if you skip this step and just run `brew install clauderig`?**
```
Error: No available formula with the name "clauderig"
```
Homebrew only knows about formulas inside taps it has added.

---

#### Command 2: `brew install clauderig`

```bash
brew install clauderig
```

**What actually happens — step by step:**

1. Homebrew reads the local formula file at `~/.../harshit9413/homebrew-clauderig/Formula/clauderig.rb`
2. Gets the download URL from the formula: `https://github.com/harshit9413/clauderig/releases/download/v1.0.10/clauderig_1.0.10_macos_arm64.zip`
3. Downloads the zip to a temp folder (shows a progress bar)
4. Calculates the **SHA256 checksum** of the downloaded file (a fingerprint of the file's contents)
5. Compares it with the `sha256 "abc123..."` line in the formula
   - If they match → download is authentic and not corrupted, proceed
   - If they DON'T match → **install fails** with an error (security protection against tampered downloads)
6. Unzips the file — extracts the `clauderig` binary
7. Copies the binary to `/opt/homebrew/Cellar/clauderig/1.0.10/bin/clauderig`
8. Creates a symlink: `/opt/homebrew/bin/clauderig` → `/opt/homebrew/Cellar/clauderig/1.0.10/bin/clauderig`
9. `/opt/homebrew/bin` is always in your `$PATH`, so `clauderig` now works from any terminal window

**Where the binary lives after install:**
```bash
which clauderig
# → /opt/homebrew/bin/clauderig
```

**What is `$PATH`?**
When you type any command in the terminal, your shell searches through a list of folders to find the program. This list is stored in a variable called `$PATH`. It looks like:
```
/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin
```
The shell checks each folder left to right until it finds the command. Since Homebrew installs to `/opt/homebrew/bin` and that folder is in `$PATH`, any program Homebrew installs becomes available everywhere.

---

#### Command 3: `brew update`

```bash
brew update
```

This updates Homebrew's **knowledge** of what packages exist. It does NOT install or upgrade anything yet.

**What it does:**
1. Runs `git pull` on every tap you've added (including `harshit9413/homebrew-clauderig`)
2. If we released v1.0.11 and pushed the updated formula to the tap repo, your local formula copy now shows v1.0.11
3. Homebrew now knows a newer version of clauderig is available

**Important distinction:**
- `brew update` = update the **recipe book** (learn what's new)
- `brew upgrade clauderig` = actually **install** the new version

If you run `brew upgrade` without `brew update` first, Homebrew uses its old cached formula and might not see the latest version.

---

#### Command 4: `brew upgrade clauderig`

```bash
brew upgrade clauderig
```

**What actually happens:**
1. Checks the installed version (e.g., 1.0.9)
2. Reads the formula — sees latest version is 1.0.10
3. Downloads the new version's zip
4. Verifies SHA256 checksum
5. Installs to `/opt/homebrew/Cellar/clauderig/1.0.10/`
6. Updates the symlink in `/opt/homebrew/bin/clauderig` to point to the new version
7. Old version is kept in `/opt/homebrew/Cellar/clauderig/1.0.9/` (for easy rollback)

**Where Homebrew stores everything — the Cellar:**
Homebrew uses a "Cellar" concept. Each program gets its own folder, each version gets its own subfolder:
```
/opt/homebrew/Cellar/clauderig/
    1.0.9/
        bin/clauderig      ← old binary (kept for rollback)
    1.0.10/
        bin/clauderig      ← new binary

/opt/homebrew/bin/clauderig  ← symlink pointing to 1.0.10's binary
```

This is why Homebrew can roll back: `brew switch clauderig 1.0.9`

---

#### Command 5: `brew update && brew upgrade clauderig`

```bash
brew update && brew upgrade clauderig
```

The `&&` symbol means: "run the second command ONLY if the first command succeeds (exit code 0)".

So this:
1. First updates the formula list (learn what's new)
2. Then upgrades clauderig to the latest version it just learned about

This is the **recommended pattern** for updating. Always `update` before `upgrade`.

---

#### Command 6: `brew uninstall clauderig`

```bash
brew uninstall clauderig
```

Removes the binary from `/opt/homebrew/Cellar/clauderig/` and deletes the symlink. The tap (formula) stays.

To remove everything including the formula:
```bash
brew uninstall clauderig          # remove the binary
brew untap harshit9413/clauderig  # remove the formula repository
```

---

### APT (Ubuntu/Debian Linux)

APT (Advanced Package Tool) is the package manager for Ubuntu, Debian, and all systems based on them (like Linux Mint, Pop!_OS, Raspberry Pi OS).

**How it works:**
1. APT reads a "sources list" — a list of URLs where packages can be found
2. Downloads metadata to know what packages are available and their versions
3. Downloads and installs `.deb` package files

---

#### Command 1 (First time): `echo "..." | sudo tee ...`

```bash
echo "deb [trusted=yes] https://harshit9413.github.io/apt-repo stable main" | sudo tee /etc/apt/sources.list.d/clauderig.list
```

This is the most complex command of the whole process. Let's break it into every single piece:

**Part 1: `echo "deb [trusted=yes] https://harshit9413.github.io/apt-repo stable main"`**

- `echo` — prints text to the terminal output. Like `print()` in Python.
- `"deb [trusted=yes] https://harshit9413.github.io/apt-repo stable main"` — this is the text being printed. It's one line in APT's "sources" format:

  | Part | Meaning |
  |------|---------|
  | `deb` | This is a binary package repository (not source code). Always `deb` for our use. |
  | `[trusted=yes]` | Trust this repo without GPG verification (simpler setup). In production, you'd use `[signed-by=/path/to/key.gpg]` instead. |
  | `https://harshit9413.github.io/apt-repo` | The URL of the repository. GitHub Pages serves this. |
  | `stable` | The "distribution" name — corresponds to the `dists/stable/` folder in the repo. |
  | `main` | The "component" — corresponds to `dists/stable/main/`. Repos can have components like `main`, `contrib`, `non-free`. We only use `main`. |

**Part 2: `|` (the pipe)**

The `|` symbol sends the output of one command as the input to the next command. So whatever `echo` prints gets passed to `sudo tee`.

**Part 3: `sudo`**

- `sudo` means "Super User DO" — run the next command as the root (administrator) user.
- Writing to `/etc/apt/sources.list.d/` requires root permission. Regular users can't modify system configuration.
- You will be asked for YOUR password (not a special root password) to authorize this.

**Part 4: `tee /etc/apt/sources.list.d/clauderig.list`**

- `tee` reads from its input and writes it to a file (and also prints it to the terminal so you can see it).
- `/etc/apt/sources.list.d/` — this is the folder where APT looks for additional package sources. Each `.list` file in here is one source.
- `clauderig.list` — we create a file named after our package. You could name it anything ending in `.list`.

**Why `tee` instead of `>`?**

You might wonder why not just use:
```bash
echo "..." > /etc/apt/sources.list.d/clauderig.list   # THIS DOESN'T WORK
```

Because `sudo` only applies to the `echo` command, not the `>` redirection. The shell performs the `>` redirect as your regular user, who doesn't have permission to write to `/etc/apt/`. The `tee` approach runs as root (via `sudo`) so it has permission.

**After running this command, a new file exists:**
```bash
cat /etc/apt/sources.list.d/clauderig.list
# Output:
# deb [trusted=yes] https://harshit9413.github.io/apt-repo stable main
```

---

#### Command 2: `sudo apt update`

```bash
sudo apt update
```

- `sudo` — need root to write to APT's cache
- `apt` — the package manager program
- `update` — refresh the local cache of what packages exist

**What actually happens:**
1. APT reads all files in `/etc/apt/sources.list` and `/etc/apt/sources.list.d/`
2. For each source (including our new `clauderig.list`), downloads the `Release` and `Packages` files
3. For our repo: downloads `https://harshit9413.github.io/apt-repo/dists/stable/Release`
4. Downloads `https://harshit9413.github.io/apt-repo/dists/stable/main/binary-amd64/Packages`
5. Stores this locally at `/var/lib/apt/lists/`

After this, APT knows clauderig 1.0.10 exists and where to download it.

**You MUST run this after adding a new source.** Without it, APT doesn't know about the new source yet.

---

#### Command 3: `sudo apt install clauderig`

```bash
sudo apt install clauderig
```

- `sudo` — need root to install software system-wide
- `apt` — the package manager
- `install` — install a package
- `clauderig` — the package name (must match exactly what's in the `Packages` metadata file)

**What actually happens:**
1. APT looks up `clauderig` in its local cache (`/var/lib/apt/lists/`)
2. Finds: version 1.0.10, download URL: `https://harshit9413.github.io/apt-repo/pool/main/c/clauderig/clauderig_1.0.10_amd64.deb`, SHA256: `abc123...`
3. Downloads the `.deb` file to `/var/cache/apt/archives/clauderig_1.0.10_amd64.deb`
4. Verifies SHA256 checksum
5. Runs `dpkg -i` to install the `.deb`:
   - Extracts the `.deb` archive
   - Copies `usr/local/bin/clauderig` to `/usr/local/bin/clauderig`
   - Makes it executable
6. Records the installation in APT's database
7. User can now type `clauderig` from anywhere

**Why `/usr/local/bin/` and not `/opt/homebrew/bin/`?**
On Linux, the standard location for user-installed programs is `/usr/local/bin/`. This folder is always in `$PATH` on Linux. On macOS (Homebrew), the standard location is `/opt/homebrew/bin/`.

---

#### Command 4: `sudo apt update && sudo apt upgrade clauderig`

```bash
sudo apt update && sudo apt upgrade clauderig
```

- First `sudo apt update` — check if any new version of clauderig was released (refresh metadata)
- `&&` — only run upgrade if update succeeded
- `sudo apt upgrade clauderig` — download and install the latest version

**`upgrade` vs `install` when already installed:**
- `sudo apt install clauderig` — if already installed, upgrades to latest (same effect as upgrade for a single package)
- `sudo apt upgrade clauderig` — more explicit upgrade command

---

#### Command 5: `sudo apt remove clauderig`

```bash
sudo apt remove clauderig
```

Removes the binary but keeps configuration files (if any).

```bash
sudo apt purge clauderig     # removes binary AND any config files
sudo apt autoremove          # removes unused dependencies
```

---

**The `.deb` file format — what's inside:**

A `.deb` file is like a zip file with a specific structure:

```
clauderig_1.0.10_amd64.deb
├── DEBIAN/
│   └── control         ← package metadata (name, version, maintainer, description)
└── usr/
    └── local/
        └── bin/
            └── clauderig  ← the actual binary (12 MB)
```

When `dpkg` installs it, it puts every file from the archive into the same path on your real system:
- `usr/local/bin/clauderig` inside the `.deb` → `/usr/local/bin/clauderig` on your system

---

### Winget (Windows)

Windows Package Manager. Users would run:

```powershell
winget install clauderig
```

(Requires submitting to the Windows Package Manager Community Repository — future work.)

---

## 15. End User Journey — How Someone Installs and Uses clauderig

### macOS User

```bash
# 1. Add the Homebrew tap (only needs to be done once)
brew tap harshit9413/clauderig

# 2. Install
brew install clauderig

# 3. Go to any project
cd ~/projects/my-fastapi-app

# 4. Run clauderig
clauderig init
# → Auto-detects: "Python → FastAPI"
# → Asks: "Use detected stack? [Y/n]"
# → Press Y
# → Creates .claude/ folder in your project

# 5. Open Claude Code
claude
# → Claude now knows your project, can use slash commands like /add-endpoint
```

**To update:**

```bash
brew update && brew upgrade clauderig
```

---

### Ubuntu/Debian Linux User

```bash
# 1. Add the APT repository (only needs to be done once)
echo "deb [trusted=yes] https://harshit9413.github.io/apt-repo stable main" | \
    sudo tee /etc/apt/sources.list.d/clauderig.list

# 2. Update and install
sudo apt update && sudo apt install clauderig

# 3. Run
cd ~/projects/my-django-app
clauderig init

# To update
sudo apt update && sudo apt upgrade clauderig
```

---

### Direct Download (Any Platform)

Users can also download the binary directly from GitHub Releases:

1. Go to `github.com/harshit9413/clauderig/releases`
2. Download the appropriate file for their OS
3. Make it executable: `chmod +x clauderig`
4. Move it to a folder in PATH: `sudo mv clauderig /usr/local/bin/`

---

### pip Install (Python Users)

Users who have Python can also install via pip:

```bash
pip install clauderig
# Then use the `claude-setup` command (defined in pyproject.toml)
claude-setup init
```

---

## 16. How to Release a New Version — Step by Step

When you want to release a new version (e.g., 1.0.11), do this:

### Step 1: Update version numbers

In `pyproject.toml`:

```toml
version = "1.0.11"
```

In `build-macos.sh`:

```bash
VERSION="${APP_VERSION:-1.0.11}"
```

In `build-linux.sh`:

```bash
VERSION="${APP_VERSION:-1.0.11}"
```

### Step 2: Commit all changes

```bash
git add pyproject.toml build-macos.sh build-linux.sh
git commit -m "Release 1.0.11: description of what changed"
git push
```

### Step 3: Create the release tag

```bash
git tag v1.0.11
git push origin v1.0.11
```

### Step 4: Create the GitHub Release

Go to `github.com/harshit9413/clauderig/releases/new`, select `v1.0.11`, click "Publish release".

OR via GitHub CLI:

```bash
gh release create v1.0.11 --title "v1.0.11" --notes "What changed in this version"
```

### Step 5: Wait for GitHub Actions

The 5 jobs run automatically. Watch them at:
`github.com/harshit9413/clauderig/actions`

When all 5 jobs show green checkmarks:

- `.deb` file is on the GitHub Release page
- macOS zip is on the GitHub Release page
- Windows zip is on the GitHub Release page
- Homebrew formula is updated
- APT repo is updated

Users can now run `brew upgrade clauderig` or `apt upgrade clauderig` to get the new version.

.

---

## Summary Table

| File                              | What It Does                                            |
| --------------------------------- | ------------------------------------------------------- |
| `pyproject.toml`                | Defines the Python package: name, version, dependencies |
| `requirements.txt`              | Lists Python libraries needed (typer, rich)             |
| `src/clauderig/__init__.py`     | Package version number                                  |
| `src/clauderig/__main__.py`     | Lets you run `python -m clauderig`                    |
| `src/clauderig/cli.py`          | Defines the commands:`init`, `list`, `version`    |
| `src/clauderig/analyzer.py`     | Auto-detects project type from files present            |
| `src/clauderig/installer.py`    | Copies template files into user's project               |
| `src/clauderig/templates/`      | The `.claude/` folder blueprints for each stack       |
| `clauderig.spec`                | PyInstaller recipe: how to build the binary             |
| `rthook_clauderig.py`           | Runs at binary startup, extracts templates from zip     |
| `build-macos.sh`                | Script to build the macOS binary                        |
| `build-linux.sh`                | Script to build the Linux binary + .deb package         |
| `.github/workflows/release.yml` | GitHub Actions: automates the entire release process    |
| `.gitignore`                    | Files git should not track                              |

| Repo                               | Purpose                                 |
| ---------------------------------- | --------------------------------------- |
| `harshit9413/clauderig`          | Main code, builds, GitHub Actions       |
| `harshit9413/homebrew-clauderig` | Homebrew formula for macOS installation |
| `harshit9413/apt-repo`           | APT repository for Linux installation   |

| Command                                        | Who Runs It  | What It Does                            |
| ---------------------------------------------- | ------------ | --------------------------------------- |
| `clauderig init`                             | End user     | Sets up `.claude/` in current project |
| `clauderig list`                             | End user     | Shows supported stacks                  |
| `clauderig version`                          | End user     | Shows version number                    |
| `brew install clauderig`                     | macOS user   | Installs clauderig via Homebrew         |
| `brew upgrade clauderig`                     | macOS user   | Updates to latest version               |
| `sudo apt install clauderig`                 | Linux user   | Installs clauderig via APT              |
| `sudo apt upgrade clauderig`                 | Linux user   | Updates to latest version               |
| `git tag v1.0.10 && git push origin v1.0.10` | Developer    | Creates release tag, triggers CI        |
| `pyinstaller clauderig.spec`                 | CI/Developer | Builds the binary from source           |
