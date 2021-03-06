#!/usr/bin/env python3

import argparse
import yaml
import sys


def parse_args(trees):
    parser = argparse.ArgumentParser(description="Generate GitHub Action Workflow YAML.")
    parser.add_argument("tree", help="The git repo and ref to filter in.",
            choices=[tree["name"] for tree in trees])
    return parser.parse_args()


def get_config():
    return yaml.load(sys.stdin, Loader=yaml.FullLoader)


def get_fragment():
    with open("job_fragment.yml", "r") as f:
        return yaml.load(f, Loader=yaml.FullLoader)

def get_repo_ref(config, tree_name):
    for tree in config["trees"]:
        if tree["name"] == tree_name:
            return tree["repo"], tree["ref"]


def get_job_name(build):
    return "ARCH=" + (build["ARCH"] if "ARCH" in build else "x86_64") \
    + " LLVM=" + str(int(build["llvm"])) + " LLVM_IAS=" + str(int(build["llvm_ias"])) \
    + " BOOT=" + str(int(build["boot"]))


def sanitize_job_name(name):
    return name.replace(" ", "_").replace("=", "_")


def get_steps(build):
    name = get_job_name(build)
    return {
        sanitize_job_name(name + "_" + build["config"]): {
            "runs-on": "ubuntu-20.04",
            "needs": "kick_tuxbuild",
            "name": name,
            "env": {
                "ARCH": build["ARCH"] if "ARCH" in build else "x86_64",
                "LLVM": build["llvm"],
                "LLVM_IAS": build["llvm_ias"],
                "INSTALL_DEPS": 1,
                "BOOT": build["boot"],
                "CONFIG": build["config"],
            },
            "steps": [{
                    "uses": "actions/checkout@v2",
                    "with": { "submodules": True },
                }, {
                    "uses": "actions/download-artifact@v2",
                    "with": { "name": "output_artifact" },
                }, {
                    "name": "Boot Test",
                    "run": "./check_logs.py",
                },
            ],
        }
    }


def print_builds(config, tree_name):
    repo, ref = get_repo_ref(config, tree_name)
    fragment = get_fragment()
    fragment["name"] += " " + tree_name
    # Bug in yaml.load()???
    fragment["on"] = fragment[True]
    del fragment[True]

    for build in config["builds"]:
        if build["repo"] == repo and build["ref"] == ref:
            steps = get_steps(build)
            fragment["jobs"].update(steps)
    print("# This file has been autogenerated by invoking:")
    print("# $ ./generate_workflow.py < generator.yml {} > .github/workflows/{}.yml".format(tree_name, tree_name))
    print("# Do not modify manually.")
    print(yaml.dump(fragment, Dumper=yaml.Dumper, width=1000, sort_keys=False))


if __name__ == "__main__":
    config = get_config()
    args = parse_args(config["trees"])
    print_builds(config, args.tree)
