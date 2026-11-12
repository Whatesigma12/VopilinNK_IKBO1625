"""Поиск обратных зависимостей пакета."""

from test_repository import build_test_graph


def find_reverse_dependencies(
    repository,
    target,
    max_depth,
):
    """Найти пакеты, которые зависят от target."""
    reverse = []

    for package in repository:
        if package == target:
            continue

        graph = build_test_graph(
            repository,
            package,
            max_depth,
        )
        if target in graph:
            reverse.append(package)

    return sorted(reverse)
