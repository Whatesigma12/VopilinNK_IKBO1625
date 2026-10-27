import os
import sys
import unittest

sys.path.insert(0, os.path.abspath("src"))

from commands import (
    exec_cd,
    exec_chmod,
    exec_date,
    exec_head,
    exec_ls,
    exec_touch,
)
from vfs import VFS, VFSNode


class TestShellEmulator(unittest.TestCase):
    """Набор тестов для проверки VFS и команд."""

    def setUp(self):
        """Настройка тестовой VFS перед каждым тестом."""
        self.vfs = VFS()
        self.vfs.load_from_dir("./vfs_data/multi")

    def test_ls_and_cd(self):
        """Проверка команд ls и cd."""
        out = exec_ls(self.vfs, [])
        self.assertIn("file1.txt", out)
        err = exec_cd(self.vfs, ["/nonexistent"])
        self.assertIn("Ошибка", err)

    def test_ls_flags(self):
        """Проверка одиночных и объединённых флагов ls."""
        self.vfs.root.children[".secret"] = VFSNode(
            ".secret", is_dir=False, content=""
        )
        regular = exec_ls(self.vfs, [])
        self.assertNotIn(".secret", regular)

        all_items = exec_ls(self.vfs, ["-a"])
        self.assertIn(".secret", all_items)

        long_all = exec_ls(self.vfs, ["-la"])
        self.assertIn("644 file1.txt", long_all)
        self.assertIn("644 .secret", long_all)

        err = exec_ls(self.vfs, ["-z"])
        self.assertIn("Ошибка", err)

    def test_head_and_date(self):
        """Проверка команд head и date."""
        out = exec_head(self.vfs, ["-n", "1", "file1.txt"])
        self.assertEqual(out.strip(), "Line 1")
        date_out = exec_date([])
        self.assertTrue(len(date_out.strip()) > 0)

    def test_head_rejects_non_positive_count(self):
        """Проверка отклонения нулевого и отрицательного количества."""
        for count in ("0", "-1"):
            with self.subTest(count=count):
                out = exec_head(
                    self.vfs, ["-n", count, "file1.txt"]
                )
                self.assertIn("положительным", out)

    def test_touch_and_chmod_in_memory(self):
        """Проверка модификации VFS в памяти командами touch и chmod."""
        exec_touch(self.vfs, ["created.txt"])
        self.assertIsNotNone(self.vfs.get_node("created.txt"))
        exec_chmod(self.vfs, ["777", "created.txt"])
        self.assertEqual(self.vfs.get_node("created.txt").mode, "777")


if __name__ == "__main__":
    unittest.main()
