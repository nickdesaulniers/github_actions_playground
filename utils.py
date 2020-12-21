import json
import sys


def _cbl_arch_to_arch(arch):
    """
    Translate what we call the ARCH in our worklist.yml to what tuxbuild calls
    it in the build.json
    """
    return {
        "arm32_v5": "arm",
        "arm32_v6": "arm",
        "arm32_v7": "arm",
        "arm64": "arm64",
        "mips": "mips",
        "ppc32": "powerpc",
        "ppc64": "powerpc",
        "ppc64le": "powerpc",
        "riscv": "riscv",
        "s390": "s390",
        "x86": "x86_64",
        "x86_64": "x86_64",
    }[arch]


def _cbl_arch_to_config(cbl_arch):
    """
    This should match tuxbuild.yml, so that we can find which build in
    builds.json is the one we care about.
    """
    return {
        "arm32_v5": "multi_v5_defconfig",
        "arm32_v6": "aspeed_g5_defconfig",
        "arm32_v7": "multi_v7_defconfig",
        "arm64": "defconfig",
        "mips": "malta_kvm_guest_defconfig",
        "ppc32": "ppc44x_defconfig",
        "ppc64": "pseries_defconfig",
        "ppc64le": "powernv_defconfig",
        "riscv": "defconfig",
        "s390": "defconfig",
        "x86": "i386_defconfig",
        "x86_64": "defconfig",
    }[cbl_arch]


def get_image_name(cbl_arch):
    return {
        "arm32_v5": "zImage",
        "arm32_v6": "zImage",
        "arm32_v7": "zImage",
        "arm64": "Image.gz",
        "mips": "vmlinux",
        "ppc32": "uImage",
        "ppc64": "vmlinux",
        "ppc64le": "zImage.epapr",
        "riscv": "Image.gz",
        "s390": "bzImage",
        "x86": "bzImage",
        "x86_64": "bzImage",
    }[cbl_arch]


def get_image_path(cbl_arch):
    return {
        "arm32_v5": "arch/arm/boot/",
        "arm32_v6": "arch/arm/boot/",
        "arm32_v7": "arch/arm/boot/",
        "arm64": "arch/arm64/boot/",
        "mips": "arch/mips/boot/",
        "ppc32": "arch/powerpc/boot/",
        "ppc64": "arch/powerpc/boot/",
        "ppc64le": "arch/powerpc/boot/",
        "riscv": "arch/riscv/boot/",
        "s390": "arch/s390/boot/",
        "x86": "arch/x86/boot/",
        "x86_64": "arch/x86_64/boot/",
    }[cbl_arch]


def _read_builds():
    try:
        with open("builds.json") as f:
            builds = json.load(f)
    except FileNotFoundError as e:
        print_red("Unable to find builds.json. Artifact not saved?")
        raise e
    return builds


def _find_build(cbl_arch, builds):
    arch = _cbl_arch_to_arch(cbl_arch)
    config = _cbl_arch_to_config(cbl_arch)
    for build in builds:
        if build["target_arch"] == arch and build["kconfig"][0] == config:
            return build
    print_red("Unable to find build")
    sys.exit(1)

def get_build(cbl_arch):
    return _find_build(cbl_arch, _read_builds())


def print_red(msg):
    print("\033[91m%s\033[0m" % msg, file=sys.stderr)


def print_yellow(msg):
    print("\033[93m%s\033[0m" % msg)
