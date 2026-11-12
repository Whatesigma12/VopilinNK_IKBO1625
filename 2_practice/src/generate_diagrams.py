"""Генерация SVG для всех тестовых JSON-графов."""

from pathlib import Path

from svg_renderer import graph_to_svg
from test_repository import load_test_repository

ROOT = Path(__file__).resolve().parents[1]
TEST_DATA = ROOT / "test_data"
OUTPUT = ROOT / "diagrams"
JSON_FILES = (
    "simple.json",
    "cycle.json",
    "depth.json",
    "reverse.json",
)


def generate_diagram(file_name):
    """Создать один SVG-файл из тестового JSON."""
    source = TEST_DATA / file_name
    graph = load_test_repository(source)
    svg = graph_to_svg(
        graph,
        title=f"Dependency graph: {file_name}",
    )
    target = OUTPUT / f"{source.stem}.svg"
    target.write_text(svg + "\n", encoding="utf-8")
    return target


def main():
    """Сгенерировать SVG для всех тестовых графов."""
    OUTPUT.mkdir(parents=True, exist_ok=True)

    for file_name in JSON_FILES:
        target = generate_diagram(file_name)
        print(target.relative_to(ROOT))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
