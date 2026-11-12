"""Тесты генерации Mermaid."""

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


from mermaid import graph_to_mermaid


class TestMermaid(unittest.TestCase):
    """Проверки представления графа Mermaid."""

    def test_header(self):
        """Описание должно начинаться с graph TD."""

        graph = {
            "A": []
        }

        result = graph_to_mermaid(
            graph
        )

        self.assertTrue(
            result.startswith("graph TD")
        )

    def test_nodes(self):
        """Все вершины должны присутствовать в результате."""

        graph = {
            "A": ["B"],
            "B": []
        }

        result = graph_to_mermaid(
            graph
        )

        self.assertIn(
            'n0["A"]',
            result
        )

        self.assertIn(
            'n1["B"]',
            result
        )

    def test_edge(self):
        """Связь между пакетами должна присутствовать."""

        graph = {
            "A": ["B"],
            "B": []
        }

        result = graph_to_mermaid(
            graph
        )

        self.assertIn(
            "n0 --> n1",
            result
        )

    def test_isolated_node(self):
        """Пакет без зависимостей тоже должен отображаться."""

        graph = {
            "A": []
        }

        result = graph_to_mermaid(
            graph
        )

        self.assertIn(
            'n0["A"]',
            result
        )

    def test_versions(self):
        """Для npm-графа можно показывать выбранную версию."""

        graph = {
            "express": []
        }

        versions = {
            "express": "4.18.2"
        }

        result = graph_to_mermaid(
            graph,
            versions
        )

        self.assertIn(
            "express (4.18.2)",
            result
        )


if __name__ == "__main__":
    unittest.main()