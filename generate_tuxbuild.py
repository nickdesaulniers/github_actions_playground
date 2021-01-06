#!/usr/bin/env python3
import argparse
import yaml
import sys


def parse_args(trees):
    parser = argparse.ArgumentParser(description="Generate TuxBuild YML.")
    parser.add_argument("tree", help="The git repo and ref to filter in.",
            choices=[tree["name"] for tree in trees])
    return parser.parse_args()


def get_config():
    # Trusted input.
    # https://github.com/yaml/pyyaml/wiki/PyYAML-yaml.load(input)-Deprecation
    return yaml.load(sys.stdin, Loader=yaml.FullLoader)


def get_repo_ref(config, tree_name):
    for tree in config["trees"]:
        if tree["name"] == tree_name:
            return tree["repo"], tree["ref"]


def gen_llvm_version_lookup(llvm_versions):
    # Example: { "12": "clang-nightly", "11": "clang-11" }
    versions = {}
    for version in llvm_versions:
        versions[str(version)] = "clang-" + str(version)
    versions[str(max(llvm_versions))] = "clang-nightly"
    return versions


def emit_tuxbuild_yml(config, tree):
    repo, ref = get_repo_ref(config, tree)
    versions = gen_llvm_version_lookup(config["llvm_versions"])
    print("# This file has been autogenerated by invoking:")
    print("# $ ./generate_tuxbuild.py < generator.yml {} > {}.tux.config".format(tree, tree))
    print("# Do not modify manually.")
    print("# Invoke tuxbuild via:")
    print("# $ tuxbuild build-set --git-repo '{}' --git-ref {} \\".format(repo, ref))
    print("#     --set-name foo-bar --json-out builds.json --tux-config {}.tux.config".format(tree))
    print("""\
sets:
  - name: foo-bar
    builds:\
""")
    for build in config["builds"]:
        if build["repo"] == repo and build["ref"] == ref:
            arch = build["ARCH"] if "ARCH" in build else "x86_64"
            toolchain = versions[str(build["llvm_version"])]
            kconfig = build["config"]
            print("      - {{target_arch: {0}, toolchain: {1}, kconfig: {2}}}".format(arch, toolchain, kconfig))

if __name__ == "__main__":
    # The list of valid trees come from the input, so we parse the input, then
    # check command line flags.
    config = get_config()
    args = parse_args(config["trees"])
    emit_tuxbuild_yml(config, args.tree)