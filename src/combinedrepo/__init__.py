import sys
import json
import os
import subprocess
import argparse

# Filename for the configuration file
CONFIG_FILENAME = "combinedrepo.json"

def find_config(directory, configName):
    """
        return path of configuration file, will search all parent directories.
        If it can't be found, returns None
    """
    cfgpath = os.path.join(directory, configName)

    if os.path.exists(cfgpath):
        return cfgpath

    parent = os.path.abspath(os.path.join(directory, ".."))

    # Reached the root directory
    if parent == directory:
        return None

    return find_config(parent, configName)

def load_config(path):
    """
        Load the configuration file from the given path
    """
    with open(path, 'r') as f:
        config = json.load(f)

        dir = os.path.dirname(path)
        extra = {
            "config.path": path,
            "config.dir": dir,
            "repository": os.path.join(dir, config["combined-repository"])
        }

        return (config, extra)

def calculate_subrepository_relative_path((config, extra), path):
    """
        Calculate the relative path to a subrepository from the
        config file.
    """
    path = path.replace(extra["config.dir"], '')
    path = path[1:] # Strip leading slash
    path = path.replace('\\', '/')

    return path

def path_to_subtree_config(config, path):
    """
        Return the subtree config for the given path. If no config could
        be found, return None instead
    """

    return config[0]["repositories"].get(
        calculate_subrepository_relative_path(config, path)
    )

def call((config, extra), args):
    """
        Call git on the combined repository
    """
    subprocess.Popen(args, cwd=extra["repository"]).wait()

def push(config, path):
    """
        Push changes in the given repository to the combined repository.
    """

    stConfig = path_to_subtree_config(config, path)

    # Construct an array of argument to pass to gitsubtree
    args = ["git", "subtree", "pull"]
    args.append("--prefix=" + stConfig["prefix"])
    args.append(path)
    args.append(stConfig["branch"])

    call(config, args)

def cmd_svn_dcommit(args):
    """
        Merge the repository and then dcommit the combined repository
    """
    repo = os.getcwd()
    config = load_config(find_config(repo, CONFIG_FILENAME))
    merge(config, repo)
    call(config, ["git", "svn", "dcommit"])

def cmd_push(args):
    """
        Push changes in the given repository to the combined repository.
    """
    repo = os.getcwd()
    config = load_config(find_config(repo, CONFIG_FILENAME))
    push(config, repo)

def cmd_add(args):
    repo = os.getcwd()
    config = load_config(find_config(repo, CONFIG_FILENAME))
    path = calculate_subrepository_relative_path(config, repo)

    (cfg, extra) = config

    if path in cfg["repositories"]:
        print "You have already added this path to the repository!"
        return

    cfg["repositories"][path] = {
        "prefix": args.prefix,
        "branch": args.branch,
    }

    with open(extra["config.path"], 'w') as f:
        json.dump(cfg, f, indent=4)

    gitargs = ["git", "subtree", "add"]
    gitargs.append("--prefix="+args.prefix)
    gitargs.append(repo)
    gitargs.append(args.branch)

    call(config, gitargs)

def cmd_init(args):
    config = {
        "combined-repository": args.repository,
        "repositories": {},
    }

    with open(CONFIG_FILENAME, 'w') as f:
        json.dump(config, f, indent=4)

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    ##################################################
    # add
    add = subparsers.add_parser(
        "add",
        help="Add a new sub-repository to the combined repository"
    )
    add.set_defaults(func=cmd_add)

    add.add_argument(
        "prefix",
        type=str,
        help="The directory that the sub-repository will occupy in the combined repository"
    )

    add.add_argument(
        "--branch", "-B",
        type=str,
        default="master",
        help="Branch of the sub-repository to add to combined repository",
    )

    ##################################################
    # init
    init = subparsers.add_parser(
        "init",
        help="Initialize the combined repository"
    )
    init.set_defaults(func=cmd_init)
    init.add_argument(
        "repository",
        type=str,
        help="Relative path to the combined repository",
    )

    ##################################################
    # push
    push = subparsers.add_parser(
        "push",
        help="Push changes from the current repository to the combined repository"
    )
    push.set_defaults(func=cmd_push)

    ##################################################
    # svn
    svn = subparsers.add_parser("svn").add_subparsers()

    ##################################################
    # svn dcommit
    svn_dcommit = svn.add_parser("dcommit")
    svn_dcommit.set_defaults(func=cmd_svn_dcommit)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
