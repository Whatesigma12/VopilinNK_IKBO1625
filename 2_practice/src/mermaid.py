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


def _build_node_ids(nodes):
    """Назначить вершинам безопасные идентификаторы."""
    return {
        package: f"n{index}"
        for index, package in enumerate(nodes)
    }


def _make_label(package, versions):
    """Сформировать отображаемую подпись вершины."""
    if package in versions:
        return f"{package} ({versions[package]})"
    return package


def _build_node_lines(nodes, node_ids, versions):
    """Сформировать строки объявления вершин Mermaid."""
    lines = []
    for package in nodes:
        label = escape_label(_make_label(package, versions))
        lines.append(
            f'    {node_ids[package]}["{label}"]'
        )
    return lines


def _build_edge_lines(graph, node_ids):
    """Сформировать строки рёбер Mermaid."""
    lines = []
    for package in sorted(graph):
        for dependency in sorted(graph[package]):
            lines.append(
                f"    {node_ids[package]} --> "
                f"{node_ids[dependency]}"
            )
    return lines


def graph_to_mermaid(graph, versions=None):
    """Преобразовать граф зависимостей в описание Mermaid."""
    versions = {} if versions is None else versions
    nodes = collect_nodes(graph)
    node_ids = _build_node_ids(nodes)
    lines = ["graph TD"]
    lines.extend(_build_node_lines(nodes, node_ids, versions))
    lines.extend(_build_edge_lines(graph, node_ids))
    return "\n".join(lines)
