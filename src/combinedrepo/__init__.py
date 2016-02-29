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

def path_to_subtree_config((config, extra), path):
    """
        Return the subtree config for the given path. If no config could
        be found, return None instead
    """

    path = path.replace(extra["config.dir"], '')
    path = path[1:] # Strip leading slash
    path = path.replace('\\', '/')

    return config["repositories"].get(path)

def call((config, extra), args):
    """
        Call git on the combined repository
    """
    subprocess.Popen(args, cwd=extra["repository"]).wait()

def merge(config, path):
    """
        Merge the given repository path into the combined repository.
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

def cmd_merge(args):
    """
        Merge the repository with the combined repository
    """
    repo = os.getcwd()
    config = load_config(find_config(repo, CONFIG_FILENAME))
    merge(config, repo)

def cmd_add(args):
    raise NotImplementedError("Add command not yet implemented")

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # merge
    merge = subparsers.add_parser("merge")
    merge.set_defaults(func=cmd_merge)

    # svn
    svn = subparsers.add_parser("svn").add_subparsers()

    # svn dcommit
    svn_dcommit = svn.add_parser("dcommit")
    svn_dcommit.set_defaults(func=cmd_svn_dcommit)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
