from pathlib import Path
import sys


def base_path() -> Path:
    """Return the runtime base directory for source and bundled builds."""
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS", Path(sys.executable).resolve().parent))
    return Path(__file__).resolve().parent


def resource_path(*parts: str) -> Path:
    return base_path().joinpath(*parts)


def project_path(*parts: str) -> Path:
    if getattr(sys, "frozen", False):
        return base_path().joinpath(*parts)
    return base_path().parent.joinpath(*parts)
