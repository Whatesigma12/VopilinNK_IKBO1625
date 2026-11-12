"""Тесты эмулятора оболочки и виртуальной файловой системы."""

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


def make_vfs():
    """Создать тестовую VFS."""
    vfs = VFS()
    vfs.load_from_dir("./vfs_data/multi")
    return vfs


class TestShellEmulator(unittest.TestCase):
    """Набор тестов для проверки VFS и команд."""

    def test_ls_and_cd(self):
        """Проверить команды ls и cd."""
        vfs = make_vfs()
        output = exec_ls(vfs, [])
        self.assertIn("file1.txt", output)
        error = exec_cd(vfs, ["/nonexistent"])
        self.assertIn("Ошибка", error)

    def test_ls_flags(self):
        """Проверить одиночные и объединённые флаги ls."""
        vfs = make_vfs()
        vfs.root.children[".secret"] = VFSNode(
            ".secret",
            is_dir=False,
            content="",
        )
        self.assertNotIn(".secret", exec_ls(vfs, []))
        self.assertIn(".secret", exec_ls(vfs, ["-a"]))
        long_all = exec_ls(vfs, ["-la"])
        self.assertIn("644 file1.txt", long_all)
        self.assertIn("644 .secret", long_all)
        self.assertIn("Ошибка", exec_ls(vfs, ["-z"]))

    def test_head_and_date(self):
        """Проверить команды head и date."""
        vfs = make_vfs()
        output = exec_head(vfs, ["-n", "1", "file1.txt"])
        self.assertEqual(output.strip(), "Line 1")
        date_output = exec_date([])
        self.assertTrue(date_output.strip())

    def test_head_rejects_non_positive_count(self):
        """Проверить отклонение неположительного количества строк."""
        vfs = make_vfs()
        for count in ("0", "-1"):
            with self.subTest(count=count):
                output = exec_head(
                    vfs,
                    ["-n", count, "file1.txt"],
                )
                self.assertIn("положительным", output)

    def test_touch_and_chmod_in_memory(self):
        """Проверить команды touch и chmod в памяти VFS."""
        vfs = make_vfs()
        exec_touch(vfs, ["created.txt"])
        self.assertIsNotNone(vfs.get_node("created.txt"))
        exec_chmod(vfs, ["777", "created.txt"])
        self.assertEqual(vfs.get_node("created.txt").mode, "777")


if __name__ == "__main__":
    unittest.main()
