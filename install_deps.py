#!/usr/bin/env python3

import subprocess
import sys

from utils import get_arch

def check_run(command_str):
    subprocess.run(command_str, check=True)

if __name__ == "__main__":
    arch_dependencies = {
      "x86_64": [
          "qemu-system-x86",
      ],
      "arm64": [
          "qemu-system-aarch64",
      ],
    }
    arch = get_arch()
    if not arch in arch_dependencies:
        print("Unknown arch: %s" % arch, file=sys.stderr)
        sys.exit(1)
    # Not specific to any arch.
    dependencies = [
        "expect", # unbuffer command used by boot-utils/boot-qemu.sh.
    ] + arch_dependencies[arch]
    print("Installing:", dependencies)

    # sudo apt-get update -qq && DEBIAN_FRONTEND=noninteractive sudo apt-get install --no-install-recommends -y expect qemu-system-aarch64 qemu-system-x86
    subprocess.run("sudo apt-get update -qq".split(" "), check=True)
    env = {"DEBIAN_FRONTEND": "noninteractive"}
    subprocess.run("sudo apt-get install --no-install-recommends -y".split(" ") + dependencies, check=True, env=env)
