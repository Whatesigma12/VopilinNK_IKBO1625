"""Тесты клиента npm Registry."""

import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src"),
)

from npm_client import (
    build_package_url,
    fetch_package_metadata,
    get_dependencies,
)


class FakeResponse:
    """Имитировать HTTP-ответ без сетевого запроса."""

    def __init__(self, data):
        """Сохранить подготовленные байты ответа."""
        self.data = data

    def read(self):
        """Вернуть подготовленные байты."""
        return self.data

    def __enter__(self):
        """Вернуть объект контекстного менеджера."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Завершить работу контекстного менеджера."""
        return False


class TestNpmClient(unittest.TestCase):
    """Проверки клиента npm Registry."""

    def test_build_package_url(self):
        """Проверить URL обычного пакета."""
        url = build_package_url(
            "https://registry.npmjs.org/",
            "express",
            "4.18.2",
        )
        self.assertEqual(
            url,
            "https://registry.npmjs.org/express/4.18.2",
        )

    def test_build_scoped_package_url(self):
        """Проверить кодирование scoped-пакета."""
        url = build_package_url(
            "https://registry.npmjs.org",
            "@babel/core",
            "7.22.0",
        )
        self.assertIn("%40babel%2Fcore", url)

    @patch("npm_client.urlopen")
    def test_fetch_package_metadata(self, mock_urlopen):
        """Проверить получение метаданных пакета."""
        payload = {
            "name": "example",
            "version": "1.0.0",
        }
        mock_urlopen.return_value = FakeResponse(
            json.dumps(payload).encode("utf-8")
        )
        result = fetch_package_metadata(
            "https://registry.npmjs.org",
            "example",
            "1.0.0",
        )
        self.assertEqual(result["name"], "example")

    @patch("npm_client.urlopen")
    def test_get_dependencies(self, mock_urlopen):
        """Проверить извлечение прямых зависимостей."""
        payload = {
            "name": "example",
            "version": "1.0.0",
            "dependencies": {
                "alpha": "^1.0.0",
                "beta": "^2.0.0",
            },
        }
        mock_urlopen.return_value = FakeResponse(
            json.dumps(payload).encode("utf-8")
        )
        result = get_dependencies(
            "https://registry.npmjs.org",
            "example",
            "1.0.0",
        )
        self.assertEqual(
            result,
            {
                "alpha": "^1.0.0",
                "beta": "^2.0.0",
            },
        )

    @patch("npm_client.urlopen")
    def test_package_without_dependencies(self, mock_urlopen):
        """Проверить пакет без поля dependencies."""
        payload = {
            "name": "example",
            "version": "1.0.0",
        }
        mock_urlopen.return_value = FakeResponse(
            json.dumps(payload).encode("utf-8")
        )
        result = get_dependencies(
            "https://registry.npmjs.org",
            "example",
            "1.0.0",
        )
        self.assertEqual(result, {})


if __name__ == "__main__":
    unittest.main()
