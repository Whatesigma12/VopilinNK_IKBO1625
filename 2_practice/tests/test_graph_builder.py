"""Тесты построения тестового графа."""

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


from test_repository import (
    TestRepositoryError,
    build_test_graph
)


class TestGraphBuilder(unittest.TestCase):
    """Проверки рекурсивного DFS."""

    def test_transitive_dependencies(self):
        """DFS должен находить транзитивные зависимости."""

        repository = {
            "A": ["B"],
            "B": ["C"],
            "C": []
        }

        graph = build_test_graph(
            repository,
            "A",
            3
        )

        self.assertEqual(
            graph["A"],
            ["B"]
        )

        self.assertEqual(
            graph["B"],
            ["C"]
        )

    def test_max_depth(self):
        """DFS должен учитывать максимальную глубину."""

        repository = {
            "A": ["B"],
            "B": ["C"],
            "C": ["D"],
            "D": []
        }

        graph = build_test_graph(
            repository,
            "A",
            1
        )

        self.assertIn(
            "B",
            graph
        )

        self.assertNotIn(
            "C",
            graph
        )

    def test_cycle(self):
        """Циклический граф не должен вызывать рекурсию бесконечно."""

        repository = {
            "A": ["B"],
            "B": ["C"],
            "C": ["A"]
        }

        graph = build_test_graph(
            repository,
            "A",
            10
        )

        self.assertIn(
            "A",
            graph
        )

        self.assertIn(
            "B",
            graph
        )

        self.assertIn(
            "C",
            graph
        )

    def test_missing_start_package(self):
        """Несуществующий стартовый пакет должен вызвать ошибку."""

        repository = {
            "A": []
        }

        with self.assertRaises(
            TestRepositoryError
        ):
            build_test_graph(
                repository,
                "B",
                2
            )


if __name__ == "__main__":
    unittest.main()