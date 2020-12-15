import os
import sys


def get_arch():
    if not "ARCH" in os.environ:
        print("$ARCH must be specified", file=sys.stderr)
        sys.exit(1)
    return os.environ["ARCH"]
