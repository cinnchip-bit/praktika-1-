
import calendar
import getpass
import shlex
import socket
from datetime import date

try:
    from .vfs import VFS
except ImportError:
    from vfs import VFS


class Shell:

    def __init__(self, vfs=None):
        self.vfs = vfs or VFS()
        self.history = []

    def prompt(self):
        return f"{getpass.getuser()}@{socket.gethostname()}:{self.vfs.cwd}$"

    def execute(self, line):
        self.history.append(line)
        try:
            args = shlex.split(line)
        except ValueError as error:
            return f"Syntax error: {error}", False
        if not args:
            return "", False
        command, params = args[0], args[1:]
        handlers = {
            "ls": self._ls,
            "cd": self._cd,
            "cal": self._cal,
            "tree": self._tree,
            "who": self._who,
            "cp": self._cp,
            "exit": self._exit,
            "джек": self._vorobey,
        }
        if command not in handlers:
            return f"Error: unknown command: {command}", False
        try:
            return handlers[command](params)
        except (ValueError, OSError, FileNotFoundError) as error:
            return f"Error: {error}", False

    def _check_count(self, params, minimum, maximum=None):
        if len(params) < minimum:
            raise ValueError("not enough arguments")
        if maximum is not None and len(params) > maximum:
            raise ValueError("too many arguments")

    def _ls(self, params):
        self._check_count(params, 0, 1)
        path = params[0] if params else self.vfs.cwd
        names = self.vfs.list_dir(path)
        return "  ".join(names) if names else "(empty directory)", False

    def _cd(self, params):
        self._check_count(params, 0, 1)
        self.vfs.change_dir(params[0] if params else "/")
        return self.vfs.cwd, False

    def _cal(self, params):
        self._check_count(params, 0, 2)
        today = date.today()
        month, year = today.month, today.year
        if len(params) == 1:
            year = int(params[0])
        elif len(params) == 2:
            month, year = int(params[0]), int(params[1])
        if not 1 <= month <= 12:
            raise ValueError("month must be from 1 to 12")
        if not 1 <= year <= 9999:
            raise ValueError("year must be from 1 to 9999")
        return calendar.month(year, month), False

    def _tree(self, params):
        self._check_count(params, 0, 1)
        start = params[0] if params else self.vfs.cwd
        lines = [start.rstrip("/") or "/"]
        self._tree_walk(start, "", lines)
        return "\n".join(lines), False

    def _tree_walk(self, path, prefix, lines):
        names = self.vfs.list_dir(path)
        for index, name in enumerate(names):
            last = index == len(names) - 1
            branch = "└── " if last else "├── "
            child_path = path.rstrip("/") + "/" + name
            node = self.vfs.get_node(child_path)
            suffix = "/" if node["type"] == "dir" else ""
            lines.append(prefix + branch + name + suffix)
            if node["type"] == "dir":
                extension = "    " if last else "│   "
                self._tree_walk(child_path, prefix + extension, lines)

    def _who(self, params):
        self._check_count(params, 0, 0)
        user = getpass.getuser()
        host = socket.gethostname()
        return f"{user}  {host}", False

    def _cp(self, params):
        self._check_count(params, 2, 2)
        self.vfs.copy(params[0], params[1])
        return f"copied: {params[0]} -> {params[1]}", False

    @staticmethod
    def _exit(params):
        if params:
            raise ValueError("exit takes no arguments")
        return "Goodbye!", True

    def _vorobey(self, params):
        if not params:
            return "нихуя ты пацан джек воробей компас на клад ты знаешь конец я буду богат", False
