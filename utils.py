import json
import os
import sys


def get_arch():
    if not "ARCH" in os.environ:
        print("$ARCH must be specified", file=sys.stderr)
        sys.exit(1)
    return os.environ["ARCH"]


def _read_builds():
    try:
        with open("builds.json") as f:
            builds = json.load(f)
    except FileNotFoundError as e:
        print(
            "Unable to find builds.json. Artifact not saved?", file=sys.stderr)
        raise e
    return builds


def _find_build(builds):
    for build in builds:
        # TODO: check more than ARCH
        if build["target_arch"] == get_arch():
            return build
    print("Unable to find build", file=sys.stderr)
    sys.exit(1)

def get_build():
    return _find_build(_read_builds())
