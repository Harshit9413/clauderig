from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("clauderig")
except PackageNotFoundError:
    try:
        from clauderig._version import __version__
    except ImportError:
        __version__ = "0.0.0"
