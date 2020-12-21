#!/usr/bin/env python3

import json
import os
import subprocess
import sys
import urllib.request

from utils import get_build, get_image_name, get_image_path
from install_deps import install_deps


def fetch_logs(build):
    url = build["download_url"] + "build.log"
    print("fetching logs from %s" % build["download_url"])
    # TODO: use something more robust like python wget library.
    response = urllib.request.urlopen(url).read().decode("UTF-8")
    print(response)


def check_log(build):
    warnings_count = build["warnings_count"]
    errors_count = build["errors_count"]
    if warnings_count + errors_count > 0:
        print("%d warnings, %d errors" % (warnings_count, errors_count))
        fetch_logs(build)


def fetch_kernel_image(cbl_arch, build):
    image_fname = get_image_name(cbl_arch)
    url = build["download_url"] + image_fname
    image_path = get_image_path(cbl_arch)
    # mkdir -p
    os.makedirs(image_path, exist_ok=True)
    print("fetching kernel image from: %s, to: %s" % (url, image_path + image_fname))
    # TODO: use something more robust like python wget library.
    urllib.request.urlretrieve(url, image_path + image_fname)
    # Suspect download is failing.
    if os.path.exists:
        print("Filesize: ", os.path.getsize(image_path + image_fname))
    else:
        print("Unable to download kernel image", file=sys.stderr)
        sys.exit(1)


def cwd():
    os.chdir(os.path.dirname(__file__))
    return os.getcwd()


def run_boot(cbl_arch):
    try:
        subprocess.run(["./boot-utils/boot-qemu.sh", "-a", cbl_arch, "-k", cwd()],
                       check=True)
    except subprocess.CalledProcessError as e:
        if e.returncode == 124:
            print("Image failed to boot", file=sys.stderr)
        raise e



def boot_test(cbl_arch, build):
    if build["errors_count"] > 0:
        print("errors encountered during build, skipping boot", file=sys.stderr)
        sys.exit(1)
    if "BOOT" in os.environ and os.environ["BOOT"] == "0":
        print("boot test disabled via config, skipping boot", file=sys.stderr)
        return
    fetch_kernel_image(cbl_arch, build)
    run_boot(cbl_arch)


if __name__ == "__main__":
    if not "ARCH" in os.environ:
        print("$ARCH must be specified", file=sys.stderr)
        sys.exit(1)
    cbl_arch = os.environ["ARCH"]
    build = get_build(cbl_arch)
    print(json.dumps(build, indent=4))
    check_log(build)
    install_deps(cbl_arch)
    boot_test(cbl_arch, build)
