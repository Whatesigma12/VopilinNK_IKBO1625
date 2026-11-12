"""Тесты поиска обратных зависимостей."""

import sys
import unittest

from pathlib import Path


sys.path.insert(
    0,
    str(
        Path(__file__).resolve().parents[1]
        / "src"
    )
)


from reverse_dependencies import (
    find_reverse_dependencies
)


class TestReverseDependencies(unittest.TestCase):
    """Проверки обратных зависимостей."""

    def test_reverse_dependencies(self):
        """Найти все пакеты, зависящие от D."""

        repository = {
            "A": ["B", "C"],
            "B": ["D"],
            "C": ["D"],
            "D": [],
            "E": ["B"],
            "F": []
        }

        result = find_reverse_dependencies(
            repository,
            "D",
            10
        )

        self.assertEqual(
            result,
            ["A", "B", "C", "E"]
        )

    def test_no_reverse_dependencies(self):
        """Пакет A ни для кого не является зависимостью."""

        repository = {
            "A": ["B"],
            "B": ["C"],
            "C": []
        }

        result = find_reverse_dependencies(
            repository,
            "A",
            10
        )

        self.assertEqual(
            result,
            []
        )

    def test_direct_reverse_dependency(self):
        """Проверить прямую обратную зависимость."""

        repository = {
            "A": ["B"],
            "B": []
        }

        result = find_reverse_dependencies(
            repository,
            "B",
            10
        )

        self.assertEqual(
            result,
            ["A"]
        )

    def test_depth_limit(self):
        """Максимальная глубина должна учитываться."""

        repository = {
            "A": ["B"],
            "B": ["C"],
            "C": ["D"],
            "D": []
        }

        result = find_reverse_dependencies(
            repository,
            "D",
            1
        )

        self.assertEqual(
            result,
            ["C"]
        )


if __name__ == "__main__":
    unittest.main()