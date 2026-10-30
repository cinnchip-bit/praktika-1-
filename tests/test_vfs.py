"""Tests for virtual file system operations."""

import unittest

from src.vfs import VFS


class VFSTest(unittest.TestCase):
    def setUp(self):
        self.vfs = VFS()

    def test_default_directory(self):
        self.assertEqual(self.vfs.list_dir("/"), ["documents", "hello.txt"])

    def test_change_directory(self):
        self.vfs.change_dir("/documents")
        self.assertEqual(self.vfs.cwd, "/documents")

    def test_read_file(self):
        self.assertIn("Hello", self.vfs.read_file("/hello.txt"))

    def test_copy_file(self):
        self.vfs.copy("/hello.txt", "/documents")
        self.assertIn("hello.txt", self.vfs.list_dir("/documents"))

    def test_missing_path(self):
        with self.assertRaises(FileNotFoundError):
            self.vfs.get_node("/missing")


if __name__ == "__main__":
    unittest.main()
