"""The Egon ``worker`` utility is responsible for spawning local processes and
reporting their status to the Egon Status API.
"""

import importlib.metadata

try:
    __version__ = importlib.metadata.version('asdf')

except importlib.metadata.PackageNotFoundError:
    __version__ = '0.0.0'
