#!/usr/bin/env python3

from sys import argv
from pathlib import Path
from argparse import ArgumentParser
from colorama import Fore, Style

def print_item(item: Path, depth: int=0, maxdepth: int=-1):
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

    print(" " * depth + color + item.name)
    
    if maxdepth != -1 and depth >= maxdepth:
        return
    
    if not is_dir:
        return
    
    for i in item.iterdir():
        print_item(i, depth + 1, maxdepth)

if __name__ == "__main__":
    parser = ArgumentParser(
        prog=argv[0], # so that it can be renamed whatever
        description="Prints a tree of files/directories",
        epilog="In development"
    )
    parser.add_argument("path", nargs='?')
    parser.add_argument("-d", "--depth", action="store", 
                        default=-1, type=int, metavar="DEPTH",
                        help="the depth to look for")
    
    args = parser.parse_args()
    
    if args.path is None:
        realpath = Path.cwd()
    else:
        realpath = Path(args.path)
    
    try:
        print_item(realpath, maxdepth=args.depth)
    except KeyboardInterrupt:
        pass
