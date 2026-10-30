
import json
from pathlib import PurePosixPath


class VFS:

    def __init__(self, data=None):
        self.root = data or {
            "type": "dir",
            "children": {
                "documents": {
                    "type": "dir",
                    "children": {
                        "readme.txt": {
                            "type": "file",
                            "content": "Welcome to the virtual file system.\n"
                        }
                    }
                },
                "hello.txt": {
                    "type": "file",
                    "content": "Hello from VFS!\n"
                }
            }
        }
        self.cwd = "/"
        self._validate_node(self.root)

    @classmethod
    def from_json(cls, path):
        """Load a VFS description from a JSON file."""
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return cls(data)

    @staticmethod
    def _validate_node(node):
        if not isinstance(node, dict):
            raise ValueError("Invalid VFS node")
        node_type = node.get("type")
        if node_type == "dir":
            children = node.get("children", {})
            if not isinstance(children, dict):
                raise ValueError("Directory children must be an object")
            for name, child in children.items():
                if not name or "/" in name or name in {".", ".."}:
                    raise ValueError("Invalid file or directory name")
                VFS._validate_node(child)
        elif node_type == "file":
            if not isinstance(node.get("content", ""), str):
                raise ValueError("File content must be text")
        else:
            raise ValueError("Node type must be 'dir' or 'file'")

    @staticmethod
    def _parts(path):
        return [part for part in PurePosixPath(path).parts
                if part not in {"/", "", "."}]

    def resolve(self, path):
        if not path:
            return self.cwd
        parts = [] if path.startswith("/") else self._parts(self.cwd)
        for part in path.split("/"):
            if part in {"", "."}:
                continue
            if part == "..":
                if parts:
                    parts.pop()
            else:
                parts.append(part)
        return "/" + "/".join(parts)

    def get_node(self, path):
        absolute = self.resolve(path)
        node = self.root
        if absolute == "/":
            return node
        for part in self._parts(absolute):
            if node.get("type") != "dir":
                raise FileNotFoundError(f"Not a directory: {part}")
            children = node.get("children", {})
            if part not in children:
                raise FileNotFoundError(f"No such file or directory: {absolute}")
            node = children[part]
        return node

    def list_dir(self, path=None):
        node = self.get_node(path or self.cwd)
        if node.get("type") != "dir":
            raise NotADirectoryError(path or self.cwd)
        return sorted(node.get("children", {}).keys())

    def change_dir(self, path):
        target = self.resolve(path)
        node = self.get_node(target)
        if node.get("type") != "dir":
            raise NotADirectoryError(target)
        self.cwd = target

    def read_file(self, path):
        node = self.get_node(path)
        if node.get("type") != "file":
            raise IsADirectoryError(path)
        return node.get("content", "")

    def copy(self, source, destination):
        source_path = self.resolve(source)
        source_node = self.get_node(source_path)
        dest_path = self.resolve(destination)
        try:
            dest_node = self.get_node(dest_path)
            if dest_node.get("type") == "dir":
                name = self._parts(source_path)[-1]
                dest_path = self.resolve(dest_path + "/" + name)
            else:
                raise FileExistsError(dest_path)
        except FileNotFoundError:
            pass
        parent_path = str(PurePosixPath(dest_path).parent)
        name = PurePosixPath(dest_path).name
        parent = self.get_node(parent_path)
        if parent.get("type") != "dir":
            raise NotADirectoryError(parent_path)
        if name in parent["children"]:
            raise FileExistsError(dest_path)
        parent["children"][name] = json.loads(json.dumps(source_node))

    def save_json(self, path):
        with open(path, "w", encoding="utf-8") as file:
            json.dump(self.root, file, ensure_ascii=False, indent=2)
