import json
import os
import sys


def get_cbl_arch():
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


def _cbl_arch_to_arch(arch):
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

def _cbl_arch_to_config(arch):
    """
    This should match tuxbuild.yml, so that we can find which build in
    builds.json is the one we care about.
    """
    return {
        "arm64": "defconfig",
        "arm32_v5": "multi_v5_defconfig",
        "arm32_v6": "aspeed_g5_defconfig",
        "arm32_v7": "defconfig",
        "mips": "malta_kvm_guest_defconfig",
        "ppc32": "ppc44x_defconfig",
        "ppc64": "pseries_defconfig",
        "ppc64le": "powernv_defconfig",
        "riscv": "defconfig",
        "s390": "defconfig",
        "x86": "i386_defconfig",
        "x86_64": "defconfig",
    }[arch]


def _find_build(builds):
    cbl_arch = get_cbl_arch()
    arch = _cbl_arch_to_arch(cbl_arch)
    config = _cbl_arch_to_config(cbl_arch)
    for build in builds:
        if build["target_arch"] == arch and build["kconfig"][0] == config:
            return build
    print("Unable to find build", file=sys.stderr)
    sys.exit(1)

def get_build():
    return _find_build(_read_builds())
