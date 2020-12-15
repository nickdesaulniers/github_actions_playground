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


def _translate_arch(arch):
    """
    Translate what we call the ARCH in our worklist.yml to what tuxbuild calls
    it in the build.json
    """
    return {
        "arm64": "arm64",
        "arm32_v5": "arm",
        "arm32_v6": "arm",
        "arm32_v7": "arm",
        "mips": "mips",
        "ppc32": "powerpc",
        "ppc64": "powerpc",
        "ppc64le": "powerpc",
        "riscv": "riscv",
        "s390": "s390",
        "x86": "x86_64",
        "x86_64": "x86_64",
    }[arch]


def _find_build(builds):
    arch = _translate_arch(get_arch())
    print(json.dumps(builds, indent=4))
    for build in builds:
        # TODO: check more than ARCH
        if build["target_arch"] == arch:
            return build
    print("Unable to find build", file=sys.stderr)
    sys.exit(1)

def get_build():
    return _find_build(_read_builds())
