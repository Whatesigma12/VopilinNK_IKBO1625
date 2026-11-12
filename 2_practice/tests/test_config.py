"""Тесты параметров командной строки."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src"),
)

from config import parse_config


def make_test_file(directory):
    """Создать временный файл тестового репозитория."""
    path = Path(directory) / "graph.json"
    path.write_text("{}", encoding="utf-8")
    return path


class TestConfig(unittest.TestCase):
    """Проверки конфигурации приложения."""

    def test_valid_config(self):
        """Проверить корректные параметры обычного режима."""
        config = parse_config([
            "--package",
            "express",
            "--repository",
            "https://registry.npmjs.org",
            "--version",
            "4.18.2",
            "--max-depth",
            "2",
        ])
        self.assertEqual(config.package, "express")
        self.assertEqual(config.version, "4.18.2")
        self.assertEqual(config.max_depth, 2)
        self.assertFalse(config.test_mode)

    def test_negative_depth(self):
        """Проверить отклонение отрицательной глубины."""
        with self.assertRaises(SystemExit):
            parse_config([
                "--package",
                "express",
                "--repository",
                "https://registry.npmjs.org",
                "--version",
                "4.18.2",
                "--max-depth",
                "-1",
            ])

    def test_invalid_url(self):
        """Проверить отклонение неправильного URL."""
        with self.assertRaises(SystemExit):
            parse_config([
                "--package",
                "express",
                "--repository",
                "wrong-address",
                "--version",
                "4.18.2",
            ])

    def test_missing_package(self):
        """Проверить отсутствие обязательного имени пакета."""
        with self.assertRaises(SystemExit):
            parse_config([
                "--repository",
                "https://registry.npmjs.org",
                "--version",
                "4.18.2",
            ])

    def test_invalid_version(self):
        """Проверить отклонение пустой версии."""
        with self.assertRaises(SystemExit):
            parse_config([
                "--package",
                "express",
                "--repository",
                "https://registry.npmjs.org",
                "--version",
                " ",
            ])

    def test_invalid_depth_text(self):
        """Проверить отклонение текста вместо глубины."""
        with self.assertRaises(SystemExit):
            parse_config([
                "--package",
                "express",
                "--repository",
                "https://registry.npmjs.org",
                "--version",
                "4.18.2",
                "--max-depth",
                "abc",
            ])

    def test_test_mode(self):
        """Проверить режим локального тестового файла."""
        with tempfile.TemporaryDirectory() as directory:
            test_file = make_test_file(directory)
            config = parse_config([
                "--package",
                "A",
                "--repository",
                str(test_file),
                "--test-mode",
                "--version",
                "1.0.0",
            ])

        self.assertTrue(config.test_mode)
        self.assertEqual(config.package, "A")

    def test_missing_test_file(self):
        """Проверить ошибку при отсутствующем тестовом файле."""
        missing = Path("missing-graph.json")
        with self.assertRaises(SystemExit):
            parse_config([
                "--package",
                "A",
                "--repository",
                str(missing),
                "--test-mode",
                "--version",
                "1.0.0",
            ])


if __name__ == "__main__":
    unittest.main()
