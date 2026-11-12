"""Формирование графа зависимостей в формате Mermaid."""


def escape_label(value):
    """Подготовить текст для безопасного вывода в Mermaid."""

    return str(value).replace('"', '\\"')


def collect_nodes(graph):
    """Получить все вершины графа."""

    nodes = set(graph)

    for dependencies in graph.values():
        nodes.update(dependencies)

    return sorted(nodes)


def graph_to_mermaid(graph, versions=None):
    """
    Преобразовать граф зависимостей в описание Mermaid.

    graph:
        {
            "A": ["B", "C"],
            "B": ["D"]
        }

    versions:
        {
            "express": "4.18.2"
        }
    """

    if versions is None:
        versions = {}

    nodes = collect_nodes(graph)

    # Mermaid удобнее работать с простыми ID:
    # n0, n1, n2...
    node_ids = {
        package: f"n{index}"
        for index, package in enumerate(nodes)
    }

    lines = [
        "graph TD"
    ]

    # Сначала описываем все вершины.
    for package in nodes:
        label = package

        if package in versions:
            label = (
                f"{package} "
                f"({versions[package]})"
            )

        label = escape_label(label)

        lines.append(
            f'    {node_ids[package]}["{label}"]'
        )

    # Затем создаём связи между вершинами.
    for package in sorted(graph):
        for dependency in sorted(graph[package]):
            lines.append(
                f"    {node_ids[package]} "
                f"--> {node_ids[dependency]}"
            )

    return "\n".join(lines)