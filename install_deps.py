import subprocess
import sys

from utils import get_arch

def check_run(command_str):
    subprocess.run(command_str, check=True)

def install_deps():
    arch_dependencies = {
      "arm64": ["qemu-system-aarch64"],
      "arm32_v5": ["qemu-system-arm"],
      "arm32_v6": ["qemu-system-arm"],
      "arm32_v7": ["qemu-system-arm"],
      "mips": ["qemu-system-mips"],
      "ppc32": ["qemu-system-ppc"],
      "ppc64": ["qemu-system-ppc"],
      "ppc64le": ["qemu-system-ppc"],
      "x86": ["qemu-system-x86"],
      "x86_64": ["qemu-system-x86"],
      "s390": ["qemu-system-misc"],
      "riscv": ["qemu-system-misc"],
    }
    arch = get_arch()
    if not arch in arch_dependencies:
        print("Unknown arch \"%s\", can't install dependencies" % arch,
              file=sys.stderr)
        sys.exit(1)
    # Not specific to any arch.
    dependencies = [
        "expect", # unbuffer command used by boot-utils/boot-qemu.sh.
    ] + arch_dependencies[arch]
    print("Installing:", dependencies)

    # sudo apt-get update && DEBIAN_FRONTEND=noninteractive sudo apt-get install --no-install-recommends -y expect qemu-system-aarch64 qemu-system-x86
    subprocess.run("sudo apt-get update".split(" "), check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    env = {"DEBIAN_FRONTEND": "noninteractive"}
    subprocess.run("sudo apt-get install --no-install-recommends -y".split(" ") + dependencies, check=True, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
