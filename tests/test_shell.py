"""Tests for shell commands."""

import unittest

from src.shell import Shell


class ShellTest(unittest.TestCase):
    def setUp(self):
        self.shell = Shell()

    def test_ls(self):
        output, done = self.shell.execute("ls")
        self.assertIn("hello.txt", output)
        self.assertFalse(done)

    def test_quoted_argument(self):
        output, done = self.shell.execute('cd "documents"')
        self.assertEqual(output, "/documents")
        self.assertFalse(done)

    def test_tree(self):
        output, done = self.shell.execute("tree")
        self.assertIn("readme.txt", output)
        self.assertFalse(done)

    def test_who(self):
        output, done = self.shell.execute("who")
        self.assertTrue(output)
        self.assertFalse(done)

    def test_exit(self):
        output, done = self.shell.execute("exit")
        self.assertTrue(done)
        self.assertEqual(output, "Goodbye!")

    def test_unknown_command(self):
        output, done = self.shell.execute("unknown")
        self.assertIn("unknown command", output)
        self.assertFalse(done)


if __name__ == "__main__":
    unittest.main()
