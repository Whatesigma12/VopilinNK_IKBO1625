
import sys
import unittest
from pathlib import Path

# Добавляем папку src в список путей поиска Python.
sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from config import parse_config


class TestConfig(unittest.TestCase):

    def setUp(self):
        # Создаём временный файл для тестового режима.
        import tempfile

        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file = Path(self.temp_dir.name) / "graph.json"
        self.test_file.write_text("{}", encoding="utf-8")

    def tearDown(self):
        # Удаляем временный файл после каждого теста.
        self.temp_dir.cleanup()

    def test_valid_config(self):
        # Проверяем правильные параметры обычного режима.
        config = parse_config([
            "--package", "express",
            "--repository", "https://registry.npmjs.org",
            "--version", "4.18.2",
            "--max-depth", "2"
        ])

        self.assertEqual(config.package, "express")
        self.assertEqual(config.version, "4.18.2")
        self.assertEqual(config.max_depth, 2)
        self.assertFalse(config.test_mode)

    def test_negative_depth(self):
        # Отрицательная глубина запрещена.
        with self.assertRaises(SystemExit):
            parse_config([
                "--package", "express",
                "--repository", "https://registry.npmjs.org",
                "--version", "4.18.2",
                "--max-depth", "-1"
            ])

    def test_invalid_url(self):
        # Вместо URL пользователь указал обычный текст.
        with self.assertRaises(SystemExit):
            parse_config([
                "--package", "express",
                "--repository", "wrong-address",
                "--version", "4.18.2"
            ])

    def test_missing_package(self):
        # Не передано обязательное название пакета.
        with self.assertRaises(SystemExit):
            parse_config([
                "--repository", "https://registry.npmjs.org",
                "--version", "4.18.2"
            ])

    def test_invalid_version(self):
        # Пустая версия запрещена.
        with self.assertRaises(SystemExit):
            parse_config([
                "--package", "express",
                "--repository", "https://registry.npmjs.org",
                "--version", " "
            ])

    def test_invalid_depth_text(self):
        # Текст вместо числа запрещён.
        with self.assertRaises(SystemExit):
            parse_config([
                "--package", "express",
                "--repository", "https://registry.npmjs.org",
                "--version", "4.18.2",
                "--max-depth", "abc"
            ])

    def test_test_mode(self):
        # Проверяем режим локального тестового файла.
        config = parse_config([
            "--package", "A",
            "--repository", str(self.test_file),
            "--test-mode",
            "--version", "1.0.0"
        ])

        self.assertTrue(config.test_mode)
        self.assertEqual(config.package, "A")

    def test_missing_test_file(self):
        # Несуществующий тестовый файл должен вызвать ошибку.
        with self.assertRaises(SystemExit):
            parse_config([
                "--package", "A",
                "--repository", str(self.test_file) + ".missing",
                "--test-mode",
                "--version", "1.0.0"
            ])


if __name__ == "__main__":
    unittest.main()
