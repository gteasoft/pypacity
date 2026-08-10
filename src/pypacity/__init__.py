"""Pypacity: ampacity calculations for overhead electrical conductors.

The public version is obtained from the installed package metadata, so the
version number only needs to be maintained in ``pyproject.toml``.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("pypacity")
except PackageNotFoundError:
    # This can occur when the source tree is used without installing the package.
    __version__ = "0.0.0"

__all__ = ["__version__"]
