
import argparse
import os
import sys

from gui import ShellGUI
from shell import Shell
from vfs import VFS


def parse_args():
    parser = argparse.ArgumentParser(
        description="Python virtual shell emulator"
    )
    parser.add_argument("--vfs", help="Path to JSON VFS file")
    parser.add_argument("--script", help="Path to startup command script")
    return parser.parse_args()


def load_vfs(path):
    if not path:
        return VFS()
    if not os.path.isfile(path):
        raise FileNotFoundError(f"VFS file not found: {path}")
    return VFS.from_json(path)


def main():
    args = parse_args()
    print(f"VFS path: {args.vfs or 'default in-memory VFS'}")
    print(f"Startup script: {args.script or 'not specified'}")
    try:
        shell = Shell(load_vfs(args.vfs))
    except (OSError, ValueError) as error:
        print(f"VFS loading error: {error}", file=sys.stderr)
        return 1
    if args.script and not os.path.isfile(args.script):
        print(f"Startup script not found: {args.script}", file=sys.stderr)
        return 1
    ShellGUI(shell, args.script).run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
