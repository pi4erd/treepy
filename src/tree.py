#!/usr/bin/env python3

import importlib.metadata
import importlib
import git
from sys import argv
from pathlib import Path
from argparse import ArgumentParser
from colorama import Fore, Style

def print_item(
    item: Path,
    ignore_wildcard: list[str]=[],
    print_file: bool=True,
    depth: int=0,
    maxdepth: int=-1
    ):
    for filename in ignore_wildcard:
        file_to_ignore = Path(filename)
        if file_to_ignore.name == item.name and depth > 0:
            return
    
    is_dir = item.is_dir()
    
    color = Fore.WHITE
    if is_dir:
        color = Fore.BLUE
    elif item.is_symlink():
        color = Fore.LIGHTCYAN_EX
    elif item.is_block_device():
        color = Fore.YELLOW
    elif item.is_char_device():
        color = Fore.LIGHTMAGENTA_EX

    if is_dir or print_file:
        print(" " * depth + color + item.name)
    
    if (maxdepth != -1 and depth >= maxdepth) or not is_dir:
        return
    
    for i in item.iterdir():
        print_item(i, ignore_wildcard, print_file, depth + 1, maxdepth)

if __name__ == "__main__":
    version = "unknown"
    try:
        package = "treepy"
        version = importlib.metadata.version(package)
    except importlib.metadata.PackageNotFoundError:
        try:
            repo = git.Repo(search_parent_directories=True)
            sha = repo.head.object.hexsha
            branch = repo.active_branch.name
            version = "git." + branch + "." + sha
        except git.InvalidGitRepositoryError:
            pass
    
    parser = ArgumentParser(
        prog=argv[0], # so that it can be renamed whatever
        description="Prints a tree of files/directories",
        epilog="In development"
    )
    parser.add_argument("path", nargs='?')
    parser.add_argument("-i", "--ignore", action='extend', nargs='*',
                        help="ignores files specified by bash wildcard")
    parser.add_argument("--version", action='version', version=f"%(prog)s {version}")
    parser.add_argument("-d", "--depth", action="store", 
                        default=-1, type=int, metavar="DEPTH",
                        help="the depth to look for")
    
    args = parser.parse_args()
    
    if args.path is None:
        realpath = Path.cwd()
    else:
        if args.path == '.':
            realpath = Path.cwd()
        else:
            realpath = Path(args.path)

    ignore_wdc = [] if args.ignore is None else [wildcards for wildcards in args.ignore]
    
    try:
        print_item(
            realpath,
            ignore_wildcard=ignore_wdc,
            print_file=True,
            depth=0,
            maxdepth=args.depth
        )
    except KeyboardInterrupt:
        pass
