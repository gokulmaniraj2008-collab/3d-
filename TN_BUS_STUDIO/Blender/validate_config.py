"""Stdlib-only validation; can run before installing Blender."""
import os
import sys
from bus_config import load_config
try:
    settings = load_config()
except (OSError, ValueError) as error:
    print("INVALID BUS CONFIG:", error, file=sys.stderr)
    sys.exit(1)
print("VALID BUS CONFIG:", settings)
