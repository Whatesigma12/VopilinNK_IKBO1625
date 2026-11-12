"""Тесты генерации автономного SVG."""

import sys
import unittest
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src"),
)

from svg_renderer import graph_to_svg


class TestSvgRenderer(unittest.TestCase):
    """Проверки SVG-представления графа."""

    def test_svg_document(self):
        """Результат должен быть полноценным SVG-документом."""
        result = graph_to_svg({"A": []}, title="Test")
        self.assertTrue(result.startswith("<svg"))
        self.assertIn("</svg>", result)
        self.assertIn("Test", result)

    def test_nodes_and_edge(self):
        """SVG должен содержать вершины и ребро."""
        result = graph_to_svg({
            "A": ["B"],
            "B": [],
        })
        self.assertIn('data-node="A"', result)
        self.assertIn('data-node="B"', result)
        self.assertIn('data-edge="A-&gt;B"', result)

    def test_cycle(self):
        """Циклическое ребро должно сохраняться в SVG."""
        result = graph_to_svg({
            "A": ["B"],
            "B": ["A"],
        })
        self.assertIn('data-edge="A-&gt;B"', result)
        self.assertIn('data-edge="B-&gt;A"', result)


if __name__ == "__main__":
    unittest.main()
